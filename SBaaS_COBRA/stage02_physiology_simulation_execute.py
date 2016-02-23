
from .stage02_physiology_simulation_io import stage02_physiology_simulation_io
# resources
from python_statistics.calculate_interface import calculate_interface
from .sampling import cobra_sampling,cobra_sampling_n
# Dependencies from cobra
from cobra.io.sbml import create_cobra_model_from_sbml_file, write_cobra_model_to_sbml_file
from cobra.flux_analysis.variability import flux_variability_analysis
from cobra.flux_analysis.parsimonious import optimize_minimal_flux
from cobra.flux_analysis import flux_variability_analysis
from cobra.manipulation.modify import convert_to_irreversible

class stage02_physiology_simulation_execute(stage02_physiology_simulation_io,):
    def execute_fva(self,):
        '''
        INPUT:
        OUTPUT:
        '''
        pass;
    def execute_fba(self,):
        '''
        INPUT:
        OUTPUT:
        '''
        pass;
    def execute_srd(self,):
        '''
        INPUT:
        OUTPUT:
        '''
        pass;
    def execute_pfba(self,):
        '''
        INPUT:
        OUTPUT:
        '''
        pass;
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
        data_dir = data_dir_I;
        models = models_I;
        # get simulation information
        simulation_info_all = [];
        simulation_info_all = self.stage02_physiology_query.get_rows_simulationID_dataStage02PhysiologySimulation(simulation_id_I);
        if not simulation_info_all:
            print('simulation not found!')
            return;
        simulation_info = simulation_info_all[0]; # unique constraint guarantees only 1 row will be returned
        # get simulation parameters
        simulation_parameters_all = [];
        simulation_parameters_all = self.stage02_physiology_query.get_rows_simulationID_dataStage02PhysiologySimulationParameters(simulation_id_I);
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
            rxn_ids = self.stage02_physiology_query.get_rows_experimentIDAndModelIDAndSampleNameAbbreviation_dataStage02PhysiologyMeasuredFluxes(simulation_info['experiment_id'],simulation_info['model_id'],simulation_info['sample_name_abbreviation']);
        for rxn in rxn_ids:
            # constrain the model
            cobra_model_copy.reactions.get_by_id(rxn['rxn_id']).lower_bound = rxn['flux_lb'];
            cobra_model_copy.reactions.get_by_id(rxn['rxn_id']).upper_bound = rxn['flux_ub'];
        # Test model
        if self.test_model(cobra_model_I=cobra_model_copy):
            sampling = cobra_sampling(data_dir_I = data_dir);
            if simulation_parameters['sampler_id']=='gpSampler':
                filename_model = simulation_id_I + '.mat';
                filename_script = simulation_id_I + '.m';
                filename_points = simulation_id_I + '_points' + '.mat';
                sampling.export_sampling_matlab(cobra_model=cobra_model_copy,filename_model=filename_model,filename_script=filename_script,filename_points=filename_points,\
                    solver_id_I = simulation_parameters['solver_id'],\
                    n_points_I = simulation_parameters['n_points'],\
                    n_steps_I = simulation_parameters['n_steps'],\
                    max_time_I = simulation_parameters['max_time']);
            elif simulation_parameters['sampler_id']=='optGpSampler':
                return;
            else:
                print('sampler_id not recognized');
        else:
            print('no solution found!');  
    def execute_analyzeSamplingPoints(self,simulation_id_I,
                               rxn_ids_I=[]):
        '''Load and analyze sampling points'''

        print('analyzing sampling points');
        
        # get simulation information
        simulation_info_all = [];
        simulation_info_all = self.stage02_physiology_query.get_rows_simulationID_dataStage02PhysiologySimulation(simulation_id_I);
        if not simulation_info_all:
            print('simulation not found!')
            return;
        simulation_info = simulation_info_all[0]; # unique constraint guarantees only 1 row will be returned
        # get simulation parameters
        simulation_parameters_all = [];
        simulation_parameters_all = self.stage02_physiology_query.get_rows_simulationID_dataStage02PhysiologySimulationParameters(simulation_id_I);
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
            rxn_ids = self.stage02_physiology_query.get_rows_experimentIDAndModelIDAndSampleNameAbbreviation_dataStage02PhysiologyMeasuredFluxes(simulation_info['experiment_id'],simulation_info['model_id'],simulation_info['sample_name_abbreviation']);
        for rxn in rxn_ids:
            # constrain the model
            cobra_model_copy.reactions.get_by_id(rxn['rxn_id']).lower_bound = rxn['flux_lb'];
            cobra_model_copy.reactions.get_by_id(rxn['rxn_id']).upper_bound = rxn['flux_ub'];
        # Test each model
        if self.test_model(cobra_model_I=cobra_model_copy):
            sampling = cobra_sampling(data_dir_I = data_dir);
            if simulation_parameters['sampler_id']=='gpSampler':
                # load the results of sampling
                filename_points = simulation_id_I + '_points' + '.mat';
                sampling.get_points_matlab(filename_points,'sampler_out');
                # check if the model contains loops
                #loops_bool = self.sampling.check_loops();
                sampling.simulate_loops(data_fva=settings.workspace_data + '/loops_fva_tmp.json');
                sampling.find_loops(data_fva=settings.workspace_data + '/loops_fva_tmp.json');
                sampling.remove_loopsFromPoints();
                sampling.descriptive_statistics();
            elif simulation_parameters['sampler_id']=='optGpSampler':
                return;
            else:
                print('sampler_id not recognized');
            # add data to the database
            row = None;
            row = data_stage02_physiology_sampledPoints(
                simulation_id_I,
                sampling.simulation_dateAndTime,
                sampling.mixed_fraction,
                sampling.matlab_path+'/'+filename_points,
                sampling.loops,
                True,
                None);
            self.session.add(row);
            for k,v in self.sampling.points_statistics.items():
                row = None;
                row = data_stage02_physiology_sampledData(
                    simulation_id_I,
                    sampling.simulation_dateAndTime,
                    k,
                    'mmol*gDW-1*hr-1',
                    None, #v['points'],
                    v['ave'],
                    v['var'],
                    v['lb'],
                    v['ub'],
                    v['min'],
                    v['max'],
                    v['median'],
                    v['iq_1'],
                    v['iq_3'],
                    True,
                    None);
                self.session.add(row);
        else:
            print('no solution found!');
        self.session.commit()  