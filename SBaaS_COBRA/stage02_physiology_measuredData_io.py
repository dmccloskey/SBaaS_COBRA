# System
import json
# SBaaS
from .stage02_physiology_measuredData_query import stage02_physiology_measuredData_query
from SBaaS_base.sbaas_template_io import sbaas_template_io
# Resources
from io_utilities.base_importData import base_importData
from io_utilities.base_exportData import base_exportData

class stage02_physiology_measuredData_io(stage02_physiology_measuredData_query,
                                         sbaas_template_io):
    def import_dataStage02PhysiologyMetabolomicsData_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_dataStage02PhysiologyMetabolomicsData(data.data);
        data.clear_data();

    def import_dataStage02PhysiologyMetabolomicsData_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage02PhysiologyMetabolomicsData(data.data);
        data.clear_data();
    def import_dataStage02PhysiologyMeasuredFluxes_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_dataStage02PhysiologyMeasuredFluxes(data.data);
        data.clear_data();

    def import_dataStage02PhysiologyMeasuredFluxes_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage02PhysiologyMeasuredFluxes(data.data);
        data.clear_data();
   