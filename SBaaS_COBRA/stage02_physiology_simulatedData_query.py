#SBaaS models
from .stage02_physiology_simulatedData_postgresql_models import *
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

class stage02_physiology_simulatedData_query(sbaas_template_query):
    def initialize_supportedTables(self):
        '''Set the supported tables dict for data_stage02_physiology_simulatedData
        '''
        tables_supported = {
            'data_stage02_physiology_simulatedData_fva':data_stage02_physiology_simulatedData_fva,
            'data_stage02_physiology_simulatedData_sra':data_stage02_physiology_simulatedData_sra,
            'data_stage02_physiology_simulatedData_pfba':data_stage02_physiology_simulatedData_pfba,
            'data_stage02_physiology_simulatedData_fba':data_stage02_physiology_simulatedData_fba,
                        };
        self.set_supportedTables(tables_supported);
    ## Query from data_stage02_physiology_simulatedData
    # query rows from data_stage02_physiology_simulatedData    
    def get_rows_simulationIDAndSimulationDateAndTime_dataStage02PhysiologySimulatedData(self,simulation_id_I,simulation_dateAndTime_I):
        '''Query rows by simulation_id and simulation_dateAndTime from data_stage02_physiology_simulatedData'''
        try:
            data = self.session.query(data_stage02_physiology_simulatedData).filter(
                    data_stage02_physiology_simulatedData.simulation_dateAndTime.like(simulation_dateAndTime_I),
                    data_stage02_physiology_simulatedData.simulation_id.like(simulation_id_I),
                    data_stage02_physiology_simulatedData.used_.is_(True)).all();
            rows_O = [];
            if data: 
                for d in data:
                    data_tmp = d.__repr__dict__();
                    rows_O.append(data_tmp);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);   
    def get_rowsDict_simulationIDAndSimulationDateAndTime_dataStage02PhysiologySimulatedData(self,simulation_id_I,simulation_dateAndTime_I):
        '''Query rows by simulation_id and simulation_dateAndTime from data_stage02_physiology_simulatedData'''
        try:
            data = self.session.query(data_stage02_physiology_simulatedData).filter(
                    data_stage02_physiology_simulatedData.simulation_dateAndTime.like(simulation_dateAndTime_I),
                    data_stage02_physiology_simulatedData.simulation_id.like(simulation_id_I),
                    data_stage02_physiology_simulatedData.used_.is_(True)).all();
            fva_data_O = {};
            sra_data_O = {};
            if data: 
                for d in data:
                    if d.rxn_id in fva_data_O:
                        print('duplicate rxn_id found!');
                    else:
                        fva_data_O[d.rxn_id]={
                            'minimum':d.fva_minimum,
                            'maximum':d.fva_maximum};
                        sra_data_O[d.rxn_id]={'gr':d.sra_gr,
                            'gr_ratio':d.sra_gr_ratio};
            return fva_data_O,sra_data_O;
        except SQLAlchemyError as e:
            print(e);    

    def get_rows_dataStage02PhysiologySimulatedData(self,
                tables_I,
                query_I,
                output_O,
                dictColumn_I=None):
        """get rows by analysis ID from data_stage02_physiology_simulatedData"""
        data_O = [];
        try:
            table_model = self.convert_tableStringList2SqlalchemyModelDict(tables_I);
            queryselect = sbaas_base_query_select(session_I=self.session,engine_I=self.engine,settings_I=self.settings,data_I=self.data);
            query = queryselect.make_queryFromString(table_model,query_I);
            data_O = queryselect.get_rows_sqlalchemyModel(
                query_I=query,
                output_O=output_O,
                dictColumn_I=dictColumn_I);
        except Exception as e:
            print(e);
        return data_O;
    def add_dataStage02PhysiologySimulatedData(self,table_I,data_I):
        '''add rows of data_stage02_physiology_simulatedData'''
        if data_I:
            try:
                model_I = self.convert_tableString2SqlalchemyModel(table_I);
                queryinsert = sbaas_base_query_insert(session_I=self.session,engine_I=self.engine,settings_I=self.settings,data_I=self.data);
                queryinsert.add_rows_sqlalchemyModel(model_I,data_I);
            except Exception as e:
                print(e);
    def update_dataStage02PhysiologySimulatedData(self,table_I,data_I):
        '''update rows of data_stage02_physiology_simulatedData'''
        if data_I:
            try:
                model_I = self.convert_tableString2SqlalchemyModel(table_I);
                queryupdate = sbaas_base_query_update(session_I=self.session,engine_I=self.engine,settings_I=self.settings,data_I=self.data);
                queryupdate.update_rows_sqlalchemyModel(model_I,data_I);
            except Exception as e:
                print(e);

    def initialize_dataStage02_physiology_simulatedData(self,
            tables_I = [],):
        try:
            if not tables_I:
                tables_I = list(self.get_supportedTables().keys());
            queryinitialize = sbaas_base_query_initialize(session_I=self.session,engine_I=self.engine,settings_I=self.settings,data_I=self.data);
            for table in tables_I:
                model_I = self.convert_tableString2SqlalchemyModel(table);
                queryinitialize.initialize_table_sqlalchemyModel(model_I);
        except Exception as e:
            print(e);
    def drop_dataStage02_physiology_simulatedData(self,
            tables_I = [],):
        try:
            if not tables_I:
                tables_I = list(self.get_supportedTables().keys());
            querydrop = sbaas_base_query_drop(session_I=self.session,engine_I=self.engine,settings_I=self.settings,data_I=self.data);
            for table in tables_I:
                model_I = self.convert_tableString2SqlalchemyModel(table);
                querydrop.drop_table_sqlalchemyModel(model_I);
        except Exception as e:
            print(e);
    def reset_dataStage02_physiology_simulatedData(self,
            tables_I = [],
            simulation_id_I = None,
            warn_I=True):
        try:
            if not tables_I:
                tables_I = list(self.get_supportedTables().keys());
            querydelete = sbaas_base_query_delete(session_I=self.session,engine_I=self.engine,settings_I=self.settings,data_I=self.data);
            for table in tables_I:
                query = {};
                query['delete_from'] = table;
                query['where'] = [{
                        'table_name':table,
                        'column_name':'simulation_id',
		                'value':self.convert_string2StringString(simulation_id_I),
		                'operator':'LIKE',
                        'connector':'AND'
                        }
	                ];
                table_model = self.convert_tableStringList2SqlalchemyModelDict([table]);
                query = querydelete.make_queryFromString(table_model,query);
                querydelete.reset_table_sqlalchemyModel(query_I=query,warn_I=warn_I);
        except Exception as e:
            print(e);
            