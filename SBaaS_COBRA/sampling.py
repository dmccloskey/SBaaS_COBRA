from .sampling_dependencies import *

class cobra_sampling(calculate_interface):

    def __init__(self,data_dir_I=None,model_I=None,loops_I=[]):#,sampler_I=None):
        if data_dir_I:self.data_dir =  data_dir_I;
        else: self.data_dir = None;
        if model_I: self.model = model_I;
        else: self.model = None;
        if loops_I: self.loops = loops_I;
        else: self.loops = [];
        #if sampler_I: self.sampler = sampler_I;
        #else: self.sampler = [];
        self.points = {};
        self.points_statistics = {};
        self.points_metabolite = {};
        self.points_subsystem = {};
        self.mixed_fraction = None;
        self.calculate = calculate_interface();
    # import functions
    def get_points_numpy(self,numpy_data,model_sbml=None):
        '''load sampling points from numpy file'''

        # extract information about the file
        import os, time
        from datetime import datetime
        from stat import ST_SIZE, ST_MTIME
        try:
            st = os.stat(self.data_dir + '/' + numpy_data)
        except IOError:
            print("failed to get information about", self.data_dir + '/' + numpy_data)
            return;
        else:
            file_size = st[ST_SIZE]
            simulation_dateAndTime_struct = time.localtime(st[ST_MTIME])
            simulation_dateAndTime = datetime.fromtimestamp(time.mktime(simulation_dateAndTime_struct))

        # load points from numpy file
        points = loadtxt(numpy_data);

        # Read in the sbml file and define the model conditions
        if model_sbml: self.model = create_cobra_model_from_sbml_file(model_sbml, print_time=True)

        points_dict = {};
        for i,r in enumerate(cobra_model.reactions):
            # extract points
            points_dict[r_id_conv]=points[i,:];

        self.points = points_dict;
        #self.mixed_fraction = mixed_fraction;
        self.simulation_dateAndTime = simulation_dateAndTime;
    # export functions
    def export_points_numpy(self,filename):
        '''export sampling points'''

        savetxt(filename,self.points);
    # plotting functions
    def plot_points_histogram(self,reaction_lst=[]):
        '''plot sampling points as a histogram'''
        if not reaction_lst:
            reaction_lst = ['ENO','FBA','FBP','G6PP','GAPD','GLBRAN2',
                        'GLCP','GLCP2','GLDBRAN2','HEX1','PDH','PFK',
                        'PGI','PGK','PGM','PPS','PYK','TPI','ENO_reverse',
                        'FBA_reverse','GAPD_reverse','PGI_reverse',
                        'PGK_reverse','PGM_reverse','TPI_reverse']
        for r in reaction_lst:
            # loop through each reaction in the list
            plt.figure()
            n, bins, patches = plt.hist(self.points[r],50,label = [r])
            plt.legend()
            plt.show()
    def plot_points_boxAndWhiskers(self,reaction_lst=[]):
        '''plot sampling points as box and whiskers plots'''
        if not reaction_lst:
            reaction_lst = ['ENO','FBA','FBP','G6PP','GAPD','GLBRAN2',
                        'GLCP','GLCP2','GLDBRAN2','HEX1','PDH','PFK',
                        'PGI','PGK','PGM','PPS','PYK','TPI','ENO_reverse',
                        'FBA_reverse','GAPD_reverse','PGI_reverse',
                        'PGK_reverse','PGM_reverse','TPI_reverse']
        for r in reaction_lst:
            # loop through each reaction in the list
            plt.figure()
            fig, ax = plt.subplots()
            bp = ax.boxplot(self.points[r], sym='k+',
                            notch=False, bootstrap=False,
                            usermedians=None,
                            conf_intervals=None)
            plt.show()
    # loop removal
    def check_loops(self,cobra_model_I=None,solver_I = 'cglpk'):
        '''Check if the model contains loops'''

        # Change all uptake reactions to 0
        if cobra_model_I: cobra_model = cobra_model_I.copy();
        else: cobra_model = self.model.copy();
        system_boundaries = [x.id for x in cobra_model.reactions if x.boundary == 'system_boundary'];
        for rxn in cobra_model.reactions:
            if rxn.id in system_boundaries:
                cobra_model.reactions.get_by_id(rxn.id).lower_bound = 0.0;
                cobra_model.reactions.get_by_id(rxn.id).upper_bound = 0.0;
        # Set ATPM to 0
        cobra_model.reactions.get_by_id('ATPM').lower_bound = 0.0
        # set the objective function to a default value
        cobra_model.change_objective('Ec_biomass_iJO1366_WT_53p95M')
        cobra_model.reactions.get_by_id('Ec_biomass_iJO1366_WT_53p95M').lower_bound=1e-6
        cobra_model.reactions.get_by_id('Ec_biomass_iJO1366_WT_53p95M').upper_bound=1e6

        loops_bool = True;
        cobra_model.optimize(solver=solver_I);
        if not cobra_model.solution.f:
            loops_bool = False;

        return loops_bool;
    def simulate_loops(self,cobra_model_I=None,data_fva='loops_fva.json',solver_I='cglpk'):
        '''Simulate FVA after closing exchange reactions and setting ATPM to 0
        reactions with flux will be involved in loops'''
        
        if cobra_model_I: cobra_model = cobra_model_I.copy();
        else: cobra_model = self.model.copy();
        # Change all uptake reactions to 0
        system_boundaries = [x.id for x in cobra_model.reactions if x.boundary == 'system_boundary'];
        for rxn in cobra_model.reactions:
            if rxn.id in system_boundaries:
                cobra_model.reactions.get_by_id(rxn.id).lower_bound = 0.0;
                cobra_model.reactions.get_by_id(rxn.id).upper_bound = 0.0;
        # Set ATPM to 0
        cobra_model.reactions.get_by_id('ATPM').lower_bound = 0.0;
        # set the objective function to a default value
        cobra_model.change_objective('Ec_biomass_iJO1366_WT_53p95M')
        cobra_model.reactions.get_by_id('Ec_biomass_iJO1366_WT_53p95M').lower_bound=0.0
        cobra_model.reactions.get_by_id('Ec_biomass_iJO1366_WT_53p95M').upper_bound=1e6

        # calculate the reaction bounds using FVA
        reaction_bounds = flux_variability_analysis(cobra_model, fraction_of_optimum=1.0,
                                          the_reactions=None, solver=solver_I);

        # Update the data file
        with open(data_fva, 'w') as outfile:
            json.dump(reaction_bounds, outfile, indent=4);
    def simulate_loops_sbml(self,ijo1366_sbml,data_fva,solver_I='cglpk'):
        '''Simulate FVA after closing exchange reactions and setting ATPM to 0
        reactions with flux will be involved in loops'''

        # Read in the sbml file and define the model conditions
        cobra_model = create_cobra_model_from_sbml_file(ijo1366_sbml, print_time=True)
        # Change all uptake reactions to 0
        for rxn in cobra_model.reactions:
            if 'EX_' in rxn.id and '_LPAREN_e_RPAREN_' in rxn.id:
                rxn.lower_bound = 0.0;
        # Set ATPM to 0
        cobra_model.reactions.get_by_id('ATPM').lower_bound = 0.0

        # calculate the reaction bounds using FVA
        reaction_bounds = flux_variability_analysis(cobra_model, fraction_of_optimum=0.9,
                                          objective_sense='maximize', the_reactions=None,
                                          allow_loops=True, solver=solver_I,
                                          the_problem='return', tolerance_optimality=1e-6,
                                          tolerance_feasibility=1e-6, tolerance_barrier=1e-8,
                                          lp_method=1, lp_parallel=0, new_objective=None,
                                          relax_b=None, error_reporting=None,
                                          number_of_processes=1, copy_model=False);

        # Update the data file
        with open(data_fva, 'w') as outfile:
            json.dump(reaction_bounds, outfile, indent=4);
    def find_loops(self,data_fva='loops_fva.json'):
        '''extract out loops from simulate_loops'''

        data_loops = json.load(open(data_fva))
        rxn_loops = [];
        for k,v in data_loops.items():
            if abs(v['minimum'])>1.0 or abs(v['maximum'])>1.0:
                rxn_loops.append(k);
        #return rxn_loops
        self.loops = rxn_loops;
    def remove_loopsFromPoints(self):
        '''remove reactions with loops from sampling points'''

        points_loopless = {};
        for k,v in self.points.items():
            if k in self.loops: continue
            else: 
                points_loopless[k] = v;

        #return points_loopless_mean;
        self.points = points_loopless;
    def remove_noFluxReactionsFromPoints(self):
        '''remove reactions that carry 0 flux'''

        points_flux = {};
        for k,v in self.points.items():
            # determine the max/min of the data
            max_point = max(v);
            min_point = min(v);
            if max_point == 0.0 and min_point == 0.0: continue;
            else: 
                points_flux[k] = v;

        self.points = points_flux;
        return
    # points QC
    def remove_points_notInSolutionSpace_v1(self):
        '''remove points that are not in the solution space
        INPUT:
        
        '''
        pruned_reactions = [];
        rxn_ids_noPointsInSolutionSpace = [];
        for rxn in self.model.reactions:
            points_copy = copy(self.points[rxn.id])
            self.points[rxn.id] = self.remove_points_notInBounds(self.points[rxn.id],rxn.lower_bound,rxn.upper_bound);
            if len(self.points[rxn.id])<1:
                print("no points found in the solution space for rxn_id " + rxn.id + "!");
                rxn_ids_noPointsInSolutionSpace.append(rxn.id);
            if len(points_copy)!= len(self.points[rxn.id]):
                pruned_reactions.append(rxn.id)
        return pruned_reactions
    def remove_points_notInSolutionSpace(self,min_points_I=1000):
        '''remove points that are not in the solution space
        INPUT:
        min_points_I = minimum number of points
        
        '''
        pruned_reactions = [];
        for rxn in self.model.reactions:
            points_copy = copy(self.points[rxn.id]);
            self.points[rxn.id] = self._remove_points_notInSolutionSpace(points_copy,rxn.lower_bound,rxn.upper_bound,min_points_I);
        return pruned_reactions
    def _remove_points_notInSolutionSpace(self,points_I,lower_bound_I,upper_bound_I,min_points_I):
        '''remove points that are not in the solution space.
        If the minimum number of points is not found, the bounds will be increased
        by +/- (upper_bound_I-lower_bound_I)/4 until the minimum number of points
        is found

        INPUT:
        points_I = list of points, float
        lower_bound_I = float
        upper_bound_I = float
        min_points_I = minimum number of points
        
        '''
        points_O=[];
        points_O=self.remove_points_notInBounds(points_I,lower_bound_I,upper_bound_I);
        if len(points_O)<min_points_I:
            adjust_bounds = (upper_bound_I-lower_bound_I)/4;
            if adjust_bounds == 0.0:
                adjust_bounds = 1.0;
            lower_bound_new = lower_bound_I-adjust_bounds;
            upper_bound_new = upper_bound_I+adjust_bounds;
            points_O=self._remove_points_notInSolutionSpace(points_I,lower_bound_new,upper_bound_new,min_points_I);
        return points_O;
    def remove_points_notInBounds(self,points_I,lower_bound_I,upper_bound_I):
        '''remove points not in the lower/upper bounds
        INPUT:
        points_I = list of points, float
        lower_bound_I = float
        upper_bound_I = float
        '''
        points_O = [p for p in points_I if p >= lower_bound_I and p<= upper_bound_I];
        return points_O;        
    # analyses
    def descriptive_statistics(self):
        '''calculate the following:
        1. mean, variance, 95% CI
        2. median, mode, 1st quartile, 3rd quartile, range'''

        points_statistics = {};
        for k,v in self.points.items():
            # calculate the mean and variance
            n = len(self.points[k]);
            m,var,lb,ub = self.calculate.calculate_ave_var(self.points[k],confidence_I = 0.95);
            # directly calculate the 95% CI
            lb,ub = self.calculate.calculate_ciFromPoints(self.points[k],alpha=0.05)
            #lb,ub = self.calculate.bootstrap(self.points[k]['points'], num_samples=100000, statistic=np.mean, alpha=0.05)
            # calculate the min, max, median, and interquartile ranges
            min,max,median,iq_1,iq_3=self.calculate.calculate_interquartiles(self.points[k],iq_range_I = [25,75])
            tmp = {};
            tmp = {
                'n':n,
                'ave':m,
                'var':var,
                'lb':lb,
                'ub':ub,
                'median':median,
                'min':min,
                'max':max,
                'iq_1':iq_1,
                'iq_3':iq_3
                }
            points_statistics[k]=tmp;
        self.points_statistics = points_statistics;
    def svd(self):
        '''Singular value decomposition of the solution space'''
        return
    def convert_points2MetabolitePoints(self):
        '''convert the reaction flux to total flux through each metabolite for each sampling point'''
        metabolite_points = {};
        first_loop = True;
        for k,v in self.points.items():
            if first_loop:
                for met in self.model.metabolites:
                    metabolite_points[met.id]=np.zeros_like(v);
                first_loop = False;
            for i,flux in enumerate(v):
                for p in self.model.reactions.get_by_id(k).products:
                    metabolite_points[p.id][i]+=0.5*abs(flux*self.model.reactions.get_by_id(k).get_coefficient(p.id))
                for p in self.model.reactions.get_by_id(k).reactants:
                    metabolite_points[p.id][i]+=0.5*abs(flux*self.model.reactions.get_by_id(k).get_coefficient(p.id))
        self.points_metabolite=metabolite_points;
    def convert_points2SubsystemPoints(self):
        '''convert the reaction flux to total flux through each subsystem for each sampling point'''
        subsystem_points = {};
        subsystems_all = [];
        for r in self.model.reactions:
            subsystems_all.append(r.subsystem);
        subsystems = list(set(subsystems_all)); 
        first_loop = True;
        for k,v in self.points.items():
            if first_loop:       
                for sub in subsystems:
                    subsystem_points[sub]=np.zeros_like(v);
                first_loop = False;
            for i,flux in enumerate(v):
                subsystem_points[self.model.reactions.get_by_id(k).subsystem][i]+=abs(flux);
        self.points_subsystem=subsystem_points;
    def normalize_points2Total(self):
        '''normalize each reaction for a given point to the total
        flux through all reactions for that point'''
        points = self.points;
        points_normalized={};
        n_points = len(points[list(points.keys())[0]]);
        for i in range(n_points):
            total=0.0;
            for k,v in points.items():
                total+=np.abs(v[i]);
            for k,v in points.items():
                if i==0:
                    points_normalized[k]=np.zeros_like(v);
                points_normalized[k][i] = v[i]/total
        self.points = points_normalized;
    def normalize_points2CarbonInput(self):
        '''normalize each reaction for a given point to the total
        carbon input flux for that point'''
        points = self.points;
        system_boundaries = [x.id for x in self.model.reactions if x.boundary == 'system_boundary'];
        points_normalized={};
        n_points = len(points[list(points.keys())[0]]);
        for i in range(n_points):
            total=0.0;
            for k,v in points.items():
                if k in system_boundaries:
                    if self.model.reactions.get_by_id(k).reactants and v[i] < 0:
                        # e.g. glc-D -->
                        mets = self.model.reactions.get_by_id(k).reactants
                        for met in mets:
                            formula_str = met.formula.formula
                            n12C = 0
                            if 'C' not in Formula(formula_str)._elements and 0 in Formula(formula_str)._elements['C']:
                                n12C += Formula(formula_str)._elements['C'][0]; #get the # of Carbons
                            total+=np.abs(v[i])*n12C;
                    elif self.model.reactions.get_by_id(k).products and v[i] > 0:
                        # e.g. --> glc-D
                        mets = self.model.reactions.get_by_id(k).reactants
                        for met in mets:
                            formula_str = met.formula.formula
                            n12C = 0
                            if 'C' not in Formula(formula_str)._elements and 0 in Formula(formula_str)._elements['C']:
                                n12C += Formula(formula_str)._elements['C'][0]; #get the # of Carbons
                            total+=np.abs(v[i])*n12C;
            for k,v in points.items():
                if i==0:
                    points_normalized[k]=np.zeros_like(v);
                points_normalized[k][i] = v[i]/total
        self.points = points_normalized;
    def normalize_points2Input(self):
        '''normalize each reaction for a given point to the total
        input flux for that point'''
        points = self.points;
        system_boundaries = [x.id for x in self.model.reactions if x.boundary == 'system_boundary'];
        points_normalized={};
        n_points = len(points[list(points.keys())[0]]);
        for i in range(n_points):
            total=0.0;
            for k,v in points.items():
                if k in system_boundaries:
                    if self.model.reactions.get_by_id(k).reactants and v[i] < 0:
                        # e.g. glc-D -->
                        total+=np.abs(v[i]);
                    elif self.model.reactions.get_by_id(k).products and v[i] > 0:
                        # e.g. --> glc-D
                        total+=np.abs(v[i]);
            for k,v in points.items():
                if i==0:
                    points_normalized[k]=np.zeros_like(v);
                points_normalized[k][i] = v[i]/total
        self.points = points_normalized;
    # add data
    def add_data(self,data_dir_I=None,model_I=None,loops_I=[]):
        '''add new data'''
        if data_dir_I:self.data_dir =  data_dir_I;
        if model_I: self.model = model_I;
        if loops_I: self.loops = loops_I;
    # clear all data
    def remove_data(self):
        '''remove all data'''
        self.data_dir = None;
        self.model = None;
        self.points = {};
        self.mixed_fraction = None;
        self.loops = {};
        self.calculate = calculate_interface();

