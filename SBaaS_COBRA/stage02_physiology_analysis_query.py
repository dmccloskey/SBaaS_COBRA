#SBaaS
from .stage02_physiology_analysis_postgresql_models import *
from .stage02_physiology_simulation_postgresql_models import data_stage02_physiology_simulation

from SBaaS_base.sbaas_base import sbaas_base
from SBaaS_base.sbaas_base_query_update import sbaas_base_query_update
from SBaaS_base.sbaas_base_query_drop import sbaas_base_query_drop
from SBaaS_base.sbaas_base_query_initialize import sbaas_base_query_initialize
from SBaaS_base.sbaas_base_query_insert import sbaas_base_query_insert
from SBaaS_base.sbaas_base_query_select import sbaas_base_query_select
from SBaaS_base.sbaas_base_query_delete import sbaas_base_query_delete

from SBaaS_base.sbaas_template_query import sbaas_template_query

class stage02_physiology_analysis_query(sbaas_template_query):
    def initialize_supportedTables(self):
        '''Set the supported tables dict for stage02_physiology_analysis
        '''
        tables_supported = {'data_stage02_physiology_analysis':data_stage02_physiology_analysis,
                        };
        self.set_supportedTables(tables_supported);  
    ## Query from data_stage02_physiology_analysis
    # query simulation_id
    def get_simulationID_analysisID_dataStage02PhysiologyAnalysis(self,analysis_id_I):
        '''Query simulations that are used for the anlaysis'''
        try:
            data = self.session.query(data_stage02_physiology_analysis.simulation_id).filter(
                    data_stage02_physiology_analysis.analysis_id.like(analysis_id_I),
                    data_stage02_physiology_analysis.used_.is_(True)).group_by(
                    data_stage02_physiology_analysis.simulation_id).order_by(
                    data_stage02_physiology_analysis.simulation_id.asc()).all();
            simulation_ids_O = [];
            if data: 
                for d in data:
                    simulation_ids_O.append(d.simulation_id);
            return simulation_ids_O;
        except SQLAlchemyError as e:
            print(e);
    # query simulation_id
    def getJoin_analysisID_dataStage02PhysiologyAnalysisAndSimulation(self,analysis_id_I):
        '''Query simulations that are used for the anlaysis'''
        try:
            data = self.session.query(data_stage02_physiology_analysis.analysis_id,
                    data_stage02_physiology_analysis.simulation_id,
                    data_stage02_physiology_simulation.experiment_id,
                    data_stage02_physiology_simulation.model_id,
                    data_stage02_physiology_simulation.sample_name_abbreviation,
                    data_stage02_physiology_simulation.simulation_type).filter(
                    data_stage02_physiology_analysis.analysis_id.like(analysis_id_I),
                    data_stage02_physiology_simulation.simulation_id.like(data_stage02_physiology_analysis.simulation_id),
                    data_stage02_physiology_analysis.used_.is_(True)).order_by(
                    data_stage02_physiology_analysis.simulation_id.asc()).all();
            rows_O = [d._asdict() for d in data];
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
