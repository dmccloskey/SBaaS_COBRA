#SBaaS base
from SBaaS_base.postgresql_orm_base import *
class data_stage02_physiology_sampledPoints(Base):
    __tablename__ = 'data_stage02_physiology_sampledPoints'
    id = Column(Integer, Sequence('data_stage02_physiology_sampledData_id_seq'), primary_key=True)
    simulation_id = Column(String(500))
    simulation_dateAndTime = Column(DateTime);
    #experiment_id = Column(String(50))
    #model_id = Column(String(50))
    #sample_name_abbreviation = Column(String(100))
    mixed_fraction = Column(Float);
    data_dir = Column(String(500)); #
    infeasible_loops = Column(postgresql.ARRAY(String));
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint('simulation_id','simulation_dateAndTime'),
            )

    def __init__(self, 
                row_dict_I,
                ):
        self.mixed_fraction=row_dict_I['mixed_fraction'];
        self.simulation_dateAndTime=row_dict_I['simulation_dateAndTime'];
        self.simulation_id=row_dict_I['simulation_id'];
        self.comment_=row_dict_I['comment_'];
        self.used_=row_dict_I['used_'];
        self.infeasible_loops=row_dict_I['infeasible_loops'];
        self.data_dir=row_dict_I['data_dir'];

    def __set__row__(self,simulation_id_I,
        simulation_dateAndTime_I,
        #experiment_id_I,model_id_I,
        #    sample_name_abbreviation_I,
            mixed_fraction_I,data_dir_I,infeasible_loops_I,
                 used__I,comment__I):
        self.simulation_id=simulation_id_I
        self.simulation_dateAndTime=simulation_dateAndTime_I
        #self.experiment_id=experiment_id_I
        #self.model_id=model_id_I
        #self.sample_name_abbreviation=sample_name_abbreviation_I
        self.mixed_fraction=mixed_fraction_I
        self.data_dir=data_dir_I
        self.infeasible_loops=infeasible_loops_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
                'simulation_id':self.simulation_id,
        'simulation_dateAndTime':self.simulation_dateAndTime,
        #'experiment_id':self.experiment_id,
        #        'model_id':self.model_id,
        #    'sample_name_abbreviation':self.sample_name_abbreviation,
                'data_dir':self.data_dir,
                'infeasible_loops':self.infeasible_loops,
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_physiology_sampledData(Base):
    __tablename__ = 'data_stage02_physiology_sampledData'
    id = Column(Integer, Sequence('data_stage02_physiology_sampledData_id_seq'), primary_key=True)
    simulation_id = Column(String(500))
    simulation_dateAndTime = Column(DateTime);
    #experiment_id = Column(String(50))
    #model_id = Column(String(50))
    #sample_name_abbreviation = Column(String(100))
    rxn_id = Column(String(100)) #TODO: change name to variable_id and add column for variable_type (e.g. met,rxn)
    flux_units = Column(String(50), default = 'mmol*gDW-1*hr-1'); #TODO: change to variable_units
    sampling_points = Column(postgresql.ARRAY(Float)); #
    sampling_n = Column(Integer);
    sampling_ave = Column(Float);
    sampling_var = Column(Float);
    sampling_lb = Column(Float);
    sampling_ub = Column(Float);
    sampling_ci = Column(Float, default = 0.95);
    sampling_min = Column(Float);
    sampling_max = Column(Float);
    sampling_median = Column(Float);
    sampling_iq_1 = Column(Float);
    sampling_iq_3 = Column(Float);
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint('simulation_id','rxn_id','simulation_dateAndTime'),
            )
    

    def __init__(self, 
                row_dict_I,
                ):
        self.comment_=row_dict_I['comment_'];
        self.used_=row_dict_I['used_'];
        self.sampling_n=row_dict_I['sampling_n'];
        self.sampling_iq_3=row_dict_I['sampling_iq_3'];
        self.sampling_iq_1=row_dict_I['sampling_iq_1'];
        self.sampling_median=row_dict_I['sampling_median'];
        self.sampling_max=row_dict_I['sampling_max'];
        self.sampling_min=row_dict_I['sampling_min'];
        self.sampling_ub=row_dict_I['sampling_ub'];
        self.sampling_lb=row_dict_I['sampling_lb'];
        self.sampling_ci=row_dict_I['sampling_ci'];
        self.sampling_var=row_dict_I['sampling_var'];
        self.sampling_ave=row_dict_I['sampling_ave'];
        self.sampling_points=row_dict_I['sampling_points'];
        self.flux_units=row_dict_I['flux_units'];
        self.rxn_id=row_dict_I['rxn_id'];
        self.simulation_dateAndTime=row_dict_I['simulation_dateAndTime'];
        self.simulation_id=row_dict_I['simulation_id'];

    def __set__row__(self,simulation_id_I,
        simulation_dateAndTime_I,
        #experiment_id_I,model_id_I,
        #    sample_name_abbreviation_I,
            rxn_id_I,flux_units_I,sampling_points_I,sampling_n_I,
                 sampling_ave_I,sampling_var_I,sampling_lb_I,sampling_ub_I,
                 sampling_ci_I,
                 sampling_min_I,sampling_max_I,sampling_median_I,
                 sampling_iq_1_I,sampling_iq_3_I,
                 used__I,comment__I):
        self.simulation_id=simulation_id_I
        self.simulation_dateAndTime=simulation_dateAndTime_I
        #self.experiment_id=experiment_id_I
        #self.model_id=model_id_I
        #self.sample_name_abbreviation=sample_name_abbreviation_I
        self.rxn_id=rxn_id_I
        self.flux_units=flux_units_I
        self.sampling_points=sampling_points_I
        self.sampling_n=sampling_n_I
        self.sampling_ave=sampling_ave_I
        self.sampling_var=sampling_var_I
        self.sampling_lb=sampling_lb_I
        self.sampling_ub=sampling_ub_I
        self.sampling_ci=sampling_ci_I
        self.sampling_min=sampling_min_I
        self.sampling_max=sampling_max_I
        self.sampling_median=sampling_median_I
        self.sampling_iq_1=sampling_iq_1_I
        self.sampling_iq_3=sampling_iq_3_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
                'simulation_id':self.simulation_id,
        'simulation_dateAndTime':str(self.simulation_dateAndTime),
        #'experiment_id':self.experiment_id,
        #        'model_id':self.model_id,
        #    'sample_name_abbreviation':self.sample_name_abbreviation,
                'rxn_id':self.rxn_id,
                'flux_units':self.flux_units,
                'sampling_points':self.sampling_points,
                'sampling_n':self.sampling_n,
                'sampling_ave':self.sampling_ave,
                'sampling_var':self.sampling_var,
                'sampling_lb':self.sampling_lb,
                'sampling_ub':self.sampling_ub,
                'sampling_ci':self.sampling_ci,
                'sampling_max':self.sampling_max,
                'sampling_min':self.sampling_min,
                'sampling_median':self.sampling_median,
                'sampling_iq_1':self.sampling_iq_1,
                'sampling_iq_3':self.sampling_iq_3,
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_physiology_samplingParameters(Base):
    __tablename__ = 'data_stage02_physiology_samplingParameters'
    id = Column(Integer, Sequence('data_stage02_physiology_samplingParameters_id_seq'), primary_key=True)
    simulation_id = Column(String(500))
    #simulation_dateAndTime = Column(DateTime);
    solver_id = Column(String);
    n_points = Column(Integer); # sampling-specific
    n_steps = Column(Integer); # sampling-specific
    max_time = Column(Float); # sampling-specific
    n_threads = Column(Integer); # sampling-specific
    sampler_id = Column(String); # sampling-specific; gpSampler (Matlab) opGpSampler (Python)
    #solve_time = Column(Float);
    #solve_time_units = Column(String);
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint('simulation_id'),
            )

    def __init__(self, 
                row_dict_I,
                ):
        self.n_points=row_dict_I['n_points'];
        self.n_threads=row_dict_I['n_threads'];
        self.solver_id=row_dict_I['solver_id'];
        self.simulation_id=row_dict_I['simulation_id'];
        self.comment_=row_dict_I['comment_'];
        self.used_=row_dict_I['used_'];
        self.sampler_id=row_dict_I['sampler_id'];
        self.id=row_dict_I['id'];
        self.max_time=row_dict_I['max_time'];
        self.n_steps=row_dict_I['n_steps'];

    def __set__row__(self,
                 simulation_id_I,
        #simulation_dateAndTime_I,
        solver_id_I,
        n_points_I,
        n_steps_I,
        n_threads_I,
        max_time_I,
        sampler_id_I,
        #solve_time_I,
        #solve_time_units_I,
        used__I,comment__I):
        self.simulation_id=simulation_id_I
        #self.simulation_dateAndTime=simulation_dateAndTime_I
        self.solver_id=solver_id_I
        self.n_points=n_points_I
        self.n_steps=n_steps_I
        self.n_threads=n_threads_I
        self.max_time=max_time_I
        self.sampler_id=sampler_id_I
        #self.solve_time=solve_time_I
        #self.solve_time_units=solve_time_units_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
                'simulation_id':self.simulation_id,
            #'simulation_dateAndTime':self.simulation_dateAndTime,
            'solver_id':self.solver_id,
            'n_points':self.n_points,
            'n_steps':self.n_steps,
            'n_threads':self.n_threads,
            'max_time':self.max_time,
            'sampler_id':self.sampler_id,
            #'solve_time':self.solve_time,
            #'solve_time_units':self.solve_time_units,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_physiology_sampledMetaboliteData(Base):
    __tablename__ = 'data_stage02_physiology_sampledMetaboliteData'
    id = Column(Integer, Sequence('data_stage02_physiology_sampledMetaboliteData_id_seq'), primary_key=True)
    simulation_id = Column(String(500))
    simulation_dateAndTime = Column(DateTime);
    #experiment_id = Column(String(50))
    #model_id = Column(String(50))
    #sample_name_abbreviation = Column(String(100))
    met_id = Column(String(100)) #TODO: change name to variable_id and add column for variable_type (e.g. met,rxn)
    flux_units = Column(String(50), default = 'mmol*gDW-1*hr-1'); #TODO: change to variable_units
    sampling_points = Column(postgresql.ARRAY(Float)); #
    sampling_n = Column(Integer);
    sampling_ave = Column(Float);
    sampling_var = Column(Float);
    sampling_lb = Column(Float);
    sampling_ub = Column(Float);
    sampling_ci = Column(Float, default = 0.95);
    sampling_min = Column(Float);
    sampling_max = Column(Float);
    sampling_median = Column(Float);
    sampling_iq_1 = Column(Float);
    sampling_iq_3 = Column(Float);
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint('simulation_id','met_id','simulation_dateAndTime'),
            )
    

    def __init__(self, 
                row_dict_I,
                ):
        self.comment_=row_dict_I['comment_'];
        self.used_=row_dict_I['used_'];
        self.sampling_n=row_dict_I['sampling_n'];
        self.sampling_iq_3=row_dict_I['sampling_iq_3'];
        self.sampling_iq_1=row_dict_I['sampling_iq_1'];
        self.sampling_median=row_dict_I['sampling_median'];
        self.sampling_max=row_dict_I['sampling_max'];
        self.sampling_min=row_dict_I['sampling_min'];
        self.sampling_ub=row_dict_I['sampling_ub'];
        self.sampling_lb=row_dict_I['sampling_lb'];
        self.sampling_ci=row_dict_I['sampling_ci'];
        self.sampling_var=row_dict_I['sampling_var'];
        self.sampling_ave=row_dict_I['sampling_ave'];
        self.sampling_points=row_dict_I['sampling_points'];
        self.flux_units=row_dict_I['flux_units'];
        self.met_id=row_dict_I['met_id'];
        self.simulation_dateAndTime=row_dict_I['simulation_dateAndTime'];
        self.simulation_id=row_dict_I['simulation_id'];

    def __set__row__(self,simulation_id_I,
        simulation_dateAndTime_I,
        #experiment_id_I,model_id_I,
        #    sample_name_abbreviation_I,
            met_id_I,flux_units_I,sampling_points_I,sampling_n_I,
                 sampling_ave_I,sampling_var_I,sampling_lb_I,sampling_ub_I,
                 sampling_ci_I,
                 sampling_min_I,sampling_max_I,sampling_median_I,
                 sampling_iq_1_I,sampling_iq_3_I,
                 used__I,comment__I):
        self.simulation_id=simulation_id_I
        self.simulation_dateAndTime=simulation_dateAndTime_I
        #self.experiment_id=experiment_id_I
        #self.model_id=model_id_I
        #self.sample_name_abbreviation=sample_name_abbreviation_I
        self.met_id=met_id_I
        self.flux_units=flux_units_I
        self.sampling_points=sampling_points_I
        self.sampling_n=sampling_n_I
        self.sampling_ave=sampling_ave_I
        self.sampling_var=sampling_var_I
        self.sampling_lb=sampling_lb_I
        self.sampling_ub=sampling_ub_I
        self.sampling_ci=sampling_ci_I
        self.sampling_min=sampling_min_I
        self.sampling_max=sampling_max_I
        self.sampling_median=sampling_median_I
        self.sampling_iq_1=sampling_iq_1_I
        self.sampling_iq_3=sampling_iq_3_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
                'simulation_id':self.simulation_id,
        'simulation_dateAndTime':str(self.simulation_dateAndTime),
        #'experiment_id':self.experiment_id,
        #        'model_id':self.model_id,
        #    'sample_name_abbreviation':self.sample_name_abbreviation,
                'met_id':self.met_id,
                'flux_units':self.flux_units,
                'sampling_points':self.sampling_points,
                'sampling_n':self.sampling_n,
                'sampling_ave':self.sampling_ave,
                'sampling_var':self.sampling_var,
                'sampling_lb':self.sampling_lb,
                'sampling_ub':self.sampling_ub,
                'sampling_ci':self.sampling_ci,
                'sampling_max':self.sampling_max,
                'sampling_min':self.sampling_min,
                'sampling_median':self.sampling_median,
                'sampling_iq_1':self.sampling_iq_1,
                'sampling_iq_3':self.sampling_iq_3,
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_physiology_sampledSubsystemData(Base):
    __tablename__ = 'data_stage02_physiology_sampledSubsystemData'
    id = Column(Integer, Sequence('data_stage02_physiology_sampledSubsystemData_id_seq'), primary_key=True)
    simulation_id = Column(String(500))
    simulation_dateAndTime = Column(DateTime);
    #experiment_id = Column(String(50))
    #model_id = Column(String(50))
    #sample_name_abbreviation = Column(String(100))
    subsystem_id = Column(String(100)) #TODO: change name to variable_id and add column for variable_type (e.g. met,rxn)
    flux_units = Column(String(50), default = 'mmol*gDW-1*hr-1'); #TODO: change to variable_units
    sampling_points = Column(postgresql.ARRAY(Float)); #
    sampling_n = Column(Integer);
    sampling_ave = Column(Float);
    sampling_var = Column(Float);
    sampling_lb = Column(Float);
    sampling_ub = Column(Float);
    sampling_ci = Column(Float, default = 0.95);
    sampling_min = Column(Float);
    sampling_max = Column(Float);
    sampling_median = Column(Float);
    sampling_iq_1 = Column(Float);
    sampling_iq_3 = Column(Float);
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint('simulation_id','subsystem_id','simulation_dateAndTime'),
            )
    

    def __init__(self, 
                row_dict_I,
                ):
        self.comment_=row_dict_I['comment_'];
        self.used_=row_dict_I['used_'];
        self.sampling_n=row_dict_I['sampling_n'];
        self.sampling_iq_3=row_dict_I['sampling_iq_3'];
        self.sampling_iq_1=row_dict_I['sampling_iq_1'];
        self.sampling_median=row_dict_I['sampling_median'];
        self.sampling_max=row_dict_I['sampling_max'];
        self.sampling_min=row_dict_I['sampling_min'];
        self.sampling_ub=row_dict_I['sampling_ub'];
        self.sampling_lb=row_dict_I['sampling_lb'];
        self.sampling_ci=row_dict_I['sampling_ci'];
        self.sampling_var=row_dict_I['sampling_var'];
        self.sampling_ave=row_dict_I['sampling_ave'];
        self.sampling_points=row_dict_I['sampling_points'];
        self.flux_units=row_dict_I['flux_units'];
        self.subsystem_id=row_dict_I['subsystem_id'];
        self.simulation_dateAndTime=row_dict_I['simulation_dateAndTime'];
        self.simulation_id=row_dict_I['simulation_id'];

    def __set__row__(self,simulation_id_I,
        simulation_dateAndTime_I,
        #experiment_id_I,model_id_I,
        #    sample_name_abbreviation_I,
            subsystem_id_I,flux_units_I,sampling_points_I,sampling_n_I,
                 sampling_ave_I,sampling_var_I,sampling_lb_I,sampling_ub_I,
                 sampling_ci_I,
                 sampling_min_I,sampling_max_I,sampling_median_I,
                 sampling_iq_1_I,sampling_iq_3_I,
                 used__I,comment__I):
        self.simulation_id=simulation_id_I
        self.simulation_dateAndTime=simulation_dateAndTime_I
        #self.experiment_id=experiment_id_I
        #self.model_id=model_id_I
        #self.sample_name_abbreviation=sample_name_abbreviation_I
        self.subsystem_id=subsystem_id_I
        self.flux_units=flux_units_I
        self.sampling_points=sampling_points_I
        self.sampling_n=sampling_n_I
        self.sampling_ave=sampling_ave_I
        self.sampling_var=sampling_var_I
        self.sampling_lb=sampling_lb_I
        self.sampling_ub=sampling_ub_I
        self.sampling_ci=sampling_ci_I
        self.sampling_min=sampling_min_I
        self.sampling_max=sampling_max_I
        self.sampling_median=sampling_median_I
        self.sampling_iq_1=sampling_iq_1_I
        self.sampling_iq_3=sampling_iq_3_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
                'simulation_id':self.simulation_id,
        'simulation_dateAndTime':str(self.simulation_dateAndTime),
        #'experiment_id':self.experiment_id,
        #        'model_id':self.model_id,
        #    'sample_name_abbreviation':self.sample_name_abbreviation,
                'subsystem_id':self.subsystem_id,
                'flux_units':self.flux_units,
                'sampling_points':self.sampling_points,
                'sampling_n':self.sampling_n,
                'sampling_ave':self.sampling_ave,
                'sampling_var':self.sampling_var,
                'sampling_lb':self.sampling_lb,
                'sampling_ub':self.sampling_ub,
                'sampling_ci':self.sampling_ci,
                'sampling_max':self.sampling_max,
                'sampling_min':self.sampling_min,
                'sampling_median':self.sampling_median,
                'sampling_iq_1':self.sampling_iq_1,
                'sampling_iq_3':self.sampling_iq_3,
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