class cobra_sampling_n(calculate_interface):

    def __init__(self,data_dir_I=None,model_I=None,loops_I=[],sample_ids_I=[],samplers_I=None,control_I=False):
        #   control_I = True: sample_ids_I[0]=control,sample_ids_I[1:]=perturbation
        #               False: pairwise test is performed on all
        #               controls how the pairwisetests are performed
        if data_dir_I:self.data_dir =  data_dir_I;
        else: self.data_dir = None;
        if model_I: self.model = model_I;
        else: self.model = None;
        if loops_I: self.loops = loops_I;
        else: self.loops = [];
        if sample_ids_I: self.sample_ids = sample_ids_I;
        else: self.sample_ids = []
        if samplers_I: self.samplers = samplers_I;
        else: self.samplers = [];
        if control_I: self.control = control_I;
        else: self.control=control_I;
        self.points = [];
        self.points_metabolites = [];
        self.points_subsystems = [];
        self.calculate = calculate_interface();
        self.data = [];

    def calculate_pairWiseTest(self):
        '''Calculate the difference of the mean and median, fold change, and p-value
         between pairwise sampling distribution'''

        data_O = [];

        test_stat = None
        test_description = 'permutation'

        for i,data_1 in enumerate(self.points):
            sample_id_1 = self.sample_ids[i];
            if self.control and i>0:
                break;
            for j,data_2 in enumerate(self.points):
                sample_id_2 = self.sample_ids[j];
                if i==j: continue;
                for r in self.model.reactions:
                    rxn_id = r.id
                    mean_difference = None
                    median_difference = None
                    pvalue = None
                    fold_change = None;
                    # check point length
                    n_data_1 = len(data_1);
                    n_data_2 = len(data_2);
                    if n_data_1 != n_data_2:
                        print('number of sampled points are not consistent')
                    n_points = n_data_1;
                    if rxn_id in list(data_1.keys()):
                        cond1 = data_1[rxn_id];
                    else:
                        cond1 = np.zeros(n_points);
                    if rxn_id in list(data_2.keys()):
                        cond2 = data_2[rxn_id];
                    else:
                        cond2 = np.zeros(n_points);
                    mean_difference = cond2.mean()-cond1.mean();
                    median_difference = np.median(cond2) - np.median(cond1) 
                    #pvalue = self.calculate.permutation_resampling(cond1,cond2);
                    pvalue = self.calculate.calculate_pvalue_permutation(cond1,cond2);
                    fold_change = cond2.mean()/cond1.mean();
                    tmp = {};
                    tmp = {'sample_id_1':sample_id_1,
                           'sample_id_2':sample_id_2,
                           'rxn_id':rxn_id,
                           'pvalue':pvalue,
                           'mean_difference':mean_difference,
                           'median_difference':median_difference,
                           'fold_change':fold_change,
                           'test_stat':test_stat,
                           'test_description':test_description};
                    data_O.append(tmp);
        self.data = data_O;

    def calculate_pairWiseTest_metabolites(self):
        '''Calculate the difference of the mean and median, fold change, and p-value
         between pairwise sampling distribution for metabolites'''

        data_O = [];

        test_stat = None
        test_description = 'permutation'

        for i,data_1 in enumerate(self.points_metabolites):
            sample_id_1 = self.sample_ids[i];
            if self.control and i>0:
                break;
            for j,data_2 in enumerate(self.points_metabolites):
                sample_id_2 = self.sample_ids[j];
                if i==j: continue;
                for m in self.model.metabolites:
                    met_id = m.id
                    mean_difference = None
                    median_difference = None
                    pvalue = None
                    fold_change = None;
                    # check point length
                    n_data_1 = len(data_1);
                    n_data_2 = len(data_2);
                    if n_data_1 != n_data_2:
                        print('number of sampled points are not consistent')
                    n_points = n_data_1;
                    if met_id in list(data_1.keys()):
                        cond1 = data_1[met_id];
                    else:
                        cond1 = np.zeros(n_points);
                    if met_id in list(data_2.keys()):
                        cond2 = data_2[met_id];
                    else:
                        cond2 = np.zeros(n_points);
                    mean_difference = cond1.mean() - cond2.mean()
                    median_difference = cond1.median() - cond2.median() 
                    #pvalue = self.calculate.permutation_resampling(cond1,cond2);
                    pvalue = self.calculate.calculate_pvalue_permutation(cond1,cond2);
                    fold_change = cond2.mean()/cond1.mean();
                    tmp = {};
                    tmp = {'sample_id_1':sample_id_1,
                           'sample_id_2':sample_id_2,
                           'met_id':met_id,
                           'pvalue':pvalue,
                           'mean_difference':mean_difference,
                           'median_difference':median_difference,
                           'fold_change':fold_change,
                           'test_stat':test_stat,
                           'test_description':test_description};
                    data_O.append(tmp);
        self.data = data_O;

    def calculate_pairWiseTest_subsystems(self):
        '''Calculate the difference of the mean and median, fold change, and p-value
         between pairwise sampling distribution for metabolites'''

        data_O = [];

        test_stat = None
        test_description = 'permutation'

        for i,data_1 in enumerate(self.points_subsystems):
            sample_id_1 = self.sample_ids[i];
            if self.control and i>0:
                break;
            for j,data_2 in enumerate(self.points_subsystems):
                sample_id_2 = self.sample_ids[j];
                if i==j: continue;
                for sub_id in list(self.points_subsystems.keys()):
                    mean_difference = None
                    median_difference = None
                    pvalue = None
                    fold_change = None;
                    # check point length
                    n_data_1 = len(data_1);
                    n_data_2 = len(data_2);
                    if n_data_1 != n_data_2:
                        print('number of sampled points are not consistent')
                    n_points = n_data_1;
                    if sub_id in list(data_1.keys()):
                        cond1 = data_1[sub_id];
                    else:
                        cond1 = np.zeros(n_points);
                    if sub_id in list(data_2.keys()):
                        cond2 = data_2[sub_id];
                    else:
                        cond2 = np.zeros(n_points);
                    mean_difference = cond1.mean() - cond2.mean()
                    median_difference = cond1.median() - cond2.median() 
                    #pvalue = self.calculate.permutation_resampling(cond1,cond2);
                    pvalue = self.calculate.calculate_pvalue_permutation(cond1,cond2);
                    fold_change = cond2.mean()/cond1.mean();
                    tmp = {};
                    tmp = {'sample_id_1':sample_id_1,
                           'sample_id_2':sample_id_2,
                           'subsystem_id':sub_id,
                           'pvalue':pvalue,
                           'mean_difference':mean_difference,
                           'median_difference':median_difference,
                           'fold_change':fold_change,
                           'test_stat':test_stat,
                           'test_description':test_description};
                    data_O.append(tmp);
        self.data = data_O;

    def calculate_anova(self):
        return

    def calculate_pca(self):
        return

    def get_points(self,data_points_I=[],remove_loops_I=True,remove_no_flux_I=True,normalize_I=True):
        '''Get multiple points from sampling'''
        sampling = cobra_sampling();
        for i,sample_id in enumerate(self.sample_ids):
            sampling.add_data(data_dir_I=self.data_dir,model_I=self.model,loops_I=self.loops);
            if self.samplers[i]=='gpSampler':
                sampling.get_points_matlab(data_points_I[i]);
            elif self.samplers[i]=='optGpSampler':
                sampling.get_points_numpy(data_points_I[i])
            if remove_loops_I: sampling.remove_loopsFromPoints();
            if remove_no_flux_I: sampling.remove_noFluxReactionsFromPoints();
            if normalize_I: sampling.normalize_points2Total();
            #sampling.convert_points2MetabolitePoints();
            #sampling.convert_points2SubsystemPoints()
            self.points.append(sampling.points);
            self.points_metabolites.append(sampling.points_metabolite)
            self.points_subsystems.append(sampling.points_subsystem)
            sampling.remove_data();
