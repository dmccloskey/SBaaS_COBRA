# System
import json
# SBaaS
from .stage02_physiology_pairWiseTest_query import stage02_physiology_pairWiseTest_query
from SBaaS_base.sbaas_template_io import sbaas_template_io
# Resources
from io_utilities.base_importData import base_importData
from io_utilities.base_exportData import base_exportData

class stage02_physiology_pairWiseTest_io(stage02_physiology_pairWiseTest_query,
                                     sbaas_template_io):
    def import_data_stage02_physiology_pairWiseTest_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_data_stage02_physiology_pairWiseTest(data.data);
        data.clear_data();
    #def export_volcanoPlot_d3(self,experiment_id_I,simulation_ids_I = [],
    #                            model_ids_dict_I={},
    #                            rxn_ids_I=[],
    #                            rxn_ids_filter_I=[],
    #                            json_var_name='data',
    #                            filename=[settings.visualization_data,'/physiology/scatterplot/','volcanoplot/']):
    #    '''generate a volcano plot from pairwiseTest table'''

    #    print('exporting volcanoPlot...')
    #    filter_O={}
    #    filter_O['sample'] = [];
    #    # get all simulations for a given experiment
    #    if simulation_ids_I:
    #        simulation_ids = simulation_ids_I;
    #    else:
    #        simulation_ids = [];
    #        simulation_ids = self.get_simulationID_experimentID_dataStage02PhysiologySimulation(experiment_id_I);
    #    for simulation_id_1 in simulation_ids:
    #        # get simulation information
    #        simulation_1_info = [];
    #        simulation_1_info = self.get_rows_simulationID_dataStage02PhysiologySimulation(simulation_id_1);
    #        sna_1 = simulation_1_info[0]['sample_name_abbreviation']
    #        model_id = simulation_1_info[0]['model_id']
    #        # get the cobra model
    #        if model_ids_dict_I:
    #            cobra_model = model_ids_dict_I[model_id];
    #        else:
    #            cobra_model_sbml = None;
    #            cobra_model_sbml = self.get_row_modelID_datastage02PhysiologyModels(model_id);
    #            # write the model to a temporary file
    #            with open('data/cobra_model_tmp.xml','wb') as file:
    #                file.write(cobra_model_sbml['model_file']);
    #            # Read in the sbml file and define the model conditions
    #            cobra_model = create_cobra_model_from_sbml_file('data/cobra_model_tmp.xml', print_time=True);
    #        # reactions to screen
    #        system_boundaries = [x.id for x in cobra_model.reactions if x.boundary == 'system_boundary'];
    #        objectives = [x.id for x in cobra_model.reactions if x.objective_coefficient == 1];
    #        for simulation_id_2 in simulation_ids:
    #            simulation_2_info = [];
    #            simulation_2_info = self.get_rows_simulationID_dataStage02PhysiologySimulation(simulation_id_2);
    #            sna_2 = simulation_2_info[0]['sample_name_abbreviation']
    #            # get simulation information
    #            if sna_1 != sna_2:
    #                # get data:
    #                data_1 = [];
    #                data_1 = self.get_RDataList_simulationIDs_dataStage02PhysiologyPairWiseTest(simulation_id_1,simulation_id_2);
    #                if data_1:
    #                    filter_sna_str = 'sample/'+sna_1 + '_' + sna_2;
    #                    filter_O['sample'].append(filter_sna_str);
    #                    print('exporting a volcano plot for sample_name_abbreviation ' + sna_1 + ' vs. ' + sna_2);
    #                    # filter out specific reactions
    #                    if rxn_ids_I:
    #                        data_1 = [x for x in data_1 if x['rxn_id'] in rxn_ids_I];
    #                    if rxn_ids_filter_I:
    #                        data_1 = [x for x in data_1 if not x['rxn_id'] in rxn_ids_filter_I]
    #                    else: # use default filters
    #                        data_1 = [x for x in data_1 if not (x['rxn_id'] in system_boundaries or x['rxn_id'] in objectives)]
    #                    # plot the data
    #                    title = sna_1 + ' vs. ' + sna_2;
    #                    xlabel = 'Mean Difference [Flux]';
    #                    ylabel = 'Probability [-log10(P)]';
    #                    x_data = [d['mean'] for d in data_1];
    #                    y_data = [d['pvalue_negLog10'] for d in data_1];
    #                    text_labels = [t['rxn_id'] for t in data_1];
    #                    #self.matplot.volcanoPlot(title,xlabel,ylabel,x_data,y_data,text_labels);
    #                    # initialize js variables
    #                    json_O = {};
    #                    options_O = {};
    #                    options_O['x_axis_label'] = 'Mean Difference [Flux]';
    #                    options_O['y_axis_label'] = 'Probability [-log10(P)]';
    #                    options_O['feature_name'] = 'reaction_id';
    #                    options_O['legend'] = False;
    #                    options_O['text_labels'] = True;
    #                    options_O['filter_by'] = 'labels';
    #                    # assign data to the js variables
    #                    data_O = [];
    #                    for d in data_1:
    #                        tmp = {};
    #                        tmp['x_data']=d['mean'];
    #                        tmp['y_data']=d['pvalue_negLog10'];
    #                        tmp['text_labels']=d['rxn_id'];
    #                        tmp['samples']=title;
    #                        data_O.append(tmp);
    #                    json_O['data'] = data_O;
    #                    json_O['options'] = options_O;
    #                    # dump the data to a json file
    #                    json_str = 'var ' + json_var_name + ' = ' + json.dumps(json_O);
    #                    filename_str = filename[0] + '/' + experiment_id_I + filename[1] + filename[2] + sna_1 + '_' + sna_2 + '.js';
    #                    with open(filename_str,'w') as file:
    #                        file.write(json_str);
    #    # dump the filter data to a json file
    #    json_str = 'var ' + 'data_filter' + ' = ' + json.dumps(filter_O);
    #    filename_str = filename[0] + '/' + experiment_id_I + filename[1] + filename[2] + 'filter.js'
    #    with open(filename_str,'w') as file:
    #        file.write(json_str)
   