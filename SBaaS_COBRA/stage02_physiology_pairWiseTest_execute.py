#SBaaS
from .stage02_physiology_pairWiseTest_io import stage02_physiology_pairWiseTest_io
from .stage02_physiology_simulation_query import stage02_physiology_simulation_query
from .stage02_physiology_sampledData_query import stage02_physiology_sampledData_query
from .stage02_physiology_analysis_query import stage02_physiology_analysis_query
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
    def execute_samplingPairWiseTests(self,analysis_id_I=[],
                    rxn_ids_I=[],
                    control_I=False,
                    redundancy_I=False,
                    remove_loops_I=True,
                    remove_no_flux_I=True,
                    normalize_I=True,
                    compare_metabolitePoints_I=True,
                    compare_subsystemPoints_I=True,
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

        physiology_simulation_query = stage02_physiology_simulation_query(self.session,self.engine,self.settings);
        physiology_sampledData_query = stage02_physiology_sampledData_query(self.session,self.engine,self.settings);
        physiology_analysis_query = stage02_physiology_analysis_query(self.session,self.engine,self.settings);

        #get the simulations
        simulation_ids = [];
        simulation_ids = physiology_analysis_query.get_simulationID_analysisID_dataStage02PhysiologyAnalysis(analysis_id_I);

        # get simulation information
        simulation_info_all = [];
        for simulation_id in simulation_ids:
            simulation_info_1_all = [];
            simulation_info_1_all = physiology_simulation_query.get_rows_simulationID_dataStage02PhysiologySimulation(simulation_id);
            if not simulation_info_1_all:
                print('simulation not found!')
                return;
            simulation_1_info = simulation_info_1_all[0]; # unique constraint guarantees only 1 row will be returned
            simulation_info_all.append(simulation_1_info);
        # get sampledPoints
        sampledPoints_all = [];
        for simulation_id in simulation_ids:
            sampledPoints_1_all = [];
            sampledPoints_1_all = physiology_sampledData_query.get_rows_simulationID_dataStage02PhysiologySampledPoints(simulation_id);
            if not sampledPoints_1_all:
                print('simulation not found!')
                return;
            sampledPoints_1_info = sampledPoints_1_all[0]; # unique constraint guarantees only 1 row will be returned
            sampledPoints_all.append(sampledPoints_1_info);
        # get list of rxns to exclude from downstream analyses
        sampledData_all = [];
        for simulation_id in simulation_ids:
            sampledData_1 = [];
            sampledData_1 = physiology_sampledData_query.get_rxnIDs_simulationID_dataStage02PhysiologySampledData(simulation_id,used__I=False);
            sampledData_all.append(sampledData_1);
        # get simulation parameters
        simulation_parameters_all = [];
        for simulation_id in simulation_ids:
            simulation_parameters_1_all = [];
            simulation_parameters_1_all = physiology_sampledData_query.get_rows_simulationID_dataStage02PhysiologySamplingParameters(simulation_id);
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
        filename_points = [];
        #filename_points = [s + '_points' + '.mat' for s in simulation_ids_I]
        for i,s in enumerate(simulation_ids):
            if sampler_ids[i]=='gpSampler':
                filename = s + '_points' + '.mat';
            elif sampler_ids[i]=='optGpSampler':
                filename = s + '_points' + '.json';
            filename_points.append(filename);
        # perform the analysis
        sampling_n = cobra_sampling_n(data_dir_I=data_dir,
                                      model_I = cobra_model,
                                      loops_I = infeasible_loops,
                                      sample_ids_I = simulation_ids,
                                      samplers_I = sampler_ids,
                                      control_I = control_I);

        sampling_n.get_points(filename_points,
                remove_loops_I=remove_loops_I,
                remove_no_flux_I=remove_loops_I,
                normalize_I=remove_loops_I,
                remove_points_I=sampledData_all,
                );
        #pairwisetest
        sampling_n.calculate_pairWiseTest(redundancy_I=redundancy_I);
        # load data into the database
        for d in sampling_n.data:
            d['analysis_id'] = analysis_id_I;
            d['used_'] = True;
            d['flux_units'] = 'geometricFC(mean)';
            d['mean']=d['mean_difference'];
            d['simulation_id_1']=d['sample_id_1'];
            d['simulation_id_2']=d['sample_id_2'];
        self.add_rows_table('data_stage02_physiology_pairWiseTest',sampling_n.data)
        #    row = None;
        #    row = data_stage02_physiology_pairWiseTest(
        #        d['sample_id_1'],
        #        d[''],
        #        d['rxn_id'],
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
        #pairwisetest_metabolites
        if compare_metabolitePoints_I:
            sampling_n.convert_points2MetabolitePoints();
            sampling_n.calculate_pairWiseTest_metabolites(redundancy_I=redundancy_I);
            # load data into the database
            for d in sampling_n.data:
                d['analysis_id'] = analysis_id_I;
                d['used_'] = True;
                d['flux_units'] = 'geometricFC(mean_metSum)';
                d['mean']=d['mean_difference'];
                d['simulation_id_1']=d['sample_id_1'];
                d['simulation_id_2']=d['sample_id_2'];
            self.add_rows_table('data_stage02_physiology_pairWiseTestMetabolites',sampling_n.data)
        #pairwisetest_subsystems
        if compare_subsystemPoints_I:
            sampling_n.convert_points2SubsystemPoints();
            sampling_n.calculate_pairWiseTest_subsystems(redundancy_I=redundancy_I);
            # load data into the database
            for d in sampling_n.data:
                d['analysis_id'] = analysis_id_I;
                d['used_'] = True;
                d['flux_units'] = 'geometricFC(mean_subsystemSum)';
                d['mean']=d['mean_difference'];
                d['simulation_id_1']=d['sample_id_1'];
                d['simulation_id_2']=d['sample_id_2'];
            self.add_rows_table('data_stage02_physiology_pairWiseTestSubsystems',sampling_n.data)