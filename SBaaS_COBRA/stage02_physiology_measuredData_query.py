#SBaaS models
from .stage02_physiology_measuredData_postgresql_models import *
#SBaaS base
from SBaaS_base.sbaas_base import sbaas_base
from SBaaS_base.sbaas_base_query_update import sbaas_base_query_update
from SBaaS_base.sbaas_base_query_drop import sbaas_base_query_drop
from SBaaS_base.sbaas_base_query_initialize import sbaas_base_query_initialize
from SBaaS_base.sbaas_base_query_insert import sbaas_base_query_insert
from SBaaS_base.sbaas_base_query_select import sbaas_base_query_select
from SBaaS_base.sbaas_base_query_delete import sbaas_base_query_delete

from SBaaS_base.sbaas_template_query import sbaas_template_query
#other

class stage02_physiology_measuredData_query(sbaas_template_query):
    def initialize_supportedTables(self):
        '''Set the supported tables dict for stage02_physiology_measuredData
        '''
        tables_supported = {'data_stage02_physiology_measuredFluxes':data_stage02_physiology_measuredFluxes,
                        };
        self.set_supportedTables(tables_supported);     
    ## Query from data_stage01_physiology_ratesAverages:
    ## query met_ids from data_stage01_physiology_ratesAverages
    #def get_metID_experimentIDAndSampleNameAbbreviation_dataStage01PhysiologyRatesAverages(self,experiment_id_I,sample_name_abbreviation_I):
    #    '''Querry rate data by sample id and met id that are used from
    #    the experiment'''
    #    try:
    #        data = self.session.query(data_stage01_physiology_ratesAverages.sample_name_abbreviation,
    #                data_stage01_physiology_ratesAverages.met_id).filter(
    #                data_stage01_physiology_ratesAverages.experiment_id.like(experiment_id_I),
    #                data_stage01_physiology_ratesAverages.used_.is_(True),
    #                data_stage01_physiology_ratesAverages.sample_name_abbreviation.like(sample_name_abbreviation_I)).group_by(
    #                data_stage01_physiology_ratesAverages.sample_name_abbreviation,
    #                data_stage01_physiology_ratesAverages.met_id).order_by(
    #                data_stage01_physiology_ratesAverages.met_id.asc()).all();
    #        met_id_O = [];
    #        if data: 
    #            for d in data:
    #                met_id_O.append(d.met_id);
    #        return met_id_O;
    #    except SQLAlchemyError as e:
    #        print(e);
    ## query rate from data_stage01_physiology_ratesAverages
    #def get_rateData_experimentIDAndSampleNameAbbreviationAndMetID_dataStage01PhysiologyRatesAverages(self,experiment_id_I,sample_name_abbreviation_I,met_id_I):
    #    '''Querry rate data by sample id and met id that are used from
    #    the experiment'''
    #    try:
    #        data = self.session.query(data_stage01_physiology_ratesAverages.slope_average,
    #                data_stage01_physiology_ratesAverages.intercept_average,
    #                data_stage01_physiology_ratesAverages.rate_average,
    #                data_stage01_physiology_ratesAverages.rate_lb,
    #                data_stage01_physiology_ratesAverages.rate_ub,
    #                data_stage01_physiology_ratesAverages.rate_units,
    #                data_stage01_physiology_ratesAverages.rate_var).filter(
    #                data_stage01_physiology_ratesAverages.met_id.like(met_id_I),
    #                data_stage01_physiology_ratesAverages.experiment_id.like(experiment_id_I),
    #                data_stage01_physiology_ratesAverages.used_.is_(True),
    #                data_stage01_physiology_ratesAverages.sample_name_abbreviation.like(sample_name_abbreviation_I)).first();
    #        slope_average, intercept_average, rate_average, rate_lb, rate_ub, rate_units, rate_var = None,None,None,None,None,None,None;
    #        if data: 
    #            slope_average, intercept_average,\
    #                rate_average, rate_lb, rate_ub, rate_units, rate_var = data.slope_average, data.intercept_average,\
    #                data.rate_average, data.rate_lb, data.rate_ub, data.rate_units, data.rate_var;
    #        return slope_average, intercept_average, rate_average, rate_lb, rate_ub, rate_units, rate_var;
    #    except SQLAlchemyError as e:
    #        print(e);

    ##TODO: convert?
    ## Query from data_stage02_physiology_metabolomicsData
    # query rows from data_stage02_physiology_metabolomicsData    
    def get_rows_experimentIDAndTimePointAndSampleNameAbbreviations_dataStage02PhysiologyMetabolomicsData(self,experiment_id_I,time_point_I,sample_name_abbreviation_I):
        '''Query rows that are used from the metabolomicsData'''
        try:
            data = self.session.query(data_stage02_physiology_metabolomicsData).filter(
                    data_stage02_physiology_metabolomicsData.time_point.like(time_point_I),
                    data_stage02_physiology_metabolomicsData.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_physiology_metabolomicsData.experiment_id.like(experiment_id_I),
                    data_stage02_physiology_metabolomicsData.measured.is_(True),
                    data_stage02_physiology_metabolomicsData.used_.is_(True)).all();
            rows_O = [];
            if data: 
                for d in data:
                    data_tmp = {'experiment_id':d.experiment_id,
                        'sample_name_abbreviation':d.sample_name_abbreviation,
                        'time_point':d.time_point,
                        'met_id':d.met_id,
                        'concentration':d.concentration,
                        'concentration_var':d.concentration_var,
                        'concentration_units':d.concentration_units,
                        'concentration_lb':d.concentration_lb,
                        'concentration_ub':d.concentration_ub,
                        'measured':d.measured,
                        'used_':d.used_,
                        'comment_':d.comment_};
                    rows_O.append(data_tmp);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);   
    def get_rowsDict_experimentIDAndTimePointAndSampleNameAbbreviations_dataStage02PhysiologyMetabolomicsData(self,experiment_id_I,time_point_I,sample_name_abbreviation_I):
        '''Query rows that are used from the metabolomicsData'''
        try:
            data = self.session.query(data_stage02_physiology_metabolomicsData).filter(
                    data_stage02_physiology_metabolomicsData.time_point.like(time_point_I),
                    data_stage02_physiology_metabolomicsData.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_physiology_metabolomicsData.experiment_id.like(experiment_id_I),
                    data_stage02_physiology_metabolomicsData.measured.is_(True),
                    data_stage02_physiology_metabolomicsData.used_.is_(True)).all();
            rows_O = {};
            if data: 
                for d in data:
                    if d.met_id in rows_O:
                        print('duplicate met_ids found!');
                    else:
                        rows_O[d.met_id]={'concentration':d.concentration,
                            'concentration_var':d.concentration_var,
                            'concentration_units':d.concentration_units,
                            'concentration_lb':d.concentration_lb,
                            'concentration_ub':d.concentration_ub};
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rowsEscherLbUb_experimentIDAndTimePointAndSampleNameAbbreviations_dataStage02PhysiologyMetabolomicsData(self,experiment_id_I,time_point_I,sample_name_abbreviation_I):
        '''Query rows that are used from the metabolomicsData'''
        try:
            data = self.session.query(data_stage02_physiology_metabolomicsData).filter(
                    data_stage02_physiology_metabolomicsData.time_point.like(time_point_I),
                    data_stage02_physiology_metabolomicsData.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_physiology_metabolomicsData.experiment_id.like(experiment_id_I),
                    data_stage02_physiology_metabolomicsData.measured.is_(True),
                    data_stage02_physiology_metabolomicsData.used_.is_(True)).all();
            rows_O = [None,None];
            rows_O[0] = {};
            rows_O[1] = {}
            if data: 
                for d in data:
                    rows_O[0][d.met_id]=d.concentration_lb;
                    rows_O[1][d.met_id]=d.concentration_ub;
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rowsEscher_experimentIDAndTimePointAndSampleNameAbbreviations_dataStage02PhysiologyMetabolomicsData(self,experiment_id_I,time_point_I,sample_name_abbreviation_I):
        '''Query rows that are used from the metabolomicsData'''
        try:
            data = self.session.query(data_stage02_physiology_metabolomicsData).filter(
                    data_stage02_physiology_metabolomicsData.time_point.like(time_point_I),
                    data_stage02_physiology_metabolomicsData.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_physiology_metabolomicsData.experiment_id.like(experiment_id_I),
                    data_stage02_physiology_metabolomicsData.measured.is_(True),
                    data_stage02_physiology_metabolomicsData.used_.is_(True)).all();
            rows_O = {}
            if data: 
                for d in data:
                    rows_O[d.met_id]=d.concentration;
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def add_dataStage02PhysiologyMetabolomicsData(self, data_I):
        '''add rows of data_stage02_physiology_metabolomicsData'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_physiology_metabolomicsData(d
                        #d['experiment_id'],
                        #d['sample_name_abbreviation'],
                        #d['time_point'],
                        #d['met_id'],
                        #d['concentration'],
                        #d['concentration_var'],
                        #d['concentration_units'],
                        #d['concentration_lb'],
                        #d['concentration_ub'],
                        #d['measured'],
                        #d['used_'],
                        #d['comment_']
                        );
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def update_dataStage02PhysiologyMetabolomicsData(self,data_I):
        #Not yet tested
        '''update rows of data_stage02_physiology_metabolomicsData'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_physiology_metabolomicsData).filter(
                            data_stage02_physiology_metabolomicsData.id.like(d['id'])).update(
                            {'experiment_id':d['experiment_id'],
                            'sample_name_abbreviation':d['sample_name_abbreviation'],
                            'time_point':d['time_point'],
                            'met_id':d['met_id'],
                            'concentration':d['concentration'],
                            'concentration_var':d['concentration_var'],
                            'concentration_units':d['concentration_units'],
                            'concentration_lb':d['concentration_lb'],
                            'concentration_ub':d['concentration_ub'],
                            'measured':d['measured'],
                            'used_':d['used_'],
                            'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
       
    ## Query from data_stage02_physiology_measuredFluxes
    # query rows from data_stage02_physiology_measuredFluxes
    def get_rows_experimentIDAndSampleNameAbbreviation_dataStage02PhysiologyMeasuredFluxes(self,experiment_id_I,sample_name_abbreviation_I):
        '''Querry rows by model_id that are used'''
        try:
            data = self.session.query(data_stage02_physiology_measuredFluxes).filter(
                    data_stage02_physiology_measuredFluxes.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_physiology_measuredFluxes.experiment_id.like(experiment_id_I),
                    data_stage02_physiology_measuredFluxes.used_.is_(True)).order_by(
                    data_stage02_physiology_measuredFluxes.model_id.asc(),
                    data_stage02_physiology_measuredFluxes.rxn_id.asc()).all();
            rows_O = [];
            if data: 
                for d in data:
                    row_tmp = {'experiment_id':d.experiment_id,
                    'model_id':d.model_id,
                    'sample_name_abbreviation':d.sample_name_abbreviation,
                    #'time_point':d.time_point,
                    'rxn_id':d.rxn_id,
                    'flux_average':d.flux_average,
                    'flux_stdev':d.flux_stdev,
                    'flux_lb':d.flux_lb,
                    'flux_ub':d.flux_ub,
                    'flux_units':d.flux_units,
                    'used_':d.used_,
                    'comment_':d.comment_};
                    rows_O.append(row_tmp);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rows_experimentIDAndModelIDAndSampleNameAbbreviation_dataStage02PhysiologyMeasuredFluxes(self,experiment_id_I,model_id_I,sample_name_abbreviation_I):
        '''Querry rows by model_id that are used'''
        try:
            data = self.session.query(data_stage02_physiology_measuredFluxes).filter(
                    data_stage02_physiology_measuredFluxes.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_physiology_measuredFluxes.model_id.like(model_id_I),
                    data_stage02_physiology_measuredFluxes.experiment_id.like(experiment_id_I),
                    data_stage02_physiology_measuredFluxes.used_.is_(True)).order_by(
                    data_stage02_physiology_measuredFluxes.model_id.asc(),
                    data_stage02_physiology_measuredFluxes.rxn_id.asc()).all();
            rows_O = [];
            if data: 
                for d in data:
                    row_tmp = {'experiment_id':d.experiment_id,
                    'model_id':d.model_id,
                    'sample_name_abbreviation':d.sample_name_abbreviation,
                    #'time_point':d.time_point,
                    'rxn_id':d.rxn_id,
                    'flux_average':d.flux_average,
                    'flux_stdev':d.flux_stdev,
                    'flux_lb':d.flux_lb,
                    'flux_ub':d.flux_ub,
                    'flux_units':d.flux_units,
                    'used_':d.used_,
                    'comment_':d.comment_};
                    rows_O.append(row_tmp);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_fluxDict_experimentIDAndModelIDAndSampleNameAbbreviationsAndTimePoint_dataStage02PhysiologyMeasuredFluxes(self,experiment_id_I,model_id_I,sample_name_abbreviation_I,time_point_I):
        '''Query rows that are used from the measuredFluxes'''
        try:
            data = self.session.query(data_stage02_physiology_measuredFluxes).filter(
                    data_stage02_physiology_measuredFluxes.time_point.like(time_point_I),
                    data_stage02_physiology_measuredFluxes.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_physiology_measuredFluxes.model_id.like(model_id_I),
                    data_stage02_physiology_measuredFluxes.experiment_id.like(experiment_id_I),
                    data_stage02_physiology_measuredFluxes.used_.is_(True)).all();
            rows_O = {};
            if data: 
                for d in data:
                    if d.rxn_id in rows_O:
                        print('duplicate rxn_ids found!');
                    else:
                        rows_O[d.rxn_id]={'flux':d.flux_average,
                            'stdev':d.flux_stdev,
                            'units':d.flux_units,
                            'lb':d.flux_lb,
                            'ub':d.flux_ub,
                            'used_':d.used_,
                            'comment_':d.comment_};
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def add_dataStage02PhysiologyMeasuredFluxes(self, data_I):
        '''add rows of data_stage02_physiology_measuredFluxes'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_physiology_measuredFluxes(d
                        #d['experiment_id'],
                        #d['model_id'],
                        #d['sample_name_abbreviation'],
                        ##d['time_point'],
                        #d['rxn_id'],
                        #d['flux_average'],
                        #d['flux_stdev'],
                        #d['flux_lb'],
                        #d['flux_ub'],
                        #d['flux_units'],
                        #d['used_'],
                        #d['comment_']
                        );
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def update_unique_dataStage02PhysiologyMeasuredFluxes(self, data_I):
        '''update rows of data_stage02_physiology_measuredFluxes by unique columns
        '''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_physiology_measuredFluxes).filter(
                            data_stage02_physiology_measuredFluxes.experiment_id.like(d['experiment_id']),
                            data_stage02_physiology_measuredFluxes.sample_name_abbreviation.like(d['sample_name_abbreviation']),
                            data_stage02_physiology_measuredFluxes.time_point.like(d['time_point']),
                            data_stage02_physiology_measuredFluxes.rxn_id.like(d['rxn_id']),
                            data_stage02_physiology_measuredFluxes.flux_units.like(d['flux_units'])).update(
                            {'experiment_id':d['experiment_id'],
                            'sample_name_abbreviation':d['sample_name_abbreviation'],
                            'time_point':d['time_point'],
                            'rxn_id':d['rxn_id'],
                            'flux_average':d['flux_average'],
                            'flux_stdev':d['flux_stdev'],
                            'flux_units':d['flux_units'],
                            'flux_lb':d['flux_lb'],
                            'flux_ub':d['flux_ub'],
                            'used_':d['used_'],
                            'comment_':d['comment_']},
                            synchronize_session=False);
                    if data_update == 0:
                        print('row not found.')
                        print(d)
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def update_dataStage02PhysiologyMeasuredFluxes(self,data_I):
        #TODO:
        '''update rows of data_stage02_physiology_measuredFluxes'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_physiology_measuredFluxes).filter(
                            data_stage02_physiology_measuredFluxes.id==d['id']
                            ).update(
                            {'experiment_id':d['experiment_id'],
                            'model_id':d['model_id'],
                            'sample_name_abbreviation':d['sample_name_abbreviation'],
                            #'time_point':d['time_point'],
                            'rxn_id':d['rxn_id'],
                            'flux_average':d['flux_average'],
                            'flux_stdev':d['flux_stdev'],
                            'flux_lb':d['flux_lb'],
                            'flux_ub':d['flux_ub'],
                            'flux_units':d['flux_units'],
                            'used_':d['used_'],
                            'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def drop_dataStage02_physiology_measuredData(self):
        try:
            data_stage02_physiology_metabolomicsData.__table__.drop(self.engine,True);
            data_stage02_physiology_measuredFluxes.__table__.drop(self.engine,True);
        except SQLAlchemyError as e:
            print(e);
    def reset_dataStage02_physiology_metabolomicsData(self,experiment_id_I = None):
        try:
            if experiment_id_I:
                reset = self.session.query(data_stage02_physiology_metabolomicsData).filter(data_stage02_physiology_metabolomicsData.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def reset_dataStage02_physiology_measuredFluxes(self,experiment_id_I = None):
        try:
            if experiment_id_I:
                reset = self.session.query(data_stage02_physiology_measuredFluxes).delete(synchronize_session=False);
                self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def initialize_dataStage02_physiology_measuredData(self):
        try:
            data_stage02_physiology_metabolomicsData.__table__.create(self.engine,True);
            data_stage02_physiology_measuredFluxes.__table__.create(self.engine,True);
        except SQLAlchemyError as e:
            print(e);