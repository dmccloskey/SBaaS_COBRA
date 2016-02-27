import sys
sys.path.append('C:/Users/dmccloskey-sbrg/Documents/GitHub/SBaaS_base')
from SBaaS_base.postgresql_settings import postgresql_settings
from SBaaS_base.postgresql_orm import postgresql_orm
# read in the settings file
filename = 'C:/Users/dmccloskey-sbrg/Google Drive/SBaaS_settings/settings_metabolomics.ini';
pg_settings = postgresql_settings(filename);
# connect to the database from the settings file
pg_orm = postgresql_orm();
pg_orm.set_sessionFromSettings(pg_settings.database_settings);
session = pg_orm.get_session();
engine = pg_orm.get_engine();
# your app...
# SBaaS paths:
sys.path.append(pg_settings.datadir_settings['github']+'/SBaaS_base')
sys.path.append(pg_settings.datadir_settings['github']+'/SBaaS_LIMS')
sys.path.append(pg_settings.datadir_settings['github']+'/SBaaS_quantification')
sys.path.append(pg_settings.datadir_settings['github']+'/SBaaS_physiology')
sys.path.append(pg_settings.datadir_settings['github']+'/SBaaS_MFA')
sys.path.append(pg_settings.datadir_settings['github']+'/SBaaS_visualization')
sys.path.append(pg_settings.datadir_settings['github']+'/SBaaS_models')
sys.path.append(pg_settings.datadir_settings['github']+'/SBaaS_COBRA')
# SBaaS dependencies paths:
sys.path.append(pg_settings.datadir_settings['github']+'/io_utilities')
sys.path.append(pg_settings.datadir_settings['github']+'/matplotlib_utilities')
sys.path.append(pg_settings.datadir_settings['github']+'/molmass')
sys.path.append(pg_settings.datadir_settings['github']+'/python_statistics')
sys.path.append(pg_settings.datadir_settings['github']+'/r_statistics')
sys.path.append(pg_settings.datadir_settings['github']+'/listDict')
sys.path.append(pg_settings.datadir_settings['github']+'/ddt_python')

#make the simulatedData table
from SBaaS_COBRA.stage02_physiology_simulatedData_execute import stage02_physiology_simulatedData_execute
simulatedData01 = stage02_physiology_simulatedData_execute(session,engine,pg_settings.datadir_settings);
simulatedData01.initialize_supportedTables();
#simulatedData01.drop_dataStage02_physiology_simulatedData();
simulatedData01.initialize_dataStage02_physiology_simulatedData();

#make the COBRA table
from SBaaS_models.models_COBRA_execute import models_COBRA_execute
exCOBRA01 = models_COBRA_execute(session,engine,pg_settings.datadir_settings);
exCOBRA01.initialize_supportedTables();
exCOBRA01.initialize_COBRA_models();

#make the simulatedData table
from SBaaS_COBRA.stage02_physiology_sampledData_execute import stage02_physiology_sampledData_execute
sampledData01 = stage02_physiology_sampledData_execute(session,engine,pg_settings.datadir_settings);
sampledData01.initialize_supportedTables();
sampledData01.initialize_dataStage02_physiology_sampledData();

#test the model
test_result = exCOBRA01.execute_testModel(model_id_I="140407_iDM2014_irreversible");

#pre-load the models
cobramodels = exCOBRA01.get_models(model_ids_I=["140407_iDM2014_irreversible"]);

simulations = [
        'WTEColi_113C80_U13C20_02_140407_iDM2014_irreversible_OxicWtGlc_0',
        ]

#for simulation in simulations:
     ##fba
     #simulatedData01.execute_fba(simulation_id_I=simulation,
     #                    rxn_ids_I=[],
     #                    models_I = cobramodels,
     #                    method_I='pfba',
     #                    allow_loops_I = True,
     #                    options_I = {},
     #                    solver_id_I='cglpk',
     #                    )
     ##fva
     #simulatedData01.execute_fva(simulation_id_I=simulation,
     #                   rxn_ids_I=[],
     #                   models_I = cobramodels,
     #                   method_I='fva',
     #                   allow_loops_I = True,
     #                    options_I = {},
     #                   solver_id_I='cglpk',
     #                   )
     ##sra
     #simulatedData01.execute_sra(simulation_id_I=simulation,
     #                    rxn_ids_I=[],
     #                    models_I = cobramodels,
     #                    method_I='fba',
     #                    options_I = {},
     #                    solver_id_I='cglpk',
     #                    )

data_dir = 'F:/Users/dmccloskey-sbrg/Dropbox (UCSD SBRG)/MATLAB/sampling_physiology';

# import sampling results
#for simulation in simulations:
    #sampledData01.execute_sampling(simulation_id_I=simulation,
    #    rxn_ids_I=[],
    #    data_dir_I = data_dir,
    #    models_I = cobramodels
    #    )
    #sampledData01.reset_dataStage02_physiology_sampledData(simulation_id_I=simulation);
    #sampledData01.execute_analyzeSamplingPoints(simulation_id_I=simulation,
    #    rxn_ids_I=[],
    #    data_dir_I = data_dir,
    #    models_I = cobramodels,
    #    )