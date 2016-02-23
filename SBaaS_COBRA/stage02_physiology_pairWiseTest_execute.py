#SBaaS
from .stage02_physiology_pairWiseTest_io import stage02_physiology_pairWiseTest_io
# resources
from python_statistics.calculate_interface import calculate_interface
from .sampling import cobra_sampling,cobra_sampling_n
# Dependencies from cobra
from cobra.io.sbml import create_cobra_model_from_sbml_file, write_cobra_model_to_sbml_file
from cobra.flux_analysis.variability import flux_variability_analysis
from cobra.flux_analysis.parsimonious import optimize_minimal_flux
from cobra.flux_analysis import flux_variability_analysis
from cobra.manipulation.modify import convert_to_irreversible

class stage02_physiology_pairWiseTest_execute(stage02_physiology_pairWiseTest_io):
    #TODO:
    def execute_samplingPairWiseTests(self,simulation_ids_I=[],
                    rxn_ids_I=[],
                    control_I=False,
                    data_dir_I='C:/Users/dmccloskey-sbrg/Documents/MATLAB/sampling_physiology',
                    models_I = {},
                    ):
        '''calculate the p-value and mean difference between sampling distributions
        INPUT:
        simulation_ids_I = [] of strings, list of simulation ids
        rxn_ids_I = [] of strings, list of reaction ids
        control_I = True: simulation_ids_I[0]=control,simulation_ids_I[1:]=perturbation
                    False: pairwise test is performed on all
        data_dir_I = string, directory of the sampled points file
        models_I = {} string:cobra_model object, model_id:cobra_model
        '''
        
        data_dir = data_dir_I;
        models = models_I;

        # get simulation information
        simulation_info_all = [];
        for simulation_id in simulation_ids_I:
            simulation_info_1_all = [];
            simulation_info_1_all = self.stage02_physiology_query.get_rows_simulationID_dataStage02PhysiologySimulation(simulation_id);
            if not simulation_info_1_all:
                print('simulation not found!')
                return;
            simulation_1_info = simulation_info_1_all[0]; # unique constraint guarantees only 1 row will be returned
            simulation_info_all.append(simulation_1_info);
        # get sampled_data
        sampledPoints_all = [];
        for simulation_id in simulation_ids_I:
            sampledPoints_1_all = [];
            sampledPoints_1_all = self.stage02_physiology_query.get_rows_simulationID_dataStage02PhysiologySampledPoints(simulation_id);
            if not sampledPoints_1_all:
                print('simulation not found!')
                return;
            sampledPoints_1_info = sampledPoints_1_all[0]; # unique constraint guarantees only 1 row will be returned
            sampledPoints_all.append(sampledPoints_1_info);
        # get simulation parameters
        simulation_parameters_all = [];
        for simulation_id in simulation_ids_I:
            simulation_parameters_1_all = [];
            simulation_parameters_1_all = self.stage02_physiology_query.get_rows_simulationID_dataStage02PhysiologySimulationParameters(simulation_id);
            if not simulation_parameters_1_all:
                print('simulation not found!')
                return;
            simulation_1_parameters = simulation_parameters_1_all[0]; # unique constraint guarantees only 1 row will be returned
            simulation_parameters_all.append(simulation_1_parameters);
        # check that all models are the same
        model_ids_all = [x['model_id'] for x in simulation_info_all]
        model_ids_unique = list(set(model_ids_all));
        if len(model_ids_unique) != 1:
            print('more than 1 model_id found')
            return
        else:
            model_id = model_ids_unique[0];
        # get the base cobra model
        cobra_model = models[model_id];
        # extract out the data directories and simulation_ids
        data_dirs = [x['data_dir'] for x in sampledPoints_all]
        simulation_ids = [x['simulation_id'] for x in sampledPoints_all]
        infeasible_loops = [x['infeasible_loops'] for x in sampledPoints_all]
        # extract out sampling parameters
        sampler_ids = [x['sampler_id'] for x in simulation_parameters_all]
        # make filename points
        filename_points = [s + '_points' + '.mat' for s in simulation_ids_I];
        # perform the analysis
        sampling_n = cobra_sampling_n(data_dir_I=data_dir,
                                      model_I = cobra_model,
                                      loops_I = infeasible_loops,
                                      sample_ids_I = simulation_ids,
                                      samplers_I = sampler_ids,
                                      control_I = control_I);
        sampling_n.get_points(filename_points);
        #pairwisetest
        sampling_n.calculate_pairWiseTest();
        # load data into the database
        for d in sampling_n.data:
            row = None;
            row = data_stage02_physiology_pairWiseTest(
                d['sample_id_1'],
                d['sample_id_2'],
                d['rxn_id'],
                'mmol*gDW-1*hr-1',
                d['mean_difference'],
                d['test_stat'],
                d['test_description'],
                d['pvalue'],
                None,None,None,None,None,
                d['fold_change'],
                True,None
                )
            self.session.add(row);
        self.session.commit();
        ##pairwisetest_metabolites
        #sampling_n.calculate_pairWiseTest_metabolites();
        ## load data into the database
        #for d in sampling_n.data:
        #    row = None;
        #    row = data_stage02_physiology_pairWiseTestMetabolites(
        #        d['sample_id_1'],
        #        d['sample_id_2'],
        #        d['met_id'],
        #        'mmol*gDW-1*hr-1',
        #        d['mean_difference'],
        #        d['test_stat'],
        #        d['test_description'],
        #        d['pvalue'],
        #        None,None,None,None,None,
        #        d['fold_change'],
        #        True,None
        #        )
        #    self.session.add(row);
        #self.session.commit();
        ##pairwisetest_subsystems
        #sampling_n.calculate_pairWiseTest_subsystems();
        ## load data into the database
        #for d in sampling_n.data:
        #    row = None;
        #    row = data_stage02_physiology_pairWiseTestSubsystems(
        #        d['sample_id_1'],
        #        d['sample_id_2'],
        #        d['subsystem_id'],
        #        'mmol*gDW-1*hr-1',
        #        d['mean_difference'],
        #        d['test_stat'],
        #        d['test_description'],
        #        d['pvalue'],
        #        None,None,None,None,None,
        #        d['fold_change'],
        #        True,None
        #        )
        #    self.session.add(row);
        #self.session.commit();