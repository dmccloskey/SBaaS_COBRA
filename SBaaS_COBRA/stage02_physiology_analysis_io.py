# System
import json
# SBaaS
from .stage02_physiology_analysis_query import stage02_physiology_analysis_query
from SBaaS_base.sbaas_template_io import sbaas_template_io
# Resources
from io_utilities.base_importData import base_importData
from io_utilities.base_exportData import base_exportData

class stage02_physiology_analysis_io(stage02_physiology_analysis_query,
                                     sbaas_template_io):
    def import_data_stage02_physiology_analysis_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_data_stage02_physiology_analysis(data.data);
        data.clear_data();
   