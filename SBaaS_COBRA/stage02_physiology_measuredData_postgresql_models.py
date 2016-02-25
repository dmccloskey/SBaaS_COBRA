#SBaaS base
from SBaaS_base.postgresql_orm_base import *
class data_stage02_physiology_metabolomicsData(Base):
    __tablename__ = 'data_stage02_physiology_metabolomicsData'
    id = Column(Integer, Sequence('data_stage02_physiology_metabolomicsData_id_seq'), primary_key=True)
    experiment_id = Column(String(100))
    sample_name_abbreviation = Column(String(100))
    time_point = Column(String(10))
    met_id = Column(String(100))
    concentration = Column(Float);
    concentration_var = Column(Float);
    concentration_units = Column(String(50));
    concentration_lb = Column(Float);
    concentration_ub = Column(Float);
    measured = Column(Boolean);
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (UniqueConstraint('experiment_id','sample_name_abbreviation','time_point','met_id'),
            )

    def __init__(self, 
                row_dict_I,
                ):
        self.used_=row_dict_I['used_'];
        self.experiment_id=row_dict_I['experiment_id'];
        self.sample_name_abbreviation=row_dict_I['sample_name_abbreviation'];
        self.time_point=row_dict_I['time_point'];
        self.met_id=row_dict_I['met_id'];
        self.concentration=row_dict_I['concentration'];
        self.concentration_var=row_dict_I['concentration_var'];
        self.concentration_units=row_dict_I['concentration_units'];
        self.concentration_lb=row_dict_I['concentration_lb'];
        self.concentration_ub=row_dict_I['concentration_ub'];
        self.measured=row_dict_I['measured'];
        self.comment_=row_dict_I['comment_'];

    def __set__row__(self, experiment_id_I, sample_name_abbreviation_I,
                 time_point_I, met_id_I,
                 concentration_I, concentration_var_I, concentration_units_I, concentration_lb_I,
                 concentration_ub_I,
                 measured_I, used__I, comment__I):
        self.experiment_id = experiment_id_I;
        self.sample_name_abbreviation = sample_name_abbreviation_I;
        self.time_point = time_point_I;
        self.met_id = met_id_I;
        self.concentration = concentration_I;
        self.concentration_var = concentration_var_I;
        self.concentration_units = concentration_units_I;
        self.concentration_lb = concentration_lb_I;
        self.concentration_ub = concentration_ub_I;
        self.measured = measured_I;
        self.used_ = used__I;
        self.comment_ = comment__I;

    def __repr__dict__(self):
        return {'id':self.id,
                'experiment_id':self.experiment_id,
                'sample_name_abbreviation':self.sample_name_abbreviation,
                'time_point':self.time_point,
                'met_id':self.met_id,
                'concentration':self.concentration,
                'concentration_var':self.concentration_var,
                'concentration_units':self.concentration_units,
                'concentration_lb':self.concentration_lb,
                'concentration_ub':self.concentration_ub,
                'measured':self.measured,
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_physiology_measuredFluxes(Base):
    __tablename__ = 'data_stage02_physiology_measuredFluxes'
    id = Column(Integer, Sequence('data_stage02_physiology_measuredFluxes_id_seq'), primary_key=True)
    experiment_id = Column(String(50))
    model_id = Column(String(50))
    sample_name_abbreviation = Column(String(100))
    #time_point = Column(String(10))
    rxn_id = Column(String(100))
    flux_average = Column(Float);
    flux_stdev = Column(Float);
    flux_lb = Column(Float); # based on 95% CI
    flux_ub = Column(Float);
    flux_units = Column(String(50));
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint('experiment_id','sample_name_abbreviation','rxn_id','model_id'),
            #UniqueConstraint('experiment_id','sample_name_abbreviation','rxn_id','model_id','time_point'),
            )

    def __init__(self, 
                row_dict_I,
                ):
        self.flux_units=row_dict_I['flux_units'];
        self.model_id=row_dict_I['model_id'];
        self.sample_name_abbreviation=row_dict_I['sample_name_abbreviation'];
        self.rxn_id=row_dict_I['rxn_id'];
        self.flux_ub=row_dict_I['flux_ub'];
        self.flux_lb=row_dict_I['flux_lb'];
        self.flux_stdev=row_dict_I['flux_stdev'];
        self.flux_average=row_dict_I['flux_average'];
        self.comment_=row_dict_I['comment_'];
        self.used_=row_dict_I['used_'];
        self.experiment_id=row_dict_I['experiment_id'];

    def __set__row__(self,experiment_id_I,
            model_id_I,
            sample_name_abbreviation_I,
            #time_point_I,
            rxn_id_I,
            flux_average_I,
            flux_stdev_I,
            flux_lb_I,
            flux_ub_I,
            flux_units_I,
            used__I,
            comment__I):
        self.experiment_id=experiment_id_I
        self.model_id=model_id_I
        self.sample_name_abbreviation=sample_name_abbreviation_I
        #self.time_point=time_point_I
        self.rxn_id=rxn_id_I
        self.flux_average=flux_average_I
        self.flux_stdev=flux_stdev_I
        self.flux_lb=flux_lb_I
        self.flux_ub=flux_ub_I
        self.flux_units=flux_units_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
                'experiment_id':self.experiment_id,
                    'model_id':self.model_id,
                    'sample_name_abbreviation':self.sample_name_abbreviation,
                    #'time_point':self.time_point,
                    'rxn_id':self.rxn_id,
                    'flux_average':self.flux_average,
                    'flux_stdev':self.flux_stdev,
                    'flux_lb':self.flux_lb,
                    'flux_ub':self.flux_ub,
                    'flux_units':self.flux_units,
                    'used_':self.used_,
                    'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

