import sys
sys.path.append('C:/Users/dmccloskey-sbrg/Documents/GitHub/SBaaS_base')
#sys.path.append('C:/Users/dmccloskey/Documents/GitHub/SBaaS_base')
from SBaaS_base.postgresql_settings import postgresql_settings
from SBaaS_base.postgresql_orm import postgresql_orm
# read in the settings file
filename = 'C:/Users/dmccloskey-sbrg/Google Drive/SBaaS_settings/settings_metabolomics.ini';
#filename = 'C:/Users/dmccloskey/Google Drive/SBaaS_settings/settings_metabolomics_labtop.ini';
#filename = 'C:/Users/dmccloskey/Google Drive/SBaaS_settings/settings_metabolomics_remote.ini';
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
sys.path.append(pg_settings.datadir_settings['github']+'/sampling')

sys.path.append(pg_settings.datadir_settings['github']+'/SBaaS_resequencing')
sys.path.append(pg_settings.datadir_settings['github']+'/sequencing_analysis')
sys.path.append(pg_settings.datadir_settings['github']+'/sequencing_utilities')

#make the COBRA table
from SBaaS_COBRA.stage02_physiology_graphData_execute import stage02_physiology_graphData_execute
graphData01 = stage02_physiology_graphData_execute(session,engine,pg_settings.datadir_settings);
graphData01.initialize_supportedTables()
graphData01.initialize_tables()


##graphData01.export_dataStage02PhysiologyGraphDataShortestPathStats_js('ALEsKOs01_151026_iDM2015_full05_OxicEvo04gndEvo01EPEcoliGlc_11')
#graphData01.export_dataStage02PhysiologyGraphDataShortestPaths_js('ALEsKOs01_151026_iDM2015_full05_OxicEvo04gndEvo01EPEcoliGlc_11')

##ADD TO NOTEBOOK
#from SBaaS_base.sbaas_template_py import sbaas_template_py
#template_py = sbaas_template_py();
#script_py = template_py.make_postgresql_modelClasses_py(
#    table_name = 'data_stage02_physiology_measuredCoverage',
#    columns = [
#        'experiment_id',
#        'sample_name_abbreviation',
#                'model_id',
#                'model_component',
#                'data_component',
#                'n_model_components',
#                'n_mapped_components',
#                'n_measured_components',
#                'fraction_mapped',
#        ],
#    )
#print(script_py)

#make the measuredData table
from SBaaS_COBRA.stage02_physiology_measuredData_execute import stage02_physiology_measuredData_execute
exmeasuredData01 = stage02_physiology_measuredData_execute(session,engine,pg_settings.datadir_settings)
exmeasuredData01.initialize_supportedTables(); 
exmeasuredData01.initialize_tables();