#class data_stage02_physiology_sampledData_(Base):
#    __tablename__ = 'data_stage02_physiology_sampledData'
#    id = Column(Integer, Sequence('data_stage02_physiology_sampledData_id_seq'), primary_key=True)
#    simulation_id = Column(String(500))
#    simulation_dateAndTime = Column(DateTime);
#    #experiment_id = Column(String(50))
#    #model_id = Column(String(50))
#    #sample_name_abbreviation = Column(String(100))
#    variable_id = Column(String(100))
#    variable_type = Column(String(50)) # e.g., flux, concentration, dG_r
#    variable_units = Column(String(50), default = 'mmol*gDW-1*hr-1'); 
#    sampling_points = Column(postgresql.ARRAY(Float)); #
#    sampling_ave = Column(Float);
#    sampling_var = Column(Float);
#    sampling_lb = Column(Float);
#    sampling_ub = Column(Float);
#    sampling_ci = Column(Float, default = 0.95);
#    sampling_min = Column(Float);
#    sampling_max = Column(Float);
#    sampling_median = Column(Float);
#    sampling_iq_1 = Column(Float);
#    sampling_iq_3 = Column(Float);
#    used_ = Column(Boolean);
#    comment_ = Column(Text);

#    __table_args__ = (
#            UniqueConstraint('simulation_id','variable_id','variable_type'),
#            )

