from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship, backref
from datetime import datetime

Base = declarative_base()
group_adset = Table('GroupAdset',
                    Base.metadata,
                    Column('adsetId', Integer, ForeignKey('Adset.id'), primary_key=True),
                    Column('groupId', Integer, ForeignKey('Groupie.id'), primary_key=True)) 
                    
class AdAccount(Base):
    __tablename__ = 'AdAccount'

    id = Column(Integer(), primary_key= True)
    campaigns = relationship("Campaign", back_populates='account')
    # groups = relationship('Group', back_populates='account')
    budget = Column(Integer(), nullable= False)
    reach = Column(Integer())
    created_on = Column(DateTime(), default=datetime.now)
    content = Column(Text)

class Campaign(Base):
    __tablename__ = 'Campaign'

    id = Column(Integer(), primary_key= True)
    account_id = Column(Integer(), ForeignKey('AdAccount.id'))
    account = relationship('AdAccount', back_populates='campaigns')
    adsets = relationship('Adset', back_populates='campaign')
    budget = Column(Integer(), nullable= False)
    reach = Column(Integer())
    created_on = Column(DateTime(), default=datetime.now)
    content = Column(Text)

class Adset(Base):
    __tablename__ = 'Adset'

    id = Column(Integer(), primary_key= True)
    campaign_id = Column(Integer(), ForeignKey('Campaign.id'))
    # group_id = Column(String(), ForeignKey('Group.id'))
    campaign = relationship('Campaign', back_populates='adsets')
    # groups = relationship('Groupie', secondary=group_adset, back_populates='adsets')
    # ads = relationship('Ad', back_populates='adset')
    budget = Column(Integer(), nullable= False)
    reach = Column(Integer())
    created_on = Column(DateTime(), default=datetime.now)
    content = Column(Text)

# class Ad(Base):
#     __tablename__ = 'Ad'

#     id = Column(Integer(), primary_key= True)
#     adset_id =  Column(Integer(), ForeignKey('Adset.id'))
#     adset = relationship('Adset', back_populates='ads')
#     reach = Column(Integer())
#     created_on = Column(DateTime(), default=datetime.now)
#     content = Column(Text)

class Groupie(Base):
    __tablename__ = 'Groupie'

    id = Column(Integer(), primary_key= True)
    # account_id = Column(Integer(), ForeignKey('AdAccount.id'))
    # adset_id = Column(Integer(), ForeignKey('Adset.id'))
    adsets = relationship('Adset', secondary=group_adset)
    # account = relationship('AdAccount', back_populates='groups')
    created_on = Column(DateTime(), default=datetime.now)
    content = Column(Text)