#platelet_sna_str = 'PLT_140_Broth-1,PLT_140_Broth-2,PLT_140_Broth-3,PLT_140_Broth-4,PLT_140_Broth-5,PLT_140_Broth-6,PLT_141_Broth-1,PLT_141_Broth-2,PLT_141_Broth-3,PLT_141_Broth-4,PLT_141_Broth-5,PLT_141_Broth-6,PLT_142_Broth-1,PLT_142_Broth-2,PLT_142_Broth-3,PLT_142_Broth-4,PLT_142_Broth-5,PLT_142_Broth-6,PLT_143_Broth-1,PLT_143_Broth-2,PLT_143_Broth-3,PLT_143_Broth-4,PLT_143_Broth-5,PLT_143_Broth-6,PLT_150_Broth-1,PLT_150_Broth-2,PLT_150_Broth-3,PLT_150_Broth-4,PLT_150_Broth-5,PLT_150_Broth-6,PLT_151_Broth-1,PLT_151_Broth-2,PLT_151_Broth-3,PLT_151_Broth-4,PLT_151_Broth-5,PLT_151_Broth-6,PLT_152_Broth-1,PLT_152_Broth-2,PLT_152_Broth-3,PLT_152_Broth-4,PLT_152_Broth-5,PLT_152_Broth-6,PLT_153_Broth-1,PLT_153_Broth-2,PLT_153_Broth-3,PLT_153_Broth-4,PLT_153_Broth-5,PLT_153_Broth-6,PLT_154_Broth-1,PLT_154_Broth-2,PLT_154_Broth-3,PLT_154_Broth-4,PLT_154_Broth-5,PLT_154_Broth-6,PLT_155_Broth-1,PLT_155_Broth-2,PLT_155_Broth-3,PLT_155_Broth-4,PLT_155_Broth-5,PLT_155_Broth-6,PLT_30_Broth-1,PLT_30_Broth-2,PLT_30_Broth-3,PLT_30_Broth-4,PLT_30_Broth-5,PLT_30_Broth-6,PLT_31_Broth-1,PLT_31_Broth-2,PLT_31_Broth-3,PLT_31_Broth-4,PLT_31_Broth-5,PLT_31_Broth-6,PLT_32_Broth-1,PLT_32_Broth-2,PLT_32_Broth-3,PLT_32_Broth-4,PLT_32_Broth-5,PLT_32_Broth-6,PLT_33_Broth-1,PLT_33_Broth-2,PLT_33_Broth-3,PLT_33_Broth-4,PLT_33_Broth-5,PLT_33_Broth-6,PLT_34_Broth-1,PLT_34_Broth-2,PLT_34_Broth-3,PLT_34_Broth-4,PLT_34_Broth-5,PLT_34_Broth-6,PLT_35_Broth-1,PLT_35_Broth-2,PLT_35_Broth-3,PLT_35_Broth-4,PLT_35_Broth-5,PLT_35_Broth-6,PLT_36_Broth-1,PLT_36_Broth-2,PLT_36_Broth-3,PLT_36_Broth-4,PLT_36_Broth-5,PLT_36_Broth-6,PLT_37_Broth-1,PLT_37_Broth-2,PLT_37_Broth-3,PLT_37_Broth-4,PLT_37_Broth-5,PLT_37_Broth-6,PLT_38_Broth-1,PLT_38_Broth-2,PLT_38_Broth-3,PLT_38_Broth-4,PLT_38_Broth-5,PLT_38_Broth-6,PLT_39_Broth-1,PLT_39_Broth-2,PLT_39_Broth-3,PLT_39_Broth-4,PLT_39_Broth-5,PLT_39_Broth-6,PLT_40_Broth-1,PLT_40_Broth-2,PLT_40_Broth-3,PLT_40_Broth-4,PLT_40_Broth-5,PLT_40_Broth-6,PLT_42_Broth-1,PLT_42_Broth-2,PLT_42_Broth-3,PLT_42_Broth-4,PLT_42_Broth-5,PLT_42_Broth-6,S01_D01_PLT_25C_0hr_Broth-1,S01_D01_PLT_25C_0hr_Broth-2,S01_D01_PLT_25C_0hr_Broth-3,S01_D01_PLT_25C_0hr_Broth-4,S01_D01_PLT_25C_0hr_Broth-5,S01_D01_PLT_25C_0hr_Broth-6,S01_D01_PLT_25C_22hr_Broth-1,S01_D01_PLT_25C_22hr_Broth-2,S01_D01_PLT_25C_22hr_Broth-3,S01_D01_PLT_25C_22hr_Broth-4,S01_D01_PLT_25C_22hr_Broth-5,S01_D01_PLT_25C_22hr_Broth-6,S01_D01_PLT_25C_2hr_Broth-1,S01_D01_PLT_25C_2hr_Broth-2,S01_D01_PLT_25C_2hr_Broth-3,S01_D01_PLT_25C_2hr_Broth-4,S01_D01_PLT_25C_2hr_Broth-5,S01_D01_PLT_25C_2hr_Broth-6,S01_D01_PLT_25C_6.5hr_Broth-1,S01_D01_PLT_25C_6.5hr_Broth-2,S01_D01_PLT_25C_6.5hr_Broth-3,S01_D01_PLT_25C_6.5hr_Broth-4,S01_D01_PLT_25C_6.5hr_Broth-5,S01_D01_PLT_25C_6.5hr_Broth-6,S01_D01_PLT_37C_22hr_Broth-1,S01_D01_PLT_37C_22hr_Broth-2,S01_D01_PLT_37C_22hr_Broth-3,S01_D01_PLT_37C_22hr_Broth-4,S01_D01_PLT_37C_22hr_Broth-5,S01_D01_PLT_37C_22hr_Broth-6,S01_D02_PLT_25C_0hr_Broth-1,S01_D02_PLT_25C_0hr_Broth-2,S01_D02_PLT_25C_0hr_Broth-3,S01_D02_PLT_25C_0hr_Broth-4,S01_D02_PLT_25C_0hr_Broth-5,S01_D02_PLT_25C_0hr_Broth-6,S01_D02_PLT_25C_22hr_Broth-1,S01_D02_PLT_25C_22hr_Broth-2,S01_D02_PLT_25C_22hr_Broth-3,S01_D02_PLT_25C_22hr_Broth-4,S01_D02_PLT_25C_22hr_Broth-5,S01_D02_PLT_25C_22hr_Broth-6,S01_D02_PLT_25C_2hr_Broth-1,S01_D02_PLT_25C_2hr_Broth-2,S01_D02_PLT_25C_2hr_Broth-3,S01_D02_PLT_25C_2hr_Broth-4,S01_D02_PLT_25C_2hr_Broth-5,S01_D02_PLT_25C_2hr_Broth-6,S01_D02_PLT_25C_6.5hr_Broth-1,S01_D02_PLT_25C_6.5hr_Broth-2,S01_D02_PLT_25C_6.5hr_Broth-3,S01_D02_PLT_25C_6.5hr_Broth-4,S01_D02_PLT_25C_6.5hr_Broth-5,S01_D02_PLT_25C_6.5hr_Broth-6,S01_D02_PLT_37C_22hr_Broth-1,S01_D02_PLT_37C_22hr_Broth-2,S01_D02_PLT_37C_22hr_Broth-3,S01_D02_PLT_37C_22hr_Broth-4,S01_D02_PLT_37C_22hr_Broth-5,S01_D02_PLT_37C_22hr_Broth-6,S01_D03_PLT_25C_0hr_Broth-1,S01_D03_PLT_25C_0hr_Broth-2,S01_D03_PLT_25C_0hr_Broth-3,S01_D03_PLT_25C_0hr_Broth-4,S01_D03_PLT_25C_0hr_Broth-5,S01_D03_PLT_25C_0hr_Broth-6,S01_D03_PLT_25C_22hr_Broth-1,S01_D03_PLT_25C_22hr_Broth-2,S01_D03_PLT_25C_22hr_Broth-3,S01_D03_PLT_25C_22hr_Broth-4,S01_D03_PLT_25C_22hr_Broth-5,S01_D03_PLT_25C_22hr_Broth-6,S01_D03_PLT_25C_2hr_Broth-1,S01_D03_PLT_25C_2hr_Broth-2,S01_D03_PLT_25C_2hr_Broth-3,S01_D03_PLT_25C_2hr_Broth-4,S01_D03_PLT_25C_2hr_Broth-5,S01_D03_PLT_25C_2hr_Broth-6,S01_D03_PLT_25C_6.5hr_Broth-1,S01_D03_PLT_25C_6.5hr_Broth-2,S01_D03_PLT_25C_6.5hr_Broth-3,S01_D03_PLT_25C_6.5hr_Broth-4,S01_D03_PLT_25C_6.5hr_Broth-5,S01_D03_PLT_25C_6.5hr_Broth-6,S01_D03_PLT_37C_22hr_Broth-1,S01_D03_PLT_37C_22hr_Broth-2,S01_D03_PLT_37C_22hr_Broth-3,S01_D03_PLT_37C_22hr_Broth-4,S01_D03_PLT_37C_22hr_Broth-5,S01_D03_PLT_37C_22hr_Broth-6,S01_D04_PLT_25C_0hr_Broth-1,S01_D04_PLT_25C_0hr_Broth-2,S01_D04_PLT_25C_0hr_Broth-3,S01_D04_PLT_25C_0hr_Broth-4,S01_D04_PLT_25C_0hr_Broth-5,S01_D04_PLT_25C_0hr_Broth-6,S01_D04_PLT_25C_22hr_Broth-1,S01_D04_PLT_25C_22hr_Broth-2,S01_D04_PLT_25C_22hr_Broth-3,S01_D04_PLT_25C_22hr_Broth-4,S01_D04_PLT_25C_22hr_Broth-5,S01_D04_PLT_25C_22hr_Broth-6,S01_D04_PLT_25C_2hr_Broth-1,S01_D04_PLT_25C_2hr_Broth-2,S01_D04_PLT_25C_2hr_Broth-3,S01_D04_PLT_25C_2hr_Broth-4,S01_D04_PLT_25C_2hr_Broth-5,S01_D04_PLT_25C_2hr_Broth-6,S01_D04_PLT_25C_6.5hr_Broth-1,S01_D04_PLT_25C_6.5hr_Broth-2,S01_D04_PLT_25C_6.5hr_Broth-3,S01_D04_PLT_25C_6.5hr_Broth-4,S01_D04_PLT_25C_6.5hr_Broth-5,S01_D04_PLT_25C_6.5hr_Broth-6,S01_D04_PLT_37C_22hr_Broth-1,S01_D04_PLT_37C_22hr_Broth-2,S01_D04_PLT_37C_22hr_Broth-3,S01_D04_PLT_37C_22hr_Broth-4,S01_D04_PLT_37C_22hr_Broth-5,S01_D04_PLT_37C_22hr_Broth-6,S01_D05_PLT_25C_0hr_Broth-1,S01_D05_PLT_25C_0hr_Broth-2,S01_D05_PLT_25C_0hr_Broth-3,S01_D05_PLT_25C_0hr_Broth-4,S01_D05_PLT_25C_0hr_Broth-5,S01_D05_PLT_25C_0hr_Broth-6,S01_D05_PLT_25C_22hr_Broth-1,S01_D05_PLT_25C_22hr_Broth-2,S01_D05_PLT_25C_22hr_Broth-3,S01_D05_PLT_25C_22hr_Broth-4,S01_D05_PLT_25C_22hr_Broth-5,S01_D05_PLT_25C_22hr_Broth-6,S01_D05_PLT_25C_2hr_Broth-1,S01_D05_PLT_25C_2hr_Broth-2,S01_D05_PLT_25C_2hr_Broth-3,S01_D05_PLT_25C_2hr_Broth-4,S01_D05_PLT_25C_2hr_Broth-5,S01_D05_PLT_25C_2hr_Broth-6,S01_D05_PLT_25C_6.5hr_Broth-1,S01_D05_PLT_25C_6.5hr_Broth-2,S01_D05_PLT_25C_6.5hr_Broth-3,S01_D05_PLT_25C_6.5hr_Broth-4,S01_D05_PLT_25C_6.5hr_Broth-5,S01_D05_PLT_25C_6.5hr_Broth-6,S01_D05_PLT_37C_22hr_Broth-1,S01_D05_PLT_37C_22hr_Broth-2,S01_D05_PLT_37C_22hr_Broth-3,S01_D05_PLT_37C_22hr_Broth-4,S01_D05_PLT_37C_22hr_Broth-5,S01_D05_PLT_37C_22hr_Broth-6,S02_D01_PLT_25C_0hr_Broth-1,S02_D01_PLT_25C_0hr_Broth-2,S02_D01_PLT_25C_0hr_Broth-3,S02_D01_PLT_25C_0hr_Broth-4,S02_D01_PLT_25C_0hr_Broth-5,S02_D01_PLT_25C_0hr_Broth-6,S02_D01_PLT_25C_22hr_Broth-1,S02_D01_PLT_25C_22hr_Broth-2,S02_D01_PLT_25C_22hr_Broth-3,S02_D01_PLT_25C_22hr_Broth-4,S02_D01_PLT_25C_22hr_Broth-5,S02_D01_PLT_25C_22hr_Broth-6,S02_D01_PLT_25C_2hr_Broth-1,S02_D01_PLT_25C_2hr_Broth-2,S02_D01_PLT_25C_2hr_Broth-3,S02_D01_PLT_25C_2hr_Broth-4,S02_D01_PLT_25C_2hr_Broth-5,S02_D01_PLT_25C_2hr_Broth-6,S02_D01_PLT_25C_6.5hr_Broth-1,S02_D01_PLT_25C_6.5hr_Broth-2,S02_D01_PLT_25C_6.5hr_Broth-3,S02_D01_PLT_25C_6.5hr_Broth-4,S02_D01_PLT_25C_6.5hr_Broth-5,S02_D01_PLT_25C_6.5hr_Broth-6,S02_D01_PLT_37C_22hr_Broth-1,S02_D01_PLT_37C_22hr_Broth-2,S02_D01_PLT_37C_22hr_Broth-3,S02_D01_PLT_37C_22hr_Broth-4,S02_D01_PLT_37C_22hr_Broth-5,S02_D01_PLT_37C_22hr_Broth-6,S02_D02_PLT_25C_0hr_Broth-1,S02_D02_PLT_25C_0hr_Broth-2,S02_D02_PLT_25C_0hr_Broth-3,S02_D02_PLT_25C_0hr_Broth-4,S02_D02_PLT_25C_0hr_Broth-5,S02_D02_PLT_25C_0hr_Broth-6,S02_D02_PLT_25C_22hr_Broth-1,S02_D02_PLT_25C_22hr_Broth-2,S02_D02_PLT_25C_22hr_Broth-3,S02_D02_PLT_25C_22hr_Broth-4,S02_D02_PLT_25C_22hr_Broth-5,S02_D02_PLT_25C_22hr_Broth-6,S02_D02_PLT_25C_2hr_Broth-1,S02_D02_PLT_25C_2hr_Broth-2,S02_D02_PLT_25C_2hr_Broth-3,S02_D02_PLT_25C_2hr_Broth-4,S02_D02_PLT_25C_2hr_Broth-5,S02_D02_PLT_25C_2hr_Broth-6,S02_D02_PLT_25C_6.5hr_Broth-1,S02_D02_PLT_25C_6.5hr_Broth-2,S02_D02_PLT_25C_6.5hr_Broth-3,S02_D02_PLT_25C_6.5hr_Broth-4,S02_D02_PLT_25C_6.5hr_Broth-5,S02_D02_PLT_25C_6.5hr_Broth-6,S02_D02_PLT_37C_22hr_Broth-1,S02_D02_PLT_37C_22hr_Broth-2,S02_D02_PLT_37C_22hr_Broth-3,S02_D02_PLT_37C_22hr_Broth-4,S02_D02_PLT_37C_22hr_Broth-5,S02_D02_PLT_37C_22hr_Broth-6,S02_D03_PLT_25C_0hr_Broth-1,S02_D03_PLT_25C_0hr_Broth-2,S02_D03_PLT_25C_0hr_Broth-3,S02_D03_PLT_25C_0hr_Broth-4,S02_D03_PLT_25C_0hr_Broth-5,S02_D03_PLT_25C_0hr_Broth-6,S02_D03_PLT_25C_22hr_Broth-1,S02_D03_PLT_25C_22hr_Broth-2,S02_D03_PLT_25C_22hr_Broth-3,S02_D03_PLT_25C_22hr_Broth-4,S02_D03_PLT_25C_22hr_Broth-5,S02_D03_PLT_25C_22hr_Broth-6,S02_D03_PLT_25C_2hr_Broth-1,S02_D03_PLT_25C_2hr_Broth-2,S02_D03_PLT_25C_2hr_Broth-3,S02_D03_PLT_25C_2hr_Broth-4,S02_D03_PLT_25C_2hr_Broth-5,S02_D03_PLT_25C_2hr_Broth-6,S02_D03_PLT_25C_6.5hr_Broth-1,S02_D03_PLT_25C_6.5hr_Broth-2,S02_D03_PLT_25C_6.5hr_Broth-3,S02_D03_PLT_25C_6.5hr_Broth-4,S02_D03_PLT_25C_6.5hr_Broth-5,S02_D03_PLT_25C_6.5hr_Broth-6,S02_D03_PLT_37C_22hr_Broth-1,S02_D03_PLT_37C_22hr_Broth-2,S02_D03_PLT_37C_22hr_Broth-3,S02_D03_PLT_37C_22hr_Broth-4,S02_D03_PLT_37C_22hr_Broth-5,S02_D03_PLT_37C_22hr_Broth-6,S02_D04_PLT_25C_0hr_Broth-1,S02_D04_PLT_25C_0hr_Broth-2,S02_D04_PLT_25C_0hr_Broth-3,S02_D04_PLT_25C_0hr_Broth-4,S02_D04_PLT_25C_0hr_Broth-5,S02_D04_PLT_25C_0hr_Broth-6,S02_D04_PLT_25C_22hr_Broth-1,S02_D04_PLT_25C_22hr_Broth-2,S02_D04_PLT_25C_22hr_Broth-3,S02_D04_PLT_25C_22hr_Broth-4,S02_D04_PLT_25C_22hr_Broth-5,S02_D04_PLT_25C_22hr_Broth-6,S02_D04_PLT_25C_2hr_Broth-1,S02_D04_PLT_25C_2hr_Broth-2,S02_D04_PLT_25C_2hr_Broth-3,S02_D04_PLT_25C_2hr_Broth-4,S02_D04_PLT_25C_2hr_Broth-5,S02_D04_PLT_25C_2hr_Broth-6,S02_D04_PLT_25C_6.5hr_Broth-1,S02_D04_PLT_25C_6.5hr_Broth-2,S02_D04_PLT_25C_6.5hr_Broth-3,S02_D04_PLT_25C_6.5hr_Broth-4,S02_D04_PLT_25C_6.5hr_Broth-5,S02_D04_PLT_25C_6.5hr_Broth-6,S02_D04_PLT_37C_22hr_Broth-1,S02_D04_PLT_37C_22hr_Broth-2,S02_D04_PLT_37C_22hr_Broth-3,S02_D04_PLT_37C_22hr_Broth-4,S02_D04_PLT_37C_22hr_Broth-5,S02_D04_PLT_37C_22hr_Broth-6,S02_D05_PLT_25C_0hr_Broth-1,S02_D05_PLT_25C_0hr_Broth-2,S02_D05_PLT_25C_0hr_Broth-3,S02_D05_PLT_25C_0hr_Broth-4,S02_D05_PLT_25C_0hr_Broth-5,S02_D05_PLT_25C_0hr_Broth-6,S02_D05_PLT_25C_22hr_Broth-1,S02_D05_PLT_25C_22hr_Broth-2,S02_D05_PLT_25C_22hr_Broth-3,S02_D05_PLT_25C_22hr_Broth-4,S02_D05_PLT_25C_22hr_Broth-5,S02_D05_PLT_25C_22hr_Broth-6,S02_D05_PLT_25C_2hr_Broth-1,S02_D05_PLT_25C_2hr_Broth-2,S02_D05_PLT_25C_2hr_Broth-3,S02_D05_PLT_25C_2hr_Broth-4,S02_D05_PLT_25C_2hr_Broth-5,S02_D05_PLT_25C_2hr_Broth-6,S02_D05_PLT_25C_6.5hr_Broth-1,S02_D05_PLT_25C_6.5hr_Broth-2,S02_D05_PLT_25C_6.5hr_Broth-3,S02_D05_PLT_25C_6.5hr_Broth-4,S02_D05_PLT_25C_6.5hr_Broth-5,S02_D05_PLT_25C_6.5hr_Broth-6,S02_D05_PLT_37C_22hr_Broth-1,S02_D05_PLT_37C_22hr_Broth-2,S02_D05_PLT_37C_22hr_Broth-3,S02_D05_PLT_37C_22hr_Broth-4,S02_D05_PLT_37C_22hr_Broth-5,S02_D05_PLT_37C_22hr_Broth-6'
#platelet_sna = platelet_sna_str.split(',')

