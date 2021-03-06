from connection.materialstrength import MaterialStrength


class Viewer:
    def __init__(self, text_edit, conn_type):
        self.text_edit = text_edit
        self.conn_type = conn_type

    def displayProject(self, project_desc):
        # self.text_edit.append('PROJECT DESCRIPTION:')
        self.text_edit.append('Job No. : ' + project_desc['job_no'] + '\t\tProject Symbol : ' +
                              project_desc['project_symbol'])
        # self.text_edit.append('Project Symbol: ' + project_desc['project_symbol'])
        self.text_edit.append('Project Title\t\t: ' + project_desc['project_title'])
        self.text_edit.append('Client/Owner\t\t: ' + project_desc['client'])
        self.text_edit.append('Structure Tag\t\t: ' + project_desc['item'])
        self.text_edit.append('')

    def displayMaterial(self, material):
        self.text_edit.append('MATERIAL SPECIFICATION:')
        self.text_edit.append('Structural Steel Section and Plates\t: ' + material[0])
        self.text_edit.append('High Strength Bolt (HSB)\t\t: ' + material[1])
        self.text_edit.append('Weld Metal Filler Classification Strength\t: ' + material[2])
        self.text_edit.append('')

    def displayConnGeometry(self, geometry):
        self.text_edit.append('CONNECTION GEOMETRY:')
        self.text_edit.append('Connection Type \t\t: ' + self.conn_type)
        self.text_edit.append('Beam/Girder size\t\t: ' + geometry['size'])
        self.text_edit.append('Bolt diameter, in\t\t: ' + geometry['dia'])
        self.text_edit.append('No. of bolts\t\t\t: ' + geometry['nos'])
        self.text_edit.append('No. of column of bolts\t\t: ' + geometry['col'])
        self.text_edit.append('Fillet weld size, in\t\t: ' + geometry['weld'])
        self.text_edit.append('Vertical edge distance, in\t\t: ' + geometry['ev'])
        self.text_edit.append('Horizontal edge distance, in\t\t: ' + geometry['eh'])
        self.text_edit.append('Gusset Plate thickness, in\t\t: ' + geometry['tg'])
        self.text_edit.append('Gusset Plate height, in\t\t: ' + geometry['H'])
        self.text_edit.append('Dist. from TOB to G.Plate,in\t\t: ' + geometry['c'])
        self.text_edit.append('Supporting member,\t\t: ' + geometry['size2'] + ' (' + geometry['support'] + ')')
        self.text_edit.append('')

    def displayLoadings(self, loadings):
        self.text_edit.append('LOADINGS:')
        self.text_edit.append('No.\tMember\t' + 'L/C\t' + 'Node\t' + 'Fx(kip)\t' + 'Fy(kip)\t' + 'Fz(kip)\t' +
                              'My(kip-in)\t' + 'Mz(kip-in)')
        index = 0
        for load in loadings:
            self.text_edit.append(str(index + 1) + '\t' + str(load[0]) + '\t' + str(load[1]) + '\t' + str(load[2]) + '\t' +
                                  str(load[3]) + '\t' + str(load[4]) + '\t' + str(load[5]) + '\t' + str(load[6]) +
                                  '\t' + str(load[7]))
            index += 1
        self.text_edit.append('')

    def displayMaterialStrength(self, material):
        ms = MaterialStrength(material[0], material[1], material[2])
        self.text_edit.append('MATERIAL STRENGTH:')
        self.text_edit.append('Structural steel yield strength, ksi\t Fy = ' + str(ms.Fy))
        self.text_edit.append('Steel min. tensile strength, ksi\t Fup = ' + str(ms.Fup))
        self.text_edit.append('HSB min. tensile strength, ksi\t Fub = ' + str(ms.Fub))
        self.text_edit.append('HSB nominal shear stress, ksi\t Fnv = ' + str(ms.Fnv))
        self.text_edit.append('HSB nominal tensile stress, ksi\t Fnt = ' + str(ms.Fnt))
        self.text_edit.append('Weld metal nominal stress, ksi\t Fnw = ' + str(ms.Fnw))
        self.text_edit.append('')

    def displayCalculationResult(self, design_result, calc_result):
        self.text_edit.append('CALCULATION RESULTS:')
        self.text_edit.append('Bolt group modulus, in\t\t Zbx = ' + str(design_result.bolt_modulus[0]))
        self.text_edit.append('Bolt group modulus, in\t\t Zby = ' + str(design_result.bolt_modulus[1]))
        self.text_edit.append('Shear force eccentricity, in\t\t e =' + str(design_result.ecc))
        self.text_edit.append('')
        self.text_edit.append('Mode \t\t\t\tLoad \tActual \tProvided \tU/R')
        self.text_edit.append('Bolt shear strength, kip\t\t\t' + str(calc_result[0][0] + 1) + '\t' + str(calc_result[0][1]) +
                              '\t' + str(calc_result[0][2]) + '\t' + str(calc_result[0][3]))
        self.text_edit.append('Bearing strength on bolt hole, kip\t\t' + str(calc_result[1][0] +1) + '\t' +
                              str(calc_result[1][1]) + '\t' + str(calc_result[1][2]) + '\t' + str(calc_result[1][3]))
        self.text_edit.append('Plate block shear strength, kip\t\t' + str(calc_result[2][0] +1) + '\t' +
                              str(calc_result[2][1]) + '\t' + str(calc_result[2][2]) + '\t' + str(calc_result[2][3]))
        self.text_edit.append('Plate shear yielding, kip\t\t\t' + str(calc_result[3][0] + 1) + '\t' +
                              str(calc_result[3][1]) + '\t' + str(calc_result[3][2]) + '\t' + str(calc_result[3][3]))
        self.text_edit.append('Plate shear rupture, kip\t\t\t' + str(calc_result[4][0] + 1) + '\t' +
                              str(calc_result[4][1]) + '\t' + str(calc_result[4][2]) + '\t' + str(calc_result[4][3]))
        self.text_edit.append('Plate tensile yielding, kip\t\t\t' + str(calc_result[5][0] + 1) + '\t' +
                              str(calc_result[5][1]) + '\t' + str(calc_result[5][2]) + '\t' + str(calc_result[5][3]))
        self.text_edit.append('Plate tensile rupture, kip\t\t\t' + str(calc_result[6][0] + 1) + '\t' +
                              str(calc_result[6][1]) + '\t' + str(calc_result[6][2]) + '\t' + str(calc_result[6][3]))
        self.text_edit.append('Plate in-plane bending, kip-in \t\t' + str(calc_result[7][0] + 1) + '\t' +
                              str(calc_result[7][1]) + '\t' + str(calc_result[7][2]) + '\t' + str(calc_result[7][3]))
        self.text_edit.append('Plate out-of-plane bending, kip-in\t\t' + str(calc_result[8][0] + 1) + '\t' +
                              str(calc_result[8][1]) + '\t' + str(calc_result[8][2]) + '\t' + str(calc_result[8][3]))
        self.text_edit.append('Weld shear strength, kip/in\t\t\t' + str(calc_result[9][0] + 1) + '\t' +
                              str(calc_result[9][1]) + '\t' + str(calc_result[9][2]) + '\t' + str(calc_result[9][3]))
        self.text_edit.append('')
        if self.conn_type == 'ShearCope':
            self.text_edit.append('Web block shear strength, kip\t\t' + str(calc_result[10][0] + 1) + '\t' +
                                  str(calc_result[10][1]) + '\t' + str(calc_result[10][2]) + '\t' + str(
                calc_result[2][3]))
            self.text_edit.append('Web shear yielding, kip\t\t\t' + str(calc_result[11][0] + 1) + '\t' +
                                  str(calc_result[11][1]) + '\t' + str(calc_result[11][2]) + '\t' + str(
                calc_result[3][3]))
            self.text_edit.append('Web shear rupture, kip\t\t\t' + str(calc_result[12][0] + 1) + '\t' +
                                  str(calc_result[12][1]) + '\t' + str(calc_result[12][2]) + '\t' + str(
                calc_result[4][3]))
            self.text_edit.append('Web tensile yielding, kip\t\t\t' + str(calc_result[13][0] + 1) + '\t' +
                                  str(calc_result[13][1]) + '\t' + str(calc_result[13][2]) + '\t' + str(
                calc_result[5][3]))
            self.text_edit.append('Web tensile rupture, kip\t\t\t' + str(calc_result[14][0] + 1) + '\t' +
                                  str(calc_result[14][1]) + '\t' + str(calc_result[14][2]) + '\t' + str(
                calc_result[6][3]))
            self.text_edit.append('Web in-plane bending, kip-in \t\t' + str(calc_result[15][0] + 1) + '\t' +
                                  str(calc_result[15][1]) + '\t' + str(calc_result[15][2]) + '\t' + str(
                calc_result[7][3]))
            self.text_edit.append('Web out-of-plane bending, kip-in\t\t' + str(calc_result[16][0] + 1) + '\t' +
                                  str(calc_result[16][1]) + '\t' + str(calc_result[16][2]) + '\t' + str(
                calc_result[16][3]))
            self.text_edit.append('')
