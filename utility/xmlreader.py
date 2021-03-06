from xml.dom import minidom


class XMLReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.doc = minidom.parse(self.file_path)

    # read Project Description from file
    def readProjectDesc(self, project_desc):
        project = self.doc.getElementsByTagName('project')[0]
        project_desc['job_no'] = project.getAttribute('job_no')
        project_desc['project_symbol'] = project.getAttribute('project_symbol')
        project_desc['project_title'] = project.getAttribute('project_title')
        project_desc['client'] = project.getAttribute('client')
        project_desc['item'] = project.getAttribute('item')
        project_desc['designed_by'] = project.getAttribute('designed_by')
        project_desc['rev'] = project.getAttribute('rev')

    # read Material Strength from file
    def readMaterial(self):
        material = self.doc.getElementsByTagName('material')[0]
        mat_strength = (material.getAttribute('steel'), material.getAttribute('bolt'), material.getAttribute('weld'))
        return mat_strength

    # read Connection Geometry from file (type of connection, properties of member and connection configuration)
    def readConnGeometry(self, conn_geometry):
        connection = self.doc.getElementsByTagName('connection')[0]
        conn_type = connection.getAttribute('type')
        member = self.doc.getElementsByTagName('member')[0]
        conn_geometry['size'] = member.getAttribute('size')
        geometry = self.doc.getElementsByTagName('geometry')[0]
        conn_geometry['dia'] = geometry.getAttribute('dia')
        conn_geometry['nos'] = geometry.getAttribute('nos')
        conn_geometry['col'] = geometry.getAttribute('col')
        conn_geometry['spacing'] = geometry.getAttribute('spacing')
        conn_geometry['weld'] = geometry.getAttribute('weld')
        conn_geometry['ev'] = geometry.getAttribute('ev')
        conn_geometry['eh'] = geometry.getAttribute('eh')
        conn_geometry['tg'] = geometry.getAttribute('tg')
        conn_geometry['H'] = geometry.getAttribute('H')
        conn_geometry['c'] = geometry.getAttribute('c')
        support = self.doc.getElementsByTagName('support')[0]
        conn_geometry['size2'] = support.getAttribute('size2')
        conn_geometry['support'] = support.getAttribute('support')
        return conn_type

    # read the loadings from file
    def readLoads(self, load_data):
        load_item = []
        loads = self.doc.getElementsByTagName('load')
        for load in loads:
            member = load.getAttribute('member')
            load_comb = load.getAttribute('load_comb')
            node = load.getAttribute('node')
            Fx = load.getAttribute('Fx')
            Fy = load.getAttribute('Fy')
            Fz = load.getAttribute('Fz')
            Mz = load.getAttribute('My')
            My = load.getAttribute('Mz')
            load_item = [member, load_comb, node, Fx, Fy, Fz, My, Mz]
            load_data.append(load_item)


