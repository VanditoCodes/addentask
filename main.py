from sqlalchemy import create_engine
from sqlalchemy.engine import URL

# from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from addentask.database import Base, Adset, Campaign, AdAccount, Groupie
from fastapi import FastAPI

url = "postgresql://postgres:tester@localhost/adden"

engine = create_engine(url)

Base.metadata.create_all(engine)
# engine = create_engine('postgresql + psycopg2://user:password\@hostname/database_name')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
app = FastAPI()


# post, get, put, delete
@app.post("/adaccount/{adaccount_id}")
async def create_account(adacount_id: int, content: str, budget: int):
    db = SessionLocal()
    db_adset = AdAccount(id=adacount_id, content=content, budget=budget)
    db.add(db_adset)
    db.commit()
    db.refresh(db_adset)
    return db_adset


@app.post("/adaccount/{adaccount_id}/campaign/{campaign_id}/")
async def create_campaign(
    adacount_id: int, content: str, budget: int, campaign_id: int
):
    db = SessionLocal()
    db_adset = Campaign(
        id=campaign_id, account_id=adacount_id, content=content, budget=budget
    )
    db.add(db_adset)
    db.commit()
    db.refresh(db_adset)
    return db_adset


@app.post("/campaign/{campaign_id}/adsets/create/{adset_id}")
async def create_adset(
    adset_id: int,
    campaign_id: int,
    budget: int,
    content: str,
):
    db = SessionLocal()
    db_adset = Adset(
        id=adset_id, campaign_id=campaign_id, budget=budget, content=content
    )
    db.add(db_adset)
    db.commit()
    db.refresh(db_adset)
    return db_adset


@app.post("{account_id}/groups/create/")
async def create_group(group_id: int, account_id: int):
    db = SessionLocal()
    db_group = Groupie(id=group_id, account_id = account_id)
    # add_adset = db.query(Adset).filter(Adset.id.in_(adset_ids)).all()
    # print(add_adset)
    # db_group.extend(add_adset)
    # adset = db.query(Adset).filter(Adset.id == adset_ids)
    # db_group.adsets.append(adset)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group


@app.post("/groups-adset/")
async def link_group_adset(adset_id: int, group_id: int):
    db = SessionLocal()

    # add_adset = db.query(Adset).filter(Adset.id.in_(adset_ids)).all()
    # print(add_adset)
    # db_group.extend(add_adset)
    # db.add(db_group)
    db_group = db.query(Groupie).filter(Groupie.id == group_id).first()
    adset = db.query(Adset).filter(Adset.id == adset_id).first()
    db_group.adsets.append(adset)
    db.commit()
    db.refresh(db_group)
    return db_group, adset


@app.get("/adsets/")
async def read_all_adsets():
    db = SessionLocal()
    adsets = db.query(Adset).all()
    return adsets


@app.get("/campaign/{campaign_id}/adsets")
async def adsets_of_campaign(campaign_id: int):
    db = SessionLocal()
    adsets = db.query(Adset).filter(Adset.campaign_id == campaign_id).all()
    return adsets
