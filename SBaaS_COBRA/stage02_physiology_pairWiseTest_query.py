#SBaaS
from .stage02_physiology_pairWiseTest_postgresql_models import *

from SBaaS_base.sbaas_base import sbaas_base
from SBaaS_base.sbaas_base_query_update import sbaas_base_query_update
from SBaaS_base.sbaas_base_query_drop import sbaas_base_query_drop
from SBaaS_base.sbaas_base_query_initialize import sbaas_base_query_initialize
from SBaaS_base.sbaas_base_query_insert import sbaas_base_query_insert
from SBaaS_base.sbaas_base_query_select import sbaas_base_query_select
from SBaaS_base.sbaas_base_query_delete import sbaas_base_query_delete

from SBaaS_base.sbaas_template_query import sbaas_template_query

#system
from math import log

class stage02_physiology_pairWiseTest_query(sbaas_template_query):
    def initialize_supportedTables(self):
        '''Set the supported tables dict for stage02_physiology_pairWiseTest
        '''
        tables_supported = {'data_stage02_physiology_pairWiseTest':data_stage02_physiology_pairWiseTest,
                            'data_stage02_physiology_pairWiseTestMetabolites':data_stage02_physiology_pairWiseTestMetabolites,
                            'data_stage02_physiology_pairWiseTestSubsystems':data_stage02_physiology_pairWiseTestSubsystems,
                        };
        self.set_supportedTables(tables_supported);  
    ## Query from data_stage02_physiology_pairWiseTest# Query data from data_stage02_physiology_pairWiseTest
    def get_RDataList_simulationIDs_dataStage02PhysiologyPairWiseTest(self,simulation_id_1_I,simulation_id_2_I):
        """get data from simulation_ids 1 and 2"""
        #Tested
        try:
            data = self.session.query(
                    data_stage02_physiology_pairWiseTest.simulation_id_1,
                    data_stage02_physiology_pairWiseTest.simulation_id_2,
                    data_stage02_physiology_pairWiseTest.rxn_id,
                    data_stage02_physiology_pairWiseTest.test_stat,
                    data_stage02_physiology_pairWiseTest.test_description,
                    data_stage02_physiology_pairWiseTest.pvalue,
                    data_stage02_physiology_pairWiseTest.pvalue_corrected,
                    data_stage02_physiology_pairWiseTest.pvalue_corrected_description,
                    data_stage02_physiology_pairWiseTest.mean,
                    data_stage02_physiology_pairWiseTest.ci_lb,
                    data_stage02_physiology_pairWiseTest.ci_ub,
                    data_stage02_physiology_pairWiseTest.ci_level,
                    data_stage02_physiology_pairWiseTest.fold_change).filter(
                    data_stage02_physiology_pairWiseTest.simulation_id_1.like(simulation_id_1_I),
                    data_stage02_physiology_pairWiseTest.simulation_id_2.like(simulation_id_2_I),
                    data_stage02_physiology_pairWiseTest.used_.is_(True)).group_by(
                    data_stage02_physiology_pairWiseTest.simulation_id_1,
                    data_stage02_physiology_pairWiseTest.simulation_id_2,
                    data_stage02_physiology_pairWiseTest.rxn_id,
                    data_stage02_physiology_pairWiseTest.test_stat,
                    data_stage02_physiology_pairWiseTest.test_description,
                    data_stage02_physiology_pairWiseTest.pvalue,
                    data_stage02_physiology_pairWiseTest.pvalue_corrected,
                    data_stage02_physiology_pairWiseTest.pvalue_corrected_description,
                    data_stage02_physiology_pairWiseTest.mean,
                    data_stage02_physiology_pairWiseTest.ci_lb,
                    data_stage02_physiology_pairWiseTest.ci_ub,
                    data_stage02_physiology_pairWiseTest.ci_level,
                    data_stage02_physiology_pairWiseTest.fold_change).order_by(
                    data_stage02_physiology_pairWiseTest.simulation_id_2.asc(),
                    data_stage02_physiology_pairWiseTest.rxn_id.asc()).all();
            data_O = [];
            for d in data: 
                data_1 = {};
                data_1['simulation_id_1'] = d.simulation_id_1;
                data_1['simulation_id_2'] = d.simulation_id_2;
                data_1['rxn_id'] = d.rxn_id;
                data_1['test_stat'] = d.test_stat;
                data_1['test_description'] = d.test_description;
                data_1['pvalue_negLog10'] = None;
                data_1['pvalue_corrected_description'] = None
                if d.pvalue_corrected:
                    data_1['pvalue_corrected_negLog10'] = -log(d.pvalue_corrected,10);
                if d.pvalue:
                    data_1['pvalue_negLog10'] = -log(d.pvalue,10);
                data_1['pvalue_corrected_description'] = d.pvalue_corrected_description;
                data_1['mean'] = d.mean;
                data_1['ci_lb'] = d.ci_lb;
                data_1['ci_ub'] = d.ci_ub;
                data_1['ci_level'] = d.ci_level;
                data_1['fold_change'] = d.fold_change;
                data_O.append(data_1);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rows_analysisID_dataStage02PhysiologyPairWiseTest(self,analysis_id_I):
        """get data from simulation_ids 1 and 2"""
        #Tested
        try:
            data = self.session.query(data_stage02_physiology_pairWiseTest).filter(
                    data_stage02_physiology_pairWiseTest.analysis_id.like(analysis_id_I),
                    data_stage02_physiology_pairWiseTest.used_.is_(True)).order_by(
                    data_stage02_physiology_pairWiseTest.simulation_id_1.asc(),
                    data_stage02_physiology_pairWiseTest.simulation_id_2.asc(),
                    data_stage02_physiology_pairWiseTest.rxn_id.asc()).all();
            data_O = [d.__repr__dict__() for d in data];
            for d in data_O: 
                d['pvalue_corrected_negLog10'] = None;
                d['pvalue_corrected_description'] = None
                if d['pvalue_corrected']:
                    d['pvalue_corrected_negLog10'] = -log(d['pvalue_corrected'],10);
                if d['pvalue']:
                    d['pvalue_negLog10'] = -log(d['pvalue'],10);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rows_analysisID_dataStage02PhysiologyPairWiseTestMetabolites(self,analysis_id_I):
        """get data from simulation_ids 1 and 2"""
        #Tested
        try:
            data = self.session.query(data_stage02_physiology_pairWiseTestMetabolites).filter(
                    data_stage02_physiology_pairWiseTestMetabolites.analysis_id.like(analysis_id_I),
                    data_stage02_physiology_pairWiseTestMetabolites.used_.is_(True)).order_by(
                    data_stage02_physiology_pairWiseTestMetabolites.simulation_id_1.asc(),
                    data_stage02_physiology_pairWiseTestMetabolites.simulation_id_2.asc(),
                    data_stage02_physiology_pairWiseTestMetabolites.met_id.asc()).all();
            data_O = [d.__repr__dict__() for d in data];
            for d in data_O: 
                d['pvalue_corrected_negLog10'] = None;
                d['pvalue_corrected_description'] = None
                if d['pvalue_corrected']:
                    d['pvalue_corrected_negLog10'] = -log(d['pvalue_corrected'],10);
                if d['pvalue']:
                    d['pvalue_negLog10'] = -log(d['pvalue'],10);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rows_analysisID_dataStage02PhysiologyPairWiseTestSubsystems(self,analysis_id_I):
        """get data from simulation_ids 1 and 2"""
        #Tested
        try:
            data = self.session.query(data_stage02_physiology_pairWiseTestSubsystems).filter(
                    data_stage02_physiology_pairWiseTestSubsystems.analysis_id.like(analysis_id_I),
                    data_stage02_physiology_pairWiseTestSubsystems.used_.is_(True)).order_by(
                    data_stage02_physiology_pairWiseTestSubsystems.simulation_id_1.asc(),
                    data_stage02_physiology_pairWiseTestSubsystems.simulation_id_2.asc(),
                    data_stage02_physiology_pairWiseTestSubsystems.subsystem_id.asc()).all();
            data_O = [d.__repr__dict__() for d in data];
            for d in data_O: 
                d['pvalue_corrected_negLog10'] = None;
                d['pvalue_corrected_description'] = None
                if d['pvalue_corrected']:
                    d['pvalue_corrected_negLog10'] = -log(d['pvalue_corrected'],10);
                if d['pvalue']:
                    d['pvalue_negLog10'] = -log(d['pvalue'],10);
            return data_O;
        except SQLAlchemyError as e:
            print(e);

    def reset_dataStage02_physiology_pairWiseTest(self,
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
