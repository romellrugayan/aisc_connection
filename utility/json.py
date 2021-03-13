import json


class WriteJson:

    def __init__(self, filename):
        self.input_data = {}
        self.filename = filename

    def projectDesc(self, project_desc):
        self.input_data["job_no"] = project_desc['job_no']
        self.input_data["project_symbol"] = project_desc['project_symbol']
        self.input_data["project_title"] = project_desc['project_title']
        self.input_data["client"] = project_desc['client']
        self.input_data["item"] = project_desc['item']
        self.input_data["designed_by"] = project_desc['designed_by']
        self.input_data['rev'] = project_desc['rev']

    def material(self, mat_specs):
        self.input_data["material"] = {"steel": mat_specs[0], "bolt": mat_specs[1], "weld": mat_specs[2]}

    def connGeometry(self, conn_type, conn_geometry):
        self.input_data["conn_type"] = conn_type
        self.input_data["member"] = conn_geometry['size']
        self.input_data["geometry"] = {"dia": conn_geometry['dia'], "nos": conn_geometry['nos'],
                                       "col": conn_geometry['col'], "spacing": conn_geometry['spacing'],
                                       "weld": conn_geometry['weld'], "ev": conn_geometry['ev'],
                                       "eh": conn_geometry['eh'], "tg": conn_geometry['tg'],
                                       "H": conn_geometry['H'], "c": conn_geometry['c']}
        self.input_data["support"] = {"supporting_member": conn_geometry['size2'],
                                      "support_type": conn_geometry['support']}

    def loadings(self, load_data):
        self.input_data["loads"] = load_data

    def dumpJson(self):
        json_file = open(self.filename, "w")
        json.dump(self.input_data, json_file, indent=2)
        json_file.close()


class ReadJson:

    def __init__(self, filename):
        json_file = open(filename, "r")
        self.input_data = json.load(json_file)
        json_file.close()

    def projectDesc(self, project_desc):
        project_desc['job_no'] = self.input_data['job_no']
        project_desc['project_symbol'] = self.input_data['project_symbol']
        project_desc['project_title'] = self.input_data['project_title']
        project_desc['client'] = self.input_data['client']
        project_desc['item'] = self.input_data['item']
        project_desc['designed_by'] = self.input_data['designed_by']
        project_desc['rev'] = self.input_data['rev']

    def material(self):
        material = self.input_data['material']
        return material['steel'], material['bolt'], material['weld']

    def connGeometry(self, conn_geometry):
        conn_type = self.input_data['conn_type']
        conn_geometry['size'] = self.input_data['member']
        geometry = self.input_data['geometry']
        conn_geometry['dia'] = geometry['dia']
        conn_geometry['nos'] = geometry['nos']
        conn_geometry['col'] = geometry['col']
        conn_geometry['spacing'] = geometry['spacing']
        conn_geometry['weld'] = geometry['weld']
        conn_geometry['ev'] = geometry['ev']
        conn_geometry['eh'] = geometry['eh']
        conn_geometry['tg'] = geometry['tg']
        conn_geometry['H'] = geometry['H']
        conn_geometry['c'] = geometry['c']
        support = self.input_data['support']
        conn_geometry['size2'] = support['supporting_member']
        conn_geometry['support'] = support['support_type']
        return conn_type

    def loadings(self, load_data):
        for load in self.input_data['loads']:
            load_data.append(load)