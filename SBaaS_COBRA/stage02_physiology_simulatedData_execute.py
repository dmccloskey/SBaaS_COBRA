#SBaaS
from .stage02_physiology_simulatedData_io import stage02_physiology_simulatedData_io
from .stage02_physiology_simulation_query import stage02_physiology_simulation_query
from .stage02_physiology_measuredData_query import stage02_physiology_measuredData_query
from SBaaS_models.models_COBRA_dependencies import models_COBRA_dependencies
# Resources
from .cobra_simulatedData import cobra_simulatedData
import datetime

class stage02_physiology_simulatedData_execute(stage02_physiology_simulatedData_io,
                                                   stage02_physiology_simulation_query,
                                                   stage02_physiology_measuredData_query):
    def execute_fva(self,simulation_id_I,
                        rxn_ids_I=[],
                        models_I = {},
                        method_I = 'fva',
                        options_I = {},
                        allow_loops_I=True,
                        solver_id_I = 'cglpk'
                        ):
        '''
        Run FVA on the simulation
        INPUT:
        simulation_id = string
        rxn_ids_I = [{}], specifying specifc rxn ub and lb
                    e.g., [{'rxn_id':string, 'rxn_lb':float, 'rxn_ub':float},...]
        models_I = {} of model_id:cobra_model
        method_I = string, method to use for optimization
        options_I = {}, optional optimization parameters
        allow_loops_I = boolean, False: loop-law will be applied prior to calculation
                                 default: True
        solver_id_I = string, solver to use for optimization
        OUTPUT:
        '''
        print('executing fva...');
        # input:
        modelsCOBRA = models_COBRA_dependencies();
        models = models_I;
        # get simulation information
        simulation_info_all = [];
        simulation_info_all = self.get_rows_simulationID_dataStage02PhysiologySimulation(simulation_id_I);
        if not simulation_info_all:
            print('simulation not found!')
            return;
        simulation_info = simulation_info_all[0]; # unique constraint guarantees only 1 row will be returned
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
            simulated_data = cobra_simulatedData();
            simulated_data.generate_fva_data(
                cobra_model,
                solver=solver_id_I,
                allow_loops=allow_loops_I); # perform flux variability analysis
            #add data to the DB
            data_O = [];
            for k,v in simulated_data.fva_data.items():
                data_tmp = {
                'simulation_id':simulation_id_I,
                'simulation_dateAndTime':datetime.datetime.now(),
                'rxn_id':k,
                'fva_minimum':simulated_data.fva_data[k]['minimum'],
                'fva_maximum':simulated_data.fva_data[k]['maximum'],
                'fva_method':method_I,
                'allow_loops':allow_loops_I,
                'fva_options':options_I,
                'solver_id':solver_id_I,
                'flux_units':'mmol*gDCW-1*hr-1',
                'used_':True,
                'comment_':None};
                data_O.append(data_tmp);
            self.add_dataStage02PhysiologySimulatedData('data_stage02_physiology_simulatedData_fva',data_O);
        else:
            print('no solution found!');  
    def execute_fba(self,simulation_id_I,
                        rxn_ids_I=[],
                        models_I = {},
                        method_I='fba',
                        options_I = {},
                        allow_loops_I=True,
                        solver_id_I = 'cglpk'):
        '''
        INPUT:
        simulation_id = string
        rxn_ids_I = [{}], specifying specifc rxn ub and lb
                    e.g., [{'rxn_id':string, 'rxn_lb':float, 'rxn_ub':float},...]
        models_I = {} of model_id:cobra_model
        method_I = string, method to use for optimization
        options_I = {}, optional optimization parameters
        allow_loops_I = boolean, False: loop-law will be applied prior to calculation
                                 default: True
        solver_id_I = string, solver to use for optimization
        OUTPUT:
        '''
        print('executing fba...');
        # input:
        modelsCOBRA = models_COBRA_dependencies();
        models = models_I;
        # get simulation information
        simulation_info_all = [];
        simulation_info_all = self.get_rows_simulationID_dataStage02PhysiologySimulation(simulation_id_I);
        if not simulation_info_all:
            print('simulation not found!')
            return;
        simulation_info = simulation_info_all[0]; # unique constraint guarantees only 1 row will be returned
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
            simulated_data = cobra_simulatedData();
            simulated_data.generate_fba_data(
                cobra_model,
                solver=solver_id_I,
                allow_loops=allow_loops_I,
                method_I=method_I
                ); # perform flux variability analysis
            #add data to the DB
            data_O = [];
            for k,v in simulated_data.fba_primal_data.items():
                data_tmp = {
                'simulation_id':simulation_id_I,
                'simulation_dateAndTime':datetime.datetime.now(),
                'rxn_id':k,
                'fba_flux':v,
                'fba_method':method_I,
                'allow_loops':allow_loops_I,
                'fba_options':options_I,
                'solver_id':solver_id_I,
                'flux_units':'mmol*gDCW-1*hr-1',
                'used_':True,
                'comment_':None};
                data_O.append(data_tmp);
            self.add_dataStage02PhysiologySimulatedData('data_stage02_physiology_simulatedData_fbaPrimal',data_O);
            data_O = [];
            for k,v in simulated_data.fba_dual_data.items():
                data_tmp = {
                'simulation_id':simulation_id_I,
                'simulation_dateAndTime':datetime.datetime.now(),
                'met_id':k,
                'fba_shadowPrice':v,
                'fba_method':method_I,
                'allow_loops':allow_loops_I,
                'fba_options':options_I,
                'solver_id':solver_id_I,
                'flux_units':'mmol*gDCW-1*hr-1',
                'used_':True,
                'comment_':None};
                data_O.append(data_tmp);
            self.add_dataStage02PhysiologySimulatedData('data_stage02_physiology_simulatedData_fbaDual',data_O);
        else:
            print('no solution found!'); 
    def execute_sra(self,simulation_id_I,
                        rxn_ids_I=[],
                        models_I = {},
                        method_I='moma',
                        options_I = {},
                        solver_id_I = 'cglpk'):
        '''Single reaction deletion analysis
        INPUT:
        simulation_id = string
        rxn_ids_I = [{}], specifying specifc rxn ub and lb
                    e.g., [{'rxn_id':string, 'rxn_lb':float, 'rxn_ub':float},...]
        models_I = {} of model_id:cobra_model
        method_I = string, method to use for optimization (fba or moma)
        allow_loops_I = boolean, False: loop-law will be applied prior to calculation
                                 default: True
        solver_id_I = string, solver to use for optimization
        OUTPUT:
        '''
        print('executing sra...');
        # input:
        modelsCOBRA = models_COBRA_dependencies();
        models = models_I;
        # get simulation information
        simulation_info_all = [];
        simulation_info_all = self.get_rows_simulationID_dataStage02PhysiologySimulation(simulation_id_I);
        if not simulation_info_all:
            print('simulation not found!')
            return;
        simulation_info = simulation_info_all[0]; # unique constraint guarantees only 1 row will be returned
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
            simulated_data = cobra_simulatedData();
            simulated_data.generate_sra_data(
                cobra_model,
                solver=solver_id_I,
                method_I=method_I); # perform flux variability analysis
            #add data to the DB
            data_O = [];
            for k,v in simulated_data.sra_data.items():
                data_tmp = {
                'simulation_id':simulation_id_I,
                'simulation_dateAndTime':datetime.datetime.now(),
                'rxn_id':k,
                'sra_gr':v['gr'],
                'sra_gr_ratio':v['gr_ratio'],
                'sra_method':method_I,
                'sra_options':options_I,
                'solver_id':solver_id_I,
                'gr_units':'hr-1',
                'used_':True,
                'comment_':None};
                data_O.append(data_tmp);
            self.add_dataStage02PhysiologySimulatedData('data_stage02_physiology_simulatedData_sra',data_O);
        else:
            print('no solution found!'); 
    