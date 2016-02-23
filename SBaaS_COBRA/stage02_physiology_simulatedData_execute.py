#SBaaS
from .stage02_physiology_simulatedData_io import stage02_physiology_simulatedData_io
from .stage02_physiology_simulation_query import stage02_physiology_simulation_query
#SBaaS models (delete if not needed)
from .stage02_physiology_simulatedData_postgresql_models import *
# Resources (delete if not needed)
from io_utilities.base_importData import base_importData
from io_utilities.base_exportData import base_exportData
# Dependencies from thermodynamics
from thermodynamics.thermodynamics_simulatedData import thermodynamics_simulatedData

class stage02_physiology_simulatedData_execute(stage02_physiology_simulatedData_io,
                                                   stage02_physiology_simulation_query):
    def execute_makeSimulatedData(self,experiment_id_I,models_I,model_ids_I = []):
        '''make simulated data
        INPUT:
        experiment_id_I = experiment_id
        models_I = dictionary of cobra models
        models_ids_I = list of model_ids to use
        '''

        # get the model ids:
        if model_ids_I:
            model_ids = model_ids_I;
        else:
            model_ids = [];
            model_ids = self.get_modelID_experimentID_dataStage03QuantificationSimulation(experiment_id_I);
        for model_id in model_ids:
            # get the cobra model
            cobra_model = models_I[model_id];
            # make simulated data
            simulated_data = thermodynamics_simulatedData();
            simulated_data.generate_sra_data(cobra_model,solver=None); # perform single reaction deletion analysis
            simulated_data.generate_fva_data(cobra_model,solver=None); # perform flux variability analysis
            # upload the results to the database
            data_O = [];
            for k,v in simulated_data.fva_data.items():
                data_tmp = {'experiment_id':experiment_id_I,
                'model_id':model_id,
                'rxn_id':k,
                'fba_flux':None, #reserved for parsimonious fba
                'fva_minimum':simulated_data.fva_data[k]['minimum'],
                'fva_maximum':simulated_data.fva_data[k]['maximum'],
                'flux_units':'mmol*gDCW-1*hr-1',
                'sra_gr':simulated_data.sra_data[k]['gr'],
                'sra_gr_ratio':simulated_data.sra_data[k]['gr_ratio'],
                'used_':True,
                'comment_':None};
                data_O.append(data_tmp);
                try:
                    row = None;
                    row = data_stage02_physiology_simulatedData(experiment_id_I,
                            model_id,
                            k,
                            None, #reserved for parsimonious fba
                            simulated_data.fva_data[k]['minimum'],
                            simulated_data.fva_data[k]['maximum'],
                            'mmol*gDCW-1*hr-1',
                            simulated_data.sra_data[k]['gr'],
                            simulated_data.sra_data[k]['gr_ratio'],
                            True,
                            None);
                    self.session.add(row);
                    self.session.commit();
                except sqlalchemy.exc.IntegrityError as e:
                    print(e);
                    print("Press any key to continue")
                    a=input();
                    self.update_dataStage03SimulatedData([tmp]);
    