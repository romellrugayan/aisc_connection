import math


class MaterialStrength:
    """ Set the material strength """

    _plate_yield = {'A36': 36, 'A992': 50}
    _plate_tensile = {'A36': 60, 'A992': 65}
    _bolt_tensile = {'A325-N': 120, 'A325-X': 120, 'A490-N': 150, 'A490-X': 150}
    _weld_tensile = {'E60XX': 60, 'E70XX': 70}

    def __init__(self, plate, bolt, weld):
        self.plate = plate
        self.bolt = bolt
        self.weld = weld
        self.Fy = self._plate_yield[self.plate]
        self.Fup = self._plate_tensile[self.plate]
        self.Fub = self._bolt_tensile[self.bolt]
        self.Fw = self._weld_tensile[self.weld]

        # nominal shear strength of bolt
        if self.bolt == 'A325-N' or self.bolt == 'A490-N':
            self.Fnv = 0.45 * self.Fub
        else:
            self.Fnv = 0.563 * self.Fub

        # nominal tensile strength of bolt
        self.Fnt = 0.75 * self.Fub

        # nominal welding strength
        self.Fnw = 0.6 * self.Fw

        # initialize buckling strength
        self.Fcr = 0

    # bolt shear strength
    def bolt_shear_cap(self, bolt_dia):
        bolt_area = math.pi * bolt_dia ** 2 / 4
        return 0.75 * bolt_area * self.Fnv

    # bolt tensile strength
    def bolt_tensile_cap(self, bolt_dia):
        bolt_area = math.pi * bolt_dia ** 2 / 4
        return 0.75 * bolt_area * self.Fnt

    # bearing strength at bolt hole
    def bolt_hole_bearing(self, bolt_dia, plate_thickness, edge_distance):
        bearing1 = 1.2 * edge_distance * plate_thickness * self.Fup
        bearing2 = 2.4 * bolt_dia * plate_thickness * self.Fup
        if bearing1 <= bearing2:
            return 0.75 * bearing1
        else:
            return 0.75 * bearing2

    # welding shear strength
    def fillet_weld_shear(self, weld_size, angle):
        return 0.75 * 0.707 * weld_size * (1 + 0.5 * (math.sin(angle * math.pi / 180)) ** 1.5) * self.Fnw

    # shear yielding of plate
    def plate_shear_yielding(self, gross_area):
        return 1.0 * 0.6 * self.Fy * gross_area

    # shear rupture of plate
    def plate_shear_rupture(self, net_area):
        return 0.75 * 0.6 * self.Fup * net_area

    # block shear strength of plate
    def plate_block_shear(self, shear_gross_area, shear_net_area, tension_net_area, Ubs):
        block_shear1 = 0.6 * self.Fup * shear_net_area + Ubs * self.Fup * tension_net_area
        block_shear2 = 0.6 * self.Fy * shear_gross_area + Ubs * self.Fup * tension_net_area
        if block_shear1 <= block_shear2:
            return 0.75 * block_shear1
        else:
            return 0.75 * block_shear2

    # tensile yielding of plate
    def plate_tensile_yielding(self, gross_area):
        return 0.9 * self.Fy * gross_area

    # tensile rupture of plate
    def plate_tensile_rupture(self, effective_net_area):
        return 0.75 * self.Fup * effective_net_area

    # compressive strength of plate
    def plate_compression_strength(self, gross_area, slenderness_ratio):
        if slenderness_ratio <= 25:
            return 0.9 * self.Fy * gross_area
        else:
            Fe = (math.pi ** 2) * 29000 / slenderness_ratio ** 2
            if slenderness_ratio <= 4.71 * math.sqrt(29000 / self.Fy):
                self.Fcr = (0.658 ** (self.Fy / Fe)) * self.Fy
            else:
                self.Fcr = 0.877 * Fe
            return 0.9 * self.Fcr * gross_area

    # bending strength of plate
    def plate_bending_strength(self, plastic_modulus):
        return 0.9 * self.Fy * plastic_modulus
