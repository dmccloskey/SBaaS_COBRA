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
    flux_units = Column(String(50), default = 'mmol*gDW-1*hr-1');
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint('simulation_id','rxn_id','simulation_dateAndTime'),
            )

    def __init__(self, 
                row_dict_I,
                ):
        self.flux_units=row_dict_I['flux_units'];
        self.fva_maximum=row_dict_I['fva_maximum'];
        self.fva_minimum=row_dict_I['fva_minimum'];
        self.rxn_id=row_dict_I['rxn_id'];
        self.simulation_dateAndTime=row_dict_I['simulation_dateAndTime'];
        self.simulation_id=row_dict_I['simulation_id'];
        self.comment_=row_dict_I['comment_'];
        self.used_=row_dict_I['used_'];

    def __set__row__(self,simulation_id_I,
        simulation_dateAndTime_I,
                 rxn_id_I,
                 fva_minimum_I,fva_maximum_I,flux_units_I,
                 used__I,comment__I):
        self.simulation_id=simulation_id_I
        self.simulation_dateAndTime=simulation_dateAndTime_I;
        self.rxn_id=rxn_id_I
        self.fva_minimum=fva_minimum_I
        self.fva_maximum=fva_maximum_I
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
    gr_units = Column(String(50), default = 'hr-1');
    sra_gr = Column(Float);
    sra_gr_ratio = Column(Float);
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint('simulation_id','rxn_id','simulation_dateAndTime'),
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

    def __set__row__(self,simulation_id_I,
        simulation_dateAndTime_I,
                 rxn_id_I,
                 gr_units_I,
                 sra_gr_I,sra_gr_ratio_I,
                 used__I,comment__I):
        self.simulation_id=simulation_id_I
        self.simulation_dateAndTime=simulation_dateAndTime_I;
        self.rxn_id=rxn_id_I
        self.gr_units=gr_units_I
        self.sra_gr=sra_gr_I
        self.sra_gr_ratio=sra_gr_ratio_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
                'simulation_id':self.simulation_id,
                'simulation_dateAndTime':self.simulation_id,
                'rxn_id':self.rxn_id,
                'gr_units':self.gr_units,
                'sra_gr':self.sra_gr,
                'sra_gr_ratio':self.sra_gr_ratio,
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_physiology_simulatedData_pfba(Base):
    __tablename__ = 'data_stage02_physiology_simulatedData_pfba'
    id = Column(Integer, Sequence('data_stage02_physiology_simulatedData_pfba_id_seq'), primary_key=True)
    simulation_id = Column(String(500))
    simulation_dateAndTime = Column(DateTime);
    rxn_id = Column(String(100))
    pfba_flux = Column(Float);
    flux_units = Column(String(50), default = 'mmol*gDW-1*hr-1');
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint('simulation_id','rxn_id','simulation_dateAndTime'),
            )

    def __init__(self, 
                row_dict_I,
                ):
        self.flux_units=row_dict_I['flux_units'];
        self.pfba_flux=row_dict_I['pfba_flux'];
        self.rxn_id=row_dict_I['rxn_id'];
        self.simulation_dateAndTime=row_dict_I['simulation_dateAndTime'];
        self.simulation_id=row_dict_I['simulation_id'];
        self.comment_=row_dict_I['comment_'];
        self.used_=row_dict_I['used_'];

    def __set__row__(self,simulation_id_I,
        simulation_dateAndTime_I,
                 rxn_id_I,pfba_flux_I,
                 flux_units_I,
                 used__I,comment__I):
        self.simulation_id=simulation_id_I
        self.simulation_dateAndTime=simulation_dateAndTime_I;
        self.rxn_id=rxn_id_I
        self.pfba_flux=pfba_flux_I
        self.flux_units=flux_units_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
                'simulation_id':self.simulation_id,
                'simulation_dateAndTime':self.simulation_id,
                'rxn_id':self.rxn_id,
                'pfba_flux':self.pfba_flux,
                'flux_units':self.flux_units,
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_physiology_simulatedData_fba(Base):
    __tablename__ = 'data_stage02_physiology_simulatedData_fba'
    id = Column(Integer, Sequence('data_stage02_physiology_simulatedData_fba_id_seq'), primary_key=True)
    simulation_id = Column(String(500))
    simulation_dateAndTime = Column(DateTime);
    rxn_id = Column(String(100))
    fba_flux = Column(Float);
    flux_units = Column(String(50), default = 'mmol*gDW-1*hr-1');
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint('simulation_id','rxn_id','simulation_dateAndTime'),
            )

    def __init__(self, 
                row_dict_I,
                ):
        self.flux_units=row_dict_I['flux_units'];
        self.fba_flux=row_dict_I['fba_flux'];
        self.rxn_id=row_dict_I['rxn_id'];
        self.simulation_dateAndTime=row_dict_I['simulation_dateAndTime'];
        self.simulation_id=row_dict_I['simulation_id'];
        self.comment_=row_dict_I['comment_'];
        self.used_=row_dict_I['used_'];

    def __set__row__(self,simulation_id_I,
        simulation_dateAndTime_I,
                 rxn_id_I,fba_flux_I,
                 flux_units_I,
                 used__I,comment__I):
        self.simulation_id=simulation_id_I
        self.simulation_dateAndTime=simulation_dateAndTime_I;
        self.rxn_id=rxn_id_I
        self.fba_flux=fba_flux_I
        self.flux_units=flux_units_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
                'simulation_id':self.simulation_id,
                'simulation_dateAndTime':self.simulation_id,
                'rxn_id':self.rxn_id,
                'fba_flux':self.fba_flux,
                'flux_units':self.flux_units,
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())