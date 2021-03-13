import math
from connection.materialstrength import MaterialStrength
from connection.boltshear import BoltShear
import sqlite3


class DesignResult:
    """
    Calculate the provided capacity of the connection based on the material strength, connection type,
    connection geometry and loadings.
    """
    def __init__(self, material, conn_type, conn_geometry):
        # connection type
        self.conn_type = conn_type
        # get the member properties both for beam and supporting member
        db = sqlite3.connect('data/aisc.db')
        db.row_factory = sqlite3.Row
        cur = db.cursor()
        member = (conn_geometry['size'],)
        cur.execute("SELECT * FROM section WHERE size=?", member)
        data = dict(cur.fetchone())
        self.d = data['d']
        self.bf = data['bf']
        self.tw = data['tw']
        self.tf = data['tf']
        member = (conn_geometry['size2'],)
        cur.execute("SELECT * FROM section WHERE size=?", member)
        data = dict(cur.fetchone())
        self.d2 = data['d']
        self.bf2 = data['bf']
        self.tw2 = data['tw']
        self.tf2 = data['tf']
        db.close()
        # get the material strength as per material specifications
        self.ms = MaterialStrength(material[0], material[1], material[2])
        # retrieve data from conn_geometry
        if self.conn_type == 'ShearGusset' or self.conn_type == 'ShearCope':
            self.col = int(conn_geometry['col'])
            self.ev = float(conn_geometry['ev'])
            self.tg = float(conn_geometry['tg'])
        elif self.conn_type == 'ShearClip':
            self.col = 1
            self.g = float(conn_geometry['g'])
            self.ev1 = float(conn_geometry['ev1'])
            self.ev2 = float(conn_geometry['ev2'])
            self.ta = float(conn_geometry['ta'])
        elif self.conn_type == 'ShearEndPlate':
            self.col = 1
            self.g = float(conn_geometry['g'])
            self.ev = float(conn_geometry['ev'])
            self.te = float(conn_geometry['te'])
            self.W = float(conn_geometry['W'])
        # common parameters from conn_geometry
        self.dia = float(conn_geometry['dia'])
        self.nos = int(conn_geometry['nos'])
        self.spacing = float(conn_geometry['spacing'])
        self.weld = float(conn_geometry['weld'])
        self.eh = float(conn_geometry['eh'])
        self.H = float(conn_geometry['H'])
        self.c = float(conn_geometry['c'])
        self.support = conn_geometry['support']
        self.weld_length = self.H
        # constant
        self.gap = 0.375
        self.weld_clearance = 0.625
        self.clip_leg = 4.0
        #
        self.ecc = self.calcEccentricity()
        self.bolt_shear = BoltShear(self.nos, self.col, self.spacing)
        self.bolt_modulus = self.bolt_shear.calcBoltModulus()
        self.web_height = self.calculateWebHeight()

    def calcEccentricity(self):
        """
        Calculate the eccentricity of the applied force based on connection type and supporting member
        """
        if self.conn_type == 'ShearGusset':
            if self.support == 'Beam' or self.support == 'Column Web':
                if self.col == 1:
                    ecc = (self.bf2 - self.tw2)/2.0 + self.gap + self.eh
                else:
                    ecc = (self.bf2 - self.tw2) / 2.0 + self.gap + self.eh + self.spacing/2.0
            elif self.support == 'Column Flange':
                if self.col == 1:
                    ecc = self.weld_clearance + self.eh
                else:
                    ecc = self.weld_clearance + self.eh + self.spacing/2.0
        elif self.conn_type == 'ShearCope':
            ecc = self.weld_clearance + self.eh
        elif self.conn_type == 'ShearClip':
            ecc = self.gap + self.clip_leg - self.eh
        return round(ecc, 2)

    def check_bolt_shear(self, load_data):
        """
        Check the bolt shear strength
        """
        Fx = float(load_data[3])
        Fy = float(load_data[4])
        bolt_shear = round(self.bolt_shear.calculateBoltShear(Fx, Fy, self.ecc), 1)
        bolt_shear_cap = round(self.ms.bolt_shear_cap(self.dia), 1)
        stress_ratio = round(bolt_shear / bolt_shear_cap, 2)
        return bolt_shear, bolt_shear_cap, stress_ratio

    def check_bolt_bearing(self, load_data):
        """
        Check the bearing strength of the plate on bolt holes
        """
        Fx = float(load_data[3])
        Fy = float(load_data[4])
        bolt_bearing = round(self.bolt_shear.calculateBoltShear(Fx, Fy, self.ecc), 1)
        if self.tg <= self.tw: tp = self.tg
        else: tp = self.tw
        bolt_bearing_cap = round(self.ms.bolt_hole_bearing(self.dia, tp, self.ev), 1)
        stress_ratio = round(bolt_bearing / bolt_bearing_cap, 2)
        return bolt_bearing, bolt_bearing_cap, stress_ratio

    def check_plate_block_shear(self, load_data):
        """
        Check the block shear strength of the plate
        """
        block_shear = float(load_data[4])
        shear_gross_area = self.tg * self.H
        shear_net_area = self.tg * (self.H - self.ev -
                                    (self.nos - 1) * (self.dia + 1 / 16) - 0.5 * (self.dia + 1 / 16))
        tension_net_area = self.tg * (self.ev - 0.5 * (self.dia + 1 / 16))
        block_shear_cap = round(self.ms.plate_block_shear(shear_gross_area, shear_net_area, tension_net_area, 1.0), 1)
        stress_ratio = round(block_shear / block_shear_cap, 2)
        return block_shear, block_shear_cap, stress_ratio

    def check_plate_shear_yielding(self, load_data):
        """
        Check the shear yielding of the plate
        """
        plate_shear_yielding = float(load_data[4])
        gross_area = self.tg * self.H
        plate_shear_yielding_cap = round(self.ms.plate_shear_yielding(gross_area), 1)
        stress_ratio = round(plate_shear_yielding / plate_shear_yielding_cap, 2)
        return plate_shear_yielding, plate_shear_yielding_cap, stress_ratio

    def check_plate_shear_rupture(self, load_data):
        """
        Check the shear rupture of the plate
        """
        plate_shear_rupture = float(load_data[4])
        net_area = self.tg * (self.H - self.nos * (self.dia + 1 / 16))
        plate_shear_rupture_cap = round(self.ms.plate_shear_rupture(net_area), 1)
        stress_ratio = round(plate_shear_rupture / plate_shear_rupture_cap, 2)
        return plate_shear_rupture, plate_shear_rupture_cap, stress_ratio

    def check_plate_tensile_yielding(self, load_data):
        """
        Check the tensile yielding of the plate
        """
        plate_tensile_yielding = float(load_data[3])
        gross_area = self.tg * self.H
        plate_tensile_yielding_cap = round(self.ms.plate_tensile_yielding(gross_area), 1)
        stress_ratio = round(plate_tensile_yielding / plate_tensile_yielding_cap, 2)
        return plate_tensile_yielding, plate_tensile_yielding_cap, stress_ratio

    def check_plate_tensile_rupture(self, load_data):
        """
        Check the tensile rupture of the plate
        """
        plate_tensile_rupture = float(load_data[3])
        effective_net_area = self.tg * (self.H - self.nos * (self.dia + 1 / 16))
        plate_tensile_rupture_cap = round(self.ms.plate_tensile_rupture(effective_net_area), 1)
        stress_ratio = round(plate_tensile_rupture / plate_tensile_rupture_cap, 2)
        return plate_tensile_rupture, plate_tensile_rupture_cap, stress_ratio

    def check_plate_bending_in(self, load_data):
        """
        Check the in-plane bending strength of the plate
        """
        plate_bending_inplane = round(float(load_data[4]) * self.ecc, 1)
        plastic_modulus = self.tg * self.H ** 2 / 4
        plate_bending_cap = round(self.ms.plate_bending_strength(plastic_modulus), 1)
        stress_ratio = round(plate_bending_inplane / plate_bending_cap, 2)
        return plate_bending_inplane, plate_bending_cap, stress_ratio

    def check_plate_bending_out(self, load_data):
        """
        Check the out-of-plane bending strength of the plate
        """
        plate_bending_outplane = round(float(load_data[5]) * self.ecc, 1)
        plastic_modulus = self.H * self.tg ** 2 / 4
        plate_bending_cap = round(self.ms.plate_bending_strength(plastic_modulus), 1)
        stress_ratio = round(plate_bending_outplane / plate_bending_cap, 2)
        return plate_bending_outplane, plate_bending_cap, stress_ratio

    def check_welding_shear(self, load_data):
        """
        Check the weld shear strength
        """
        welding_shear_unit = round(math.sqrt(float(load_data[3]) ** 2 + float(load_data[4]) ** 2) /
                                   (2 * self.weld_length), 2)
        angle = 90
        if float(load_data[4]) != 0:
            angle = math.atan(float(load_data[3]) / float(load_data[4])) * 180 / math.pi
        welding_shear_cap = round(self.ms.fillet_weld_shear(self.weld, angle), 2)
        stress_ratio = round(welding_shear_unit / welding_shear_cap, 2)
        return welding_shear_unit, welding_shear_cap, stress_ratio

    # for cope type connection
    def calculateWebHeight(self):
        """
        Calculate the height of the web for cope type connection (single-coped or double-coped)
        """
        if self.d <= (self.d2 - self.c):
            webH = self.d - self.c
        else:
            webH = self.d - 2.0*self.c
        return webH

    def check_web_block_shear(self, load_data):
        block_shear = float(load_data[4])
        shear_gross_area = self.tw * self.web_height
        shear_net_area = self.tw * (self.web_height - self.ev -
                                    (self.nos - 1) * (self.dia + 1 / 16) - 0.5 * (self.dia + 1 / 16))
        tension_net_area = self.tw * (self.ev - 0.5 * (self.dia + 1 / 16))
        block_shear_cap = round(self.ms.plate_block_shear(shear_gross_area, shear_net_area, tension_net_area, 1.0), 1)
        stress_ratio = round(block_shear / block_shear_cap, 2)
        return block_shear, block_shear_cap, stress_ratio

    def check_web_shear_yielding(self, load_data):
        web_shear_yielding = float(load_data[4])
        gross_area = self.tw * self.web_height
        web_shear_yielding_cap = round(self.ms.plate_shear_yielding(gross_area), 1)
        stress_ratio = round(web_shear_yielding / web_shear_yielding_cap, 2)
        return web_shear_yielding, web_shear_yielding_cap, stress_ratio

    def check_web_shear_rupture(self, load_data):
        web_shear_rupture = float(load_data[4])
        net_area = self.tw * (self.web_height - self.nos * (self.dia + 1 / 16))
        web_shear_rupture_cap = round(self.ms.plate_shear_rupture(net_area), 1)
        stress_ratio = round(web_shear_rupture / web_shear_rupture_cap, 2)
        return web_shear_rupture, web_shear_rupture_cap, stress_ratio

    def check_web_tensile_yielding(self, load_data):
        web_tensile_yielding = float(load_data[3])
        gross_area = self.tw * self.web_height
        web_tensile_yielding_cap = round(self.ms.plate_tensile_yielding(gross_area), 1)
        stress_ratio = round(web_tensile_yielding / web_tensile_yielding_cap, 2)
        return web_tensile_yielding, web_tensile_yielding_cap, stress_ratio

    def check_web_tensile_rupture(self, load_data):
        web_tensile_rupture = float(load_data[3])
        effective_net_area = self.tw * (self.web_height - self.nos * (self.dia + 1 / 16))
        web_tensile_rupture_cap = round(self.ms.plate_tensile_rupture(effective_net_area), 1)
        stress_ratio = round(web_tensile_rupture / web_tensile_rupture_cap, 2)
        return web_tensile_rupture, web_tensile_rupture_cap, stress_ratio

    def check_web_bending_in(self, load_data):
        web_bending_inplane = round(float(load_data[4]) * self.ecc, 1)
        plastic_modulus = self.tw * self.web_height ** 2 / 4
        web_bending_cap = round(self.ms.plate_bending_strength(plastic_modulus), 1)
        stress_ratio = round(web_bending_inplane / web_bending_cap, 2)
        return web_bending_inplane, web_bending_cap, stress_ratio

    def check_web_bending_out(self, load_data):
        web_bending_outplane = round(float(load_data[5]) * self.ecc, 1)
        plastic_modulus = self.web_height * self.tw ** 2 / 4
        web_bending_cap = round(self.ms.plate_bending_strength(plastic_modulus), 1)
        stress_ratio = round(web_bending_outplane / web_bending_cap, 2)
        return web_bending_outplane, web_bending_cap, stress_ratio

