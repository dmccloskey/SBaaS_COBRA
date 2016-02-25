from SBaaS_base.postgresql_orm_base import *
class data_stage02_physiology_pairWiseTest(Base):
    __tablename__ = 'data_stage02_physiology_pairWiseTest'
    id = Column(Integer, Sequence('data_stage02_physiology_pairWiseTest_id_seq'), primary_key=True)
    simulation_id_1 = Column(String(500))
    simulation_id_2 = Column(String(500))
    #simulation_dateAndTime = Column(DateTime);
    #experiment_id = Column(String(50))
    #model_id = Column(String(50))
    #sample_name_abbreviation = Column(String(100))
    rxn_id = Column(String(100))
    flux_units = Column(String(50), default = 'mmol*gDW-1*hr-1');
    test_stat = Column(Float)
    test_description = Column(String(50));
    pvalue = Column(Float)
    pvalue_corrected = Column(Float)
    pvalue_corrected_description = Column(String(500))
    mean = Column(Float)
    ci_lb = Column(Float)
    ci_ub = Column(Float)
    ci_level = Column(Float)
    fold_change = Column(Float)
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint('simulation_id_1','simulation_id_2','rxn_id'),
            )

    def __init__(self, 
                row_dict_I,
                ):
        self.pvalue_corrected=row_dict_I['pvalue_corrected'];
        self.comment_=row_dict_I['comment_'];
        self.used_=row_dict_I['used_'];
        self.fold_change=row_dict_I['fold_change'];
        self.ci_level=row_dict_I['ci_level'];
        self.ci_ub=row_dict_I['ci_ub'];
        self.ci_lb=row_dict_I['ci_lb'];
        self.mean=row_dict_I['mean'];
        self.pvalue_corrected_description=row_dict_I['pvalue_corrected_description'];
        self.pvalue=row_dict_I['pvalue'];
        self.test_description=row_dict_I['test_description'];
        self.test_stat=row_dict_I['test_stat'];
        self.flux_units=row_dict_I['flux_units'];
        self.rxn_id=row_dict_I['rxn_id'];
        self.simulation_id_2=row_dict_I['simulation_id_2'];
        self.simulation_id_1=row_dict_I['simulation_id_1'];

    def __set__row__(self,simulation_id_1_I,simulation_id_2_I,
        #simulation_dateAndTime_I,
        #experiment_id_I,model_id_I,
        #    sample_name_abbreviation_I,
            rxn_id_I,flux_units_I,
                 mean_I, test_stat_I, test_description_I,
                 pvalue_I, pvalue_corrected_I, pvalue_corrected_description_I,
                 ci_lb_I, ci_ub_I, ci_level_I,
                 fold_change_I,
                 used__I,comment__I):
        self.simulation_id_1=simulation_id_1_I
        self.simulation_id_2=simulation_id_2_I
        #self.simulation_dateAndTime=simulation_dateAndTime_I
        #self.experiment_id=experiment_id_I
        #self.model_id=model_id_I
        #self.sample_name_abbreviation=sample_name_abbreviation_I
        self.rxn_id=rxn_id_I
        self.flux_units=flux_units_I
        self.mean=mean_I;
        self.test_stat=test_stat_I;
        self.test_description=test_description_I;
        self.pvalue=pvalue_I;
        self.pvalue_corrected=pvalue_corrected_I;
        self.pvalue_corrected_description=pvalue_corrected_description_I;
        self.ci_lb=ci_lb_I;
        self.ci_ub=ci_ub_I;
        self.ci_level=ci_level_I;
        self.fold_change=fold_change_I;
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
                'simulation_id_1':self.simulation_id_1,
                'simulation_id_2':self.simulation_id_2,
        #       'simulation_dateAndTime':self.simulation_dateAndTime,
        #       'experiment_id':self.experiment_id,
        #        'model_id':self.model_id,
        #       'sample_name_abbreviation':self.sample_name_abbreviation,
                'rxn_id':self.rxn_id,
                'flux_units':self.flux_units,
                'sampling_delta_ave':self.sampling_delta_ave,
                'sampling_delta_var':self.sampling_delta_var,
                'sampling_delta_lb':self.sampling_delta_lb,
                'sampling_delta_ub':self.sampling_delta_ub,
                'z_delta':self.z_delta,
                'pvalue_delta':self.pvalue_delta,
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_physiology_pairWiseTestMetabolites(Base):
    __tablename__ = 'data_stage02_physiology_pairWiseTestMetabolites'
    id = Column(Integer, Sequence('data_stage02_physiology_pairWiseTestMetabolites_id_seq'), primary_key=True)
    simulation_id_1 = Column(String(500))
    simulation_id_2 = Column(String(500))
    #simulation_dateAndTime = Column(DateTime);
    #experiment_id = Column(String(50))
    #model_id = Column(String(50))
    #sample_name_abbreviation = Column(String(100))
    met_id = Column(String(100))
    flux_units = Column(String(50), default = 'mmol*gDW-1*hr-1');
    test_stat = Column(Float)
    test_description = Column(String(50));
    pvalue = Column(Float)
    pvalue_corrected = Column(Float)
    pvalue_corrected_description = Column(String(500))
    mean = Column(Float)
    ci_lb = Column(Float)
    ci_ub = Column(Float)
    ci_level = Column(Float)
    fold_change = Column(Float)
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint('simulation_id_1','simulation_id_2','met_id'),
            )

    def __init__(self, 
                row_dict_I,
                ):
        self.pvalue_corrected_description=row_dict_I['pvalue_corrected_description'];
        self.used_=row_dict_I['used_'];
        self.comment_=row_dict_I['comment_'];
        self.test_description=row_dict_I['test_description'];
        self.test_stat=row_dict_I['test_stat'];
        self.flux_units=row_dict_I['flux_units'];
        self.met_id=row_dict_I['met_id'];
        self.simulation_id_2=row_dict_I['simulation_id_2'];
        self.simulation_id_1=row_dict_I['simulation_id_1'];
        self.pvalue=row_dict_I['pvalue'];
        self.pvalue_corrected=row_dict_I['pvalue_corrected'];
        self.fold_change=row_dict_I['fold_change'];
        self.ci_level=row_dict_I['ci_level'];
        self.ci_ub=row_dict_I['ci_ub'];
        self.ci_lb=row_dict_I['ci_lb'];
        self.mean=row_dict_I['mean'];

    def __set__row__(self,simulation_id_1_I,simulation_id_2_I,
        #simulation_dateAndTime_I,
        #experiment_id_I,model_id_I,
        #    sample_name_abbreviation_I,
            met_id_I,flux_units_I,
                 mean_I, test_stat_I, test_description_I,
                 pvalue_I, pvalue_corrected_I, pvalue_corrected_description_I,
                 ci_lb_I, ci_ub_I, ci_level_I,
                 fold_change_I,
                 used__I,comment__I):
        self.simulation_id_1=simulation_id_1_I
        self.simulation_id_2=simulation_id_2_I
        #self.simulation_dateAndTime=simulation_dateAndTime_I
        #self.experiment_id=experiment_id_I
        #self.model_id=model_id_I
        #self.sample_name_abbreviation=sample_name_abbreviation_I
        self.met_id=met_id_I
        self.flux_units=flux_units_I
        self.mean=mean_I;
        self.test_stat=test_stat_I;
        self.test_description=test_description_I;
        self.pvalue=pvalue_I;
        self.pvalue_corrected=pvalue_corrected_I;
        self.pvalue_corrected_description=pvalue_corrected_description_I;
        self.ci_lb=ci_lb_I;
        self.ci_ub=ci_ub_I;
        self.ci_level=ci_level_I;
        self.fold_change=fold_change_I;
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
                'simulation_id_1':self.simulation_id_1,
                'simulation_id_2':self.simulation_id_2,
        #'simulation_dateAndTime':self.simulation_dateAndTime,
        #'experiment_id':self.experiment_id,
        #        'model_id':self.model_id,
        #    'sample_name_abbreviation':self.sample_name_abbreviation,
                'met_id':self.met_id,
                'flux_units':self.flux_units,
                'sampling_delta_ave':self.sampling_delta_ave,
                'sampling_delta_var':self.sampling_delta_var,
                'sampling_delta_lb':self.sampling_delta_lb,
                'sampling_delta_ub':self.sampling_delta_ub,
                'z_delta':self.z_delta,
                'pvalue_delta':self.pvalue_delta,
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_physiology_pairWiseTestSubsystems(Base):
    __tablename__ = 'data_stage02_physiology_pairWiseTestSubsystems'
    id = Column(Integer, Sequence('data_stage02_physiology_pairWiseTestSubsystems_id_seq'), primary_key=True)
    simulation_id_1 = Column(String(500))
    simulation_id_2 = Column(String(500))
    #simulation_dateAndTime = Column(DateTime);
    #experiment_id = Column(String(50))
    #model_id = Column(String(50))
    #sample_name_abbreviation = Column(String(100))
    subsystem_id = Column(String(100))
    flux_units = Column(String(50), default = 'mmol*gDW-1*hr-1');
    test_stat = Column(Float)
    test_description = Column(String(50));
    pvalue = Column(Float)
    pvalue_corrected = Column(Float)
    pvalue_corrected_description = Column(String(500))
    mean = Column(Float)
    ci_lb = Column(Float)
    ci_ub = Column(Float)
    ci_level = Column(Float)
    fold_change = Column(Float)
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint('simulation_id_1','simulation_id_2','subsystem_id'),
            )

    def __init__(self, 
                row_dict_I,
                ):
        self.mean=row_dict_I['mean'];
        self.simulation_id_1=row_dict_I['simulation_id_1'];
        self.simulation_id_2=row_dict_I['simulation_id_2'];
        self.subsystem_id=row_dict_I['subsystem_id'];
        self.flux_units=row_dict_I['flux_units'];
        self.test_stat=row_dict_I['test_stat'];
        self.test_description=row_dict_I['test_description'];
        self.pvalue=row_dict_I['pvalue'];
        self.pvalue_corrected=row_dict_I['pvalue_corrected'];
        self.pvalue_corrected_description=row_dict_I['pvalue_corrected_description'];
        self.ci_lb=row_dict_I['ci_lb'];
        self.ci_ub=row_dict_I['ci_ub'];
        self.ci_level=row_dict_I['ci_level'];
        self.fold_change=row_dict_I['fold_change'];
        self.used_=row_dict_I['used_'];
        self.comment_=row_dict_I['comment_'];

    def __set__row__(self,simulation_id_1_I,simulation_id_2_I,
        #simulation_dateAndTime_I,
        #experiment_id_I,model_id_I,
        #    sample_name_abbreviation_I,
            subsystem_id_I,flux_units_I,
                 mean_I, test_stat_I, test_description_I,
                 pvalue_I, pvalue_corrected_I, pvalue_corrected_description_I,
                 ci_lb_I, ci_ub_I, ci_level_I,
                 fold_change_I,
                 used__I,comment__I):
        self.simulation_id_1=simulation_id_1_I
        self.simulation_id_2=simulation_id_2_I
        #self.simulation_dateAndTime=simulation_dateAndTime_I
        #self.experiment_id=experiment_id_I
        #self.model_id=model_id_I
        #self.sample_name_abbreviation=sample_name_abbreviation_I
        self.subsystem_id=subsystem_id_I
        self.flux_units=flux_units_I
        self.mean=mean_I;
        self.test_stat=test_stat_I;
        self.test_description=test_description_I;
        self.pvalue=pvalue_I;
        self.pvalue_corrected=pvalue_corrected_I;
        self.pvalue_corrected_description=pvalue_corrected_description_I;
        self.ci_lb=ci_lb_I;
        self.ci_ub=ci_ub_I;
        self.ci_level=ci_level_I;
        self.fold_change=fold_change_I;
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
                'simulation_id_1':self.simulation_id_1,
                'simulation_id_2':self.simulation_id_2,
        #'simulation_dateAndTime':self.simulation_dateAndTime,
        #'experiment_id':self.experiment_id,
        #        'model_id':self.model_id,
        #    'sample_name_abbreviation':self.sample_name_abbreviation,
                'subsystem_id':self.subsystem_id,
                'flux_units':self.flux_units,
                'sampling_delta_ave':self.sampling_delta_ave,
                'sampling_delta_var':self.sampling_delta_var,
                'sampling_delta_lb':self.sampling_delta_lb,
                'sampling_delta_ub':self.sampling_delta_ub,
                'z_delta':self.z_delta,
                'pvalue_delta':self.pvalue_delta,
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