#rbc_sna_str = 'RBC_140_Broth-1,RBC_140_Broth-2,RBC_140_Broth-3,RBC_140_Broth-4,RBC_140_Broth-5,RBC_140_Broth-6,RBC_141_Broth-1,RBC_141_Broth-2,RBC_141_Broth-3,RBC_141_Broth-4,RBC_141_Broth-5,RBC_141_Broth-6,RBC_142_Broth-1,RBC_142_Broth-2,RBC_142_Broth-3,RBC_142_Broth-4,RBC_142_Broth-5,RBC_142_Broth-6,RBC_143_Broth-1,RBC_143_Broth-2,RBC_143_Broth-3,RBC_143_Broth-4,RBC_143_Broth-5,RBC_143_Broth-6,RBC_150_Broth-1,RBC_150_Broth-2,RBC_150_Broth-3,RBC_150_Broth-4,RBC_150_Broth-5,RBC_150_Broth-6,RBC_151_Broth-1,RBC_151_Broth-2,RBC_151_Broth-3,RBC_151_Broth-4,RBC_151_Broth-5,RBC_151_Broth-6,RBC_152_Broth-1,RBC_152_Broth-2,RBC_152_Broth-3,RBC_152_Broth-4,RBC_152_Broth-5,RBC_152_Broth-6,RBC_153_Broth-1,RBC_153_Broth-2,RBC_153_Broth-3,RBC_153_Broth-4,RBC_153_Broth-5,RBC_153_Broth-6,RBC_154_Broth-1,RBC_154_Broth-2,RBC_154_Broth-3,RBC_154_Broth-4,RBC_154_Broth-5,RBC_154_Broth-6,RBC_155_Broth-1,RBC_155_Broth-2,RBC_155_Broth-3,RBC_155_Broth-4,RBC_155_Broth-5,RBC_155_Broth-6,RBC_30_Broth-1,RBC_30_Broth-2,RBC_30_Broth-3,RBC_30_Broth-4,RBC_30_Broth-5,RBC_30_Broth-6,RBC_31_Broth-1,RBC_31_Broth-2,RBC_31_Broth-3,RBC_31_Broth-4,RBC_31_Broth-5,RBC_31_Broth-6,RBC_32_Broth-1,RBC_32_Broth-2,RBC_32_Broth-3,RBC_32_Broth-4,RBC_32_Broth-5,RBC_32_Broth-6,RBC_33_Broth-1,RBC_33_Broth-2,RBC_33_Broth-3,RBC_33_Broth-4,RBC_33_Broth-5,RBC_33_Broth-6,RBC_34_Broth-1,RBC_34_Broth-2,RBC_34_Broth-3,RBC_34_Broth-4,RBC_34_Broth-5,RBC_34_Broth-6,RBC_35_Broth-1,RBC_35_Broth-2,RBC_35_Broth-3,RBC_35_Broth-4,RBC_35_Broth-5,RBC_35_Broth-6,RBC_36_Broth-1,RBC_36_Broth-2,RBC_36_Broth-3,RBC_36_Broth-4,RBC_36_Broth-5,RBC_36_Broth-6,RBC_37_Broth-1,RBC_37_Broth-2,RBC_37_Broth-3,RBC_37_Broth-4,RBC_37_Broth-5,RBC_37_Broth-6,RBC_38_Broth-1,RBC_38_Broth-2,RBC_38_Broth-3,RBC_38_Broth-4,RBC_38_Broth-5,RBC_38_Broth-6,RBC_39_Broth-1,RBC_39_Broth-2,RBC_39_Broth-3,RBC_39_Broth-4,RBC_39_Broth-5,RBC_39_Broth-6,RBC_40_Broth-1,RBC_40_Broth-2,RBC_40_Broth-3,RBC_40_Broth-4,RBC_40_Broth-5,RBC_40_Broth-6,RBC_42_Broth-1,RBC_42_Broth-2,RBC_42_Broth-3,RBC_42_Broth-4,RBC_42_Broth-5,RBC_42_Broth-6,S01_D01_RBC_25C_0hr_Broth-1,S01_D01_RBC_25C_0hr_Broth-2,S01_D01_RBC_25C_0hr_Broth-3,S01_D01_RBC_25C_0hr_Broth-4,S01_D01_RBC_25C_0hr_Broth-5,S01_D01_RBC_25C_0hr_Broth-6,S01_D01_RBC_25C_2hr_Broth-1,S01_D01_RBC_25C_2hr_Broth-2,S01_D01_RBC_25C_2hr_Broth-3,S01_D01_RBC_25C_2hr_Broth-4,S01_D01_RBC_25C_2hr_Broth-5,S01_D01_RBC_25C_2hr_Broth-6,S01_D01_RBC_25C_6.5hr_Broth-1,S01_D01_RBC_25C_6.5hr_Broth-2,S01_D01_RBC_25C_6.5hr_Broth-3,S01_D01_RBC_25C_6.5hr_Broth-4,S01_D01_RBC_25C_6.5hr_Broth-5,S01_D01_RBC_25C_6.5hr_Broth-6,S01_D02_RBC_25C_0hr_Broth-1,S01_D02_RBC_25C_0hr_Broth-2,S01_D02_RBC_25C_0hr_Broth-3,S01_D02_RBC_25C_0hr_Broth-4,S01_D02_RBC_25C_0hr_Broth-5,S01_D02_RBC_25C_0hr_Broth-6,S01_D02_RBC_25C_2hr_Broth-1,S01_D02_RBC_25C_2hr_Broth-2,S01_D02_RBC_25C_2hr_Broth-3,S01_D02_RBC_25C_2hr_Broth-4,S01_D02_RBC_25C_2hr_Broth-5,S01_D02_RBC_25C_2hr_Broth-6,S01_D02_RBC_25C_6.5hr_Broth-1,S01_D02_RBC_25C_6.5hr_Broth-2,S01_D02_RBC_25C_6.5hr_Broth-3,S01_D02_RBC_25C_6.5hr_Broth-4,S01_D02_RBC_25C_6.5hr_Broth-5,S01_D02_RBC_25C_6.5hr_Broth-6,S01_D02_RBC_37C_22hr_Broth-1,S01_D02_RBC_37C_22hr_Broth-2,S01_D02_RBC_37C_22hr_Broth-3,S01_D02_RBC_37C_22hr_Broth-4,S01_D02_RBC_37C_22hr_Broth-5,S01_D02_RBC_37C_22hr_Broth-6,S01_D03_RBC_25C_0hr_Broth-1,S01_D03_RBC_25C_0hr_Broth-2,S01_D03_RBC_25C_0hr_Broth-3,S01_D03_RBC_25C_0hr_Broth-4,S01_D03_RBC_25C_0hr_Broth-5,S01_D03_RBC_25C_0hr_Broth-6,S01_D03_RBC_25C_2hr_Broth-1,S01_D03_RBC_25C_2hr_Broth-2,S01_D03_RBC_25C_2hr_Broth-3,S01_D03_RBC_25C_2hr_Broth-4,S01_D03_RBC_25C_2hr_Broth-5,S01_D03_RBC_25C_2hr_Broth-6,S01_D03_RBC_25C_6.5hr_Broth-1,S01_D03_RBC_25C_6.5hr_Broth-2,S01_D03_RBC_25C_6.5hr_Broth-3,S01_D03_RBC_25C_6.5hr_Broth-4,S01_D03_RBC_25C_6.5hr_Broth-5,S01_D03_RBC_25C_6.5hr_Broth-6,S01_D03_RBC_37C_22hr_Broth-1,S01_D03_RBC_37C_22hr_Broth-2,S01_D03_RBC_37C_22hr_Broth-3,S01_D03_RBC_37C_22hr_Broth-4,S01_D03_RBC_37C_22hr_Broth-5,S01_D03_RBC_37C_22hr_Broth-6,S01_D04_RBC_25C_0hr_Broth-1,S01_D04_RBC_25C_0hr_Broth-2,S01_D04_RBC_25C_0hr_Broth-3,S01_D04_RBC_25C_0hr_Broth-4,S01_D04_RBC_25C_0hr_Broth-5,S01_D04_RBC_25C_0hr_Broth-6,S01_D04_RBC_25C_2hr_Broth-1,S01_D04_RBC_25C_2hr_Broth-2,S01_D04_RBC_25C_2hr_Broth-3,S01_D04_RBC_25C_2hr_Broth-4,S01_D04_RBC_25C_2hr_Broth-5,S01_D04_RBC_25C_2hr_Broth-6,S01_D04_RBC_37C_22hr_Broth-1,S01_D04_RBC_37C_22hr_Broth-2,S01_D04_RBC_37C_22hr_Broth-3,S01_D04_RBC_37C_22hr_Broth-4,S01_D04_RBC_37C_22hr_Broth-5,S01_D04_RBC_37C_22hr_Broth-6,S01_D05_RBC_25C_0hr_Broth-1,S01_D05_RBC_25C_0hr_Broth-2,S01_D05_RBC_25C_0hr_Broth-3,S01_D05_RBC_25C_0hr_Broth-4,S01_D05_RBC_25C_0hr_Broth-5,S01_D05_RBC_25C_0hr_Broth-6,S01_D05_RBC_25C_2hr_Broth-1,S01_D05_RBC_25C_2hr_Broth-2,S01_D05_RBC_25C_2hr_Broth-3,S01_D05_RBC_25C_2hr_Broth-4,S01_D05_RBC_25C_2hr_Broth-5,S01_D05_RBC_25C_2hr_Broth-6,S01_D05_RBC_37C_22hr_Broth-1,S01_D05_RBC_37C_22hr_Broth-2,S01_D05_RBC_37C_22hr_Broth-3,S01_D05_RBC_37C_22hr_Broth-4,S01_D05_RBC_37C_22hr_Broth-5,S01_D05_RBC_37C_22hr_Broth-6,S02_D01_RBC_25C_0hr_Broth-1,S02_D01_RBC_25C_0hr_Broth-2,S02_D01_RBC_25C_0hr_Broth-3,S02_D01_RBC_25C_0hr_Broth-4,S02_D01_RBC_25C_0hr_Broth-5,S02_D01_RBC_25C_0hr_Broth-6,S02_D01_RBC_25C_22hr_Broth-1,S02_D01_RBC_25C_22hr_Broth-2,S02_D01_RBC_25C_22hr_Broth-3,S02_D01_RBC_25C_22hr_Broth-4,S02_D01_RBC_25C_22hr_Broth-5,S02_D01_RBC_25C_22hr_Broth-6,S02_D01_RBC_25C_2hr_Broth-1,S02_D01_RBC_25C_2hr_Broth-2,S02_D01_RBC_25C_2hr_Broth-3,S02_D01_RBC_25C_2hr_Broth-4,S02_D01_RBC_25C_2hr_Broth-5,S02_D01_RBC_25C_2hr_Broth-6,S02_D01_RBC_25C_6.5hr_Broth-1,S02_D01_RBC_25C_6.5hr_Broth-2,S02_D01_RBC_25C_6.5hr_Broth-3,S02_D01_RBC_25C_6.5hr_Broth-4,S02_D01_RBC_25C_6.5hr_Broth-5,S02_D01_RBC_25C_6.5hr_Broth-6,S02_D01_RBC_37C_22hr_Broth-1,S02_D01_RBC_37C_22hr_Broth-2,S02_D01_RBC_37C_22hr_Broth-3,S02_D01_RBC_37C_22hr_Broth-4,S02_D01_RBC_37C_22hr_Broth-5,S02_D01_RBC_37C_22hr_Broth-6,S02_D02_RBC_25C_0hr_Broth-1,S02_D02_RBC_25C_0hr_Broth-2,S02_D02_RBC_25C_0hr_Broth-3,S02_D02_RBC_25C_0hr_Broth-4,S02_D02_RBC_25C_0hr_Broth-5,S02_D02_RBC_25C_0hr_Broth-6,S02_D02_RBC_25C_22hr_Broth-1,S02_D02_RBC_25C_22hr_Broth-2,S02_D02_RBC_25C_22hr_Broth-3,S02_D02_RBC_25C_22hr_Broth-4,S02_D02_RBC_25C_22hr_Broth-5,S02_D02_RBC_25C_22hr_Broth-6,S02_D02_RBC_25C_2hr_Broth-1,S02_D02_RBC_25C_2hr_Broth-2,S02_D02_RBC_25C_2hr_Broth-3,S02_D02_RBC_25C_2hr_Broth-4,S02_D02_RBC_25C_2hr_Broth-5,S02_D02_RBC_25C_2hr_Broth-6,S02_D02_RBC_25C_6.5hr_Broth-1,S02_D02_RBC_25C_6.5hr_Broth-2,S02_D02_RBC_25C_6.5hr_Broth-3,S02_D02_RBC_25C_6.5hr_Broth-4,S02_D02_RBC_25C_6.5hr_Broth-5,S02_D02_RBC_25C_6.5hr_Broth-6,S02_D02_RBC_37C_22hr_Broth-1,S02_D02_RBC_37C_22hr_Broth-2,S02_D02_RBC_37C_22hr_Broth-3,S02_D02_RBC_37C_22hr_Broth-4,S02_D02_RBC_37C_22hr_Broth-5,S02_D02_RBC_37C_22hr_Broth-6,S02_D03_RBC_25C_0hr_Broth-1,S02_D03_RBC_25C_0hr_Broth-2,S02_D03_RBC_25C_0hr_Broth-3,S02_D03_RBC_25C_0hr_Broth-4,S02_D03_RBC_25C_0hr_Broth-5,S02_D03_RBC_25C_0hr_Broth-6,S02_D03_RBC_25C_22hr_Broth-1,S02_D03_RBC_25C_22hr_Broth-2,S02_D03_RBC_25C_22hr_Broth-3,S02_D03_RBC_25C_22hr_Broth-4,S02_D03_RBC_25C_22hr_Broth-5,S02_D03_RBC_25C_22hr_Broth-6,S02_D03_RBC_25C_2hr_Broth-1,S02_D03_RBC_25C_2hr_Broth-2,S02_D03_RBC_25C_2hr_Broth-3,S02_D03_RBC_25C_2hr_Broth-4,S02_D03_RBC_25C_2hr_Broth-5,S02_D03_RBC_25C_2hr_Broth-6,S02_D03_RBC_25C_6.5hr_Broth-1,S02_D03_RBC_25C_6.5hr_Broth-2,S02_D03_RBC_25C_6.5hr_Broth-3,S02_D03_RBC_25C_6.5hr_Broth-4,S02_D03_RBC_25C_6.5hr_Broth-5,S02_D03_RBC_25C_6.5hr_Broth-6,S02_D03_RBC_37C_22hr_Broth-1,S02_D03_RBC_37C_22hr_Broth-2,S02_D03_RBC_37C_22hr_Broth-3,S02_D03_RBC_37C_22hr_Broth-4,S02_D03_RBC_37C_22hr_Broth-5,S02_D03_RBC_37C_22hr_Broth-6,S02_D04_RBC_25C_0hr_Broth-1,S02_D04_RBC_25C_0hr_Broth-2,S02_D04_RBC_25C_0hr_Broth-3,S02_D04_RBC_25C_0hr_Broth-4,S02_D04_RBC_25C_0hr_Broth-5,S02_D04_RBC_25C_0hr_Broth-6,S02_D04_RBC_25C_22hr_Broth-1,S02_D04_RBC_25C_22hr_Broth-2,S02_D04_RBC_25C_22hr_Broth-3,S02_D04_RBC_25C_22hr_Broth-4,S02_D04_RBC_25C_22hr_Broth-5,S02_D04_RBC_25C_22hr_Broth-6,S02_D04_RBC_25C_2hr_Broth-1,S02_D04_RBC_25C_2hr_Broth-2,S02_D04_RBC_25C_2hr_Broth-3,S02_D04_RBC_25C_2hr_Broth-4,S02_D04_RBC_25C_2hr_Broth-5,S02_D04_RBC_25C_2hr_Broth-6,S02_D04_RBC_25C_6.5hr_Broth-1,S02_D04_RBC_25C_6.5hr_Broth-2,S02_D04_RBC_25C_6.5hr_Broth-3,S02_D04_RBC_25C_6.5hr_Broth-4,S02_D04_RBC_25C_6.5hr_Broth-5,S02_D04_RBC_25C_6.5hr_Broth-6,S02_D04_RBC_37C_22hr_Broth-1,S02_D04_RBC_37C_22hr_Broth-2,S02_D04_RBC_37C_22hr_Broth-3,S02_D04_RBC_37C_22hr_Broth-4,S02_D04_RBC_37C_22hr_Broth-5,S02_D04_RBC_37C_22hr_Broth-6,S02_D05_RBC_25C_0hr_Broth-1,S02_D05_RBC_25C_0hr_Broth-2,S02_D05_RBC_25C_0hr_Broth-3,S02_D05_RBC_25C_0hr_Broth-4,S02_D05_RBC_25C_0hr_Broth-5,S02_D05_RBC_25C_0hr_Broth-6,S02_D05_RBC_25C_22hr_Broth-1,S02_D05_RBC_25C_22hr_Broth-2,S02_D05_RBC_25C_22hr_Broth-3,S02_D05_RBC_25C_22hr_Broth-4,S02_D05_RBC_25C_22hr_Broth-5,S02_D05_RBC_25C_22hr_Broth-6,S02_D05_RBC_25C_2hr_Broth-1,S02_D05_RBC_25C_2hr_Broth-2,S02_D05_RBC_25C_2hr_Broth-3,S02_D05_RBC_25C_2hr_Broth-4,S02_D05_RBC_25C_2hr_Broth-5,S02_D05_RBC_25C_2hr_Broth-6,S02_D05_RBC_25C_6.5hr_Broth-1,S02_D05_RBC_25C_6.5hr_Broth-2,S02_D05_RBC_25C_6.5hr_Broth-3,S02_D05_RBC_25C_6.5hr_Broth-4,S02_D05_RBC_25C_6.5hr_Broth-5,S02_D05_RBC_25C_6.5hr_Broth-6,S02_D05_RBC_37C_22hr_Broth-1,S02_D05_RBC_37C_22hr_Broth-2,S02_D05_RBC_37C_22hr_Broth-3,S02_D05_RBC_37C_22hr_Broth-4,S02_D05_RBC_37C_22hr_Broth-5,S02_D05_RBC_37C_22hr_Broth-6'
#rbc_sna = rbc_sna_str.split(',')