#    def __init__(self, 
#                row_dict_I,
#                ):

#    def __set__row__(self,simulation_id_I,
#        simulation_dateAndTime_I,
#        #experiment_id_I,model_id_I,
#        #    sample_name_abbreviation_I,
#            variable_id_I,variable_type_I,variable_units_I,
#            sampling_points_I,
#                 sampling_ave_I,sampling_var_I,sampling_lb_I,sampling_ub_I,
#                 sampling_ci_I,
#                 sampling_min_I,sampling_max_I,sampling_median_I,
#                 sampling_iq_1_I,sampling_iq_3_I,
#                 used__I,comment__I):
#        self.simulation_id=simulation_id_I
#        self.simulation_dateAndTime=simulation_dateAndTime_I
#        #self.experiment_id=experiment_id_I
#        #self.model_id=model_id_I
#        #self.sample_name_abbreviation=sample_name_abbreviation_I
#        self.variable_id=variable_id_I
#        self.variable_type=variable_type_I
#        self.variable_units=variable_units_I
#        self.sampling_points=sampling_points_I
#        self.sampling_ave=sampling_ave_I
#        self.sampling_var=sampling_var_I
#        self.sampling_lb=sampling_lb_I
#        self.sampling_ub=sampling_ub_I
#        self.sampling_ci=sampling_ci_I
#        self.sampling_min=sampling_min_I
#        self.sampling_max=sampling_max_I
#        self.sampling_median=sampling_median_I
#        self.sampling_iq_1=sampling_iq_1_I
#        self.sampling_iq_3=sampling_iq_3_I
#        self.used_=used__I
#        self.comment_=comment__I

#    def __repr__dict__(self):
#        return {'id':self.id,
#                'simulation_id':self.simulation_id,
#        'simulation_dateAndTime':self.simulation_dateAndTime,
#        #'experiment_id':self.experiment_id,
#        #        'model_id':self.model_id,
#        #    'sample_name_abbreviation':self.sample_name_abbreviation,
#                'variable_id':self.variable_id,
#                'variable_type':self.variable_type,
#                'variable_units':self.variable_units,
#                'sampling_points':self.sampling_points,
#                'sampling_ave':self.sampling_ave,
#                'sampling_var':self.sampling_var,
#                'sampling_lb':self.sampling_lb,
#                'sampling_ub':self.sampling_ub,
#                'sampling_ci':self.sampling_ci,
#                'sampling_max':self.sampling_max,
#                'sampling_min':self.sampling_min,
#                'sampling_median':self.sampling_median,
#                'sampling_iq_1':self.sampling_iq_1,
#                'sampling_iq_3':self.sampling_iq_3,
#                'used_':self.used_,
#                'comment_':self.comment_}
    
#    def __repr__json__(self):
#        return json.dumps(self.__repr__dict__())