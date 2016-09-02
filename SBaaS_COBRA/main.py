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

#make the pairWiseTest Table
from SBaaS_COBRA.stage02_physiology_graphData_execute import stage02_physiology_graphData_execute
graphData01 = stage02_physiology_graphData_execute(session,engine,pg_settings.datadir_settings)
graphData01.initialize_supportedTables(); 
graphData01.initialize_tables();

analysis_ids = [
        'ALEsKOs01_iDM2015_0_11_evo04'
        ]
# generate the exclusion list of non-carbon and cofactor metabolites
exclusion_noC_str = '2fe1s,2fe2s,3fe4s,4fe4s,ag,apoACP,aso3,aso4,tsul,\
dsbdox,dsbdrd,fe2,fe3,flxr,flxso,grxox,grxrd,h,h2,h2o,h2o2,h2s,hg2,iscs,\
iscssh,iscu,iscu_DASH_2fe2s,iscu_DASH_2fe2s2,iscu_DASH_4fe4s,k,mg2,mn2,mobd,\
n2o,na1,nh4,ni2,no,no2,no3,o2,o2s,pi,ppi,pppi,sel,seln,selnp,slnt,so2,so3,\
so4,sufbcd,sufbcd_DASH_2fe2s,sufbcd_DASH_2fe2s2,sufbcd_DASH_4fe4s,sufse,\
sufsesh,trdox,trdrd,trnaala,trnaarg,trnaasp,trnacys,trnagln,trnaglu,trnagly,\
trnahis,trnaile,trnaleu,trnalys,trnamet,trnaphe,trnapro,trnasecys,trnaser,\
trnathr,trnatrp,trnatyr,trnaval,tungs,zn2,ppt,alpp,dsbaox,dsbard,dsbcox,dsbcrd,\
dsbgox,dsbgrd'
exclusion_noC = exclusion_noC_str.split(',');
exclusion_other = ['co2','co']
exclusion_cofactors = [
        #'nad','nadh','nadp','nadph',
        #'atp','adp','amp','gtp','gdp','gmp',
        #'utp','udp','ump','ctp','cdp','cmp',
        #'itp','idp','imp',
        #'fad','fadh','fadh2',
        #'coa',
        #'glu_DASH_L','gln_DASH_L','akg',
        'mql8','mql8h2','2dmmql8','2dmmql8h2','q8','q8h2',
        'thf',
        'ACP'
        ]
exclusion_mets = [];
exclusion_mets.extend(exclusion_noC)
exclusion_mets.extend(exclusion_cofactors)
exclusion_mets.extend(exclusion_other)
exclusion_list = ['F6PA'];
# define other inputs
nodes_startAndStop = [
    ['g6p_c','icit_c'],
    ['g6p_c','r5p_c'],
    ['g6p_c','gthrd_c'],
    ];
algorithms_params = [
    {'algorithm':'all_shortest_paths','params':{'weight':'weight'}},
    {'algorithm':'all_simple_paths','params':{'cutoff':25}},
    {'algorithm':'astar_path','params':{'weight':'weight'}},
                     ];
for met in exclusion_mets:
    exclusion_list.append(met+'_c')
    exclusion_list.append(met+'_p')
    exclusion_list.append(met+'_e')
#for analysis_id in analysis_ids:
#    print("running analysis_id " + analysis_id);
#    graphData01.reset_dataStage02_physiology_graphData(
#            tables_I = ['data_stage02_physiology_graphData_shortestPathStats',
#                        'data_stage02_physiology_graphData_shortestPaths',
#            ],
#            analysis_id_I = analysis_id,
#            warn_I=False
#            )
#    graphData01.execute_findShortestPaths(
#            analysis_id_I = analysis_id,
#            algorithms_params_I = algorithms_params,
#            nodes_startAndStop_I = nodes_startAndStop,
#            exclusion_list_I = exclusion_list,
#            weights_I='stage02_physiology_sampledData_query'
#    )

