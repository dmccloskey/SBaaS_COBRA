# Dependencies from cobra
from cobra.io.sbml import create_cobra_model_from_sbml_file
from cobra.flux_analysis import flux_variability_analysis
from cobra.flux_analysis.single_deletion import single_reaction_deletion,single_gene_deletion
from cobra.flux_analysis.objective import update_objective
from cobra.flux_analysis.parsimonious import optimize_minimal_flux
from cobra.flux_analysis.loopless import construct_loopless_model

import json, csv
from math import sqrt,exp,pow
from numpy import average, var, log

from io_utilities.base_exportData import base_exportData

class cobra_simulatedData():
    """Class to generate and handle COBRA simulated data"""

    def __init__(self,fva_data_I={},
                 sra_data_I={},
                 sga_data_I={},
                 fba_primal_data_I={},
                 fba_dual_data_I={}):
        if fva_data_I:
            self.fva_data = self._convert_fluxBounds2var(fva_data_I);
        else:
            self.fva_data = {}
        if sra_data_I:
            self.sra_data = sra_data_I;
        else:
            self.sra_data = {}
        if fba_primal_data_I:
            self.fba_primal_data = fba_primal_data_I;
        else:
            self.fba_primal_data = {}
        if fba_dual_data_I:
            self.fba_dual_data = fba_dual_data_I;
        else:
            self.fba_dual_data = {}
        if sga_data_I:
            self.sga_data = sra_data_I;
        else:
            self.sga_data = {}

    def check_data(self):
        '''check data integrity'''
        return

    def generate_sra_data(self, cobra_model, reaction_list=None,
                            method_I='fba', solver='cglpk'):
        '''Single reaction deletion analysis
        INPUT:
        method_I = string 'fba', 'moma'
        '''

        print('Single Reaction Deletion...')

        # single reaction deletion
        single_reaction_deletions = single_reaction_deletion(cobra_model,
                        #reaction_list=reaction_list,
                        method=method_I,
                        solver=solver
                        );

        # FBA
        cobra_model.optimize(solver=solver);

        for k,v in single_reaction_deletions[0].items():
            self.sra_data[k] = {'gr':None,'gr_ratio':None,'method':method_I};
            if v:
                self.sra_data[k] = {'gr':v,'gr_ratio':v/cobra_model.solution.f};

    def export_sra_data(self, filename):
        '''export sra data'''
        exportdata = base_exportData(self.sra_data);
        exportdata.write_dict2json(filename);

    def import_sra_data(self,filename):
        '''import sra data'''
        self.sra_data = json.load(open(filename));

    def generate_fva_data(self, cobra_model, fraction_of_optimum=0.9,
                                      objective_sense='maximize', reaction_list=None,
                                      allow_loops=True, solver='glpk'):

        print('FVA...')
        #add in loop law constrain
        if not allow_loops: cobra_model=construct_loopless_model(cobra_model);
        # calculate the reaction bounds using FVA
        self.fva_data = flux_variability_analysis(cobra_model, fraction_of_optimum=0.9,
                                      objective_sense='maximize', solver=solver,
                                      reaction_list=reaction_list,
                                      );

    def export_fva_data(self, filename):
        '''export fva data'''
        exportdata = base_exportData(self.fva_data);
        exportdata.write_dict2json(filename)


    def import_fva_data(self,filename):
        '''import fva data'''
        fva = json.load(open(filename));
        self.fva_data = self._convert_fluxBounds2var(fva);
        
    def _convert_fluxBounds2var(self, flux_bounds):
        """
        convert flux bounds from FVA to median and variance
    
        variance = (max - median)^2

        flux_bounds: {reaction.id: {'maximum': float, 'minimum': float}}

        returns a dictionary: {reaction.id: {'flux': float, 'flux_var': float, 'flux_units': 'mmol*gDW-1*hr-1'}

        """

        flux_bounds_O = {};
        for k,v in flux_bounds.items():
            median = (v['maximum'] - v['minimum'])/2;
            variance = (v['maximum'] - median)*(v['maximum'] - median);
            flux_bounds_O[k] = {'flux': median, 'flux_var': variance, 'flux_units': 'mmol*gDW-1*hr-1',
                                'flux_lb': v['minimum'], 'flux_ub': v['maximum']};

        return flux_bounds_O

    def generate_fba_data(self,cobra_model,allow_loops=True, method_I='fba',solver='glpk'):
        '''
        perform FBA simulation on the model
        INPUT:
        OUTPUT:
        '''
        #add in loop law constrain
        if not allow_loops: cobra_model=construct_loopless_model(cobra_model);
        #check for the optimization method:
        if method_I=='fba' or method_I=='loopless-fba':
            sol = cobra_model.optimize(solver=solver);
        elif method_I =='pfba' or method_I=='loopless-pfba':
            sol = optimize_minimal_flux(model=cobra_model,solver=solver);
        else:
            print('method not recognized.')
            return;
        
        self.fba_primal_data={};
        for k,v in sol.x_dict.items():
            self.fba_primal_data[k] = v;
        self.fba_dual_data={};
        for k,v in sol.y_dict.items():
            self.fba_dual_data[k] = v;

    def generate_sga_data(self, cobra_model, gene_list=None,
                            method_I='fba', solver='cglpk'):
        '''Single gene deletion analysis
        INPUT:
        method_I = string 'fba', 'moma'
        '''

        print('Single Reaction Deletion...')

        # single gene deletion
        single_gene_deletions = single_gene_deletion(cobra_model,
                        #gene_list=gene_list,
                        method=method_I,
                        solver=solver
                        );

        # FBA
        cobra_model.optimize(solver=solver);

        for k,v in single_gene_deletions[0].items():
            self.sga_data[k] = {'gr':None,'gr_ratio':None,'method':method_I};
            if v:
                self.sga_data[k] = {'gr':v,'gr_ratio':v/cobra_model.solution.f};

    def export_sga_data(self, filename):
        '''export sga data'''
        exportdata = base_exportData(self.sga_data);
        exportdata.write_dict2json(filename);

    def import_sga_data(self,filename):
        '''import sga data'''
        self.sga_data = json.load(open(filename));

    #TODO:
    def reduce_model(self,cobra_model,method_I='fba',solver='cglpk'):
        '''reduce the model'''
        pass;
    def generate_fluxSum_data(self,cobra_model,method_I='fba',solver='cglpk'):
        '''
        perform a fluxSum analysis
        INPUT:
        '''
        pass;