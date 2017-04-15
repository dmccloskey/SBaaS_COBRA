# System
import json
# SBaaS
from .stage02_physiology_measuredData_query import stage02_physiology_measuredData_query
from SBaaS_base.sbaas_template_io import sbaas_template_io
# Resources
from io_utilities.base_importData import base_importData
from io_utilities.base_exportData import base_exportData
from ddt_python.ddt_container_filterMenuAndChart2dAndTable import ddt_container_filterMenuAndChart2dAndTable
from ddt_python.ddt_container import ddt_container

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
    def export_dataStage02PhyusiologyMeasuredCoverage_js(
        self,analysis_id_I,single_plot_I=False,
        data_dir_I='tmp',
        ):
        """
        Horizontal pies chart representing the following:
        model unmapped
        measured unmapped
        measured mapped to model

        """

        

        # make the data parameters
        data1_keys = [
                    'experiment_id',
                    'model_id',
                    'sample_name_abbreviation',
                    'model_component',
                    'data_component',
                    ];
        data1_nestkeys = [
            'left',
            'right',
                          ];
        data1_keymap = {'xdata':'node_id',
                        'ydata':'weight',
                        'serieslabel':'algorithm',
                        'featureslabel':''};

        svgparameters = {
            "svgmargin":{ 'top': 100, 'right': 100, 'bottom': 100, 'left': 100 },
            "svgwidth":500,
            "svgheight":500,
            "svgduration":750,
            'colclass':"col-sm-12",
            'svgcolorcategory':'blue2red64',
            'svgcolordomain':'min,max',
			'svgcolordatalabel':'parent_classes',
            'svgcolorscale':'quantile',
            };
        
        nsvgtable = ddt_container_filterMenuAndChart2dAndTable();
        nsvgtable.make_filterMenuAndChart2dAndTable(
            data_filtermenu=data_reactions_O,
            data_filtermenu_keys=data1_keys,
            data_filtermenu_nestkeys=data1_nestkeys,
            data_filtermenu_keymap=data1_keymap,
            data_svg_keys=None,
            data_svg_nestkeys=None,
            data_svg_keymap=data2_keymap,
            data_table_keys=None,
            data_table_nestkeys=None,
            data_table_keymap=None,
            data_svg=None,
            data_table=data_O,
            svgtype='verticalpieschart2d_01',
            tabletype='responsivetable_01',
            svgx1axislabel='',
            svgy1axislabel='',
            tablekeymap = [data1_keymap],
            svgkeymap = [data2_keymap],
            formtile2datamap=[0],
            tabletile2datamap=[1],
            svgtile2datamap=[0],
            svgfilters=None,
            svgtileheader='Shortest Path',
            tablefilters=None,
            tableheaders=None,
            svgparameters_I= svgparameters,
            );

        if data_dir_I=='tmp':
            filename_str = self.settings['visualization_data'] + '/tmp/ddt_data.js'
        elif data_dir_I=='data_json':
            data_json_O = nsvgtable.get_allObjects_js();
            return data_json_O;
        with open(filename_str,'w') as file:
            file.write(nsvgtable.get_allObjects());

   