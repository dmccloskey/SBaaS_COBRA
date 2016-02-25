# Dependencies from cobra
from cobra.io.sbml import create_cobra_model_from_sbml_file
from cobra.flux_analysis import flux_variability_analysis
from cobra.flux_analysis import single_deletion
from cobra.flux_analysis.objective import update_objective
from cobra.flux_analysis.parsimonious import optimize_minimal_flux

import json, csv
from math import sqrt,exp,pow
from numpy import average, var, log

from io_utilities.base_exportData import base_exportData

class cobra_simulatedData(thermodynamics_io):
    """Class to generate and handle COBRA simulated data"""

    def __init__(self,fva_data_I={},sra_data_I={},fba_data_I={},pfba_data_I={}):
        if fva_data_I:
            self.fva_data = self._convert_fluxBounds2var(fva_data_I);
        else:
            self.fva_data = {}
        if sra_data_I:
            self.sra_data = sra_data_I;
        else:
            self.sra_data = {}
        if fba_data_I:
            self.fba_data = fba_data_I;
        else:
            self.fba_data = {}
        if pfba_data_I:
            self.pfba_data = pfba_data_I;
        else:
            self.pfba_data = {}

    def check_data(self):
        '''check data integrity'''
        return

    def generate_sra_data(self, cobra_model, element_list=None,
                            method='fba', element_type='reaction', solver='gurobi'):

        print('Single Reaction Deletion...')

        # single reaction deletion
        single_reaction_deletions = single_deletion(cobra_model, element_list=None,
                            method='fba', element_type='reaction', solver=solver);

        # FBA
        cobra_model.optimize(solver=solver);

        for k,v in single_reaction_deletions[0].items():
            self.sra_data[k] = {'gr':None,'gr_ratio':None};
            if v:
                self.sra_data[k] = {'gr':v,'gr_ratio':v/cobra_model.solution.f};

    def export_sra_data(self, filename):
        '''export sra data'''
        exportdata = base_exportData(self.sra_data);
        exportdata.write_dict2json(filename);

    def generate_fva_data(self, cobra_model, fraction_of_optimum=0.9,
                                      objective_sense='maximize', the_reactions=None,
                                      allow_loops=True, solver='gurobi',
                                      the_problem='return', tolerance_optimality=1e-6,
                                      tolerance_feasibility=1e-6, tolerance_barrier=1e-8,
                                      lp_method=1, lp_parallel=0, new_objective=None,
                                      relax_b=None, error_reporting=None,
                                      number_of_processes=1, copy_model=True):

        print('FVA...')
        # calculate the reaction bounds using FVA
        self.fva_data = flux_variability_analysis(cobra_model, fraction_of_optimum=0.9,
                                      objective_sense='maximize', solver=solver,
                                      #the_reactions=None,
                                      #allow_loops=True, 
                                      #the_problem='return', tolerance_optimality=1e-6,
                                      #tolerance_feasibility=1e-6, tolerance_barrier=1e-8,
                                      #lp_method=1, lp_parallel=0, new_objective=None,
                                      #relax_b=None, error_reporting=None,
                                      #number_of_processes=1, copy_model=True
                                      );

    def export_fva_data(self, filename):
        '''export fva data'''
        exportdata = base_exportData(self.fva_data);
        exportdata.write_dict2json(filename)

    def import_sra_data(self,filename):
        '''import sra data'''
        self.sra_data = json.load(open(filename));

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

    def generate_fba_data(self,cobra_model,allow_loops=True, solver='gurobi'):
        '''
        perform FBA simulation on the model
        INPUT:
        OUTPUT:
        '''
        pass;
    def generate_pfba_data(self,cobra_model, solver='gurobi'):
        '''
        perform FBA simulation on the model
        INPUT:
        OUTPUT:
        '''
        pass;