#SBaaS
from .stage02_physiology_graphData_io import stage02_physiology_graphData_io
from SBaaS_models.models_COBRA_execute import models_COBRA_execute
from .stage02_physiology_analysis_query import stage02_physiology_analysis_query
#System
import copy

class stage02_physiology_graphData_execute(stage02_physiology_graphData_io):
    def execute_findShortestPaths(self,
            analysis_id_I,
            algorithms_params_I,
            nodes_startAndStop_I,
            exclusion_list_I=[],
            weights_I=[]
            ):
        '''
        compute the shortest paths
        INPUT:
        model_id_I
        algorithms_params_I
        nodes_startAndStop_I
        simulation_id_I
        exclusion_list_I
        OUTPUT:

        '''
        exCOBRA01 = models_COBRA_execute(self.session,self.engine,self.settings);
        exCOBRA01.initialize_supportedTables();
        physiology_analysis_query = stage02_physiology_analysis_query(self.session,self.engine,self.settings);
        physiology_analysis_query.initialize_supportedTables();

        data_O=[];
        data_graphs_O=[];

        rows = physiology_analysis_query.getJoin_analysisID_dataStage02PhysiologyAnalysisAndSimulation(analysis_id_I);

        for row in rows:
            weights = [];
            if type(weights_I)==type([]):
                weights = weights_I;
                weights_str = '[]';
            elif type(weights_I)==type(''):
                if weights_I == 'stage02_physiology_sampledData_query':
                    weights = self.import_graphWeights_sampledData(row['simulation_id']);
                    weights_str = 'stage02_physiology_sampledData_query';
                elif weights_I == 'stage02_physiology_simulatedData_query':
                    weights = self.import_graphWeights_simulatedData(row['simulation_id']);
                    weights_str = 'stage02_physiology_simulatedData_query';
                else:
                    print('weights source not recognized');

            # run the analysis for different algorithms/params
            for ap in algorithms_params_I:
                shortestPaths = exCOBRA01.execute_findShortestPath_nodes(
                    row['model_id'],
                    nodes_startAndStop_I = nodes_startAndStop_I,
                    algorithm_I=ap['algorithm'],
                    exclusion_list_I=exclusion_list_I,
                    params_I=ap['params'],    
                    weights_I=weights
                    )
                for sp in shortestPaths:
                    tmp = {};
                    tmp['analysis_id']=analysis_id_I
                    tmp['simulation_id']=row['simulation_id']
                    tmp['weights']=weights_str;
                    tmp['used_']=True;
                    tmp['comment_']=None;
                    tmp['params']=sp['params']
                    tmp['path_start']=sp['start']
                    tmp['algorithm']=sp['algorithm']
                    tmp1 = copy.copy(tmp);
                    tmp1['path_stop']=sp['stop']
                    tmp1['path_n']=sp['path_n']
                    tmp1['path_iq_1']=sp['path_iq_1']
                    tmp1['path_var']=sp['path_var']
                    tmp1['path_ci_lb']=sp['path_ci_lb']
                    tmp1['path_cv']=sp['path_cv']
                    tmp1['path_iq_3']=sp['path_iq_3']
                    tmp1['path_ci_ub']=sp['path_ci_ub']
                    tmp1['path_average']=sp['path_average']
                    tmp1['path_max']=sp['path_max']
                    tmp1['path_median']=sp['path_median']
                    tmp1['path_ci_level']=sp['path_ci_level']
                    tmp1['path_min']=sp['path_min']
                    data_O.append(tmp1);
                    for path in sp['all_paths']:
                        tmp2 = copy.copy(tmp);
                        tmp2['paths']=path;
                        data_graphs_O.append(tmp2);
                #for sp in shortestPaths:
                #dict_keys(['stop', 'params', 'path_n', 'all_paths', 'path_iq_1', 'path_var', 'path_ci_lb', 'path_cv', 'path_iq_3', 'path_ci_ub', 'path_average', 'path_max', 'path_median', 'start', 'algorithm', 'path_ci_level', 'path_min'])
                #    str = "start: %s, stop: %s, min: %s, max: %s, average: %s, " \
                #            %(sp['start'],sp['stop'],sp['path_min'],
                #              sp['path_max'],sp['path_average'])
                #    print(str)

        self.add_rows_table('data_stage02_physiology_graphData_shortestPathStats',data_O);
        self.add_rows_table('data_stage02_physiology_graphData_shortestPaths',data_graphs_O);