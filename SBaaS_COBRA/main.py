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

#make the measuredData table
from SBaaS_COBRA.stage02_physiology_measuredData_execute import stage02_physiology_measuredData_execute
exmeasuredData01 = stage02_physiology_measuredData_execute(session,engine,pg_settings.datadir_settings)
exmeasuredData01.initialize_supportedTables(); 
exmeasuredData01.initialize_dataStage02_physiology_measuredData();

#define simulation2quantId conversion
IDsQuantification2SimulationIDsIsotopomer = {
    "ALEsKOs01_150526_iDM2015_full05_OxicEvo04Ecoli13CGlc_0":{"sample_name_abbreviation":"OxicEvo04EcoliGlc","experiment_id":"ALEsKOs01","model_id":"151026_iDM2015","simulation_dateAndTime":"2-18-2016 7:53","flux_units":"mmol*gDCW-1*hr-1"},
};
#exmeasuredData01.execute_makeFluxomicsData(
#    IDsQuantification2SimulationIDsIsotopomer_I = IDsQuantification2SimulationIDsIsotopomer,
#      criteria_I = 'flux_lb/flux_ub',
#      flip_rxn_direction_I=[]
#    );

#make the simulatedData table
from SBaaS_COBRA.stage02_physiology_sampledData_execute import stage02_physiology_sampledData_execute
sampledData01 = stage02_physiology_sampledData_execute(session,engine,pg_settings.datadir_settings);
sampledData01.initialize_supportedTables();
sampledData01.initialize_dataStage02_physiology_sampledData();

##test the model
#test_result = exCOBRA01.execute_testModel(model_id_I="140407_iDM2014_irreversible");

#pre-load the models
cobramodels = exCOBRA01.get_models(model_ids_I=["150526_iDM2015"]);
rxns = [rxn.id for rxn in cobramodels["150526_iDM2015"].reactions]
print(str(len(rxns)))
exCOBRA01.revert2reversible(cobramodels["150526_iDM2015"],ignore_reflection=True)
rxns = [rxn.id for rxn in cobramodels["150526_iDM2015"].reactions]
print(str(len(rxns)))

simulations = [
        #'WTEColi_113C80_U13C20_02_140407_iDM2014_irreversible_OxicWtGlc_0',
        'ALEsKOs01_151026_iDM2015_full05_OxicEvo04gndEvo01EPEcoliGlc_11'
        ]

for simulation in simulations:
    print("running simulation " + simulation);
    #simulatedData01.reset_dataStage02_physiology_simulatedData(
    #        tables_I = ['data_stage02_physiology_simulatedData_fva',
    #                    'data_stage02_physiology_simulatedData_fbaPrimal',
    #                    'data_stage02_physiology_simulatedData_fbaDual',
    #                    'data_stage02_physiology_simulatedData_sra',
    #                    ],
    #        simulation_id_I = simulation,
    #        warn_I=False)
    #data = simulatedData01.execute_testConstraintsIndividual(simulation_id_I=simulation,
    #                    rxn_ids_I=[],
    #                    models_I = cobramodels,
    #                    solver_id_I = 'cglpk',
    #                    gr_check_I = 0.921935424379276,
    #                    diagnose_threshold_I=0.98,
    #                    diagnose_break_I=0.1)
    #for d in data: print(d)
    #data = simulatedData01.execute_testConstraintsCumulative(simulation_id_I=simulation,
    #                    rxn_ids_I=[],
    #                    models_I = cobramodels,
    #                    solver_id_I = 'cglpk',
    #                    gr_check_I = 0.921935424379276,
    #                    diagnose_threshold_I=0.98,
    #                    diagnose_break_I=0.1)
    #for d in data: print(d)
    ##fba
    #simulatedData01.execute_fba(simulation_id_I=simulation,
    #                    rxn_ids_I=[],
    #                    models_I = cobramodels,
    #                    method_I='fba',
    #                    allow_loops_I = True,
    #                    options_I = {},
    #                    solver_id_I='cglpk',
    #                    )
    ##fva
    #simulatedData01.execute_fva(simulation_id_I=simulation,
    #                rxn_ids_I=[],
    #                models_I = cobramodels,
    #                method_I='fva',
    #                allow_loops_I = True,
    #                    options_I = {},
    #                solver_id_I='cglpk',
    #                )
    ##sra
    #simulatedData01.execute_sra(simulation_id_I=simulation,
    #                    rxn_ids_I=[],
    #                    models_I = cobramodels,
    #                    method_I='fba',
    #                    options_I = {},
    #                    solver_id_I='cglpk',
    #                    )
    
data_dir = 'F:/Users/dmccloskey-sbrg/Dropbox (UCSD SBRG)/Phenomics_ALEsKOs01/sampling'

