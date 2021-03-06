import math


class BoltShear:

    def __init__(self, bolt_nos, col_nos, spacing):
        self.bolt_nos = bolt_nos
        self.col_nos = col_nos
        self.spacing = spacing

    # calculate bolt group modulus
    def calcBoltModulus(self):
        if self.col_nos == 1:
            Zbx = self.bolt_nos * (self.bolt_nos + 1) * self.spacing / 6
            Zby = 0
        elif self.col_nos == 2 and self.bolt_nos >= 4:
            bolt_per_col = int(self.bolt_nos / self.col_nos)
            y_max = (bolt_per_col - 1) * self.spacing / 2
            Ix = 0
            for y in range(int(bolt_per_col / 2)):
                Ix = Ix + 4 * (y_max - y * self.spacing) ** 2
            Iy = 2 * bolt_per_col * (self.spacing / 2) ** 2
            Ib = Ix + Iy
            Zby = Ib / (self.spacing / 2)
            Zbx = Ib / y_max
        else:
            Zbx = 0
            Zby = 2*(self.spacing/2)
        return round(Zbx, 2), round(Zby, 2)

    # calculate actual bolt shear
    def calculateBoltShear(self, axial_force, shear_force, shear_ecc):
        Zb = self.calcBoltModulus()
        if self.col_nos == 1:
            Vy1 = shear_force / self.bolt_nos
            Vy2 = 0
            Vx1 = axial_force / self.bolt_nos
            Vx2 = shear_force * shear_ecc / Zb[0]
        elif self.col_nos == 2 and self.bolt_nos >= 4:
            Vy1 = shear_force / self.bolt_nos
            Vy2 = shear_force * shear_ecc / Zb[1]
            Vx1 = axial_force / self.bolt_nos
            Vx2 = shear_force * shear_ecc / Zb[0]
        else:
            Vy1 = shear_force / self.bolt_nos
            Vy2 = shear_force * shear_ecc / Zb[1]
            Vx1 = axial_force / self.bolt_nos
            Vx2 = 0
        return math.sqrt((Vx1 + Vx2) ** 2 + (Vy1 + Vy2) ** 2)