#snp_sna_str = 'BloodProject01_UID1,BloodProject01_UID10,BloodProject01_UID11,BloodProject01_UID12,BloodProject01_UID13,BloodProject01_UID14,BloodProject01_UID15,BloodProject01_UID16,BloodProject01_UID18,BloodProject01_UID19,BloodProject01_UID2,BloodProject01_UID20,BloodProject01_UID21,BloodProject01_UID22,BloodProject01_UID23,BloodProject01_UID24,BloodProject01_UID25,BloodProject01_UID26,BloodProject01_UID30,BloodProject01_UID35,BloodProject01_UID39,BloodProject01_UID4,BloodProject01_UID41,BloodProject01_UID42,BloodProject01_UID5,BloodProject01_UID6,BloodProject01_UID7,BloodProject01_UID8,BloodProject01_UID9'
#snp_sna = snp_sna_str.split(',')

#exmeasuredData01.reset_dataStage02_physiology_measuredData(
#            tables_I = ['data_stage02_physiology_measuredCoverage'],
#            experiment_id_I = 'BloodProject01',
#            warn_I=False)
##platelet model
#exmeasuredData01.execute_measuredCoverage(
#    model_id_I = 'iAT_PLT_636',
#    experiment_ids_I = 'BloodProject01',
#    sample_name_abbreviations_I = platelet_sna + snp_sna)
##RBC model
#exmeasuredData01.execute_measuredCoverage(
#    model_id_I = 'iAB_RBC_283',
#    experiment_ids_I = 'BloodProject01',
#    sample_name_abbreviations_I = rbc_sna + snp_sna)



