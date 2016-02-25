#SBaaS
from .stage02_physiology_measuredData_io import stage02_physiology_measuredData_io
from .stage02_physiology_simulation_query import stage02_physiology_simulation_query
from SBaaS_quantification.stage01_quantification_averages_query import stage01_quantification_averages_query
from SBaaS_physiology.stage01_physiology_rates_query import stage01_physiology_rates_query
from SBaaS_MFA.stage02_isotopomer_fittedNetFluxes_query import stage02_isotopomer_fittedNetFluxes_query
from SBaaS_models.models_COBRA_dependencies import models_COBRA_dependencies
# Resources (delete if not needed)
from io_utilities.base_importData import base_importData
from io_utilities.base_exportData import base_exportData
import copy

class stage02_physiology_measuredData_execute(stage02_physiology_measuredData_io,
                                                  stage02_physiology_simulation_query,
                                                      stage01_quantification_averages_query,
                                                      stage01_physiology_rates_query,
                                                      stage02_isotopomer_fittedNetFluxes_query):

    def execute_makeMetabolomicsData_intracellular(self,experiment_id_I,data_I=[],compartment_id_I='c'):
        '''Get the currated metabolomics data from data_stage01_quantification_averagesMIGeo'''
        # get rows:
        
        met_id_conv_dict = {'Hexose_Pool_fru_glc-D':['glc-D','fru-D'],
                            'Pool_2pg_3pg':['2pg','3pg'],
                            '23dpg':['13dpg']};
        cobradependencies = models_COBRA_dependencies();
        data_O = [];
        if data_I:
            data = data_I;
        else:
            data = [];
            data = self.get_rows_experimentID_dataStage01AveragesMIgeo(experiment_id_I);
        for d in data:
            if d['component_group_name'] in list(met_id_conv_dict.keys()):
                met2conv = d['component_group_name'];
                for met_conv in met_id_conv_dict[met2conv]:
                    row_tmp = copy.copy(d)
                    row_tmp['component_group_name'] = met_conv;
                    data_O.append(row_tmp);
            else:
                data_O.append(d);
        for d in data_O:
            d['met_id']=cobradependencies.format_metid(d['component_group_name'],compartment_id_I);
            d['measured']=True;
            d['comment_']=None;
        #add data to the DB
        self.add_dataStage02PhysiologyMetabolomicsData(data_O);
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
        INPUT not yet implemented:
        flip_rxn_direction_I = list of reaction_ids to flip the direction of flux
        '''
        data_O = [];
        for simulation_id in list(IDsQuantification2SimulationIDsIsotopomer_I.keys()):
            # get the fittedNetFluxes
            fittedNetFluxes = [];
            fittedNetFluxes = self.get_rows_simulationIDAndSimulationDateAndTimeAndFluxUnits_dataStage02IsotopomerfittedNetFluxes(simulation_id,
                IDsQuantification2SimulationIDsIsotopomer_I[simulation_id]['simulation_dateAndTime'],
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
                    tmp = {'experiment_id':IDsQuantification2SimulationIDsIsotopomer_I[simulation_id]['experiment_id'],
                        'model_id':IDsQuantification2SimulationIDsIsotopomer_I[simulation_id]['model_id'],
                        'sample_name_abbreviation':IDsQuantification2SimulationIDsIsotopomer_I[simulation_id]['sample_name_abbreviation'],
                        'time_point':IDsQuantification2SimulationIDsIsotopomer_I[simulation_id]['time_point'],
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
    def execute_addMeasuredFluxes(self,experiment_id_I, ko_list={}, flux_dict={}, model_ids_I=[], sample_name_abbreviations_I=[],time_points_I=[]):
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
            model_ids = self.get_modelID_experimentID_dataStage03QuantificationSimulation(experiment_id_I);
        for model_id in model_ids:
            # get sample names and sample name abbreviations
            if sample_name_abbreviations_I:
                sample_name_abbreviations = sample_name_abbreviations_I;
            else:
                sample_name_abbreviations = [];
                sample_name_abbreviations = self.get_sampleNameAbbreviations_experimentIDAndModelID_dataStage03QuantificationSimulation(experiment_id_I,model_id);
            for sna_cnt,sna in enumerate(sample_name_abbreviations):
                print('Adding experimental fluxes for sample name abbreviation ' + sna);
                if time_points_I:
                    time_points = time_points_I;
                else:
                    time_points = [];
                    time_points = self.get_timePoints_experimentIDAndModelIDAndSampleNameAbbreviation_dataStage03QuantificationSimulation(experiment_id_I,model_id,sna)
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
                            ##add data to the database
                            #row = [];
                            #row = data_stage02_physiology_measuredFluxes(
                            #    experiment_id_I,
                            #    model_id,
                            #    sna,
                            #    tp,
                            #    k,
                            #    v['ave'],
                            #    v['stdev'],
                            #    v['lb'], 
                            #    v['ub'],
                            #    v['units'],
                            #    True,
                            #    None);
                            #self.session.add(row);
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
                            #add data to the database
                            #row = [];
                            #row = data_stage02_physiology_measuredFluxes(
                            #    experiment_id_I,
                            #    model_id,
                            #    sna,
                            #    tp,
                            #    k,
                            #    0.0,
                            #    0.0,
                            #    0.0, 
                            #    0.0,
                            #    'mmol*gDCW-1*hr-1',
                            #    True,
                            #    None);
                            #self.session.add(row);
        #add data to the database:
        self.add_dataStage02PhysiologyMeasuredFluxes(data_O);
        #self.session.commit();
    def execute_makeMeasuredFluxes(self,experiment_id_I, metID2RxnID_I = {}, sample_name_abbreviations_I = [], met_ids_I = []):
        '''Collect and flux data from data_stage01_physiology_ratesAverages for physiological simulation'''
        #Input:
        #   metID2RxnID_I = e.g. {'glc-D':{'model_id':'140407_iDM2014','rxn_id':'EX_glc_LPAREN_e_RPAREN_'},
        #                        {'ac':{'model_id':'140407_iDM2014','rxn_id':'EX_ac_LPAREN_e_RPAREN_'},
        #                        {'succ':{'model_id':'140407_iDM2014','rxn_id':'EX_succ_LPAREN_e_RPAREN_'},
        #                        {'lac-L':{'model_id':'140407_iDM2014','rxn_id':'EX_lac_DASH_L_LPAREN_e_RPAREN_'},
        #                        {'biomass':{'model_id':'140407_iDM2014','rxn_id':'Ec_biomass_iJO1366_WT_53p95M'}};

        data_O = [];
        # get sample names and sample name abbreviations
        if sample_name_abbreviations_I:
            sample_name_abbreviations = sample_name_abbreviations_I;
        else:
            sample_name_abbreviations = [];
            sample_name_abbreviations = self.get_sampleNameAbbreviations_experimentID_dataStage03QuantificationSimulation(experiment_id_I);
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
                model_id = metID2RxnID_I[met]['model_id'];
                rxn_id = metID2RxnID_I[met]['rxn_id'];
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
            model_ids = self.get_modelID_experimentID_dataStage03QuantificationSimulation(experiment_id_I);
        for model_id in model_ids:
            diagnose_variables_O[model_id] = {};
            cobra_model_base = models_I[model_id];
            print('testing model ' + model_id);
            # get sample names and sample name abbreviations
            if sample_name_abbreviations_I:
                sample_name_abbreviations = sample_name_abbreviations_I;
            else:
                sample_name_abbreviations = [];
                sample_name_abbreviations = self.get_sampleNameAbbreviations_experimentIDAndModelID_dataStage03QuantificationSimulation(experiment_id_I,model_id);
            for sna_cnt,sna in enumerate(sample_name_abbreviations):
                diagnose_variables_O[model_id][sna] = {};
                print('testing sample_name_abbreviation ' + sna);
                # get the time_points
                if time_points_I:
                    time_points = time_points_I;
                else:
                    time_points = [];
                    time_points = self.get_timePoints_experimentIDAndModelIDAndSampleNameAbbreviation_dataStage03QuantificationSimulation(experiment_id_I,model_id,sna)
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
