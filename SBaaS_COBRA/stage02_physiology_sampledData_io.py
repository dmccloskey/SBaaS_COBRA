# System
import json
# SBaaS
from .stage02_physiology_sampledData_query import stage02_physiology_sampledData_query
from .stage02_physiology_analysis_query import stage02_physiology_analysis_query
from SBaaS_base.sbaas_template_io import sbaas_template_io
# Resources
from io_utilities.base_importData import base_importData
from io_utilities.base_exportData import base_exportData
from listDict.listDict import listDict
from .sampling import cobra_sampling,cobra_sampling_n
from python_statistics.calculate_histogram import calculate_histogram
from ddt_python.ddt_container_filterMenuAndChart2dAndTable import ddt_container_filterMenuAndChart2dAndTable


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

    def export_dataStage02PhysiologySampledPoints_js(self,
        analysis_id_I,
        query_I={},
        data_dir_I='tmp'
        ):
        '''Visualize the sampling distribution
        DESCRIPTION:
        tile1=filtermenu
        tile2=sampling distribution
        tile3=table
        '''
        calculatehistogram = calculate_histogram();
        physiology_analysis_query = stage02_physiology_analysis_query(self.session,self.engine,self.settings);
        data_sampledPoints_O = [];
        data_O = [];
        #get the analysis info
        simulation_ids = physiology_analysis_query.get_simulationID_analysisID_dataStage02PhysiologyAnalysis(analysis_id_I);
        for simulation_id in simulation_ids:
            #get the data_dirs for the simulations and read in the points
            sampledPoints = self.get_rows_simulationID_dataStage02PhysiologySampledPoints(simulation_id);
            sampledPoints = sampledPoints[0];
            data_sampledPoints_O.append(sampledPoints);
            # get simulation information
            simulation_info_all = [];
            simulation_info_all = self.get_rows_simulationIDAndSimulationType_dataStage02PhysiologySimulation(simulation_id,'sampling');
            if not simulation_info_all:
                print('simulation not found!')
                return;
            simulation_info = simulation_info_all[0]; # unique constraint guarantees only 1 row will be returned
            # get simulation parameters
            simulation_parameters_all = [];
            simulation_parameters_all = self.get_rows_simulationID_dataStage02PhysiologySamplingParameters(simulation_id);
            if not simulation_parameters_all:
                print('simulation not found!')
                return;
            simulation_parameters = simulation_parameters_all[0]; # unique constraint guarantees only 1 row will be returned
            #fill the sampledData with the actual points
            sampling = cobra_sampling(model_I=None,data_dir_I = sampledPoints['data_dir'],loops_I=sampledPoints['infeasible_loops']);
            if simulation_parameters['sampler_id']=='gpSampler':
                # load the results of sampling
                sampling.get_points_matlab(matlab_data=None,sampler_model_name='sampler_out');
                sampling.remove_loopsFromPoints();
            elif simulation_parameters['sampler_id']=='optGpSampler':
                return;
            else:
                print('sampler_id not recognized');
            #store the sampledPoints
            for k,v in sampling.points.items():
                n_bins = 100;
                calc_bins_I = False;
                x_O,dx_O,y_O = calculatehistogram.histogram(data_I=v,n_bins_I=n_bins,calc_bins_I=calc_bins_I);
                for i,b in enumerate(x_O):
                    tmp = {
                        'simulation_id':simulation_id,
                        'rxn_id':k,
                        #'feature_units':feature_units,
                        'bin':b,
                        'bin_width':dx_O[i],
                        'frequency':int(y_O[i]),
                        'used_':True,
                        'comment_':None};
                    data_O.append(tmp);
            #data_listDict = listDict();
            #data_listDict.set_dictList(sampling.points);
            #data_listDict.convert_dictList2DataFrame();
            #points, rxn_ids = data_listDict.get_flattenedDataAndColumnLabels();
            #data_listDict.clear_allData();
            #data_listDict.add_column2DataFrame('rxn_id',rxn_ids);
            #data_listDict.add_column2DataFrame('points',points);
            #data_listDict.add_column2DataFrame('simulation_id',simulation_id);
            #data_listDict.convert_dataFrame2ListDict();
            #data_O.extend(data_listDict.get_listDict());
        #make the DDT histograms  
        # visualization parameters
        data1_keys = ['simulation_id',
                      'rxn_id',
                      'bin',
                      ];
        data1_nestkeys = [
            'bin'
            ];
        data1_keymap = {
                'xdata':'bin',
                'ydata':'frequency',
                'serieslabel':'simulation_id',
                'featureslabel':'bin',
                'tooltiplabel':'rxn_id',
                'ydatalb':None,
                'ydataub':None};
        
        
        nsvgtable = ddt_container_filterMenuAndChart2dAndTable();
        nsvgtable.make_filterMenuAndChart2dAndTable(
            data_filtermenu=data_O,
            data_filtermenu_keys=data1_keys,
            data_filtermenu_nestkeys=data1_nestkeys,
            data_filtermenu_keymap=data1_keymap,
            data_svg_keys=None,
            data_svg_nestkeys=None,
            data_svg_keymap=None,
            data_table_keys=None,
            data_table_nestkeys=None,
            data_table_keymap=None,
            data_svg=None,
            data_table=None,
            svgtype='verticalbarschart2d_01',
            tabletype='responsivetable_01',
            svgx1axislabel='',
            svgy1axislabel='',
            tablekeymap = [data1_keymap],
            svgkeymap = [data1_keymap],
            formtile2datamap=[0],
            tabletile2datamap=[0],
            svgtile2datamap=[0], #calculated on the fly
            svgfilters=None,
            svgtileheader='Sampled points',
            tablefilters=None,
            tableheaders=None
            );

        if data_dir_I=='tmp':
            filename_str = self.settings['visualization_data'] + '/tmp/ddt_data.js'
        elif data_dir_I=='data_json':
            data_json_O = nsvgtable.get_allObjects_js();
            return data_json_O;
        with open(filename_str,'w') as file:
            file.write(nsvgtable.get_allObjects());
   