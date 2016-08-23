# System
import json
# SBaaS
from .stage02_physiology_sampledData_query import stage02_physiology_sampledData_query
from .stage02_physiology_analysis_query import stage02_physiology_analysis_query
from SBaaS_base.sbaas_template_io import sbaas_template_io
# Resources
from io_utilities.base_importData import base_importData
from io_utilities.base_exportData import base_exportData
from listDict.listDict import listDict
from .sampling import cobra_sampling,cobra_sampling_n
from python_statistics.calculate_histogram import calculate_histogram
from ddt_python.ddt_container_filterMenuAndChart2dAndTable import ddt_container_filterMenuAndChart2dAndTable
from ddt_python.ddt_container import ddt_container


class stage02_physiology_sampledData_io(stage02_physiology_sampledData_query,
                                        sbaas_template_io):
    def import_dataStage02PhysiologySamplingParameters_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_dataStage02PhysiologySamplingParameters(data.data);
        data.clear_data();
    def import_dataStage02PhysiologySamplingParameters_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage02PhysiologySamplingParameters(data.data);

    def export_dataStage02PhysiologySampledPoints_js(self,
        analysis_id_I,
        simulation_ids_I = [],
        rxn_ids_I = [],
        query_I={},
        data_dir_I='tmp'
        ):
        '''Visualize the sampling distribution
        DESCRIPTION:
        tile1=filtermenu
        tile2=sampling distribution
        tile3=table
        '''
        calculatehistogram = calculate_histogram();
        physiology_analysis_query = stage02_physiology_analysis_query(self.session,self.engine,self.settings);
        data_sampledPoints_O = [];
        data_O = [];
        #get the analysis info
        simulation_ids = physiology_analysis_query.get_simulationID_analysisID_dataStage02PhysiologyAnalysis(analysis_id_I);
        if simulation_ids_I:
            simulation_ids = [s for s in simulation_ids if s in simulation_ids_I];
        for simulation_id in simulation_ids:
            #get the data_dirs for the simulations and read in the points
            sampledPoints = self.get_rows_simulationID_dataStage02PhysiologySampledPoints(simulation_id);
            sampledPoints = sampledPoints[0];
            data_sampledPoints_O.append(sampledPoints);
            # get simulation information
            simulation_info_all = [];
            simulation_info_all = self.get_rows_simulationIDAndSimulationType_dataStage02PhysiologySimulation(simulation_id,'sampling');
            if not simulation_info_all:
                print('simulation not found!')
                return;
            simulation_info = simulation_info_all[0]; # unique constraint guarantees only 1 row will be returned
            # get simulation parameters
            simulation_parameters_all = [];
            simulation_parameters_all = self.get_rows_simulationID_dataStage02PhysiologySamplingParameters(simulation_id);
            if not simulation_parameters_all:
                print('simulation not found!')
                return;
            simulation_parameters = simulation_parameters_all[0]; # unique constraint guarantees only 1 row will be returned
            #fill the sampledData with the actual points
            sampling = cobra_sampling(model_I=None,data_dir_I = sampledPoints['data_dir'],loops_I=sampledPoints['infeasible_loops']);
            if simulation_parameters['sampler_id']=='gpSampler':
                # load the results of sampling
                sampling.get_points_matlab(matlab_data=None,sampler_model_name='sampler_out');
                sampling.remove_loopsFromPoints();
            elif simulation_parameters['sampler_id']=='optGpSampler':
                sampling.get_points_json();
                sampling.remove_loopsFromPoints();
            else:
                print('sampler_id not recognized');
            #store the sampledPoints
            for k,v in sampling.points.items():
                if rxn_ids_I: 
                    if not k in rxn_ids_I: 
                        continue;
                n_bins = 100;
                calc_bins_I = False;
                x_O,dx_O,y_O = calculatehistogram.histogram(data_I=v,n_bins_I=n_bins,calc_bins_I=calc_bins_I);
                for i,b in enumerate(x_O):
                    tmp = {
                        'simulation_id':simulation_id,
                        'rxn_id':k,
                        #'feature_units':feature_units,
                        'bin':b,
                        'bin_width':dx_O[i],
                        'frequency':int(y_O[i]),
                        'used_':True,
                        'comment_':None};
                    data_O.append(tmp);
            #data_listDict = listDict();
            #data_listDict.set_dictList(sampling.points);
            #data_listDict.convert_dictList2DataFrame();
            #points, rxn_ids = data_listDict.get_flattenedDataAndColumnLabels();
            #data_listDict.clear_allData();
            #data_listDict.add_column2DataFrame('rxn_id',rxn_ids);
            #data_listDict.add_column2DataFrame('points',points);
            #data_listDict.add_column2DataFrame('simulation_id',simulation_id);
            #data_listDict.convert_dataFrame2ListDict();
            #data_O.extend(data_listDict.get_listDict());
        #make the DDT histograms  
        # visualization parameters
        data1_keys = ['simulation_id',
                      'rxn_id',
                      'bin',
                      ];
        data1_nestkeys = [
            'bin'
            ];
        data1_keymap = {
                'xdata':'bin',
                'ydata':'frequency',
                'serieslabel':'simulation_id',
                'featureslabel':'bin',
                'tooltiplabel':'rxn_id',
                'ydatalb':None,
                'ydataub':None};
        
        
        nsvgtable = ddt_container_filterMenuAndChart2dAndTable();
        nsvgtable.make_filterMenuAndChart2dAndTable(
            data_filtermenu=data_O,
            data_filtermenu_keys=data1_keys,
            data_filtermenu_nestkeys=data1_nestkeys,
            data_filtermenu_keymap=data1_keymap,
            data_svg_keys=None,
            data_svg_nestkeys=None,
            data_svg_keymap=None,
            data_table_keys=None,
            data_table_nestkeys=None,
            data_table_keymap=None,
            data_svg=None,
            data_table=None,
            svgtype='verticalbarschart2d_01',
            tabletype='responsivetable_01',
            svgx1axislabel='',
            svgy1axislabel='',
            tablekeymap = [data1_keymap],
            svgkeymap = [data1_keymap],
            formtile2datamap=[0],
            tabletile2datamap=[0],
            svgtile2datamap=[0], #calculated on the fly
            svgfilters=None,
            svgtileheader='Sampled points',
            tablefilters=None,
            tableheaders=None
            );

        if data_dir_I=='tmp':
            filename_str = self.settings['visualization_data'] + '/tmp/ddt_data.js'
        elif data_dir_I=='data_json':
            data_json_O = nsvgtable.get_allObjects_js();
            return data_json_O;
        with open(filename_str,'w') as file:
            file.write(nsvgtable.get_allObjects());
            
    def export_dataStage02PhysiologySampledPointsDescriptiveStats_js(self,analysis_id_I,plot_points_I=True,vertical_I=True,data_dir_I='tmp'):
        '''Export data for a box and whiskers plot
        INPUT:
        analysis_id_I = string,
        plot_points_I = boolean, default=False, raw data points will not be plotted on the same plot
        vertical_I = boolean, default=True, orient the boxes vertical as opposed to horizontal
        '''
        physiology_analysis_query=stage02_physiology_analysis_query(self.session,self.engine,self.settings);
        physiology_analysis_query.initialize_supportedTables();

        data_O = [];
        data_points_O = [];
        #get the analysis information
        simulation_ids = [];
        simulation_ids = physiology_analysis_query.get_simulationID_analysisID_dataStage02PhysiologyAnalysis(analysis_id_I);
        #get the data for the analysis
        if plot_points_I:
        #get the replicate data for the analysis
            #TODO... (copy code from above io function)
            #data_points_O = [];
            #data_points_O = quantification_dataPreProcessing_replicates_query.get_rowsAndSampleNameAbbreviations_analysisID_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I);
            for simulation in simulation_ids:
                data_tmp = self.get_rows_simulationID_dataStage02PhysiologySampledData(simulation);
                data_O.extend(data_tmp);
        else:
            for simulation in simulation_ids:
                data_tmp = self.get_rows_simulationID_dataStage02PhysiologySampledData(simulation);
                data_O.extend(data_tmp);
        # make the tile objects
        parametersobject_O = [];
        tile2datamap_O = {};
        filtermenuobject_O = [];
        dataobject_O = [];
        # dump chart parameters to a js files
        data1_keys = [
            #'analysis_id',
                      'simulation_id',
                      'simulation_dateAndTime',
                      'rxn_id',
                      'flux_units',
                    ];
        data1_nestkeys = ['rxn_id'];
        data2_keys = [
            #'analysis_id',
                      'simulation_id',
                      'simulation_dateAndTime',
                      'rxn_id',
                      'flux_units',
                    ];
        data2_nestkeys = ['rxn_id'];
        if vertical_I:
            data1_keymap = {
                        'xdata':'rxn_id',
                        'ydata':'sampling_ave',
                        'ydatamean':'sampling_ave',
                        'ydatalb':'sampling_lb',
                        'ydataub':'sampling_ub',
                        'ydatamin':'sampling_min',
                        'ydatamax':'sampling_max',
                        'ydataiq1':'sampling_iq_1',
                        'ydataiq3':'sampling_iq_3',
                        'ydatamedian':'sampling_median',
                        'serieslabel':'simulation_id',
                        'featureslabel':'rxn_id'};
            data2_keymap = {
                        'xdata':'rxn_id',
                        'ydata':'sampling_points',
                        'serieslabel':'simulation_id',
                        'featureslabel':'rxn_id'};
        else:
            data1_keymap = {
                        'ydata':'rxn_id',
                        'xdatamean':'sampling_ave',
                        'xdata':'sampling_ave',
                        'xdatalb':'sampling_lb',
                        'xdataub':'sampling_ub',
                        'xdatamin':'sampling_min',
                        'xdatamax':'sampling_max',
                        'xdataiq1':'sampling_iq_1',
                        'xdataiq3':'sampling_iq_3',
                        'xdatamedian':'sampling_median',
                        'serieslabel':'simulation_id',
                        'featureslabel':'rxn_id'};
            data2_keymap = {
                        'ydata':'rxn_id',
                        'xdata':'sampling_points',
                        'serieslabel':'simulation_id',
                        'featureslabel':'rxn_id'};

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
                                "svgx1axislabel":"rxn_id",
                                "svgy1axislabel":"sampling points",
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
                                "svgx1axislabel":"rxn_id","svgy1axislabel":"sampling points",
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
                                "svgx1axislabel":"sampling points",
                                "svgy1axislabel":"rxn_id",
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
                                "svgx1axislabel":"sampling points",
                                "svgy1axislabel":"rxn_id",
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
    def export_dataStage02PhysiologySampledPointsMetabolitesDescriptiveStats_js(self,analysis_id_I,plot_points_I=True,vertical_I=True,data_dir_I='tmp'):
        '''Export data for a box and whiskers plot
        INPUT:
        analysis_id_I = string,
        plot_points_I = boolean, default=False, raw data points will not be plotted on the same plot
        vertical_I = boolean, default=True, orient the boxes vertical as opposed to horizontal
        '''
        physiology_analysis_query=stage02_physiology_analysis_query(self.session,self.engine,self.settings);
        physiology_analysis_query.initialize_supportedTables();

        data_O = [];
        data_points_O = [];
        #get the analysis information
        simulation_ids = [];
        simulation_ids = physiology_analysis_query.get_simulationID_analysisID_dataStage02PhysiologyAnalysis(analysis_id_I);
        #get the data for the analysis
        if plot_points_I:
        #get the replicate data for the analysis
            #TODO... (copy code from above io function)
            #data_points_O = [];
            #data_points_O = quantification_dataPreProcessing_replicates_query.get_rowsAndSampleNameAbbreviations_analysisID_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I);
            for simulation in simulation_ids:
                data_tmp = self.get_rows_simulationID_dataStage02PhysiologySampledMetaboliteData(simulation);
                data_O.extend(data_tmp);
        else:
            for simulation in simulation_ids:
                data_tmp = self.get_rows_simulationID_dataStage02PhysiologySampledMetaboliteData(simulation);
                data_O.extend(data_tmp);
        # make the tile objects
        parametersobject_O = [];
        tile2datamap_O = {};
        filtermenuobject_O = [];
        dataobject_O = [];
        # dump chart parameters to a js files
        data1_keys = [
            #'analysis_id',
                      'simulation_id',
                      'simulation_dateAndTime',
                      'met_id',
                      'flux_units',
                    ];
        data1_nestkeys = ['met_id'];
        data2_keys = [
            #'analysis_id',
                      'simulation_id',
                      'simulation_dateAndTime',
                      'rxn_id',
                      'flux_units',
                    ];
        data2_nestkeys = ['met_id'];
        if vertical_I:
            data1_keymap = {
                        'xdata':'met_id',
                        'ydata':'sampling_ave',
                        'ydatamean':'sampling_ave',
                        'ydatalb':'sampling_lb',
                        'ydataub':'sampling_ub',
                        'ydatamin':'sampling_min',
                        'ydatamax':'sampling_max',
                        'ydataiq1':'sampling_iq_1',
                        'ydataiq3':'sampling_iq_3',
                        'ydatamedian':'sampling_median',
                        'serieslabel':'simulation_id',
                        'featureslabel':'met_id'};
            data2_keymap = {
                        'xdata':'met_id',
                        'ydata':'sampling_points',
                        'serieslabel':'simulation_id',
                        'featureslabel':'met_id'};
        else:
            data1_keymap = {
                        'ydata':'met_id',
                        'xdatamean':'sampling_ave',
                        'xdata':'sampling_ave',
                        'xdatalb':'sampling_lb',
                        'xdataub':'sampling_ub',
                        'xdatamin':'sampling_min',
                        'xdatamax':'sampling_max',
                        'xdataiq1':'sampling_iq_1',
                        'xdataiq3':'sampling_iq_3',
                        'xdatamedian':'sampling_median',
                        'serieslabel':'simulation_id',
                        'featureslabel':'met_id'};
            data2_keymap = {
                        'ydata':'met_id',
                        'xdata':'sampling_points',
                        'serieslabel':'simulation_id',
                        'featureslabel':'met_id'};

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
                                "svgx1axislabel":"met_id",
                                "svgy1axislabel":"sampling points",
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
                                "svgx1axislabel":"met_id","svgy1axislabel":"sampling points",
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
                                "svgx1axislabel":"sampling points",
                                "svgy1axislabel":"rxn_id",
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
                                "svgx1axislabel":"sampling points",
                                "svgy1axislabel":"met_id",
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
    def export_dataStage02PhysiologySampledPointsSubsystemsDescriptiveStats_js(self,analysis_id_I,plot_points_I=True,vertical_I=True,data_dir_I='tmp'):
        '''Export data for a box and whiskers plot
        INPUT:
        analysis_id_I = string,
        plot_points_I = boolean, default=False, raw data points will not be plotted on the same plot
        vertical_I = boolean, default=True, orient the boxes vertical as opposed to horizontal
        '''
        physiology_analysis_query=stage02_physiology_analysis_query(self.session,self.engine,self.settings);
        physiology_analysis_query.initialize_supportedTables();

        data_O = [];
        data_points_O = [];
        #get the analysis information
        simulation_ids = [];
        simulation_ids = physiology_analysis_query.get_simulationID_analysisID_dataStage02PhysiologyAnalysis(analysis_id_I);
        #get the data for the analysis
        if plot_points_I:
        #get the replicate data for the analysis
            #TODO... (copy code from above io function)
            #data_points_O = [];
            #data_points_O = quantification_dataPreProcessing_replicates_query.get_rowsAndSampleNameAbbreviations_analysisID_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I);
            for simulation in simulation_ids:
                data_tmp = self.get_rows_simulationID_dataStage02PhysiologySampledSubsystemData(simulation);
                data_O.extend(data_tmp);
        else:
            for simulation in simulation_ids:
                data_tmp = self.get_rows_simulationID_dataStage02PhysiologySampledSubsystemData(simulation);
                data_O.extend(data_tmp);
        # make the tile objects
        parametersobject_O = [];
        tile2datamap_O = {};
        filtermenuobject_O = [];
        dataobject_O = [];
        # dump chart parameters to a js files
        data1_keys = [
            #'analysis_id',
                      'simulation_id',
                      'simulation_dateAndTime',
                      'subsystem_id',
                      'flux_units',
                    ];
        data1_nestkeys = ['subsystem_id'];
        data2_keys = [
            #'analysis_id',
                      'simulation_id',
                      'simulation_dateAndTime',
                      'rxn_id',
                      'flux_units',
                    ];
        data2_nestkeys = ['subsystem_id'];
        if vertical_I:
            data1_keymap = {
                        'xdata':'subsystem_id',
                        'ydata':'sampling_ave',
                        'ydatamean':'sampling_ave',
                        'ydatalb':'sampling_lb',
                        'ydataub':'sampling_ub',
                        'ydatamin':'sampling_min',
                        'ydatamax':'sampling_max',
                        'ydataiq1':'sampling_iq_1',
                        'ydataiq3':'sampling_iq_3',
                        'ydatamedian':'sampling_median',
                        'serieslabel':'simulation_id',
                        'featureslabel':'subsystem_id'};
            data2_keymap = {
                        'xdata':'subsystem_id',
                        'ydata':'sampling_points',
                        'serieslabel':'simulation_id',
                        'featureslabel':'subsystem_id'};
        else:
            data1_keymap = {
                        'ydata':'subsystem_id',
                        'xdatamean':'sampling_ave',
                        'xdata':'sampling_ave',
                        'xdatalb':'sampling_lb',
                        'xdataub':'sampling_ub',
                        'xdatamin':'sampling_min',
                        'xdatamax':'sampling_max',
                        'xdataiq1':'sampling_iq_1',
                        'xdataiq3':'sampling_iq_3',
                        'xdatamedian':'sampling_median',
                        'serieslabel':'simulation_id',
                        'featureslabel':'subsystem_id'};
            data2_keymap = {
                        'ydata':'subsystem_id',
                        'xdata':'sampling_points',
                        'serieslabel':'simulation_id',
                        'featureslabel':'subsystem_id'};

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
                                "svgx1axislabel":"subsystem_id",
                                "svgy1axislabel":"sampling points",
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
                                "svgx1axislabel":"subsystem_id","svgy1axislabel":"sampling points",
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
                                "svgx1axislabel":"sampling points",
                                "svgy1axislabel":"rxn_id",
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
                                "svgx1axislabel":"sampling points",
                                "svgy1axislabel":"subsystem_id",
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
   