#make the COBRA table
from SBaaS_models.models_COBRA_execute import models_COBRA_execute
exCOBRA01 = models_COBRA_execute(session,engine,pg_settings.datadir_settings);
exCOBRA01.initialize_supportedTables();
exCOBRA01.initialize_tables();

#pre-load the models
cobramodels = exCOBRA01.get_models(model_ids_I=["150526_iDM2015"]);
#cobramodels = exCOBRA01.get_models(model_ids_I=["iJO1366"]);

#pre-load the models
cobramodels = exCOBRA01.get_models(model_ids_I=["150526_iDM2015"]);
# cobramodels = exCOBRA01.get_models(model_ids_I=["iJO1366"]);

#revert to reversible
rxns = [rxn.id for rxn in cobramodels["150526_iDM2015"].reactions]
print(str(len(rxns)))
exCOBRA01.revert2reversible(cobramodels["150526_iDM2015"],ignore_reflection=True)
rxns = [rxn.id for rxn in cobramodels["150526_iDM2015"].reactions]
print(str(len(rxns)))

simulations = [
    'ALEsKOs01_151026_iDM2015_full05_OxicEvo04EcoliGlc_0',
    'ALEsKOs01_151026_iDM2015_full05_OxicEvo04Evo01EPEcoliGlc_11',
    'ALEsKOs01_151026_iDM2015_full05_OxicEvo04Evo02EPEcoliGlc_11',
    'ALEsKOs01_151026_iDM2015_full05_OxicEvo04gndEcoliGlc_0',
    'ALEsKOs01_151026_iDM2015_full05_OxicEvo04gndEvo01EPEcoliGlc_11',
    'ALEsKOs01_151026_iDM2015_full05_OxicEvo04gndEvo02EPEcoliGlc_11',
    'ALEsKOs01_151026_iDM2015_full05_OxicEvo04gndEvo03EPEcoliGlc_11',
    'ALEsKOs01_151026_iDM2015_full05_OxicEvo04pgiEcoliGlc_0',
    'ALEsKOs01_151026_iDM2015_full05_OxicEvo04pgiEvo01EPEcoliGlc_11',
    'ALEsKOs01_151026_iDM2015_full05_OxicEvo04pgiEvo02EPEcoliGlc_11',
    'ALEsKOs01_151026_iDM2015_full05_OxicEvo04pgiEvo03EPEcoliGlc_11',
    'ALEsKOs01_151026_iDM2015_full05_OxicEvo04pgiEvo04EPEcoliGlc_11',
    'ALEsKOs01_151026_iDM2015_full05_OxicEvo04pgiEvo05EPEcoliGlc_11',
    'ALEsKOs01_151026_iDM2015_full05_OxicEvo04pgiEvo06EPEcoliGlc_11',
    'ALEsKOs01_151026_iDM2015_full05_OxicEvo04pgiEvo07EPEcoliGlc_11',
    'ALEsKOs01_151026_iDM2015_full05_OxicEvo04pgiEvo08EPEcoliGlc_11',
    'ALEsKOs01_151026_iDM2015_full05_OxicEvo04ptsHIcrrEcoliGlc_0',
    'ALEsKOs01_151026_iDM2015_full05_OxicEvo04ptsHIcrrEvo01EPEcoliGlc_11',
    'ALEsKOs01_151026_iDM2015_full05_OxicEvo04ptsHIcrrEvo02EPEcoliGlc_11',
    'ALEsKOs01_151026_iDM2015_full05_OxicEvo04ptsHIcrrEvo03EPEcoliGlc_11',
    'ALEsKOs01_151026_iDM2015_full05_OxicEvo04ptsHIcrrEvo04EPEcoliGlc_11',
    'ALEsKOs01_151026_iDM2015_full05_OxicEvo04sdhCBEcoliGlc_0',
    'ALEsKOs01_151026_iDM2015_full05_OxicEvo04sdhCBEvo01EPEcoliGlc_11',
    'ALEsKOs01_151026_iDM2015_full05_OxicEvo04sdhCBEvo02EPEcoliGlc_11',
    'ALEsKOs01_151026_iDM2015_full05_OxicEvo04sdhCBEvo03EPEcoliGlc_11',
    'ALEsKOs01_151026_iDM2015_full05_OxicEvo04tpiAEcoliGlc_0',
    'ALEsKOs01_151026_iDM2015_full05_OxicEvo04tpiAEvo01EPEcoliGlc_11',
    'ALEsKOs01_151026_iDM2015_full05_OxicEvo04tpiAEvo02EPEcoliGlc_11',
    'ALEsKOs01_151026_iDM2015_full05_OxicEvo04tpiAEvo03EPEcoliGlc_11',
    'ALEsKOs01_151026_iDM2015_full05_OxicEvo04tpiAEvo04EPEcoliGlc_11',
        ]

