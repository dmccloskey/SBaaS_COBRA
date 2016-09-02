#SBaaS
from .stage02_physiology_graphData_postgresql_models import *

from SBaaS_base.sbaas_base import sbaas_base
from SBaaS_base.sbaas_base_query_update import sbaas_base_query_update
from SBaaS_base.sbaas_base_query_drop import sbaas_base_query_drop
from SBaaS_base.sbaas_base_query_initialize import sbaas_base_query_initialize
from SBaaS_base.sbaas_base_query_insert import sbaas_base_query_insert
from SBaaS_base.sbaas_base_query_select import sbaas_base_query_select
from SBaaS_base.sbaas_base_query_delete import sbaas_base_query_delete

from SBaaS_base.sbaas_template_query import sbaas_template_query

class stage02_physiology_graphData_query(sbaas_template_query):
    def initialize_supportedTables(self):
        '''Set the supported tables dict for stage02_physiology_graphData
        '''
        tables_supported = {'data_stage02_physiology_graphData_shortestPathStats':data_stage02_physiology_graphData_shortestPathStats,
                            'data_stage02_physiology_graphData_shortestPaths':data_stage02_physiology_graphData_shortestPaths,
                        };
        self.set_supportedTables(tables_supported);  
    def reset_dataStage02_physiology_graphData(self,
            tables_I = [],
            analysis_id_I = None,
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
                        'column_name':'analysis_id',
                        'value':analysis_id_I,
		                'operator':'LIKE',
                        'connector':'AND'
                        }
	                ];
                table_model = self.convert_tableStringList2SqlalchemyModelDict([table]);
                query = querydelete.make_queryFromString(table_model,query);
                querydelete.reset_table_sqlalchemyModel(query_I=query,warn_I=warn_I);
        except Exception as e:
            print(e);
    def get_rows_analysisID_dataStage02PhysiologyGraphDataShortestPathStats(self,analysis_id_I):
        """get rows by analysis ID from data_stage02_physiology_graphData_shortestPathStats"""
        #Tested
        try:
            data = self.session.query(data_stage02_physiology_graphData_shortestPathStats).filter(
                    data_stage02_physiology_graphData_shortestPathStats.analysis_id.like(analysis_id_I),
                    data_stage02_physiology_graphData_shortestPathStats.used_.is_(True)).order_by(
                    data_stage02_physiology_graphData_shortestPathStats.analysis_id.asc(),
                    data_stage02_physiology_graphData_shortestPathStats.simulation_id.asc(),
                    data_stage02_physiology_graphData_shortestPathStats.path_start.asc(),
                    data_stage02_physiology_graphData_shortestPathStats.path_stop.asc(),
                    data_stage02_physiology_graphData_shortestPathStats.algorithm.asc()).all();
            data_O = [d.__repr__dict__() for d in data];
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rows_analysisID_dataStage02PhysiologyGraphDataShortestPaths(self,analysis_id_I):
        """get rows by analysis ID from data_stage02_physiology_graphData_shortestPathStats"""
        #Tested
        try:
            data = self.session.query(data_stage02_physiology_graphData_shortestPaths).filter(
                    data_stage02_physiology_graphData_shortestPaths.analysis_id.like(analysis_id_I),
                    data_stage02_physiology_graphData_shortestPaths.used_.is_(True)).order_by(
                    data_stage02_physiology_graphData_shortestPaths.analysis_id.asc(),
                    data_stage02_physiology_graphData_shortestPaths.simulation_id.asc(),
                    data_stage02_physiology_graphData_shortestPaths.path_start.asc(),
                    data_stage02_physiology_graphData_shortestPaths.path_stop.asc(),
                    data_stage02_physiology_graphData_shortestPaths.algorithm.asc()).all();
            data_O = [d.__repr__dict__() for d in data];
            return data_O;
        except SQLAlchemyError as e:
            print(e);
