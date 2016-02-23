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
        self.mixed_fraction=data_dict_I['mixed_fraction'];
        self.simulation_dateAndTime=data_dict_I['simulation_dateAndTime'];
        self.simulation_id=data_dict_I['simulation_id'];
        self.comment_=data_dict_I['comment_'];
        self.used_=data_dict_I['used_'];
        self.infeasible_loops=data_dict_I['infeasible_loops'];
        self.data_dir=data_dict_I['data_dir'];

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
    variable_id = Column(String(100))
    variable_type = Column(String(50)) # e.g., flux, concentration, dG_r
    variable_units = Column(String(50), default = 'mmol*gDW-1*hr-1'); 
    sampling_points = Column(postgresql.ARRAY(Float)); #
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
            UniqueConstraint('simulation_id','variable_id','variable_type'),
            )

    def __init__(self, 
                row_dict_I,
                ):
        self.comment_=data_dict_I['comment_'];
        self.used_=data_dict_I['used_'];
        self.sampling_iq_3=data_dict_I['sampling_iq_3'];
        self.sampling_iq_1=data_dict_I['sampling_iq_1'];
        self.sampling_median=data_dict_I['sampling_median'];
        self.sampling_max=data_dict_I['sampling_max'];
        self.sampling_min=data_dict_I['sampling_min'];
        self.sampling_ub=data_dict_I['sampling_ub'];
        self.sampling_lb=data_dict_I['sampling_lb'];
        self.sampling_var=data_dict_I['sampling_var'];
        self.sampling_ave=data_dict_I['sampling_ave'];
        self.sampling_points=data_dict_I['sampling_points'];
        self.flux_units=data_dict_I['flux_units'];
        self.rxn_id=data_dict_I['rxn_id'];
        self.simulation_dateAndTime=data_dict_I['simulation_dateAndTime'];
        self.simulation_id=data_dict_I['simulation_id'];

    def __set__row__(self,simulation_id_I,
        simulation_dateAndTime_I,
        #experiment_id_I,model_id_I,
        #    sample_name_abbreviation_I,
            variable_id_I,variable_type_I,variable_units_I,
            sampling_points_I,
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
        self.variable_id=variable_id_I
        self.variable_type=variable_type_I
        self.variable_units=variable_units_I
        self.sampling_points=sampling_points_I
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
        'simulation_dateAndTime':self.simulation_dateAndTime,
        #'experiment_id':self.experiment_id,
        #        'model_id':self.model_id,
        #    'sample_name_abbreviation':self.sample_name_abbreviation,
                'variable_id':self.variable_id,
                'variable_type':self.variable_type,
                'variable_units':self.variable_units,
                'sampling_points':self.sampling_points,
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

#class data_stage02_physiology_sampledData_v1(Base):
#    __tablename__ = 'data_stage02_physiology_sampledData'
#    id = Column(Integer, Sequence('data_stage02_physiology_sampledData_id_seq'), primary_key=True)
#    simulation_id = Column(String(500))
#    simulation_dateAndTime = Column(DateTime);
#    #experiment_id = Column(String(50))
#    #model_id = Column(String(50))
#    #sample_name_abbreviation = Column(String(100))
#    rxn_id = Column(String(100)) #TODO: change name to variable_id and add column for variable_type (e.g. met,rxn)
#    flux_units = Column(String(50), default = 'mmol*gDW-1*hr-1'); #TODO: change to variable_units
#    sampling_points = Column(postgresql.ARRAY(Float)); #
#    sampling_ave = Column(Float);
#    sampling_var = Column(Float);
#    sampling_lb = Column(Float);
#    sampling_ub = Column(Float);
#    #sampling_ci = Column(Float, default = 0.95);
#    sampling_min = Column(Float);
#    sampling_max = Column(Float);
#    sampling_median = Column(Float);
#    sampling_iq_1 = Column(Float);
#    sampling_iq_3 = Column(Float);
#    used_ = Column(Boolean);
#    comment_ = Column(Text);

#    __table_args__ = (
#            UniqueConstraint('simulation_id','rxn_id','simulation_dateAndTime'),
#            )

#    def __init__(self,simulation_id_I,
#        simulation_dateAndTime_I,
#        #experiment_id_I,model_id_I,
#        #    sample_name_abbreviation_I,
#            rxn_id_I,flux_units_I,sampling_points_I,
#                 sampling_ave_I,sampling_var_I,sampling_lb_I,sampling_ub_I,
#                 #sampling_ci_I,
#                 sampling_min_I,sampling_max_I,sampling_median_I,
#                 sampling_iq_1_I,sampling_iq_3_I,
#                 used__I,comment__I):
#        self.simulation_id=simulation_id_I
#        self.simulation_dateAndTime=simulation_dateAndTime_I
#        #self.experiment_id=experiment_id_I
#        #self.model_id=model_id_I
#        #self.sample_name_abbreviation=sample_name_abbreviation_I
#        self.rxn_id=rxn_id_I
#        self.flux_units=flux_units_I
#        self.sampling_points=sampling_points_I
#        self.sampling_ave=sampling_ave_I
#        self.sampling_var=sampling_var_I
#        self.sampling_lb=sampling_lb_I
#        self.sampling_ub=sampling_ub_I
#        #self.sampling_ci=sampling_ci_I
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
#                'rxn_id':self.rxn_id,
#                'flux_units':self.flux_units,
#                'sampling_points':self.sampling_points,
#                'sampling_ave':self.sampling_ave,
#                'sampling_var':self.sampling_var,
#                'sampling_lb':self.sampling_lb,
#                'sampling_ub':self.sampling_ub,
#                #'sampling_ci':self.sampling_ci,
#                'sampling_max':self.sampling_max,
#                'sampling_min':self.sampling_min,
#                'sampling_median':self.sampling_median,
#                'sampling_iq_1':self.sampling_iq_1,
#                'sampling_iq_3':self.sampling_iq_3,
#                'used_':self.used_,
#                'comment_':self.comment_}
    
#    def __repr__json__(self):
#        return json.dumps(self.__repr__dict__())