#simulations = [
#        'ALEsKOs01_iJO1366_OxicEvo04EcoliGlc',
#        'ALEsKOs01_iJO1366_OxicEvo04gndEcoliGlc',
#        'ALEsKOs01_iJO1366_OxicEvo04pgiEcoliGlc',
#        'ALEsKOs01_iJO1366_OxicEvo04ptsHIcrrEcoliGlc',
#        'ALEsKOs01_iJO1366_OxicEvo04sdhCBEcoliGlc',
#        'ALEsKOs01_iJO1366_OxicEvo04tpiAEcoliGlc',
#        'ALEsKOs01_iJO1366_OxicEvo04pgiEvo01EPEcoliGlc',
#        'ALEsKOs01_iJO1366_OxicEvo04pgiEvo02EPEcoliGlc',
#        'ALEsKOs01_iJO1366_OxicEvo04pgiEvo03EPEcoliGlc',
#        'ALEsKOs01_iJO1366_OxicEvo04pgiEvo04EPEcoliGlc',
#        'ALEsKOs01_iJO1366_OxicEvo04pgiEvo05EPEcoliGlc',
#        'ALEsKOs01_iJO1366_OxicEvo04pgiEvo06EPEcoliGlc',
#        'ALEsKOs01_iJO1366_OxicEvo04pgiEvo07EPEcoliGlc',
#        'ALEsKOs01_iJO1366_OxicEvo04pgiEvo08EPEcoliGlc',
#        'ALEsKOs01_iJO1366_OxicEvo04ptsHIcrrEvo01EPEcoliGlc',
#        'ALEsKOs01_iJO1366_OxicEvo04ptsHIcrrEvo02EPEcoliGlc',
#        'ALEsKOs01_iJO1366_OxicEvo04ptsHIcrrEvo03EPEcoliGlc',
#        'ALEsKOs01_iJO1366_OxicEvo04ptsHIcrrEvo04EPEcoliGlc',
#        'ALEsKOs01_iJO1366_OxicEvo04tpiAEvo01EPEcoliGlc',
#        'ALEsKOs01_iJO1366_OxicEvo04tpiAEvo02EPEcoliGlc',
#        'ALEsKOs01_iJO1366_OxicEvo04tpiAEvo03EPEcoliGlc',
#        'ALEsKOs01_iJO1366_OxicEvo04tpiAEvo04EPEcoliGlc',
#        'ALEsKOs01_iJO1366_OxicEvo04gndEvo01EPEcoliGlc',
#        'ALEsKOs01_iJO1366_OxicEvo04gndEvo02EPEcoliGlc',
#        'ALEsKOs01_iJO1366_OxicEvo04gndEvo03EPEcoliGlc',
#        'ALEsKOs01_iJO1366_OxicEvo04sdhCBEvo01EPEcoliGlc',
#        'ALEsKOs01_iJO1366_OxicEvo04sdhCBEvo02EPEcoliGlc',
#        'ALEsKOs01_iJO1366_OxicEvo04sdhCBEvo03EPEcoliGlc',
#        'ALEsKOs01_iJO1366_OxicEvo04Evo02EPEcoliGlc',
#        'ALEsKOs01_iJO1366_OxicEvo04Evo01EPEcoliGlc'
#        ]

