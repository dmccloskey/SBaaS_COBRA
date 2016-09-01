from SBaaS_base.postgresql_orm_base import *
class data_stage02_physiology_graphData_shortestPathStats(Base):
    __tablename__ = 'data_stage02_physiology_graphData_shortestPathStats'
    id = Column(Integer, Sequence('data_stage02_physiology_graphData_shortestPathStats_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    simulation_id = Column(String(500))
    path_average = Column(Float);
    path_ci_lb = Column(Float);
    path_ci_level = Column(Float);
    path_ci_ub = Column(Float);
    path_cv = Column(Float);
    path_iq_1 = Column(Float);
    path_iq_3 = Column(Float);
    path_max = Column(Float);
    path_median = Column(Float);
    path_min = Column(Float);
    path_n = Column(Integer);
    path_var = Column(Float);
    path_start = Column(String(100))
    path_stop = Column(String(100))
    params = Column(postgresql.JSON);
    algorithm = Column(String(50));
    weights = Column(String(50));
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint('analysis_id',
                             'simulation_id',
                             'path_start',
                             'path_stop',
                             #'params',
                             'algorithm',
                             'weights'),
            )

    def __init__(self, 
                row_dict_I,
                ):
        self.analysis_id=row_dict_I['analysis_id']
        self.simulation_id=row_dict_I['simulation_id']
        self.path_average=row_dict_I['path_average']
        self.path_ci_lb=row_dict_I['path_ci_lb']
        self.path_ci_level=row_dict_I['path_ci_level']
        self.path_ci_ub=row_dict_I['path_ci_ub']
        self.path_cv=row_dict_I['path_cv']
        self.path_iq_1=row_dict_I['path_iq_1']
        self.path_iq_3=row_dict_I['path_iq_3']
        self.path_max=row_dict_I['path_max']
        self.path_median=row_dict_I['path_median']
        self.path_min=row_dict_I['path_min']
        self.path_n=row_dict_I['path_n']
        self.path_var=row_dict_I['path_var']
        self.path_start=row_dict_I['path_start']
        self.path_stop=row_dict_I['path_stop']
        self.weights=row_dict_I['weights']
        self.algorithm=row_dict_I['algorithm']
        self.params=row_dict_I['params']
        self.used_=row_dict_I['used_']
        self.comment_=row_dict_I['comment_']

    def __set__row__(self,analysis_id_I,
        simulation_id_I,
        path_average_I,
        path_ci_lb_I,
        path_ci_level_I,
        path_ci_ub_I,
        path_cv_I,
        path_iq_1_I,
        path_iq_3_I,
        path_max_I,
        path_median_I,
        path_min_I,
        path_n_I,
        path_var_I,
        path_start_I,
        path_stop_I,
        weights_I,
        algorithm_I,
        params_I,
        used__I,
        comment__I,):        
        self.analysis_id=analysis_id_I
        self.simulation_id=simulation_id_I
        self.path_average=path_average_I
        self.path_ci_lb=path_ci_lb_I
        self.path_ci_level=path_ci_level_I
        self.path_ci_ub=path_ci_ub_I
        self.path_cv=path_cv_I
        self.path_iq_1=path_iq_1_I
        self.path_iq_3=path_iq_3_I
        self.path_max=path_max_I
        self.path_median=path_median_I
        self.path_min=path_min_I
        self.path_n=path_n_I
        self.path_var=path_var_I
        self.path_start=path_start_I
        self.path_stop=path_stop_I
        self.weights=weights_I
        self.algorithm=algorithm_I
        self.params=params_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
                'analysis_id':self.analysis_id,
                'simulation_id':self.simulation_id,
                'path_average':self.path_average,
                'path_ci_lb':self.path_ci_lb,
                'path_ci_level':self.path_ci_level,
                'path_ci_ub':self.path_ci_ub,
                'path_cv':self.path_cv,
                'path_iq_1':self.path_iq_1,
                'path_iq_3':self.path_iq_3,
                'path_max':self.path_max,
                'path_median':self.path_median,
                'path_min':self.path_min,
                'path_n':self.path_n,
                'path_var':self.path_var,
                'path_start':self.path_start,
                'path_stop':self.path_stop,
                'weights':self.weights,
                'algorithm':self.algorithm,
                'params':self.params,
                'used_':self.used_,
                'comment_':self.comment_,
        }
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_physiology_graphData_shortestPaths(Base):
    __tablename__ = 'data_stage02_physiology_graphData_shortestPaths'
    id = Column(Integer, Sequence('data_stage02_physiology_graphData_shortestPaths_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    simulation_id = Column(String(500))
    paths = Column(postgresql.ARRAY(String(500)));
    path_start = Column(String(100))
    path_stop = Column(String(100))
    params = Column(postgresql.JSON);
    algorithm = Column(String(50));
    weights = Column(String(50));
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint('analysis_id',
                             'simulation_id',
                             'paths',
                             'path_start',
                             'path_stop',
                             #'params',
                             'algorithm',
                             'weights'),
            )

    def __init__(self, 
                row_dict_I,
                ):
        self.analysis_id=row_dict_I['analysis_id']
        self.simulation_id=row_dict_I['simulation_id']
        self.paths=row_dict_I['paths']
        self.path_start=row_dict_I['path_start']
        self.path_stop=row_dict_I['path_stop']
        self.algorithm=row_dict_I['algorithm']
        self.params=row_dict_I['params']
        self.weights=row_dict_I['weights']
        self.used_=row_dict_I['used_']
        self.comment_=row_dict_I['comment_']

    def __set__row__(self,analysis_id_I,
        simulation_id_I,
        paths_I,
        path_start_I,
        path_stop_I,
        algorithm_I,
        params_I,
        weights_I,
        used__I,
        comment__I,):
        self.analysis_id=analysis_id_I
        self.simulation_id=simulation_id_I
        self.paths=paths_I
        self.path_start=path_start_I
        self.path_stop=path_stop_I
        self.algorithm=algorithm_I
        self.params=params_I
        self.weights=weights_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
                'analysis_id':self.analysis_id,
                'simulation_id':self.simulation_id,
                'paths':self.paths,
                'path_start':self.path_start,
                'path_stop':self.path_stop,
                'algorithm':self.algorithm,
                'params':self.params,
                'weights':self.weights,
                'used_':self.used_,
                'comment_':self.comment_,
        }
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
#class data_stage02_physiology_graphData(Base):
#    __tablename__ = 'data_stage02_physiology_graphData'
#    id = Column(Integer, Sequence('data_stage02_physiology_graphData_id_seq'), primary_key=True)
#    analysis_id = Column(String(500))
#    simulation_id = Column(String(500))


#    params = Column(postgresql.JSON);
#    algorithm = Column(String(50));
#    weights = Column(String(50));
#    used_ = Column(Boolean);
#    comment_ = Column(Text);

#    __table_args__ = (
#            UniqueConstraint('analysis_id',
#                             'simulation_id',
#                             'path_start',
#                             'path_stop',
#                             'params',
#                             'algorithm',
#                             'weights'),
#            )

#    def __init__(self, 
#                row_dict_I,
#                ):


#    def __set__row__(self,):


#    def __repr__dict__(self):
#        return {'id':self.id,
#        }
    
#    def __repr__json__(self):
#        return json.dumps(self.__repr__dict__())