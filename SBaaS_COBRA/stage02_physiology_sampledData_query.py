#SBaaS models
from .stage02_physiology_sampledData_postgresql_models import *
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

class stage02_physiology_sampledData_query(sbaas_template_query):
    def initialize_supportedTables(self):
        '''Set the supported tables dict for stage02_physiology_sampledData
        '''
        tables_supported = {'data_stage02_physiology_sampledPoints':data_stage02_physiology_sampledPoints,
                            'data_stage02_physiology_sampledData':data_stage02_physiology_sampledData,
                            'data_stage02_physiology_samplingParameters':data_stage02_physiology_samplingParameters,
                            'data_stage02_physiology_sampledMetaboliteData':data_stage02_physiology_sampledMetaboliteData,
                            'data_stage02_physiology_sampledSubsystemData':data_stage02_physiology_sampledSubsystemData,
                        };
        self.set_supportedTables(tables_supported); 

    ## Query from data_stage02_physiology_sampledData
    # query rows from data_stage02_physiology_sampledData    
    def get_rows_experimentIDAndModelIDAndSampleNameAbbreviations_dataStage02PhysiologySampledData(self,experiment_id_I,model_id_I,sample_name_abbreviation_I):
        '''Query rows that are used from the sampledData'''
        try:
            data = self.session.query(data_stage02_physiology_sampledData).filter(
                    data_stage02_physiology_sampledData.model_id.like(model_id_I),
                    data_stage02_physiology_sampledData.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_physiology_sampledData.experiment_id.like(experiment_id_I),
                    data_stage02_physiology_sampledData.used_.is_(True)).all();
            rows_O = [];
            if data: 
                for d in data:
                    data_tmp = {'experiment_id':d.experiment_id,
                'model_id':d.model_id,
                'sample_name_abbreviation':d.sample_name_abbreviation,
                'rxn_id':d.rxn_id,
                'flux_units':d.flux_units,
                'sampling_ave':d.sampling_ave,
                'sampling_var':d.sampling_var,
                'sampling_lb':d.sampling_lb,
                'sampling_ub':d.sampling_ub,
                'used_':d.used_,
                'comment_':d.comment_};
                    rows_O.append(data_tmp);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);   
    def get_rows_simulationID_dataStage02PhysiologySampledData(self,simulation_id_I):
        '''Query rows that are used from the sampledData'''
        try:
            data = self.session.query(data_stage02_physiology_sampledData).filter(
                    data_stage02_physiology_sampledData.simulation_id.like(simulation_id_I),
                    data_stage02_physiology_sampledData.used_.is_(True)).all();
            rows_O = [d.__repr__dict__() for d in data];
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rows_simulationID_dataStage02PhysiologySampledMetaboliteData(self,simulation_id_I):
        '''Query rows that are used from the sampledData'''
        try:
            data = self.session.query(data_stage02_physiology_sampledMetaboliteData).filter(
                    data_stage02_physiology_sampledMetaboliteData.simulation_id.like(simulation_id_I),
                    data_stage02_physiology_sampledMetaboliteData.used_.is_(True)).all();
            rows_O = [d.__repr__dict__() for d in data];
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rows_simulationID_dataStage02PhysiologySampledSubsystemData(self,simulation_id_I):
        '''Query rows that are used from the sampledData'''
        try:
            data = self.session.query(data_stage02_physiology_sampledSubsystemData).filter(
                    data_stage02_physiology_sampledSubsystemData.simulation_id.like(simulation_id_I),
                    data_stage02_physiology_sampledSubsystemData.used_.is_(True)).all();
            rows_O = [d.__repr__dict__() for d in data];
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rxnIDs_simulationID_dataStage02PhysiologySampledData(self,simulation_id_I,used__I=True):
        '''Query rows that are used from the sampledData'''
        try:
            data = self.session.query(data_stage02_physiology_sampledData.rxn_id).filter(
                    data_stage02_physiology_sampledData.simulation_id.like(simulation_id_I),
                    data_stage02_physiology_sampledData.used_.is_(used__I)).all();
            rows_O = [d.rxn_id for d in data];
            return rows_O;
        except SQLAlchemyError as e:
            print(e); 
    def get_rowsDict_experimentIDAndModelIDAndSampleNameAbbreviations_dataStage02PhysiologySampledData(self,experiment_id_I,model_id_I,sample_name_abbreviation_I):
        '''Query rows that are used from the sampledData'''
        try:
            data = self.session.query(data_stage02_physiology_sampledData).filter(
                    data_stage02_physiology_sampledData.model_id.like(model_id_I),
                    data_stage02_physiology_sampledData.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_physiology_sampledData.experiment_id.like(experiment_id_I),
                    data_stage02_physiology_sampledData.used_.is_(True)).all();
            rows_O = {};
            if data: 
                for d in data:
                    if d.rxn_id in rows_O:
                        print('duplicate rxn_ids found!');
                    else:
                        rows_O[d.rxn_id]={'sampling_ave':d.sampling_ave,
                'sampling_var':d.sampling_var,
                'sampling_lb':d.sampling_lb,
                'sampling_ub':d.sampling_ub};
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rowsEscherLbUb_experimentIDAndModelIDAndSampleNameAbbreviations_dataStage02PhysiologySampledData(self,experiment_id_I,model_id_I,sample_name_abbreviation_I):
        '''Query rows that are used from the sampledData'''
        try:
            data = self.session.query(data_stage02_physiology_sampledData).filter(
                    data_stage02_physiology_sampledData.model_id.like(model_id_I),
                    data_stage02_physiology_sampledData.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_physiology_sampledData.experiment_id.like(experiment_id_I),
                    data_stage02_physiology_sampledData.used_.is_(True)).all();
            rows_O = [None,None];
            rows_O[0] = {};
            rows_O[1] = {}
            if data: 
                for d in data:
                    rows_O[0][d.rxn_id]=d.sampling_lb;
                    rows_O[1][d.rxn_id]=d.sampling_ub;
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rowsEscher_experimentIDAndModelIDAndSampleNameAbbreviations_dataStage02PhysiologySampledData(self,experiment_id_I,model_id_I,sample_name_abbreviation_I):
        '''Query rows that are used from the sampledData'''
        try:
            data = self.session.query(data_stage02_physiology_sampledData).filter(
                    data_stage02_physiology_sampledData.model_id.like(model_id_I),
                    data_stage02_physiology_sampledData.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_physiology_sampledData.experiment_id.like(experiment_id_I),
                    data_stage02_physiology_sampledData.used_.is_(True)).all();
            rows_O = {}
            if data: 
                for d in data:
                    rows_O[d.rxn_id]=d.sampling_ave;
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def add_dataStage02PhysiologySampledData(self, data_I):
        '''add rows of data_stage02_physiology_sampledData'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_physiology_sampledData(d
                        );
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    ##  Query from data_stage02_physiology_sampledPoints
    # query rows from data_stage02_physiology_sampledPoints
    def get_rows_simulationID_dataStage02PhysiologySampledPoints(self,simulation_id_I):
        '''Querry rows that are used from sampledPoints'''
        try:
            data = self.session.query(data_stage02_physiology_sampledPoints).filter(
                    data_stage02_physiology_sampledPoints.simulation_id.like(simulation_id_I),
                    data_stage02_physiology_sampledPoints.used_.is_(True)).all();
            rows_O = [d.__repr__dict__() for d in data];
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def add_dataStage02PhysiologySampledPoints(self, data_I):
        '''add rows of data_stage02_physiology_sampledPoints'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_physiology_sampledPoints(d
                        );
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    
    def drop_dataStage02_physiology_sampledData(self):
        try:
            data_stage02_physiology_sampledPoints.__table__.drop(self.engine,True);
            data_stage02_physiology_sampledData.__table__.drop(self.engine,True);
            data_stage02_physiology_samplingParameters.__table__.drop(self.engine,True);
        except SQLAlchemyError as e:
            print(e);
    def reset_dataStage02_physiology_sampledData(self,
            tables_I = [],
            simulation_id_I = None,
            warn_I=True):
        try:
            if not tables_I:
                tables_I = list(self.get_supportedTables().keys());
            querydelete = sbaas_base_query_delete(session_I=self.session,engine_I=self.engine,settings_I=self.settings,data_I=self.data);
            for table in tables_I:
                query = {};
                query['delete_from'] = [{'table_name':table}];
                query['where'] = [{
                        'table_name':table,
                        'column_name':'simulation_id',
                        'value':simulation_id_I,
		                'operator':'LIKE',
                        'connector':'AND'
                        }
	                ];
                table_model = self.convert_tableStringList2SqlalchemyModelDict([table]);
                query = querydelete.make_queryFromString(table_model,query);
                querydelete.reset_table_sqlalchemyModel(query_I=query,warn_I=warn_I);
        except Exception as e:
            print(e);
    def initialize_dataStage02_physiology_sampledData(self):
        try:
            data_stage02_physiology_sampledPoints.__table__.create(self.engine,True);
            data_stage02_physiology_sampledData.__table__.create(self.engine,True);
            data_stage02_physiology_samplingParameters.__table__.create(self.engine,True);
        except SQLAlchemyError as e:
            print(e);

    
    ##  Query from data_stage02_physiology_samplingParameters
    # query rows from data_stage02_physiology_simulation
    def get_rows_simulationID_dataStage02PhysiologySamplingParameters(self,simulation_id_I):
        '''Querry rows that are used from the samplingParameters'''
        try:
            data = self.session.query(data_stage02_physiology_samplingParameters).filter(
                    data_stage02_physiology_samplingParameters.simulation_id.like(simulation_id_I),
                    data_stage02_physiology_samplingParameters.used_.is_(True)).all();
            rows_O = [d.__repr__dict__() for d in data];
            return rows_O;
        except SQLAlchemyError as e:
            print(e);