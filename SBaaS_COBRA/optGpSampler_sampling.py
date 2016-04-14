from .sampling import cobra_sampling
from .sampling_dependencies import *

class optGpSampler_sampling(cobra_sampling):
    def mix_fraction(self, sample1, sample2, **kwargs):
        """ Compares two sets of sampled points and determines how mixed
        they are.

        Arguments
         sample1, sample2   Ordered set of points, numpy arrays.  The points must be in
                           the same order otherwise it does not make sense.
        kwargs
         fixed (optional)   The directions which are fixed and are not expected (indices)

        Returns
         mix                the mix fraction.  Goes from 0 to 1 with 1 being
                            completely unmixed and .5 being essentially 
                            perfectly mixed.  


        """
        from numpy import min, isnan, median, outer
    
        if 'fixed' not in kwargs:
            fixed = []
        else:
            fixed = kwargs['fixed']
        

        # ignore NAN rows
        ignore_rows = isnan(min(sample1,1)) | isnan(min(sample2,1))
        if len(fixed) > 0:
            ignore_rows[fixed] = True
        keep_rows = ~ ignore_rows

        sample1_reduced = sample1[keep_rows,:]
        sample2_reduced = sample2[keep_rows,:]

        m1 = median(sample1_reduced, 1)
        LPproblem = median(sample2_reduced, 1)
        n_rxn_reduced, n_points = sample1_reduced.shape

        l1 = (sample1_reduced > (outer(m1, ones([1, n_points]))))
        eq1 = (sample1_reduced == outer(m1, ones([1, n_points])))
        l2 = (sample2_reduced > outer(LPproblem, ones([1, n_points])))
        eq2 = (sample2_reduced == outer(LPproblem, ones([1, n_points])))

        eqtotal = eq1 | eq2

        fr_mix = float(sum(sum((l1 == l2) & (~ eqtotal))))/float(l1.size-sum(sum(eqtotal)))

        return fr_mix

    def export_sampling_optGpSampler(self,
            cobra_model,
            fraction_optimal = None, 
            filename_model='sample_model.mat',
            filename_script='sample_script.m', 
            filename_points='points.mat',
            solver_id_I='glpk',
            n_points_I = None, 
            n_steps_I = 20000, 
            max_time_I = None):
        '''export model and script for sampling using optGpSampler'''

        if n_points_I:
            n_points = n_points_I;
        if n_steps_I:
            n_steps = n_steps_I;
        if max_time_I:
            max_time = max_time_I;
        # confine the objective to a fraction of maximum optimal
        if fraction_optimal:
            # optimize
            cobra_model.optimize(solver_id_I);
            objective = [x.id for x in cobra_model.reactions if x.objective_coefficient == 1]
            cobra_model.reactions.get_by_id(objective[0]).upper_bound = fraction_optimal * cobra_model.solution.f;

    def generate_samples(self,
            cobra_model,
            fraction_optimal = None, 
            filename_model='sample_model.pickle',
            filename_script='sample_script.m', 
            filename_points='points.pickle',
            solver_id_I='glpk',
            n_points_I = None, 
            n_steps_I = 20000,
            n_threads_I = 8,
            verbose_I = 1,
            ):
        '''sample the model using optGpSampler
        '''

        # confine the objective to a fraction of maximum optimal
        if fraction_optimal:
            # optimize
            cobra_model.optimize(solver_id_I);
            objective = [x.id for x in cobra_model.reactions if x.objective_coefficient == 1]
            cobra_model.reactions.get_by_id(objective[0]).upper_bound = fraction_optimal * cobra_model.solution.f;

        model = cobra_model.to_array_based_model(deepcopy_model=True)

        model = CbModel.convertPyModel(model)
        rm = CbModelReducer(model)
        rm.fixStoichiometricMatrix(0)
        rm.setTolerance(1e-6)
        rm.setSolverName(solver_id_I)
        rm.setVerbose(verbose_I)

        # get warmup points:
        sampler = CbModelSampler(model)
        sampler.setNrSamples(n_points_I)
        sampler.setNrSteps(n_steps_I)
        sampler.setSolverName(solver_id_I)
        sampler.setNrThreads(n_threads_I)
        sampler.setVerbose(1)
        sModel = sampler.sample()
        warmup = sModel.samplePts
        print('done warmup');

        #sample
        sampler = CbModelSampler(model)
        sampler.setNrSamples(n_points_I)
        sampler.setNrSteps(n_steps_I)
        sampler.setSolverName(solver_id_I)
        sampler.setNrThreads(n_threads_I)
        sampler.setWarmupPts(warmup)
        sampler.setVerbose(verbose_I)

        sModel = sampler.sample()
        samples = sModel.samplePts
        print('done sampling');
        LBS = np.tile(sModel.lower_bounds, (n_points_I,1))    
        UBS = np.tile(sModel.upper_bounds, (n_points_I,1))   
        
        max_dev_null = abs(sModel.S * samples).max();
        max_dev_lb = max((LBS.T - samples).max(), 0);
        max_dev_ub = max((samples - UBS.T).max(), 0)
        print("Maximum deviation from the nullspace = " + max_dev_null);
        print("Maximum violation of lb = " + max_dev_ub);
        print("Maximum violation of ub = " + max_dev_lb);

        points_dict = {};
        points_dict = {k:samples[i,:] for k,i in enumerate(model.reactions)};
        self.points = points_dict;
        self.export_points_numpy(filename_points);

        #samples = pd.DataFrame(data=samples.T, columns=[i for i in model.reactions])
        #dump(samples, open(filename_points,'w'));

    def get_points_optGpSampler(self,optGpSampler_data=None,
                                #sampler_model='sampler_out'
                                ):
        '''load sampling points from optGpSampler'''

        # extract information about the file
        import os, time
        from datetime import datetime
        from stat import ST_SIZE, ST_MTIME
        if optGpSampler_data:
            filename=self.data_dir + '/' + optGpSampler_data;
        else:
            filename=self.data_dir;
        try:
            st = os.stat(filename)
        except IOError:
            print("failed to get information about", filename)
            return;
        else:
            file_size = st[ST_SIZE]
            simulation_dateAndTime_struct = time.localtime(st[ST_MTIME])
            simulation_dateAndTime = datetime.fromtimestamp(time.mktime(simulation_dateAndTime_struct))

        ## load model from MATLAB file
        #try:
        #    model = load_json_model(sampler_model);
        #except NotImplementedError as e:
        #    print(e);
        #    model = self.model;

        # load sample points from file into numpy array
        try:
            points_dict = self.get_points_numpy(filename)
        except NotImplementedError as e:
            print(e);

        self.points = points_dict;
        self.model = model;
        #self.mixed_fraction = mixed_fraction;
        self.simulation_dateAndTime = simulation_dateAndTime;