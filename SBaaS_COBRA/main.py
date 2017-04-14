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

#make the COBRA table
from SBaaS_COBRA.stage02_physiology_graphData_execute import stage02_physiology_graphData_execute
graphData01 = stage02_physiology_graphData_execute(session,engine,pg_settings.datadir_settings);
graphData01.initialize_supportedTables()
graphData01.initialize_tables()


##graphData01.export_dataStage02PhysiologyGraphDataShortestPathStats_js('ALEsKOs01_151026_iDM2015_full05_OxicEvo04gndEvo01EPEcoliGlc_11')
#graphData01.export_dataStage02PhysiologyGraphDataShortestPaths_js('ALEsKOs01_151026_iDM2015_full05_OxicEvo04gndEvo01EPEcoliGlc_11')

from SBaaS_base.sbaas_template_py import sbaas_template_py
template_py = sbaas_template_py();
script_py = template_py.make_postgresql_modelClasses_py(
    table_name = 'data_stage02_physiology_measuredCoverage',
    columns = [
        'experiment_id','sample_name_abbreviation',
                'model_id',
                'model_component',
                'data_component',
                'n_model_components',
                'n_mapped_components',
                'fraction_mapped',
        ],
    )
print(script_py)