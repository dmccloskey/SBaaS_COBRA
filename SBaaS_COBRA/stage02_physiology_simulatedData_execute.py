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
                        ):
        '''
        Run FVA on the simulation
        INPUT:
        simulation_id = string
        rxn_ids_I = [{}], specifying specifc rxn ub and lb
                    e.g., [{'rxn_id':string, 'rxn_lb':float, 'rxn_ub':float},...]
        models_I = {} of model_id:cobra_model
        OUTPUT:
        '''
        print('executing fva...');
        # input:
        modelsCOBRA = models_COBRA_dependencies();
        models = models_I;
        # get simulation information
        simulation_info_all = [];
        simulation_info_all = self.get_rows_simulationIDAndSimulationType_dataStage02PhysiologySimulation(simulation_id_I,'fva');
        if not simulation_info_all:
            print('simulation not found!')
            return;
        simulation_info = simulation_info_all[0]; # unique constraint guarantees only 1 row will be returned
        # get simulation parameters
        simulation_parameters_all = [];
        simulation_parameters_all = self.get_rows_simulationID_dataStage02PhysiologySimulationParameters(simulation_id_I);
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
        # Test model
        if modelsCOBRA.test_model(cobra_model_I=cobra_model_copy):
            simulated_data = cobra_simulatedData();
            simulated_data.generate_fva_data(cobra_model,solver=simulation_parameters['solver_id']); # perform flux variability analysis
            #add data to the DB
            data_O = [];
            for k,v in simulated_data.fva_data.items():
                data_tmp = {
                'simulation_id':simulation_id_I,
                'simulation_dateAndTime':datetime.datetime.now(),
                'rxn_id':k,
                'fva_minimum':simulated_data.fva_data[k]['minimum'],
                'fva_maximum':simulated_data.fva_data[k]['maximum'],
                'flux_units':'mmol*gDCW-1*hr-1',
                'used_':True,
                'comment_':None};
                data_O.append(data_tmp);
            self.add_dataStage02PhysiologySimulatedData('data_stage02_physiology_simulatedData_fva',data_O);
        else:
            print('no solution found!');  
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
    