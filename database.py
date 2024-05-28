from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()
# association table between adsets and groups
group_adset = Table(
    "GroupAdset",
    Base.metadata,
    Column("adsetId", Integer, ForeignKey("Adset.id"), primary_key=True),
    Column("groupId", Integer, ForeignKey("Groupie.id"), primary_key=True),
)


# Adaccount Table
class AdAccount(Base):
    __tablename__ = "AdAccount"
    id = Column(Integer(), primary_key=True)
    campaigns = relationship("Campaign", back_populates="account")
    groups = relationship("Groupie")
    reach = Column(Integer())
    created_on = Column(DateTime(), default=datetime.now)
    content = Column(Text)


# Campaign Table
class Campaign(Base):
    __tablename__ = "Campaign"
    id = Column(Integer(), primary_key=True)
    account_id = Column(Integer(), ForeignKey("AdAccount.id"))
    account = relationship("AdAccount", back_populates="campaigns")
    adsets = relationship("Adset", back_populates="campaign")
    budget = Column(Integer(), nullable=False)
    reach = Column(Integer())
    created_on = Column(DateTime(), default=datetime.now)
    content = Column(Text)


# Adset Table
class Adset(Base):
    __tablename__ = "Adset"
    id = Column(Integer(), primary_key=True)
    campaign_id = Column(Integer(), ForeignKey("Campaign.id"))
    campaign = relationship("Campaign", back_populates="adsets")
    budget = Column(Integer(), nullable=False)
    reach = Column(Integer())
    created_on = Column(DateTime(), default=datetime.now)
    content = Column(Text)


# Groupie TAble
class Groupie(Base):
    __tablename__ = "Groupie"
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    account_id = Column(Integer(), ForeignKey("AdAccount.id"))
    adsets = relationship("Adset", secondary=group_adset)
    created_on = Column(DateTime(), default=datetime.now)
    content = Column(Text)