#make the simulation table
from SBaaS_COBRA.stage02_physiology_simulatedData_execute import stage02_physiology_simulatedData_execute
simulatedData01 = stage02_physiology_simulatedData_execute(session,engine,pg_settings.datadir_settings);
simulatedData01.initialize_supportedTables();
simulatedData01.initialize_tables();

## Test the constraints
#for simulation in simulations:
#    print('running simulation ' + simulation);
#    data = simulatedData01.execute_testConstraintsIndividual(simulation_id_I=simulation,
#                       rxn_ids_I=[],
#                       models_I = cobramodels,
#                       solver_id_I = "glpk",
#                       gr_check_I = 0.1,
#                       diagnose_threshold_I=0.99,
#                       diagnose_break_I=0.1)
#    for d in data: print(d)
#    data = simulatedData01.execute_testConstraintsCumulative(simulation_id_I=simulation,
#                       rxn_ids_I=[],
#                       models_I = cobramodels,
#                       solver_id_I = "glpk",
#                       gr_check_I = 0.1,
#                       diagnose_threshold_I=0.99,
#                       diagnose_break_I=0.1)
#    for d in data: print(d)

#for simulation in simulations:
#    print('running simulation ' + simulation);
#    simulatedData01.reset_dataStage02_physiology_simulatedData(
#            tables_I = ['data_stage02_physiology_simulatedData_fva',
#                        'data_stage02_physiology_simulatedData_fbaPrimal',
#                        'data_stage02_physiology_simulatedData_fbaDual',
#                        'data_stage02_physiology_simulatedData_sra',],
#            simulation_id_I = simulation,
#            warn_I=False)
#    #fba
#    simulatedData01.execute_fba(simulation_id_I=simulation,
#                        rxn_ids_I=[],
#                        models_I = cobramodels,
#                        method_I='fba',
#                        allow_loops_I = True,
#                        options_I = {},
#                        solver_id_I='glpk',
#                        )
#    #fva
#    simulatedData01.execute_fva(simulation_id_I=simulation,
#                    rxn_ids_I=[],
#                    models_I = cobramodels,
#                    method_I='fva',
#                    allow_loops_I = True,
#                        options_I = {},
#                    solver_id_I='glpk',
#                    )

