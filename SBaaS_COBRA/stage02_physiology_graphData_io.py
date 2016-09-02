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
from ddt_python.ddt_container import ddt_container
import numpy as np

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

    def export_dataStage02PhysiologyGraphDataShortestPaths_js(self,analysis_id_I,data_dir_I='tmp'):
        '''export graph of shortest paths'''

        data_O = [];
        data_tmp = self.get_rows_analysisID_dataStage02PhysiologyGraphDataShortestPaths(analysis_id_I);
        for d in data_tmp:
            d['path_id'] = d['path_start'] + '-->' + d['path_stop']
            if np.isnan(d['path_ci_lb']):d['path_ci_lb']=d['path_average'];
            if np.isnan(d['path_ci_ub']):d['path_ci_ub']=d['path_average'];
            data_O.append(d);

        # break into individual reactions
        data_reactions = [];
        for d in data_O:
            d['flux']=1;
            left = dependencies.convert_bioCycList2List(d['left']);
            right = dependencies.convert_bioCycList2List(d['right']);
            reaction = d['gene'];
            for l in left:
                tmp = copy.copy(d);
                tmp['left'] = l;
                tmp['right'] = reaction;
                data_reactions.append(tmp);
            for r in right:
                tmp = copy.copy(d);
                tmp['left'] = reaction;
                tmp['right'] = r;
                data_reactions.append(tmp);

        # make the data parameters
        data1_keys = [
                    'gene',
                    'parent_classes',
                    'left',
                    'right',
                    'in_pathway',
                    'name'
                    ];
        data1_nestkeys = [
            'left',
            #'name',
            'right',
                          ];
        data1_keymap = {'xdata':'parent_classes',
                        'ydata':'mode',
                        'serieslabel':'mode',
                        'featureslabel':''};

        data2_keymap = {
            'xdata':'parent_classes',
            'ydata':'flux',
            'xdatalabel':'parent_classes',
            'ydatalabel':'name',
            'serieslabel':'regulator',
            'featureslabel':'transcription_unit',
            #'tooltiplabel':'component_name',
            };

        svgparameters = {
            "svgmargin":{ 'top': 100, 'right': 100, 'bottom': 100, 'left': 100 },
            "svgwidth":500,
            "svgheight":500,
            "svgduration":750,
            'colclass':"col-sm-12",
            'svgcolorcategory':'blue2red64',
            'svgcolordomain':'min,max',
			'svgcolordatalabel':'parent_classes',
            'svgcolorscale':'quantile',
            };
        
        nsvgtable = ddt_container_filterMenuAndChart2dAndTable();
        nsvgtable.make_filterMenuAndChart2dAndTable(
            data_filtermenu=data_reactions,
            data_filtermenu_keys=data1_keys,
            data_filtermenu_nestkeys=data1_nestkeys,
            data_filtermenu_keymap=data1_keymap,
            data_svg_keys=None,
            data_svg_nestkeys=None,
            data_svg_keymap=data2_keymap,
            data_table_keys=None,
            data_table_nestkeys=None,
            data_table_keymap=None,
            data_svg=None,
            data_table=None,
            #svgtype='sankeydiagram2d_01',
            svgtype='forcedirectedgraph2d_01',
            tabletype='responsivetable_01',
            svgx1axislabel='',
            svgy1axislabel='',
            tablekeymap = [data1_keymap],
            svgkeymap = [data2_keymap],
            formtile2datamap=[0],
            tabletile2datamap=[0],
            svgtile2datamap=[0],
            svgfilters=None,
            svgtileheader='BioCyc Reaction',
            tablefilters=None,
            tableheaders=None,
            svgparameters_I= svgparameters,
            );

        if data_dir_I=='tmp':
            filename_str = self.settings['visualization_data'] + '/tmp/ddt_data.js'
        elif data_dir_I=='data_json':
            data_json_O = nsvgtable.get_allObjects_js();
            return data_json_O;
        with open(filename_str,'w') as file:
            file.write(nsvgtable.get_allObjects());

    def export_dataStage02PhysiologyGraphDataShortestPathStats_js(self,
                analysis_id_I,
                plot_points_I=False,
                vertical_I=True,
                data_dir_I='tmp'):
        '''export descriptive stats of shortest paths'''
        
        data_O = [];
        data_points_O = [];
        if plot_points_I:
        #get the replicate data for the analysis
            #TODO... (copy code from above io function)
            #data_points_O = [];
            #data_points_O = quantification_dataPreProcessing_replicates_query.get_rowsAndSampleNameAbbreviations_analysisID_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I);
            data_tmp = self.get_rows_analysisID_dataStage02PhysiologyGraphDataShortestPathStats(analysis_id_I);
            for d in data_tmp:
                d['path_id'] = d['path_start'] + '-->' + d['path_stop']
                if np.isnan(d['path_ci_lb']):d['path_ci_lb']=d['path_average'];
                if np.isnan(d['path_ci_ub']):d['path_ci_ub']=d['path_average'];
                data_O.append(d);
        else:
            data_tmp = self.get_rows_analysisID_dataStage02PhysiologyGraphDataShortestPathStats(analysis_id_I);
            for d in data_tmp:
                d['path_id'] = d['path_start'] + '-->' + d['path_stop']
                if np.isnan(d['path_ci_lb']):d['path_ci_lb']=d['path_average'];
                if np.isnan(d['path_ci_ub']):d['path_ci_ub']=d['path_average'];
                data_O.append(d);
        # make the tile objects
        parametersobject_O = [];
        tile2datamap_O = {};
        filtermenuobject_O = [];
        dataobject_O = [];
        # dump chart parameters to a js files
        data1_keys = [
            #'analysis_id',
                      'simulation_id',
                      'path_start',
                      'path_stop',
                      'algorithm',
                    ];
        data1_nestkeys = ['path_id'];
        data2_keys = [
            #'analysis_id',
                      'simulation_id',
                      'path_start',
                      'path_stop',
                      'algorithm',
                    ];
        data2_nestkeys = ['path_id'];
        if vertical_I:
            data1_keymap = {
                        'xdata':'path_id',
                        'ydata':'path_average',
                        'ydatamean':'path_average',
                        'ydatalb':'path_ci_lb',
                        'ydataub':'path_ci_ub',
                        'ydatamin':'path_min',
                        'ydatamax':'path_max',
                        'ydataiq1':'path_iq_1',
                        'ydataiq3':'path_iq_3',
                        'ydatamedian':'path_median',
                        #'serieslabel':'simulation_id',
                        'serieslabel':'algorithm',
                        'featureslabel':'path_id'};
            data2_keymap = {
                        'xdata':'path_id',
                        'ydata':'path_length',
                        #'serieslabel':'simulation_id',
                        'serieslabel':'algorithm',
                        'featureslabel':'path_id'};
        else:
            data1_keymap = {
                        'ydata':'path_id',
                        'xdatamean':'path_average',
                        'xdata':'path_average',
                        'xdatalb':'path_ci_lb',
                        'xdataub':'path_ci_ub',
                        'xdatamin':'path_min',
                        'xdatamax':'path_max',
                        'xdataiq1':'path_iq_1',
                        'xdataiq3':'path_iq_3',
                        'xdatamedian':'path_median',
                        #'serieslabel':'simulation_id',
                        'serieslabel':'algorithm',
                        'featureslabel':'path_id'};
            data2_keymap = {
                        'ydata':'path_id',
                        'xdata':'path_length',
                        #'serieslabel':'simulation_id',
                        'serieslabel':'algorithm',
                        'featureslabel':'path_id'};

        # make the data object
        dataobject_O.append({"data":data_O,"datakeys":data1_keys,"datanestkeys":data1_nestkeys});

        # make the tile parameter objects
        formtileparameters_O = {'tileheader':'Filter menu','tiletype':'html','tileid':"filtermenu1",'rowid':"row1",'colid':"col1",
            'tileclass':"panel panel-default",'rowclass':"row",'colclass':"col-sm-4"};
        formparameters_O = {'htmlid':'filtermenuform1',"htmltype":'form_01',"formsubmitbuttonidtext":{'id':'submit1','text':'submit'},"formresetbuttonidtext":{'id':'reset1','text':'reset'},"formupdatebuttonidtext":{'id':'update1','text':'update'}};
        formtileparameters_O.update(formparameters_O);
        parametersobject_O.append(formtileparameters_O);
        if plot_points_I:
            tile2datamap_O.update({"filtermenu1":[1]});
        else:
            tile2datamap_O.update({"filtermenu1":[0]});
        
        #make the svg object
        if plot_points_I and vertical_I:
            dataobject_O.append({"data":data_points_O,"datakeys":data2_keys,"datanestkeys":data2_nestkeys});
            svgparameters_O = {"svgtype":'boxandwhiskersplot2d_02',
                               "svgkeymap":[data1_keymap,data2_keymap],
                                'svgid':'svg1',
                                "svgmargin":{ 'top': 50, 'right': 150, 'bottom': 50, 'left': 50 },
                                "svgwidth":500,"svgheight":350,
                                "svgx1axislabel":"path id",
                                "svgy1axislabel":"path length",
                                "svgdata2pointsradius":5.0,
    						    };
            svgtileparameters_O = {'tileheader':'Custom box and whiskers plot','tiletype':'svg','tileid':"tile2",'rowid':"row1",'colid':"col2",
                'tileclass':"panel panel-default",'rowclass':"row",'colclass':"col-sm-8"};
            svgtileparameters_O.update(svgparameters_O);
            parametersobject_O.append(svgtileparameters_O);
            tile2datamap_O.update({"tile2":[0,1]});
        elif not plot_points_I and vertical_I:
            svgparameters_O = {"svgtype":'boxandwhiskersplot2d_01',
                               "svgkeymap":[data1_keymap],
                                'svgid':'svg1',
                                "svgmargin":{ 'top': 50, 'right': 150, 'bottom': 50, 'left': 50 },
                                "svgwidth":500,"svgheight":350,
                                "svgx1axislabel":"path id",
                                "svgy1axislabel":"path length",
    						    'svgformtileid':'filtermenu1','svgresetbuttonid':'reset1','svgsubmitbuttonid':'submit1'};
            svgtileparameters_O = {'tileheader':'Custom box and whiskers plot','tiletype':'svg','tileid':"tile2",'rowid':"row1",'colid':"col2",
                'tileclass':"panel panel-default",'rowclass':"row",'colclass':"col-sm-8"};
            svgtileparameters_O.update(svgparameters_O);
            parametersobject_O.append(svgtileparameters_O);
            tile2datamap_O.update({"tile2":[0]});
        elif plot_points_I and not vertical_I:
            dataobject_O.append({"data":data_points_O,"datakeys":data2_keys,"datanestkeys":data2_nestkeys});
            svgparameters_O = {"svgtype":'horizontalBoxAndWhiskersPlot2d_02',
                               "svgkeymap":[data1_keymap,data2_keymap],
                                'svgid':'svg1',
                                "svgmargin":{ 'top': 50, 'right': 150, 'bottom': 50, 'left': 50 },
                                "svgwidth":500,"svgheight":350,
                                "svgx1axislabel":"path length",
                                "svgy1axislabel":"path id",
                                "svgdata2pointsradius":5.0,
    						    };
            svgtileparameters_O = {'tileheader':'Custom box and whiskers plot','tiletype':'svg','tileid':"tile2",'rowid':"row1",'colid':"col2",
                'tileclass':"panel panel-default",'rowclass':"row",'colclass':"col-sm-8"};
            svgtileparameters_O.update(svgparameters_O);
            parametersobject_O.append(svgtileparameters_O);
            tile2datamap_O.update({"tile2":[0,1]});
        elif not plot_points_I and not vertical_I:
            svgparameters_O = {"svgtype":'horizontalBoxAndWhiskersPlot2d_01',
                               "svgkeymap":[data1_keymap],
                                'svgid':'svg1',
                                "svgmargin":{ 'top': 50, 'right': 150, 'bottom': 50, 'left': 50 },
                                "svgwidth":500,"svgheight":350,
                                "svgx1axislabel":"path length",
                                "svgy1axislabel":"path id",
    						    'svgformtileid':'filtermenu1','svgresetbuttonid':'reset1','svgsubmitbuttonid':'submit1'};
            svgtileparameters_O = {'tileheader':'Custom box and whiskers plot','tiletype':'svg','tileid':"tile2",'rowid':"row1",'colid':"col2",
                'tileclass':"panel panel-default",'rowclass':"row",'colclass':"col-sm-8"};
            svgtileparameters_O.update(svgparameters_O);
            parametersobject_O.append(svgtileparameters_O);
            tile2datamap_O.update({"tile2":[0]});

        #make the table object
        tableparameters_O = {"tabletype":'responsivetable_01',
                    'tableid':'table1',
                    "tablefilters":None,
                    "tableclass":"table  table-condensed table-hover",
    			    'tableformtileid':'filtermenu1','tableresetbuttonid':'reset1','tablesubmitbuttonid':'submit1'};
        tabletileparameters_O = {'tileheader':'descriptiveStats','tiletype':'table','tileid':"tile3",'rowid':"row2",'colid':"col1",
            'tileclass':"panel panel-default",'rowclass':"row",'colclass':"col-sm-12"};
        tabletileparameters_O.update(tableparameters_O);
        parametersobject_O.append(tabletileparameters_O);
        tile2datamap_O.update({"tile3":[0]});

        # dump the data to a json file
        ddtutilities = ddt_container(parameters_I = parametersobject_O,data_I = dataobject_O,tile2datamap_I = tile2datamap_O,filtermenu_I = filtermenuobject_O);

        if data_dir_I=='tmp':
            filename_str = self.settings['visualization_data'] + '/tmp/ddt_data.js'
        elif data_dir_I=='data_json':
            data_json_O = ddtutilities.get_allObjects_js();
            return data_json_O;
        with open(filename_str,'w') as file:
            file.write(ddtutilities.get_allObjects());