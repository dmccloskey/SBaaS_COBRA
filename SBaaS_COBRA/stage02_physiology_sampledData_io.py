# System
import json
# SBaaS
from .stage02_physiology_sampledData_query import stage02_physiology_sampledData_query
from SBaaS_base.sbaas_template_io import sbaas_template_io
# Resources
from io_utilities.base_importData import base_importData
from io_utilities.base_exportData import base_exportData

class stage02_physiology_sampledData_io(stage02_physiology_sampledData_query,
                                        sbaas_template_io):
    def import_dataStage02PhysiologySamplingParameters_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_dataStage02PhysiologySamplingParameters(data.data);
        data.clear_data();
    def import_dataStage02PhysiologySamplingParameters_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage02PhysiologySamplingParameters(data.data);
   