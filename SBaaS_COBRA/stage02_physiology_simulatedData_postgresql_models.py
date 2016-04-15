#SBaaS base
from SBaaS_base.postgresql_orm_base import *
class data_stage02_physiology_simulatedData_fva(Base):
    __tablename__ = 'data_stage02_physiology_simulatedData_fva'
    id = Column(Integer, Sequence('data_stage02_physiology_simulatedData_fva_id_seq'), primary_key=True)
    simulation_id = Column(String(500))
    simulation_dateAndTime = Column(DateTime);
    rxn_id = Column(String(100))
    fva_minimum = Column(Float);
    fva_maximum = Column(Float);
    fva_method = Column(String(100))
    allow_loops = Column(Boolean);
    fva_options = Column(postgresql.JSON);
    solver_id = Column(String);
    flux_units = Column(String(50), default = 'mmol*gDW-1*hr-1');
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint('simulation_id',
                             'rxn_id',
                             'simulation_dateAndTime',
                             'flux_units',
                             'fva_method',
                             'allow_loops',
                             'solver_id'
                             ),
            )

    def __init__(self, 
                row_dict_I,
                ):
        self.flux_units=row_dict_I['flux_units'];
        self.fva_maximum=row_dict_I['fva_maximum'];
        self.fva_minimum=row_dict_I['fva_minimum'];
        self.fva_method=row_dict_I['fva_method'];
        self.rxn_id=row_dict_I['rxn_id'];
        self.simulation_dateAndTime=row_dict_I['simulation_dateAndTime'];
        self.simulation_id=row_dict_I['simulation_id'];
        self.comment_=row_dict_I['comment_'];
        self.used_=row_dict_I['used_'];
        self.fva_options=row_dict_I['fva_options'];
        self.allow_loops=row_dict_I['allow_loops'];
        self.solver_id=row_dict_I['solver_id'];

    def __set__row__(self,simulation_id_I,
        simulation_dateAndTime_I,
                 rxn_id_I,
                 fva_minimum_I,fva_maximum_I,fva_method_I,
                 allow_loops_I,
                 fva_options_I,
        solver_id_I,flux_units_I,
                 used__I,comment__I):
        self.simulation_id=simulation_id_I
        self.simulation_dateAndTime=simulation_dateAndTime_I;
        self.rxn_id=rxn_id_I
        self.fva_minimum=fva_minimum_I
        self.fva_maximum=fva_maximum_I
        self.fva_method=fva_method_I
        self.allow_loops=allow_loops_I
        self.fva_options=fva_options_I
        self.solver_id=solver_id_I
        self.flux_units=flux_units_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
                'simulation_id':self.simulation_id,
                'simulation_dateAndTime':self.simulation_id,
                'rxn_id':self.rxn_id,
                'fva_minimum':self.fva_minimum,
                'fva_maximum':self.fva_maximum,
                'fva_method':self.fva_maximum,
                'allow_loops':self.allow_loops,
                'fva_options':self.fva_options,
            'solver_id':self.solver_id,
                'flux_units':self.flux_units,
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_physiology_simulatedData_sra(Base):
    __tablename__ = 'data_stage02_physiology_simulatedData_sra'
    id = Column(Integer, Sequence('data_stage02_physiology_simulatedData_sra_id_seq'), primary_key=True)
    simulation_id = Column(String(500))
    simulation_dateAndTime = Column(DateTime);
    rxn_id = Column(String(100))
    sra_gr = Column(Float);
    gr_units = Column(String(50), default = 'hr-1');
    sra_gr_ratio = Column(Float);
    sra_method = Column(String(100))
    sra_options = Column(postgresql.JSON);
    solver_id = Column(String);
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint('simulation_id','rxn_id','simulation_dateAndTime','gr_units','sra_method',
                             'solver_id'),
            )

    def __init__(self, 
                row_dict_I,
                ):
        self.gr_units=row_dict_I['gr_units'];
        self.rxn_id=row_dict_I['rxn_id'];
        self.simulation_dateAndTime=row_dict_I['simulation_dateAndTime'];
        self.simulation_id=row_dict_I['simulation_id'];
        self.comment_=row_dict_I['comment_'];
        self.used_=row_dict_I['used_'];
        self.sra_gr_ratio=row_dict_I['sra_gr_ratio'];
        self.sra_gr=row_dict_I['sra_gr'];
        self.sra_method=row_dict_I['sra_method'];
        self.solver_id=row_dict_I['solver_id'];

    def __set__row__(self,simulation_id_I,
        simulation_dateAndTime_I,
                 rxn_id_I,
                 sra_gr_I,
                 gr_units_I,
                 sra_gr_ratio_I,
                 sra_method_I,
        solver_id_I,
                 used__I,comment__I):
        self.simulation_id=simulation_id_I
        self.simulation_dateAndTime=simulation_dateAndTime_I;
        self.rxn_id=rxn_id_I
        self.gr_units=gr_units_I
        self.sra_gr=sra_gr_I
        self.sra_method=sra_method_I
        self.sra_gr_ratio=sra_gr_ratio_I
        self.solver_id=solver_id_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
                'simulation_id':self.simulation_id,
                'simulation_dateAndTime':self.simulation_id,
                'rxn_id':self.rxn_id,
                'gr_units':self.gr_units,
                'sra_gr':self.sra_gr,
                'sra_method':self.sra_method,
                'sra_gr_ratio':self.sra_gr_ratio,
            'solver_id':self.solver_id,
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_physiology_simulatedData_fbaPrimal(Base):
    __tablename__ = 'data_stage02_physiology_simulatedData_fbaPrimal'
    id = Column(Integer, Sequence('data_stage02_physiology_simulatedData_fbaPrimal_id_seq'), primary_key=True)
    simulation_id = Column(String(500))
    simulation_dateAndTime = Column(DateTime);
    rxn_id = Column(String(100))
    fba_flux = Column(Float);
    fba_method = Column(String(100))
    allow_loops = Column(Boolean);
    fba_options = Column(postgresql.JSON);
    solver_id = Column(String);
    flux_units = Column(String(50), default = 'mmol*gDW-1*hr-1');
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint('simulation_id','rxn_id','simulation_dateAndTime','fba_method','flux_units',
                             'allow_loops',
                             'solver_id'),
            )

    def __init__(self, 
                row_dict_I,
                ):
        self.flux_units=row_dict_I['flux_units'];
        self.fba_flux=row_dict_I['fba_flux'];
        self.fba_method=row_dict_I['fba_method'];
        self.rxn_id=row_dict_I['rxn_id'];
        self.simulation_dateAndTime=row_dict_I['simulation_dateAndTime'];
        self.simulation_id=row_dict_I['simulation_id'];
        self.comment_=row_dict_I['comment_'];
        self.used_=row_dict_I['used_'];
        self.fba_options=row_dict_I['fba_options'];
        self.allow_loops=row_dict_I['allow_loops'];
        self.solver_id=row_dict_I['solver_id'];

    def __set__row__(self,simulation_id_I,
        simulation_dateAndTime_I,
                 rxn_id_I,
                 fba_flux_I,
                 fba_method_I,
                 allow_loops_I,
                 fba_options_I,
        solver_id_I,
                 flux_units_I,
                 used__I,comment__I):
        self.simulation_id=simulation_id_I
        self.simulation_dateAndTime=simulation_dateAndTime_I;
        self.rxn_id=rxn_id_I
        self.fba_flux=fba_flux_I
        self.fba_method=fba_method_I
        self.allow_loops=allow_loops_I
        self.fba_options=fba_options_I
        self.solver_id=solver_id_I
        self.flux_units=flux_units_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
                'simulation_id':self.simulation_id,
                'simulation_dateAndTime':self.simulation_id,
                'rxn_id':self.rxn_id,
                'fba_flux':self.fba_flux,
                'fba_method':self.fba_method,
                'allow_loops':self.allow_loops,
                'fba_options':self.fba_options,
            'solver_id':self.solver_id,
                'flux_units':self.flux_units,
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_physiology_simulatedData_fbaDual(Base):
    __tablename__ = 'data_stage02_physiology_simulatedData_fbaDual'
    id = Column(Integer, Sequence('data_stage02_physiology_simulatedData_fbaDual_id_seq'), primary_key=True)
    simulation_id = Column(String(500))
    simulation_dateAndTime = Column(DateTime);
    met_id = Column(String(100))
    fba_shadowPrice = Column(Float);
    fba_method = Column(String(100))
    allow_loops = Column(Boolean);
    fba_options = Column(postgresql.JSON);
    solver_id = Column(String);
    flux_units = Column(String(50), default = 'mmol*gDW-1*hr-1');
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint('simulation_id','met_id','simulation_dateAndTime','fba_method','flux_units',
                             'allow_loops',
                             'solver_id'),
            )

    def __init__(self, 
                row_dict_I,
                ):
        self.flux_units=row_dict_I['flux_units'];
        self.fba_shadowPrice=row_dict_I['fba_shadowPrice'];
        self.fba_method=row_dict_I['fba_method'];
        self.met_id=row_dict_I['met_id'];
        self.simulation_dateAndTime=row_dict_I['simulation_dateAndTime'];
        self.simulation_id=row_dict_I['simulation_id'];
        self.comment_=row_dict_I['comment_'];
        self.used_=row_dict_I['used_'];
        self.fba_options=row_dict_I['fba_options'];
        self.allow_loops=row_dict_I['allow_loops'];
        self.solver_id=row_dict_I['solver_id'];

    def __set__row__(self,simulation_id_I,
        simulation_dateAndTime_I,
                 met_id_I,
                 fba_shadowPrice_I,
                 fba_method_I,
                 allow_loops_I,
                 fba_options_I,
                 solver_id_I,
                 flux_units_I,
                 used__I,comment__I):
        self.simulation_id=simulation_id_I
        self.simulation_dateAndTime=simulation_dateAndTime_I;
        self.met_id=met_id_I
        self.fba_shadowPrice=fba_shadowPrice_I
        self.fba_method=fba_method_I
        self.allow_loops=allow_loops_I
        self.fba_options=fba_options_I
        self.solver_id=solver_id_I
        self.flux_units=flux_units_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
                'simulation_id':self.simulation_id,
                'simulation_dateAndTime':self.simulation_id,
                'met_id':self.met_id,
                'fba_shadowPrice':self.fba_shadowPrice,
                'fba_method':self.fba_method,
                'allow_loops':self.allow_loops,
                'fba_options':self.fba_options,
            'solver_id':self.solver_id,
                'flux_units':self.flux_units,
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())