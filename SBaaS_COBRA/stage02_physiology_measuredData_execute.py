#SBaaS
from .stage02_physiology_measuredData_io import stage02_physiology_measuredData_io
from .stage02_physiology_simulation_query import stage02_physiology_simulation_query
from SBaaS_physiology.stage01_physiology_rates_query import stage01_physiology_rates_query
from SBaaS_MFA.stage02_isotopomer_fittedNetFluxes_query import stage02_isotopomer_fittedNetFluxes_query
from SBaaS_models.models_COBRA_dependencies import models_COBRA_dependencies
# Resources
import copy
from math import sqrt

class stage02_physiology_measuredData_execute(stage02_physiology_measuredData_io,
                                                  stage02_physiology_simulation_query,
                                                      stage01_physiology_rates_query):

    def execute_makeFluxomicsData(self,IDsQuantification2SimulationIDsIsotopomer_I = {},
                                  criteria_I = 'flux_lb/flux_ub',
                                  flip_rxn_direction_I=[]):
        '''Collect estimated flux data from data_stage02_istopomer_fittedNetFluxes for thermodynamic simulation
        INPUT:
        IDsQuantification2SimulationIDsIsotopomer_I = {'simulation_id':{'experiment_id':..., (quant id)
                                                                        'sample_name_abbreviation':..., (quant id)
                                                                        'model_id':..., (quant id)
                                                                        'time_point':..., (quant id)
                                                                        'flux_units':..., (isotopomer id)
                                                                        'simulation_dateAndTime':..., (isotopomer id)
                                                                        },
                                                              ...}
        criteria_I = string, if 'flux_lb/flux_ub', the lower/upper bounds will be used
                             if 'flux_mean/flux_stdev', the lower/upper bounds will be replaced by mean +/- stdev
                             if 'least_constraining', the lowest/highest value for the lower/upper bounds will be used
                                                        i.e., of either the flux_lb or flux_mean-flux_stdev/flux_ub or flux_mean+stdev
                             if 'most_constraining', the highest/lowest value for the lower/upper bounds will be used
        INPUT not yet implemented:
        flip_rxn_direction_I = list of reaction_ids to flip the direction of flux
        '''

        isotopomer_fittedNetFluxes_query=stage02_isotopomer_fittedNetFluxes_query(self.session,self.engine,self.settings)

        data_O = [];
        for simulation_id in list(IDsQuantification2SimulationIDsIsotopomer_I.keys()): 
            # get the fittedNetFluxes
            fittedNetFluxes = [];
            #simulation_dateAndTime = self.convert_string2datetime(IDsQuantification2SimulationIDsIsotopomer_I[simulation_id]['simulation_dateAndTime'])
            #fittedNetFluxes = isotopomer_fittedNetFluxes_query.get_rows_simulationIDAndSimulationDateAndTimeAndFluxUnits_dataStage02IsotopomerfittedNetFluxes(simulation_id,
            #    simulation_dateAndTime,
            #    IDsQuantification2SimulationIDsIsotopomer_I[simulation_id]['flux_units']);
            fittedNetFluxes = isotopomer_fittedNetFluxes_query.get_rows_simulationIDAndFluxUnits_dataStage02IsotopomerfittedNetFluxes(simulation_id,
                IDsQuantification2SimulationIDsIsotopomer_I[simulation_id]['flux_units']);
            if fittedNetFluxes:
                for d in fittedNetFluxes:
                    # change the direction
                    if d['rxn_id'] in flip_rxn_direction_I:
                        rate_tmp,rate_lb_tmp,rate_ub_tmp = d['flux'],d['flux_lb'],d['flux_ub'];
                        #TODO:
                        #d['flux_lb'] = -max([abs(x) for x in [rate_lb_tmp,rate_ub_tmp]]);
                        #d['flux_ub'] = -min([abs(x) for x in [rate_lb_tmp,rate_ub_tmp]]);
                    if criteria_I == 'flux_mean/flux_stdev':
                        d['flux_lb']=d['flux']-d['flux_stdev']
                        d['flux_ub']=d['flux']+d['flux_stdev']
                    elif criteria_I == 'least_constraining':
                        lb=d['flux']-d['flux_stdev']
                        ub=d['flux']+d['flux_stdev']
                        if lb<d['flux_lb']:d['flux_lb']=lb
                        if ub>d['flux_ub']:d['flux_ub']=ub
                    elif criteria_I == 'most_constraining':
                        lb=d['flux']-d['flux_stdev']
                        ub=d['flux']+d['flux_stdev']
                        if lb>d['flux_lb']:d['flux_lb']=lb
                        if ub<d['flux_ub']:d['flux_ub']=ub
                    tmp = {'experiment_id':IDsQuantification2SimulationIDsIsotopomer_I[simulation_id]['experiment_id'],
                        'model_id':IDsQuantification2SimulationIDsIsotopomer_I[simulation_id]['model_id'],
                        'sample_name_abbreviation':IDsQuantification2SimulationIDsIsotopomer_I[simulation_id]['sample_name_abbreviation'],
                        #'time_point':IDsQuantification2SimulationIDsIsotopomer_I[simulation_id]['time_point'],
                        'rxn_id':d['rxn_id'],
                        'flux_average':d['flux'],
                        'flux_stdev':d['flux_stdev'],
                        'flux_lb':d['flux_lb'],
                        'flux_ub':d['flux_ub'],
                        'flux_units':d['flux_units'],
                        'used_':d['used_'],
                        'comment_':d['comment_']}
                    data_O.append(tmp);
        # add data to the database
        self.add_dataStage02PhysiologyMeasuredFluxes(data_O);
    def execute_addMeasuredFluxes(self,
            experiment_id_I, ko_list={}, flux_dict={}, model_ids_I=[], sample_name_abbreviations_I=[],time_points_I=[]):
        '''Add flux data for physiological simulation'''
        #Input:
            #flux_dict = {};
            #flux_dict['iJO1366'] = {};
            #flux_dict['iJO1366'] = {};
            #flux_dict['iJO1366']['sna'] = {};
            #flux_dict['iJO1366']['sna']['tp'] = {};
            #flux_dict['iJO1366']['sna']['tp']['Ec_biomass_iJO1366_WT_53p95M'] = {'ave':None,'stdev':None,'units':'mmol*gDCW-1*hr-1','lb':0.704*0.9,'ub':0.704*1.1};
            #flux_dict['iJO1366']['sna']['tp']['EX_ac_LPAREN_e_RPAREN_'] = {'ave':None,'stdev':None,'units':'mmol*gDCW-1*hr-1','lb':2.13*0.9,'ub':2.13*1.1};
            #flux_dict['iJO1366']['sna']['tp']['EX_o2_LPAREN_e_RPAREN__reverse'] = {'ave':None,'units':'mmol*gDCW-1*hr-1','stdev':None,'lb':0,'ub':16};
            #flux_dict['iJO1366']['sna']['tp']['EX_glc_LPAREN_e_RPAREN_'] = {'ave':None,'stdev':None,'units':'mmol*gDCW-1*hr-1','lb':-7.4*1.1,'ub':-7.4*0.9};

        data_O = [];
        # get the model ids:
        if model_ids_I:
            model_ids = model_ids_I;
        else:
            model_ids = [];
            model_ids = self.get_modelID_experimentID_dataStage02PhysiologySimulation(experiment_id_I);
        for model_id in model_ids:
            # get sample names and sample name abbreviations
            if sample_name_abbreviations_I:
                sample_name_abbreviations = sample_name_abbreviations_I;
            else:
                sample_name_abbreviations = [];
                sample_name_abbreviations = self.get_sampleNameAbbreviations_experimentIDAndModelID_dataStage02PhysiologySimulation(experiment_id_I,model_id);
            for sna_cnt,sna in enumerate(sample_name_abbreviations):
                print('Adding experimental fluxes for sample name abbreviation ' + sna);
                if time_points_I:
                    time_points = time_points_I;
                else:
                    time_points = [];
                    time_points = self.get_timePoints_experimentIDAndModelIDAndSampleNameAbbreviation_dataStage02PhysiologySimulation(experiment_id_I,model_id,sna)
                for tp in time_points:
                    if flux_dict:
                        for k,v in flux_dict[model_id][sna][tp].items():
                            # record the data
                            data_tmp = {'experiment_id':experiment_id_I,
                                    'model_id':model_id,
                                    'sample_name_abbreviation':sna,
                                    'time_point':tp,
                                    'rxn_id':k,
                                    'flux_average':v['ave'],
                                    'flux_stdev':v['stdev'],
                                    'flux_lb':v['lb'], 
                                    'flux_ub':v['ub'],
                                    'flux_units':v['units'],
                                    'used_':True,
                                    'comment_':None}
                            data_O.append(data_tmp);
                    if ko_list:
                        for k in ko_list[model_id][sna][tp]:
                            # record the data
                            data_tmp = {'experiment_id':experiment_id_I,
                                    'model_id':model_id,
                                    'sample_name_abbreviation':sna,
                                    'time_point':tp,
                                    'rxn_id':k,
                                    'flux_average':0.0,
                                    'flux_stdev':0.0,
                                    'flux_lb':0.0, 
                                    'flux_ub':0.0,
                                    'flux_units':'mmol*gDCW-1*hr-1',
                                    'used_':True,
                                    'comment_':None}
                            data_O.append(data_tmp);
        #add data to the database:
        self.add_dataStage02PhysiologyMeasuredFluxes(data_O);
    def execute_makeMeasuredFluxes(self,
            experiment_id_I,
            metID2RxnID_I = {},
            sample_name_abbreviations_I = [],
            met_ids_I = [],
            correct_EX_glc_LPAREN_e_RPAREN_I = True
            ):
        '''Collect and flux data from data_stage01_physiology_ratesAverages for physiological simulation
        INPUT:
        metID2RxnID_I = e.g. {'glc-D':{'model_id':'140407_iDM2014','rxn_id':'EX_glc_LPAREN_e_RPAREN_'},
                                {'ac':{'model_id':'140407_iDM2014','rxn_id':'EX_ac_LPAREN_e_RPAREN_'},
                                {'succ':{'model_id':'140407_iDM2014','rxn_id':'EX_succ_LPAREN_e_RPAREN_'},
                                {'lac-L':{'model_id':'140407_iDM2014','rxn_id':'EX_lac_DASH_L_LPAREN_e_RPAREN_'},
                                {'biomass':{'model_id':'140407_iDM2014','rxn_id':'Ec_biomass_iJO1366_WT_53p95M'}};
        correct_EX_glc_LPAREN_e_RPAREN_I = boolean, if True, the direction of glucose input will be reversed
                                '''

        data_O = [];
        # get sample names and sample name abbreviations
        if sample_name_abbreviations_I:
            sample_name_abbreviations = sample_name_abbreviations_I;
        else:
            sample_name_abbreviations = [];
            sample_name_abbreviations = self.get_sampleNameAbbreviations_experimentID_dataStage02PhysiologySimulation(experiment_id_I);
        for sna in sample_name_abbreviations:
            print('Collecting experimental fluxes for sample name abbreviation ' + sna);
            # get met_ids
            if not met_ids_I:
                met_ids = [];
                met_ids = self.get_metID_experimentIDAndSampleNameAbbreviation_dataStage01PhysiologyRatesAverages(experiment_id_I,sna);
            else:
                met_ids = met_ids_I;
            if not(met_ids): continue #no component information was found
            for met in met_ids:
                print('Collecting experimental fluxes for metabolite ' + met);
                # get rateData
                slope_average, intercept_average, rate_average, rate_lb, rate_ub, rate_units, rate_var = None,None,None,None,None,None,None;
                slope_average, intercept_average, rate_average, rate_lb, rate_ub, rate_units, rate_var = self.get_rateData_experimentIDAndSampleNameAbbreviationAndMetID_dataStage01PhysiologyRatesAverages(experiment_id_I,sna,met);
                rate_stdev = sqrt(rate_var);
                # check that the metID2RxnID_I mapping is provided
                if not met in metID2RxnID_I.keys():
                    print('no metID2RxnID mapping provided for metabolite ' + met);
                    continue;
                model_id = metID2RxnID_I[met]['model_id'];
                rxn_id = metID2RxnID_I[met]['rxn_id'];
                # correct for glucose uptake
                if rxn_id == 'EX_glc_LPAREN_e_RPAREN_' and correct_EX_glc_LPAREN_e_RPAREN_I:
                    rate_lb_tmp,rate_ub_tmp = rate_lb,rate_ub;
                    rate_lb = min([abs(x) for x in [rate_lb_tmp,rate_ub_tmp]]);
                    rate_ub = max([abs(x) for x in [rate_lb_tmp,rate_ub_tmp]]);
                    rate_average = abs(rate_average);
                # record the data
                data_tmp = {'experiment_id':experiment_id_I,
                        'model_id':model_id,
                        'sample_name_abbreviation':sna,
                        'rxn_id':rxn_id,
                        'flux_average':rate_average,
                        'flux_stdev':rate_stdev,
                        'flux_lb':rate_lb, 
                        'flux_ub':rate_ub,
                        'flux_units':rate_units,
                        'used_':True,
                        'comment_':None}
                data_O.append(data_tmp);
                ##add data to the database
                #row = [];
                #row = data_stage02_physiology_measuredFluxes(
                #    experiment_id_I,
                #    model_id,
                #    sna,
                #    rxn_id,
                #    rate_average,
                #    rate_stdev,
                #    rate_lb, 
                #    rate_ub,
                #    rate_units,
                #    True,
                #    None);
                #self.session.add(row);
        #add data to the database:
        self.add_dataStage02PhysiologyMeasuredFluxes(data_O);
        #self.session.commit();
    def execute_testMeasuredFluxes(self,experiment_id_I, models_I, ko_list_I={}, flux_dict_I={}, model_ids_I=[], sample_name_abbreviations_I=[],time_points_I=[],
                                   adjustment_1_I=True,adjustment_2_I=True,diagnose_I=False,
                                   update_measuredFluxes_I=False):
        '''Test each model constrained to the measure fluxes'''
        
        cobradependencies = models_COBRA_dependencies();
        diagnose_variables_O = {};
        flux_dict_O = [];
        test_O = [];
        # get the model ids:
        if model_ids_I:
            model_ids = model_ids_I;
        else:
            model_ids = [];
            model_ids = self.get_modelID_experimentID_dataStage02PhysiologySimulation(experiment_id_I);
        for model_id in model_ids:
            diagnose_variables_O[model_id] = {};
            cobra_model_base = models_I[model_id];
            print('testing model ' + model_id);
            # get sample names and sample name abbreviations
            if sample_name_abbreviations_I:
                sample_name_abbreviations = sample_name_abbreviations_I;
            else:
                sample_name_abbreviations = [];
                sample_name_abbreviations = self.get_sampleNameAbbreviations_experimentIDAndModelID_dataStage02PhysiologySimulation(experiment_id_I,model_id);
            for sna_cnt,sna in enumerate(sample_name_abbreviations):
                diagnose_variables_O[model_id][sna] = {};
                print('testing sample_name_abbreviation ' + sna);
                # get the time_points
                if time_points_I:
                    time_points = time_points_I;
                else:
                    time_points = [];
                    time_points = self.get_timePoints_experimentIDAndModelIDAndSampleNameAbbreviation_dataStage02PhysiologySimulation(experiment_id_I,model_id,sna)
                for tp in time_points:
                    diagnose_variables_O[model_id][sna][tp] = {'bad_lbub_1':None,'bad_lbub_2':None};
                    print('testing time_point ' + tp);
                    # get the flux data
                    if flux_dict_I:
                        flux_dict = flux_dict_I
                    else:
                        flux_dict = {};
                        flux_dict = self.get_fluxDict_experimentIDAndModelIDAndSampleNameAbbreviationsAndTimePoint_dataStage03QuantificationMeasuredFluxes(experiment_id_I,model_id,sna,tp);
                    # get the ko list
                    if ko_list_I:
                        ko_list = ko_list_I;
                    else:
                        ko_list = [];
                    # copy the cobra_model
                    cobra_model = cobra_model_base.copy();
                    # check each flux bounds
                    if diagnose_I:
                        # record the variables
                        summary_O = cobradependencies.diagnose_modelLBAndUB(cobra_model,ko_list,flux_dict,
                              adjustment_1_I=adjustment_1_I,adjustment_2_I=adjustment_2_I)
                        diagnose_variables_O[model_id][sna][tp]=summary_O;
                        diagnose_variables_O[model_id][sna][tp]['flux_dict']=flux_dict;
                        for rxn_id,d in list(flux_dict.items()):
                            #if rxn_id in summary_O['bad_lbub_1'] or rxn_id in summary_O['bad_lbub_2']:
                            #    comment_ = 'adjusted';
                            #else:
                            #    comment_ = None;
                            tmp = {'experiment_id':experiment_id_I,
                                'model_id':model_id,
                                'sample_name_abbreviation':sna,
                                'time_point':tp,
                                'rxn_id':rxn_id,
                                'flux_average':d['flux'],
                                'flux_stdev':d['stdev'],
                                'flux_lb':d['lb'],
                                'flux_ub':d['ub'],
                                'flux_units':d['units'],
                                'used_':d['used_'],
                                'comment_':d['comment_']}
                            flux_dict_O.append(tmp);
                    else:
                        # test and constrain each model
                        test = False;
                        test = cobradependencies.test_model(cobra_model_I=cobra_model,ko_list=ko_list,flux_dict=flux_dict,description=None);
                        test_O.append(test);
        if diagnose_I and update_measuredFluxes_I:
            #update measuredFluxes
            self.update_unique_dataStage03QuantificationMeasuredFluxes(flux_dict_O);
            return diagnose_variables_O;
        elif diagnose_I:
            return diagnose_variables_O;
        else: 
            return test_O;

    

    def execute_measuredCoverage(
        self,
        model_id_I,
        experiment_ids_I,
        sample_name_abbreviations_I,
        genes_I = [],
        transcripts_I = [],
        proteins_I = [],
        fluxes_I = [],
        metabolites_I = []):
        '''Calculate the model coverage for 
        A. genes from DNAreseq data that map to
            1. model genes and 2. model reactions
        B. transcripts from RNAseq data that map to
            1. model genes and 2. model reactions
        C. metabolites from quantification data that map to 
            1. model metabolites and 2. model reactions
        D. fluxes from MFA data that map to
            1. model reactions

        Assumptions:
        1. all omics data has the same experiment_id and sample_name_abbreviations
        
        INPUT:
        experiment_id_I = string TODO: needs to be refactored
        sample_name_abbreviation_I = string TODO: needs to be refactored
        model_id_I = string
        genes_I = list, strings
        proteins_I = list, strings
        fluxes_I = list, string
        metabolites = list, strings
        
        OUTPUT:
        data_O = {}

        TODO: 
        add support for proteins, transcripts, and fluxes
                
        '''
        from SBaaS_models.models_COBRA_query import models_COBRA_query
        COBRA_query = models_COBRA_query(self.session,self.engine,self.settings)
        #query model data:
        rows = COBRA_query.get_rows_modelID_dataStage02PhysiologyModelReactions(model_id_I);

        #query the gene data:        
        from SBaaS_resequencing.stage01_resequencing_mutations_query import stage01_resequencing_mutations_query
        resequencing_mutations_query = stage01_resequencing_mutations_query(self.session,self.engine,self.settings)
        resequencing_mutations_query.initialize_supportedTables();
        genes_rows = resequencing_mutations_query.get_mutations_experimentIDsAndSampleNames_dataStage01ResequencingMutationsAnnotated(
            experiment_ids_I = experiment_ids_I,
            sample_names_I = sample_name_abbreviations_I)
        genes_I = list(set([m for d in genes_rows for m in d['mutation_links']]))

        #query the metabolite data:  
        from SBaaS_quantification.stage01_quantification_replicatesMI_query import stage01_quantification_replicatesMI_query
        quantification_replicatesMI_query = stage01_quantification_replicatesMI_query(self.session,self.engine,self.settings)
        quantification_replicatesMI_query.initialize_supportedTables();
        metabolites_rows = quantification_replicatesMI_query.get_rows_experimentIDsAndSampleNames_dataStage01QuantificationReplicatesMI(
            experiment_ids_I = experiment_ids_I,
            sample_name_shorts_I = sample_name_abbreviations_I)
        metabolites_I = list(set([d['component_group_name'] for d in metabolites_rows]))

        #parse data:
        nrxns,\
            genes_mapped,ngenes,nMappedGenes,nMappedRxnsGenes,nMeasuredGenes,\
            mets_mapped,nmets,nMappedMets,nMappedRxnsMets,nMeasuredMets = self.calculate_measuredCoverage(
            model_data_I = rows,
            genes_I =genes_I,
            transcripts_I = transcripts_I,
            proteins_I = proteins_I,
            fluxes_I = fluxes_I,
            metabolites_I = metabolites_I)

        #prepare the output structure
        data_O = []
        if genes_I:
            data_O.append({
                'experiment_id':experiment_ids_I,
                'sample_name_abbreviation':None,
                'model_id':model_id_I,
                'model_component':'genes',
                'data_component':'genes',
                'n_model_components':ngenes,
                'n_mapped_components':nMappedGenes,
                'n_measured_components':nMeasuredGenes,
                'fraction_mapped':float(nMappedGenes)/float(ngenes),
                'used_':True,
                });
            data_O.append({
                'experiment_id':experiment_ids_I,
                'sample_name_abbreviation':None,
                'model_id':model_id_I,
                'model_component':'reactions',
                'data_component':'genes',
                'n_model_components':nrxns,
                'n_mapped_components':nMappedRxnsGenes,
                'n_measured_components':nMeasuredGenes,
                'fraction_mapped':float(nMappedRxnsGenes)/float(nrxns),
                'used_':True,
                });
        if metabolites_I:
            data_O.append({
                'experiment_id':experiment_ids_I,
                'sample_name_abbreviation':None,
                'model_id':model_id_I,
                'model_component':'metabolites',
                'data_component':'metabolites',
                'n_model_components':nmets,
                'n_mapped_components':nMappedMets,
                'n_measured_components':nMeasuredMets,
                'fraction_mapped':float(nMappedMets)/float(nmets),
                'used_':True,
                });
            data_O.append({
                'experiment_id':experiment_ids_I,
                'sample_name_abbreviation':None,
                'model_id':model_id_I,
                'model_component':'reactions',
                'data_component':'metabolites',
                'n_model_components':nrxns,
                'n_mapped_components':nMappedRxnsMets,
                'n_measured_components':nMeasuredMets,
                'fraction_mapped':float(nMappedRxnsMets)/float(nrxns),
                'used_':True,
                });
        if proteins_I:
            pass;
        if fluxes_I:
            pass;
        
        self.add_rows_table('data_stage02_physiology_measuredCoverage',data_O)

    def calculate_measuredCoverage(
        self,
        model_data_I,
        genes_I = [],
        transcripts_I = [],
        proteins_I = [],
        fluxes_I = [],
        metabolites_I = []):
        '''Calculate the model coverage for 
        A. genes from DNAreseq or RNAseq data that map to
            1. model genes and 2. model reactions
        B. metabolites from quantification or isotopomer data that map to 
            1. model metabolites and 2. model reactions
        C. fluxes from MFA data that map to
            1. model reactions
        
        INPUT:
        model_data_I = rows of model table reactions
        genes_I = list, strings
        proteins_I = list, strings
        transcripts_I = list, strings
        fluxes_I = list, string
        metabolites = list, strings
        
        OUTPUT:
        data_O = ()

        TODO: 
        add support for proteins, transcripts, and fluxes
                
        '''
        from SBaaS_models.models_COBRA_dependencies import models_COBRA_dependencies
        COBRA_dependencies = models_COBRA_dependencies()

        #reformat the metabolites
        metabolites_I = [m.replace('23dpg','13dpg')\
                        .replace('Pool_2pg_3pg','3pg')\
                        .replace('Hexose_Pool_fru_glc-D','glc_DASH_D')  for m in metabolites_I]

        #parse data:
        genes_all = [];
        rxns_all = [];
        mets_all = [];
        rxn_genes_mapped = [];
        rxn_mets_mapped = [];
        for row in model_data_I:
            geneids = [COBRA_dependencies.deformat_geneid(g) for g in row['genes']]
            genes_all.extend(geneids)
            rxns_all.append(row['rxn_id'])
            metids_comp = row['reactants_ids'] + row['products_ids']
            metids = []
            for m in metids_comp: 
                m_deform = COBRA_dependencies.deformat_metid(m)
                metids.append(m_deform)
            mets_all.extend(metids);
            if genes_I and \
                len(list(set(geneids+genes_I)))<len(list(set(geneids))+list(set(genes_I))):
                rxn_genes_mapped.append(row['rxn_id'])
            if metabolites_I and \
                len(list(set(metids+metabolites_I)))<\
                len(list(set(metids))+list(set(metabolites_I))):
                rxn_mets_mapped.append(row['rxn_id'])
        genes_unique = list(set(genes_all));
        rxns_unique = list(set(rxns_all));
        mets_unique = list(set(mets_all));

        nrxns = len(rxns_unique)
        genes_mapped,ngenes,nMappedGenes,nMappedRxnsGenes,nMeasuredGenes,\
            mets_mapped,nmets,nMappedMets,nMappedRxnsMets,nMeasuredMets=None,None,None,None,None,\
            None,None,None,None,None;
        
        if genes_I:
            #calculate coverage for genes
            genes_mapped = list(set([d for d in genes_all if d in genes_I]))
            ngenes = len(genes_unique)
            nMappedGenes = len(genes_mapped)
            nMappedRxnsGenes = len(rxn_genes_mapped)
            nMeasuredGenes = len(set(genes_I))

        if metabolites_I:
            #calculate coverage for metabolites
            mets_mapped = list(set([d for d in mets_all if d in metabolites_I]))
            nmets = len(mets_unique)        
            nMappedMets = len(mets_mapped)
            nMappedRxnsMets = len(rxn_mets_mapped)
            nMeasuredMets = len(set(metabolites_I))

        return nrxns,genes_mapped,ngenes,nMappedGenes,nMappedRxnsGenes,nMeasuredGenes,mets_mapped,nmets,nMappedMets,nMappedRxnsMets,nMeasuredMets