# import sampling results
for simulation in simulations:
    print('running simulation ' + simulation);
    #sampledData01.execute_sampling(simulation_id_I=simulation,
    #    rxn_ids_I=[],
    #    data_dir_I = data_dir,
    #    models_I = cobramodels
    #    )
    #sampledData01.reset_dataStage02_physiology_sampledData(
    #    tables_I = ['data_stage02_physiology_sampledPoints',
    #               'data_stage02_physiology_sampledData',
    #               'data_stage02_physiology_sampledMetaboliteData',
    #               'data_stage02_physiology_sampledSubsystemData',
    #               ],
    #    simulation_id_I = simulation,
    #    warn_I=False
    #);
    #sampledData01.execute_analyzeSamplingPoints(simulation_id_I=simulation,
    #    rxn_ids_I=[],
    #    data_dir_I = data_dir,
    #    models_I = cobramodels,
    #    points_overview_I=False,
    #    flux_stats_I=False,
    #    metabolite_stats_I=True,
    #    subsystem_stats_I=True,
    #    )
    #sampledData01.reset_dataStage02_physiology_sampledData(
    #    tables_I = [
    #               'data_stage02_physiology_sampledMetaboliteData',
    #               'data_stage02_physiology_sampledSubsystemData',
    #               ],
    #    simulation_id_I = simulation,
    #    warn_I=False
    #);
    #sampledData01.execute_analyzeSamplingMetabolitesAndSubsystemPoints(
    #    simulation_id_I=simulation,
    #    rxn_ids_I=[],
    #    data_dir_I = data_dir,
    #    models_I = cobramodels,
    #    metabolite_stats_I=True,
    #    subsystem_stats_I=True,
    #    )

#sampledData01.export_dataStage02PhysiologySampledPoints_js(
#    'ALEsKOs01_iDM2015_0_evo04_0_11_evo04gnd',
#        simulation_ids_I = ['ALEsKOs01_151026_iDM2015_full05_OxicEvo04gndEvo01EPEcoliGlc_11'],
#        rxn_ids_I = ['SUCDi'],
#        );
#sampledData01.export_dataStage02PhysiologySampledPointsDescriptiveStats_js(
#    #'ALEsKOs01_iDM2015_0_11_evo04',
#    'ALEsKOs01_iDM2015_0_evo04_0_11_evo04gnd',
#    plot_points_I=False,
#    vertical_I=True,
#    data_dir_I='tmp'
#    )
sampledData01.export_dataStage02PhysiologySampledPointsMetabolitesDescriptiveStats_js(
    #'ALEsKOs01_iDM2015_0_11_evo04',
    'ALEsKOs01_iDM2015_0_evo04_0_11_evo04gnd',
    plot_points_I=False,
    vertical_I=True,
    data_dir_I='tmp'
    )
sampledData01.export_dataStage02PhysiologySampledPointsSubsystemsDescriptiveStats_js(
    #'ALEsKOs01_iDM2015_0_11_evo04',
    'ALEsKOs01_iDM2015_0_evo04_0_11_evo04gnd',
    plot_points_I=False,
    vertical_I=True,
    data_dir_I='tmp'
    )

#make the pairWiseTest Table
from SBaaS_COBRA.stage02_physiology_pairWiseTest_execute import stage02_physiology_pairWiseTest_execute
pairWiseTest01 = stage02_physiology_pairWiseTest_execute(session,engine,pg_settings.datadir_settings)
pairWiseTest01.initialize_supportedTables(); 
pairWiseTest01.initialize_tables();

analysis_ids = [
        'ALEsKOs01_iDM2015_0_11_evo04'
        ]

#for analysis_id in analysis_ids:
#    print("running analysis_id " + analysis_id);
#    pairWiseTest01.reset_dataStage02_physiology_pairWiseTest(
#            tables_I = ['data_stage02_physiology_pairWiseTest',
#                        'data_stage02_physiology_pairWiseTestMetabolites',
#                        'data_stage02_physiology_pairWiseTestSubsystems',
#            ],
#            analysis_id_I = analysis_id,
#            warn_I=True
#            )
#    pairWiseTest01.execute_samplingPairWiseTests(
#        analysis_id_I = analysis_id,
#        rxn_ids_I=[],
#        control_I=False,
#        redundancy_I=False,
#        remove_loops_I=False,
#        remove_no_flux_I=True,
#        normalize_I=False,
#        compare_metabolitePoints_I=True,
#        compare_subsystemPoints_I=True,
#        data_dir_I = data_dir,
#        models_I = cobramodels,
#    )

#pairWiseTest01.export_dataStage02PhysiologyPairWiseTest_js('ALEsKOs01_iDM2015_0_11_evo04')
#pairWiseTest01.export_dataStage02PhysiologyPairWiseTestMetabolites_js('ALEsKOs01_iDM2015_0_11_evo04')
#pairWiseTest01.export_dataStage02PhysiologyPairWiseTestSubsystems_js('ALEsKOs01_iDM2015_0_11_evo04')