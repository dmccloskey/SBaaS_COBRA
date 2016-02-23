# System
import json
# SBaaS
from .stage02_physiology_simulation_query import stage02_physiology_simulation_query
from SBaaS_base.sbaas_template_io import sbaas_template_io
# Resources
from io_utilities.base_importData import base_importData
from io_utilities.base_exportData import base_exportData
from ddt_python.ddt_container import ddt_container
from listDict.listDict import listDict

class stage02_physiology_simulation_io(stage02_physiology_simulation_query,
                                      sbaas_template_io):

    def import_dataStage02PhysiologySimulation_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_dataStage02PhysiologySimulation(data.data);
        data.clear_data();    

    def import_dataStage02PhysiologySimulation_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage02PhysiologySimulation(data.data);
        data.clear_data();
    def import_dataStage02PhysiologySimulationParameters_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_dataStage02PhysiologySimulationParameters(data.data);
        data.clear_data();
    def import_dataStage02PhysiologySimulationParameters_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage02PhysiologySimulationParameters(data.data);
        data.clear_data();