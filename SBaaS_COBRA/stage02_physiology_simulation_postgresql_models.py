from SBaaS_base.postgresql_orm_base import *
class data_stage02_physiology_simulation(Base):
    __tablename__ = 'data_stage02_physiology_simulation'
    id = Column(Integer, Sequence('data_stage02_physiology_simulation_id_seq'), primary_key=True)
    simulation_id = Column(String(500))
    experiment_id = Column(String(50))
    model_id = Column(String(50))
    sample_name_abbreviation = Column(String(100))
    #time_point = Column(String(10))
    simulation_type = Column(String(50)); # sampling, fva, sra, fba, etc.
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint('experiment_id','model_id','sample_name_abbreviation','simulation_type','simulation_id'),
            #UniqueConstraint('experiment_id','model_id','sample_name_abbreviation','time_point','simulation_type'),
            #UniqueConstraint('experiment_id','model_id','sample_name_abbreviation','simulation_type'),
            UniqueConstraint('simulation_id'),
            )

    def __init__(self, 
                row_dict_I,
                ):
        self.used_=row_dict_I['used_'];
        self.simulation_id=row_dict_I['simulation_id'];
        self.experiment_id=row_dict_I['experiment_id'];
        self.model_id=row_dict_I['model_id'];
        self.sample_name_abbreviation=row_dict_I['sample_name_abbreviation'];
        self.simulation_type=row_dict_I['simulation_type'];
        self.comment_=row_dict_I['comment_'];

    def __set__row__(self,simulation_id_I,
                 experiment_id_I,
            model_id_I,
            sample_name_abbreviation_I,
            #time_point_I,
            simulation_type_I,
            used__I,
            comment__I):
        self.simulation_id=simulation_id_I
        self.experiment_id=experiment_id_I
        self.model_id=model_id_I
        self.sample_name_abbreviation=sample_name_abbreviation_I
        #self.time_point=time_point_I
        self.simulation_type=simulation_type_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
                'simulation_id':self.simulation_id,
            'experiment_id':self.experiment_id,
            'model_id':self.model_id,
            'sample_name_abbreviation':self.sample_name_abbreviation,
            'time_point':self.time_point,
            'simulation_type':self.simulation_type,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
