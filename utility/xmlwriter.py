from xml.dom import minidom


class XMLWriter:
    def __init__(self):
        self.root = minidom.Document()
        self.xml = self.root.createElement('connection_design')
        self.root.appendChild(self.xml)

    def projectDesc(self, project_desc):
        project = self.root.createElement('project')
        project.setAttribute('job_no', project_desc['job_no'])
        project.setAttribute('project_symbol', project_desc['project_symbol'])
        project.setAttribute('project_title', project_desc['project_title'])
        project.setAttribute('client', project_desc['client'])
        project.setAttribute('item', project_desc['item'])
        project.setAttribute('designed_by', project_desc['designed_by'])
        project.setAttribute('rev', project_desc['rev'])
        self.xml.appendChild(project)

    def material(self, mat_strength):
        material = self.root.createElement('material')
        material.setAttribute('steel', mat_strength[0])
        material.setAttribute('bolt', mat_strength[1])
        material.setAttribute('weld', mat_strength[2])
        self.xml.appendChild(material)

    def connGeometry(self, conn_type, conn_geometry):
        connection = self.root.createElement('connection')
        connection.setAttribute('type', conn_type)
        self.xml.appendChild(connection)
        member = self.root.createElement('member')
        member.setAttribute('size', conn_geometry['size'])
        connection.appendChild(member)
        geometry = self.root.createElement('geometry')
        geometry.setAttribute('dia', conn_geometry['dia'])
        geometry.setAttribute('nos', conn_geometry['nos'])
        geometry.setAttribute('col', conn_geometry['col'])
        geometry.setAttribute('spacing', conn_geometry['spacing'])
        geometry.setAttribute('weld', conn_geometry['weld'])
        geometry.setAttribute('ev', conn_geometry['ev'])
        geometry.setAttribute('eh', conn_geometry['eh'])
        geometry.setAttribute('tg', conn_geometry['tg'])
        geometry.setAttribute('H', conn_geometry['H'])
        geometry.setAttribute('c', conn_geometry['c'])
        connection.appendChild(geometry)
        support = self.root.createElement('support')
        support.setAttribute('size2', conn_geometry['size2'])
        support.setAttribute('support', conn_geometry['support'])
        connection.appendChild(support)

    def loadings(self, load_data):
        loads = self.root.createElement('loads')
        self.xml.appendChild(loads)
        for row in range(0, len(load_data)):
            load_item = self.root.createElement('load')
            load_item.setAttribute('member', load_data[row][0])
            load_item.setAttribute('load_comb', str(load_data[row][1]))
            load_item.setAttribute('node', str(load_data[row][2]))
            load_item.setAttribute('Fx', str(load_data[row][3]))
            load_item.setAttribute('Fy', str(load_data[row][4]))
            load_item.setAttribute('Fz', str(load_data[row][5]))
            load_item.setAttribute('My', str(load_data[row][6]))
            load_item.setAttribute('Mz', str(load_data[row][7]))
            loads.appendChild(load_item)

    def saveXMLFile(self, save_path):
        xml_str = self.root.toprettyxml(indent='\t')
        with open(save_path, 'w') as f:
            f.write(xml_str)