analysis_ids = [
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
nodes_startAndStop = {
'ALEsKOs01_151026_iDM2015_full05_OxicEvo04gndEcoliGlc_0':{'nodes_start':['6pgc_c','ru5p_DASH_D_c'],'analysis_id':'ALEsKOs01_0_evo04_0_11_evo04gnd','sample_name_abbreviation_2':'OxicEvo04gndEcoliGlc','sample_name_abbreviation_1':'OxicEvo04EcoliGlc'},
'ALEsKOs01_151026_iDM2015_full05_OxicEvo04gndEvo01EPEcoliGlc_11':{'nodes_start':['6pgc_c','ru5p_DASH_D_c'],'analysis_id':'ALEsKOs01_0_11_evo04gnd','sample_name_abbreviation_2':'OxicEvo04gndEvo01EPEcoliGlc','sample_name_abbreviation_1':'OxicEvo04gndEcoliGlc'},
'ALEsKOs01_151026_iDM2015_full05_OxicEvo04gndEvo02EPEcoliGlc_11':{'nodes_start':['6pgc_c','ru5p_DASH_D_c'],'analysis_id':'ALEsKOs01_0_11_evo04gnd','sample_name_abbreviation_2':'OxicEvo04gndEvo02EPEcoliGlc','sample_name_abbreviation_1':'OxicEvo04gndEcoliGlc'},
'ALEsKOs01_151026_iDM2015_full05_OxicEvo04gndEvo03EPEcoliGlc_11':{'nodes_start':['6pgc_c','ru5p_DASH_D_c'],'analysis_id':'ALEsKOs01_0_11_evo04gnd','sample_name_abbreviation_2':'OxicEvo04gndEvo03EPEcoliGlc','sample_name_abbreviation_1':'OxicEvo04gndEcoliGlc'},
'ALEsKOs01_151026_iDM2015_full05_OxicEvo04pgiEcoliGlc_0':{'nodes_start':['g6p_c','f6p_c'],'analysis_id':'ALEsKOs01_0_evo04_0_11_evo04pgi','sample_name_abbreviation_2':'OxicEvo04pgiEcoliGlc','sample_name_abbreviation_1':'OxicEvo04EcoliGlc'},
'ALEsKOs01_151026_iDM2015_full05_OxicEvo04pgiEvo01EPEcoliGlc_11':{'nodes_start':['g6p_c','f6p_c'],'analysis_id':'ALEsKOs01_0_11_evo04pgi','sample_name_abbreviation_2':'OxicEvo04pgiEvo01EPEcoliGlc','sample_name_abbreviation_1':'OxicEvo04pgiEcoliGlc'},
'ALEsKOs01_151026_iDM2015_full05_OxicEvo04pgiEvo02EPEcoliGlc_11':{'nodes_start':['g6p_c','f6p_c'],'analysis_id':'ALEsKOs01_0_11_evo04pgi','sample_name_abbreviation_2':'OxicEvo04pgiEvo02EPEcoliGlc','sample_name_abbreviation_1':'OxicEvo04pgiEcoliGlc'},
'ALEsKOs01_151026_iDM2015_full05_OxicEvo04pgiEvo03EPEcoliGlc_11':{'nodes_start':['g6p_c','f6p_c'],'analysis_id':'ALEsKOs01_0_11_evo04pgi','sample_name_abbreviation_2':'OxicEvo04pgiEvo03EPEcoliGlc','sample_name_abbreviation_1':'OxicEvo04pgiEcoliGlc'},
'ALEsKOs01_151026_iDM2015_full05_OxicEvo04pgiEvo04EPEcoliGlc_11':{'nodes_start':['g6p_c','f6p_c'],'analysis_id':'ALEsKOs01_0_11_evo04pgi','sample_name_abbreviation_2':'OxicEvo04pgiEvo04EPEcoliGlc','sample_name_abbreviation_1':'OxicEvo04pgiEcoliGlc'},
'ALEsKOs01_151026_iDM2015_full05_OxicEvo04pgiEvo05EPEcoliGlc_11':{'nodes_start':['g6p_c','f6p_c'],'analysis_id':'ALEsKOs01_0_11_evo04pgi','sample_name_abbreviation_2':'OxicEvo04pgiEvo05EPEcoliGlc','sample_name_abbreviation_1':'OxicEvo04pgiEcoliGlc'},
'ALEsKOs01_151026_iDM2015_full05_OxicEvo04pgiEvo06EPEcoliGlc_11':{'nodes_start':['g6p_c','f6p_c'],'analysis_id':'ALEsKOs01_0_11_evo04pgi','sample_name_abbreviation_2':'OxicEvo04pgiEvo06EPEcoliGlc','sample_name_abbreviation_1':'OxicEvo04pgiEcoliGlc'},
'ALEsKOs01_151026_iDM2015_full05_OxicEvo04pgiEvo07EPEcoliGlc_11':{'nodes_start':['g6p_c','f6p_c'],'analysis_id':'ALEsKOs01_0_11_evo04pgi','sample_name_abbreviation_2':'OxicEvo04pgiEvo07EPEcoliGlc','sample_name_abbreviation_1':'OxicEvo04pgiEcoliGlc'},
'ALEsKOs01_151026_iDM2015_full05_OxicEvo04pgiEvo08EPEcoliGlc_11':{'nodes_start':['g6p_c','f6p_c'],'analysis_id':'ALEsKOs01_0_11_evo04pgi','sample_name_abbreviation_2':'OxicEvo04pgiEvo08EPEcoliGlc','sample_name_abbreviation_1':'OxicEvo04pgiEcoliGlc'},
'ALEsKOs01_151026_iDM2015_full05_OxicEvo04ptsHIcrrEcoliGlc_0':{'nodes_start':['pep_c','pyr_c'],'analysis_id':'ALEsKOs01_0_evo04_0_11_evo04ptsHIcrr','sample_name_abbreviation_2':'OxicEvo04ptsHIcrrEcoliGlc','sample_name_abbreviation_1':'OxicEvo04EcoliGlc'},
'ALEsKOs01_151026_iDM2015_full05_OxicEvo04ptsHIcrrEvo01EPEcoliGlc_11':{'nodes_start':['pep_c','pyr_c'],'analysis_id':'ALEsKOs01_0_11_evo04ptsHIcrr','sample_name_abbreviation_2':'OxicEvo04ptsHIcrrEvo01EPEcoliGlc','sample_name_abbreviation_1':'OxicEvo04ptsHIcrrEcoliGlc'},
'ALEsKOs01_151026_iDM2015_full05_OxicEvo04ptsHIcrrEvo02EPEcoliGlc_11':{'nodes_start':['pep_c','pyr_c'],'analysis_id':'ALEsKOs01_0_11_evo04ptsHIcrr','sample_name_abbreviation_2':'OxicEvo04ptsHIcrrEvo02EPEcoliGlc','sample_name_abbreviation_1':'OxicEvo04ptsHIcrrEcoliGlc'},
'ALEsKOs01_151026_iDM2015_full05_OxicEvo04ptsHIcrrEvo03EPEcoliGlc_11':{'nodes_start':['pep_c','pyr_c'],'analysis_id':'ALEsKOs01_0_11_evo04ptsHIcrr','sample_name_abbreviation_2':'OxicEvo04ptsHIcrrEvo03EPEcoliGlc','sample_name_abbreviation_1':'OxicEvo04ptsHIcrrEcoliGlc'},
'ALEsKOs01_151026_iDM2015_full05_OxicEvo04ptsHIcrrEvo04EPEcoliGlc_11':{'nodes_start':['pep_c','pyr_c'],'analysis_id':'ALEsKOs01_0_11_evo04ptsHIcrr','sample_name_abbreviation_2':'OxicEvo04ptsHIcrrEvo04EPEcoliGlc','sample_name_abbreviation_1':'OxicEvo04ptsHIcrrEcoliGlc'},
'ALEsKOs01_151026_iDM2015_full05_OxicEvo04sdhCBEcoliGlc_0':{'nodes_start':['succ_c','fum_c'],'analysis_id':'ALEsKOs01_0_evo04_0_11_evo04sdhCB','sample_name_abbreviation_2':'OxicEvo04sdhCBEcoliGlc','sample_name_abbreviation_1':'OxicEvo04EcoliGlc'},
'ALEsKOs01_151026_iDM2015_full05_OxicEvo04sdhCBEvo01EPEcoliGlc_11':{'nodes_start':['succ_c','fum_c'],'analysis_id':'ALEsKOs01_0_11_evo04sdhCB','sample_name_abbreviation_2':'OxicEvo04sdhCBEvo01EPEcoliGlc','sample_name_abbreviation_1':'OxicEvo04sdhCBEcoliGlc'},
'ALEsKOs01_151026_iDM2015_full05_OxicEvo04sdhCBEvo02EPEcoliGlc_11':{'nodes_start':['succ_c','fum_c'],'analysis_id':'ALEsKOs01_0_11_evo04sdhCB','sample_name_abbreviation_2':'OxicEvo04sdhCBEvo02EPEcoliGlc','sample_name_abbreviation_1':'OxicEvo04sdhCBEcoliGlc'},
'ALEsKOs01_151026_iDM2015_full05_OxicEvo04sdhCBEvo03EPEcoliGlc_11':{'nodes_start':['succ_c','fum_c'],'analysis_id':'ALEsKOs01_0_11_evo04sdhCB','sample_name_abbreviation_2':'OxicEvo04sdhCBEvo03EPEcoliGlc','sample_name_abbreviation_1':'OxicEvo04sdhCBEcoliGlc'},
'ALEsKOs01_151026_iDM2015_full05_OxicEvo04tpiAEcoliGlc_0':{'nodes_start':['dhap_c','g3p_c'],'analysis_id':'ALEsKOs01_0_evo04_0_11_evo04tpiA','sample_name_abbreviation_2':'OxicEvo04tpiAEcoliGlc','sample_name_abbreviation_1':'OxicEvo04EcoliGlc'},
'ALEsKOs01_151026_iDM2015_full05_OxicEvo04tpiAEvo01EPEcoliGlc_11':{'nodes_start':['dhap_c','g3p_c'],'analysis_id':'ALEsKOs01_0_11_evo04tpiA','sample_name_abbreviation_2':'OxicEvo04tpiAEvo01EPEcoliGlc','sample_name_abbreviation_1':'OxicEvo04tpiAEvo01EPEcoliGlc'},
'ALEsKOs01_151026_iDM2015_full05_OxicEvo04tpiAEvo02EPEcoliGlc_11':{'nodes_start':['dhap_c','g3p_c'],'analysis_id':'ALEsKOs01_0_11_evo04tpiA','sample_name_abbreviation_2':'OxicEvo04tpiAEvo02EPEcoliGlc','sample_name_abbreviation_1':'OxicEvo04tpiAEvo01EPEcoliGlc'},
'ALEsKOs01_151026_iDM2015_full05_OxicEvo04tpiAEvo03EPEcoliGlc_11':{'nodes_start':['dhap_c','g3p_c'],'analysis_id':'ALEsKOs01_0_11_evo04tpiA','sample_name_abbreviation_2':'OxicEvo04tpiAEvo03EPEcoliGlc','sample_name_abbreviation_1':'OxicEvo04tpiAEvo01EPEcoliGlc'},
'ALEsKOs01_151026_iDM2015_full05_OxicEvo04tpiAEvo04EPEcoliGlc_11':{'nodes_start':['dhap_c','g3p_c'],'analysis_id':'ALEsKOs01_0_11_evo04tpiA','sample_name_abbreviation_2':'OxicEvo04tpiAEvo04EPEcoliGlc','sample_name_abbreviation_1':'OxicEvo04tpiAEvo01EPEcoliGlc'},
    
}
#metabolites not in the model
mets_ignore = []
from SBaaS_models.models_COBRA_dependencies import models_COBRA_dependencies
COBRA_dependencies = models_COBRA_dependencies();

#for analysis_id in analysis_ids:
#    print("running analysis_id " + analysis_id);
#    graphData01.reset_dataStage02_physiology_graphData(
#        tables_I = ['data_stage02_physiology_graphData_shortestPathStats',
#                    'data_stage02_physiology_graphData_shortestPaths',
#        ],
#        analysis_id_I = analysis_id,
#        warn_I=False
#        )
#    #query the stop nodes
#    cmd = 'SELECT component_group_name '
#    cmd += 'FROM "data_stage02_quantification_pairWiseTest" '
#    cmd += "WHERE analysis_id LIKE '%s' " %(nodes_startAndStop[analysis_id]['analysis_id'])
#    cmd += "AND sample_name_abbreviation_1 LIKE '%s' " %(nodes_startAndStop[analysis_id]['sample_name_abbreviation_1'])
#    cmd += "AND sample_name_abbreviation_2 LIKE '%s' " %(nodes_startAndStop[analysis_id]['sample_name_abbreviation_2'])
#    cmd += 'AND used_ AND pvalue_corrected < 0.01 '
#    cmd += 'AND (fold_change > 2.0 OR fold_change < 0.5) '
#    cmd += 'GROUP BY component_group_name '
#    cmd += 'ORDER BY component_group_name ASC;'
#    try:
#        ans = session.execute(cmd);
#        data = ans.fetchall();
#    except Exception as e:
#        print(e);
#        session.rollback();
#    #parse the names
#    nodes_stop = [COBRA_dependencies.format_metid(d.component_group_name,"c") for d in data]; 
#    #generate the nodes_startAndStop_list
#    nodes_startAndStop_list = [];
#    for node_start in nodes_startAndStop[analysis_id]['nodes_start']:
#        for node_stop in nodes_stop:
#            node_stop.replace('23dpg_c','13dpg_c')
#            node_stop.replace('Pool_2pg_3pg_c','3pg_c')
#            if node_start == node_stop:
#                continue;
#            if node_stop in mets_ignore:
#                continue;
#            nodes_startAndStop_list.append([node_start,node_stop])
#    for node_start in nodes_stop:
#        node_start.replace('23dpg_c','13dpg_c')
#        node_start.replace('Pool_2pg_3pg_c','3pg_c')
#        if node_start in mets_ignore:
#            continue;
#        for node_stop in nodes_startAndStop[analysis_id]['nodes_start']:
#            if node_start == node_stop:
#                continue;
#            nodes_startAndStop_list.append([node_start,node_stop])
#    # calculate the shortest paths
#    graphData01.execute_findShortestPaths(
#        analysis_id_I = analysis_id,
#        algorithms_params_I = algorithms_params,
#        nodes_startAndStop_I = nodes_startAndStop_list,
#        exclusion_list_I = exclusion_list,
#        weights_I='stage02_physiology_sampledData_query'
#    )

graphData01.export_dataStage02PhysiologyGraphDataShortestPathStats_js('ALEsKOs01_151026_iDM2015_full05_OxicEvo04gndEvo01EPEcoliGlc_11')