# System
import json
# SBaaS
from .stage02_physiology_graphData_query import stage02_physiology_graphData_query
from SBaaS_base.sbaas_template_io import sbaas_template_io
from .stage02_physiology_sampledData_query import stage02_physiology_sampledData_query
from .stage02_physiology_simulatedData_query import stage02_physiology_simulatedData_query
# Resources
from io_utilities.base_importData import base_importData
from io_utilities.base_exportData import base_exportData
from ddt_python.ddt_container_filterMenuAndChart2dAndTable import ddt_container_filterMenuAndChart2dAndTable

class stage02_physiology_graphData_io(stage02_physiology_graphData_query,
                                     sbaas_template_io):
    def import_graphWeights_sampledData(self,simulation_id_I):
        '''
        import weights from sampled data
        INPUT:
        simulation_id_I
        
        '''
        qSampledData01 = stage02_physiology_sampledData_query(self.session,self.engine,self.settings);
        qSampledData01.initialize_supportedTables();

        rows=qSampledData01.get_rows_simulationID_dataStage02PhysiologySampledData(
            simulation_id_I,
            );

        weights = {d['rxn_id']:d['sampling_ave'] for d in rows};
        weights_reverse = {d['rxn_id']+'_reverse':-d['sampling_ave'] for d in rows};
        weights.update(weights_reverse);
        return weights;

    def import_graphWeights_simulatedData(self,simulation_id_I):
        '''
        import weights from sampled data
        INPUT:
        simulation_id_I
        
        TODO: get_rows_simulationID_dataStage02PhysiologySimulatedData does not exist
        '''
        qSimulatedData01 = stage02_physiology_simulatedData_query(self.session,self.engine,self.settings);
        qSimulatedData01.initialize_supportedTables();
        qSimulatedData01.initialize_tables();

        rows=qSimulatedData01.get_rows_simulationID_dataStage02PhysiologySimulatedData(
            simulation_id_I,
            );

        weights = {d['rxn_id']:d['fba_flux'] for d in rows};
        weights_reverse = {d['rxn_id']+'_reverse':-d['fba_flux'] for d in rows};
        weights.update(weights_reverse);
        return weights;

    def export_graphDataShortestPaths_js(self,analysis_id_I,data_dir_I='tmp'):
        '''export graph of shortest paths'''

        if data_dir_I=='tmp':
            filename_str = self.settings['visualization_data'] + '/tmp/ddt_data.js'
        elif data_dir_I=='data_json':
            data_json_O = ddtutilities.get_allObjects_js();
            return data_json_O;
        with open(filename_str,'w') as file:
            file.write(ddtutilities.get_allObjects());

    def export_graphDataShortestPathStats_js(self,analysis_id_I,data_dir_I='tmp'):
        '''export descriptive stats of shortest paths'''

        if data_dir_I=='tmp':
            filename_str = self.settings['visualization_data'] + '/tmp/ddt_data.js'
        elif data_dir_I=='data_json':
            data_json_O = ddtutilities.get_allObjects_js();
            return data_json_O;
        with open(filename_str,'w') as file:
            file.write(ddtutilities.get_allObjects());