#make the simulatedData table
from SBaaS_COBRA.stage02_physiology_sampledData_execute import stage02_physiology_sampledData_execute
sampledData01 = stage02_physiology_sampledData_execute(session,engine,pg_settings.datadir_settings);
sampledData01.initialize_supportedTables();
sampledData01.initialize_tables();

#data_dir = pg_settings.datadir_settings['workspace_data']+'/_output';
data_dir = 'F:/Users/dmccloskey-sbrg/Dropbox (UCSD SBRG)/Phenomics_ALEsKOs01/sampling'
#data_dir = 'F:/Users/dmccloskey-sbrg/Dropbox (UCSD SBRG)/MATLAB/sampling_physiology'

# import sampling results
for simulation in simulations:
    print('running simulation ' + simulation);
#    sampledData01.reset_dataStage02_physiology_sampledData(
#        tables_I = ['data_stage02_physiology_sampledPoints',
#                   'data_stage02_physiology_sampledData',
#                   'data_stage02_physiology_sampledMetaboliteData',
#                   'data_stage02_physiology_sampledSubsystemData',
#                   ],
#        simulation_id_I = simulation,
#        warn_I=False
#    );
    sampledData01.execute_analyzeSamplingPoints(simulation_id_I=simulation,
        rxn_ids_I=[],
        data_dir_I = data_dir,
        models_I = cobramodels,
        points_overview_I=False,
        flux_stats_I=True,
        metabolite_stats_I=False,
        subsystem_stats_I=False,
       remove_loops = False,
       normalize_points2Input = True,
       normalize_rnx_ids = ['EX_glc_LPAREN_e_RPAREN_']
        )