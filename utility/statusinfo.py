import sqlite3


class StatusInfo:
    def __init__(self, text_edit, conn_type, geometry):
        self.text_edit = text_edit
        self.conn_type = conn_type
        self.geometry = geometry

        # get the member properties both for beam and supporting member
        db = sqlite3.connect('./data/aisc.db')
        db.row_factory = sqlite3.Row
        cur = db.cursor()
        member = (self.geometry['size'],)
        cur.execute("SELECT * FROM section WHERE size=?", member)
        data = dict(cur.fetchone())
        self.d = data['d']
        self.bf = data['bf']
        self.tw = data['tw']
        self.tf = data['tf']
        self.k = data['k']
        member = (self.geometry['size2'],)
        cur.execute("SELECT * FROM section WHERE size=?", member)
        data = dict(cur.fetchone())
        self.d2 = data['d']
        self.bf2 = data['bf']
        self.tw2 = data['tw']
        self.tf2 = data['tf']
        self.k2 = data['k']
        db.close()
        self.dia = float(self.geometry['dia'])
        self.nos = int(self.geometry['nos'])
        self.spacing = float(self.geometry['spacing'])
        self.ev = float(self.geometry['ev'])
        self.eh = float(self.geometry['eh'])
        self.H = float(self.geometry['H'])
        self.c = float(self.geometry['c'])
        self.support = self.geometry['support']
        if self.conn_type == 'ShearGusset' or self.conn_type == 'ShearCope':
            self.col = int(self.geometry['col'])
            self.weld = float(self.geometry['weld'])
            self.tg = float(self.geometry['tg'])
        elif self.conn_type == 'ShearClip':
            self.g = float(self.geometry['g'])
            self.ta = float(self.geometry['ta'])

    def displayInfo(self):
        self.text_edit.append('CONNECTION TYPE\t: ' + self.conn_type)
        self.text_edit.append('Member Size\t\t: ' + self.geometry['size'])
        self.text_edit.append('Bolt diameter\t\t: ' + self.geometry['dia'])
        self.text_edit.append('No. of bolts\t\t: ' + self.geometry['nos'])

        if self.conn_type == 'ShearGusset' or self.conn_type == 'ShearCope':
            self.text_edit.append('No. of column of bolts\t: ' + self.geometry['col'])
        elif self.conn_type == 'ShearClip':
            self.text_edit.append('Gage distance\t: ' + self.geometry['g'])

        self.text_edit.append('Bolt spacing\t\t: ' + self.geometry['spacing'])
        self.text_edit.append('Vertical edge distance\t: ' + self.geometry['ev'])
        self.text_edit.append('Horizontal edge distance\t: ' + self.geometry['eh'])
        if self.conn_type == 'ShearGusset' or self.conn_type == 'ShearCope':
            self.text_edit.append('Gusset plate thickness\t: ' + self.geometry['tg'])
            self.text_edit.append('Gusset plate height\t: ' + self.geometry['H'])
            self.text_edit.append('Dist. from TOB to G.Plate\t: ' + self.geometry['c'])
            self.text_edit.append('Weld size\t\t: ' + self.geometry['weld'])
        elif self.conn_type == 'ShearClip':
            self.text_edit.append('Clip angle size\t: ' + self.geometry['clip_size'])
            self.text_edit.append('Clip angle thickness\t: ' + self.geometry['ta'])
            self.text_edit.append('Clip angle height\t: ' + self.geometry['H'])
            self.text_edit.append('Dist. from TOB to Angle\t: ' + self.geometry['c'])

        self.text_edit.append('Supporting member\t: ' + self.geometry['size2'] + ' (' + self.geometry['support'] + ')')
        self.text_edit.append('')

    def checkDimensions(self):
        self.text_edit.append('***')
        h1 = self.c + self.H
        h2 = self.d2 - self.tf2
        if self.support == 'Beam' and h1 > h2:
            self.text_edit.append('* Supporting member depth is smaller than beam depth. NOT recommended!')

        if self.dia < 0.75:
            self.text_edit.append('* Bolt diameter shall not be less than minimum size requirement')

        if self.spacing < 2.375:
            self.text_edit.append('* Bolt spacing shall not be less than minimum spacing requirement.')

        if self.ev < 1.5 or self.eh < 1.5:
            self.text_edit.append('* Edge distance shall not be less than minimum edge distance requirement')

        if self.conn_type == 'ShearGusset' or self.conn_type == 'ShearCope':
            required_d1 = self.c + (self.nos/self.col - 1)*self.spacing + self.ev*2.0 + self.k
        elif self.conn_type == 'ShearClip':
            required_d1 = self.c + (self.nos - 1) * self.spacing + self.ev * 2.0 + self.k
        required_d2 = self.c + self.H + self.k
        if (required_d1 > self.d) or (required_d2 > self.d):
            self.text_edit.append('* Required gusset plate height will not fit to the beam depth')

        if self.conn_type == 'ShearGusset' or self.conn_type == 'ShearCope':
            if self.tg < self.tw:
                self.text_edit.append('* Gusset plate thickness is thinner than beam web thickness. NOT recommended!')











