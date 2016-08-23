#SBaaS
from .stage02_physiology_sampledData_io import stage02_physiology_sampledData_io
from .stage02_physiology_simulation_query import stage02_physiology_simulation_query
from .stage02_physiology_measuredData_query import stage02_physiology_measuredData_query
from SBaaS_models.models_COBRA_dependencies import models_COBRA_dependencies
# resources
from python_statistics.calculate_interface import calculate_interface
from .sampling import cobra_sampling,cobra_sampling_n
from .matlab_sampling import matlab_sampling
from .optGpSampler_sampling import optGpSampler_sampling
import datetime
class stage02_physiology_sampledData_execute(stage02_physiology_sampledData_io,
                                            stage02_physiology_simulation_query,
                                            stage02_physiology_measuredData_query): 
    def execute_sampling(self,simulation_id_I,
                               rxn_ids_I=[],
                               data_dir_I='C:/Users/dmccloskey-sbrg/Documents/MATLAB/sampling_physiology',
                               models_I = {},
                               ):
        '''Sample a specified model that is constrained to measured physiological data
        INPUT:
        OUTPUT:
        '''
        print('executing sampling...');
        # input
        modelsCOBRA = models_COBRA_dependencies();
        data_dir = data_dir_I;
        models = models_I;
        # get simulation information
        simulation_info_all = [];
        simulation_info_all = self.get_rows_simulationID_dataStage02PhysiologySimulation(simulation_id_I);
        if not simulation_info_all:
            print('simulation not found!')
            return;
        simulation_info = simulation_info_all[0]; # unique constraint guarantees only 1 row will be returned
        # get simulation parameters
        simulation_parameters_all = [];
        simulation_parameters_all = self.get_rows_simulationID_dataStage02PhysiologySamplingParameters(simulation_id_I);
        if not simulation_parameters_all:
            print('simulation parameters not found!')
            return;
        simulation_parameters = simulation_parameters_all[0]; # unique constraint guarantees only 1 row will be returned
        # get the cobra model
        cobra_model = models[simulation_info['model_id']];
        # copy the model
        cobra_model_copy = cobra_model.copy();
        # get rxn_ids
        if rxn_ids_I:
            rxn_ids = rxn_ids_I;
        else:
            rxn_ids = [];
            rxn_ids = self.get_rows_experimentIDAndModelIDAndSampleNameAbbreviation_dataStage02PhysiologyMeasuredFluxes(simulation_info['experiment_id'],simulation_info['model_id'],simulation_info['sample_name_abbreviation']);
        for rxn in rxn_ids:
            # constrain the model
            cobra_model_copy.reactions.get_by_id(rxn['rxn_id']).lower_bound = rxn['flux_lb'];
            cobra_model_copy.reactions.get_by_id(rxn['rxn_id']).upper_bound = rxn['flux_ub'];
        # Test model
        if modelsCOBRA.test_model(cobra_model_I=cobra_model_copy):
            if simulation_parameters['sampler_id']=='gpSampler':
                sampling = matlab_sampling(data_dir_I = data_dir);
                filename_model = simulation_id_I + '.mat';
                filename_script = simulation_id_I + '.m';
                filename_points = simulation_id_I + '_points' + '.mat';
                sampling.export_sampling_matlab(cobra_model=cobra_model_copy,
                    filename_model=filename_model,
                    filename_script=filename_script,
                    filename_points=filename_points,
                    solver_id_I = simulation_parameters['solver_id'],
                    n_points_I = simulation_parameters['n_points'],
                    n_steps_I = simulation_parameters['n_steps'],
                    max_time_I = simulation_parameters['max_time']);
            elif simulation_parameters['sampler_id']=='optGpSampler':
                sampling = optGpSampler_sampling(data_dir_I = data_dir);
                filename_model = simulation_id_I + '.json';
                filename_script = simulation_id_I + '.py';
                filename_points = simulation_id_I + '_points' + '.json';
                filename_warmup = simulation_id_I + '_warmup' + '.json';
                sampling.export_sampling_optGpSampler(cobra_model=cobra_model_copy,
                    filename_model=filename_model,
                    filename_script=filename_script,
                    filename_points=filename_points,
                    filename_warmup=filename_warmup,
                    solver_id_I = simulation_parameters['solver_id'],
                    n_points_I = simulation_parameters['n_points'],
                    n_steps_I = simulation_parameters['n_steps'],
                    n_threads_I = simulation_parameters['n_threads']);
                #sampling.generate_samples(cobra_model=cobra_model_copy,
                #    filename_points=filename_points,
                #    solver_id_I = simulation_parameters['solver_id'],
                #    n_points_I = simulation_parameters['n_points'],
                #    n_steps_I = simulation_parameters['n_steps']);
            else:
                print('sampler_id not recognized');
        else:
            print('no solution found!'); 
    def execute_analyzeSamplingPoints(self,simulation_id_I,
                               rxn_ids_I=[],
                               data_dir_I='C:/Users/dmccloskey-sbrg/Documents/MATLAB/sampling_physiology',
                               models_I = {},
                               points_overview_I=True,
                               flux_stats_I=True,
                               metabolite_stats_I=False,
                               subsystem_stats_I=False,
                               ):
        '''Load and analyze sampling points
        INPUT:
        simulation_id_I = 
        rxn_ids_I = [] of strings, list of reaction ids
        data_dir_I = string, directory of the sampled points file
        models_I = {} string:cobra_model object, model_id:cobra_model
        points_overview_I = boolean, if True, the sampled points overview will be added to the database
        flux_stats_I = boolean, if True, sampled points descriptive statistics will be calcluated
        metabolite_stats_I = boolean, if True, sampled points will be converted to metabolite flux sum values
                                               and descriptive statistics will be calculated
        subsystem_stats_I = boolean, if True, sampled points will be converted to subsystem flux sum values
                                               and descriptive statistics will be calculated
        OUTPUT:
        '''

        print('analyzing sampling points');
        
        modelsCOBRA = models_COBRA_dependencies();
        data_dir = data_dir_I;
        models = models_I;
                
        # get simulation information
        simulation_info_all = [];
        simulation_info_all = self.get_rows_simulationIDAndSimulationType_dataStage02PhysiologySimulation(simulation_id_I,'sampling');
        if not simulation_info_all:
            print('simulation not found!')
            return;
        simulation_info = simulation_info_all[0]; # unique constraint guarantees only 1 row will be returned
        # get simulation parameters
        simulation_parameters_all = [];
        simulation_parameters_all = self.get_rows_simulationID_dataStage02PhysiologySamplingParameters(simulation_id_I);
        if not simulation_parameters_all:
            print('simulation not found!')
            return;
        simulation_parameters = simulation_parameters_all[0]; # unique constraint guarantees only 1 row will be returned
        # get the cobra model
        cobra_model = models[simulation_info['model_id']];
        # copy the model
        cobra_model_copy = cobra_model.copy();
        # get rxn_ids
        if rxn_ids_I:
            rxn_ids = rxn_ids_I;
        else:
            rxn_ids = [];
            rxn_ids = self.get_rows_experimentIDAndModelIDAndSampleNameAbbreviation_dataStage02PhysiologyMeasuredFluxes(simulation_info['experiment_id'],simulation_info['model_id'],simulation_info['sample_name_abbreviation']);
        for rxn in rxn_ids:
            # constrain the model
            cobra_model_copy.reactions.get_by_id(rxn['rxn_id']).lower_bound = rxn['flux_lb'];
            cobra_model_copy.reactions.get_by_id(rxn['rxn_id']).upper_bound = rxn['flux_ub'];
        # Test each model
        if modelsCOBRA.test_model(cobra_model_I=cobra_model_copy):
            if simulation_parameters['sampler_id']=='gpSampler':
                sampling = matlab_sampling(data_dir_I = data_dir);
                # load the results of sampling
                filename_points = simulation_id_I + '_points' + '.mat';
                sampling.get_points_matlab(filename_points,'sampler_out');
            elif simulation_parameters['sampler_id']=='optGpSampler':
                sampling = optGpSampler_sampling(
                    data_dir_I = data_dir,
                    model_I=cobra_model_copy);
                filename_points = simulation_id_I + '_points' + '.json';
                filename_warmup = simulation_id_I + '_warmup' + '.json';
                sampling.get_points_json(filename_points);
                sampling.get_warmup_json(filename_warmup);
                sampling.calculate_mixFraction();
            else:
                print('sampler_id not recognized');
                return;
            # check if the model contains loops
            #loops_bool = self.sampling.check_loops();
            sampling.simulate_loops(
                data_fva=self.settings['workspace_data'] + '/loops_fva_tmp.json',
                solver_I = simulation_parameters['solver_id']);
            sampling.find_loops(data_fva=self.settings['workspace_data'] + '/loops_fva_tmp.json');
            sampling.remove_loopsFromPoints();
            # add points overview to the database
            if points_overview_I:
                row = {'simulation_id':simulation_id_I,
                    'simulation_dateAndTime':sampling.simulation_dateAndTime,
                    'mixed_fraction':sampling.mixed_fraction,
                    'data_dir':data_dir_I+'/'+filename_points,
                    'infeasible_loops':sampling.loops,
                    'used_':True,
                    'comment_':None
                    };
                self.add_dataStage02PhysiologySampledPoints([row])
            # calculate the flux descriptive statistics
            if flux_stats_I:
                sampling.descriptive_statistics(points_I='flux');
                # add data to the database
                sampledData_O = [];
                for k,v in sampling.points_statistics.items():
                    row = {'simulation_id':simulation_id_I,
                        'simulation_dateAndTime':sampling.simulation_dateAndTime,
                        'rxn_id':k,
                        'flux_units':'mmol*gDW-1*hr-1',
                        'sampling_points':None, #v['points'],
                        'sampling_n':v['n'],
                        'sampling_ave':v['ave'],
                        'sampling_var':v['var'],
                        'sampling_lb':v['lb'],
                        'sampling_ub':v['ub'],
                        'sampling_ci':0.95,
                        'sampling_min':v['min'],
                        'sampling_max':v['max'],
                        'sampling_median':v['median'],
                        'sampling_iq_1':v['iq_1'],
                        'sampling_iq_3':v['iq_3'],
                        'used_':True,
                        'comment_':None};
                    sampledData_O.append(row);
                self.add_rows_table('data_stage02_physiology_sampledData',sampledData_O);
            # calculate descriptive stats for metabolites
            if metabolite_stats_I:
                sampling.convert_points2MetabolitePoints();
                sampling.descriptive_statistics(points_I='metabolite');
                # add data to the database
                sampledData_O = [];
                for k,v in sampling.points_statistics.items():
                    row = {'simulation_id':simulation_id_I,
                        'simulation_dateAndTime':sampling.simulation_dateAndTime,
                        'met_id':k,
                        'flux_units':'mmol*gDW-1*hr-1',
                        'sampling_points':None, #v['points'],
                        'sampling_n':v['n'],
                        'sampling_ave':v['ave'],
                        'sampling_var':v['var'],
                        'sampling_lb':v['lb'],
                        'sampling_ub':v['ub'],
                        'sampling_ci':0.95,
                        'sampling_min':v['min'],
                        'sampling_max':v['max'],
                        'sampling_median':v['median'],
                        'sampling_iq_1':v['iq_1'],
                        'sampling_iq_3':v['iq_3'],
                        'used_':True,
                        'comment_':None};
                    sampledData_O.append(row);
                self.add_rows_table('data_stage02_physiology_sampledMetaboliteData',sampledData_O);
            # calculate descriptive stats for subsystems
            if subsystem_stats_I:
                sampling.convert_points2SubsystemPoints();
                sampling.descriptive_statistics(points_I='subsystem');
                # add data to the database
                sampledData_O = [];
                for k,v in sampling.points_statistics.items():
                    row = {'simulation_id':simulation_id_I,
                        'simulation_dateAndTime':sampling.simulation_dateAndTime,
                        'subsystem_id':k,
                        'flux_units':'mmol*gDW-1*hr-1',
                        'sampling_points':None, #v['points'],
                        'sampling_n':v['n'],
                        'sampling_ave':v['ave'],
                        'sampling_var':v['var'],
                        'sampling_lb':v['lb'],
                        'sampling_ub':v['ub'],
                        'sampling_ci':0.95,
                        'sampling_min':v['min'],
                        'sampling_max':v['max'],
                        'sampling_median':v['median'],
                        'sampling_iq_1':v['iq_1'],
                        'sampling_iq_3':v['iq_3'],
                        'used_':True,
                        'comment_':None};
                    sampledData_O.append(row);
                self.add_rows_table('data_stage02_physiology_sampledSubsystemData',sampledData_O);
        else:
            print('no solution found!');
    def execute_analyzeSamplingMetabolitesAndSubsystemPoints(self,simulation_id_I,
                               rxn_ids_I=[],
                               data_dir_I='C:/Users/dmccloskey-sbrg/Documents/MATLAB/sampling_physiology',
                               models_I = {},
                               metabolite_stats_I=False,
                               subsystem_stats_I=False,
                               ):
        '''Load and analyze sampling points
        INPUT:
        simulation_id_I = 
        rxn_ids_I = [] of strings, list of reaction ids
        data_dir_I = string, directory of the sampled points file
        models_I = {} string:cobra_model object, model_id:cobra_model
        metabolite_stats_I = boolean, if True, sampled points will be converted to metabolite flux sum values
                                               and descriptive statistics will be calculated
        subsystem_stats_I = boolean, if True, sampled points will be converted to subsystem flux sum values
                                               and descriptive statistics will be calculated
        OUTPUT:
        '''

        print('analyzing sampling points');
        
        modelsCOBRA = models_COBRA_dependencies();
        data_dir = data_dir_I;
        models = models_I;
                
        # get simulation information
        simulation_info_all = [];
        simulation_info_all = self.get_rows_simulationIDAndSimulationType_dataStage02PhysiologySimulation(simulation_id_I,'sampling');
        if not simulation_info_all:
            print('simulation not found!')
            return;
        simulation_info = simulation_info_all[0]; # unique constraint guarantees only 1 row will be returned
        # get simulation parameters
        simulation_parameters_all = [];
        simulation_parameters_all = self.get_rows_simulationID_dataStage02PhysiologySamplingParameters(simulation_id_I);
        if not simulation_parameters_all:
            print('simulation not found!')
            return;
        simulation_parameters = simulation_parameters_all[0]; # unique constraint guarantees only 1 row will be returned
        # get the cobra model
        cobra_model = models[simulation_info['model_id']];
        # copy the model
        cobra_model_copy = cobra_model.copy();
        # get rxn_ids
        if rxn_ids_I:
            rxn_ids = rxn_ids_I;
        else:
            rxn_ids = [];
            rxn_ids = self.get_rows_experimentIDAndModelIDAndSampleNameAbbreviation_dataStage02PhysiologyMeasuredFluxes(simulation_info['experiment_id'],simulation_info['model_id'],simulation_info['sample_name_abbreviation']);
        for rxn in rxn_ids:
            # constrain the model
            cobra_model_copy.reactions.get_by_id(rxn['rxn_id']).lower_bound = rxn['flux_lb'];
            cobra_model_copy.reactions.get_by_id(rxn['rxn_id']).upper_bound = rxn['flux_ub'];
        # Test each model
        if modelsCOBRA.test_model(cobra_model_I=cobra_model_copy):
            if simulation_parameters['sampler_id']=='gpSampler':
                sampling = matlab_sampling(data_dir_I = data_dir);
                # load the results of sampling
                filename_points = simulation_id_I + '_points' + '.mat';
                sampling.get_points_matlab(filename_points,'sampler_out');
            elif simulation_parameters['sampler_id']=='optGpSampler':
                sampling = optGpSampler_sampling(
                    data_dir_I = data_dir,
                    model_I=cobra_model_copy);
                filename_points = simulation_id_I + '_points' + '.json';
                filename_warmup = simulation_id_I + '_warmup' + '.json';
                sampling.get_points_json(filename_points);
                sampling.get_warmup_json(filename_warmup);
                sampling.calculate_mixFraction();
            else:
                print('sampler_id not recognized');
                return;
            # check if the model contains loops
            #loops_bool = self.sampling.check_loops();
            sampling.simulate_loops(
                data_fva=self.settings['workspace_data'] + '/loops_fva_tmp.json',
                solver_I = simulation_parameters['solver_id']);
            sampling.find_loops(data_fva=self.settings['workspace_data'] + '/loops_fva_tmp.json');
            sampling.remove_loopsFromPoints();
            # check for QCd points that will be removed in down-stream analyses:
            rxn_ids = self.get_rxnIDs_simulationID_dataStage02PhysiologySampledData(simulation_id_I,used__I=False);
            sampling.remove_points(rxn_ids);
            # calculate descriptive stats for metabolites
            if metabolite_stats_I:
                sampling.convert_points2MetabolitePoints();
                sampling.descriptive_statistics(points_I='metabolite');
                # add data to the database
                sampledData_O = [];
                for k,v in sampling.points_statistics.items():
                    row = {'simulation_id':simulation_id_I,
                        'simulation_dateAndTime':sampling.simulation_dateAndTime,
                        'met_id':k,
                        'flux_units':'mmol*gDW-1*hr-1',
                        'sampling_points':None, #v['points'],
                        'sampling_n':v['n'],
                        'sampling_ave':v['ave'],
                        'sampling_var':v['var'],
                        'sampling_lb':v['lb'],
                        'sampling_ub':v['ub'],
                        'sampling_ci':0.95,
                        'sampling_min':v['min'],
                        'sampling_max':v['max'],
                        'sampling_median':v['median'],
                        'sampling_iq_1':v['iq_1'],
                        'sampling_iq_3':v['iq_3'],
                        'used_':True,
                        'comment_':None};
                    sampledData_O.append(row);
                self.add_rows_table('data_stage02_physiology_sampledMetaboliteData',sampledData_O);
            # calculate descriptive stats for subsystems
            if subsystem_stats_I:
                sampling.convert_points2SubsystemPoints();
                sampling.descriptive_statistics(points_I='subsystem');
                # add data to the database
                sampledData_O = [];
                for k,v in sampling.points_statistics.items():
                    row = {'simulation_id':simulation_id_I,
                        'simulation_dateAndTime':sampling.simulation_dateAndTime,
                        'subsystem_id':k,
                        'flux_units':'mmol*gDW-1*hr-1',
                        'sampling_points':None, #v['points'],
                        'sampling_n':v['n'],
                        'sampling_ave':v['ave'],
                        'sampling_var':v['var'],
                        'sampling_lb':v['lb'],
                        'sampling_ub':v['ub'],
                        'sampling_ci':0.95,
                        'sampling_min':v['min'],
                        'sampling_max':v['max'],
                        'sampling_median':v['median'],
                        'sampling_iq_1':v['iq_1'],
                        'sampling_iq_3':v['iq_3'],
                        'used_':True,
                        'comment_':None};
                    sampledData_O.append(row);
                self.add_rows_table('data_stage02_physiology_sampledSubsystemData',sampledData_O);
        else:
            print('no solution found!');
    