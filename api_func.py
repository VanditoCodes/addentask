from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, Adset, Campaign, AdAccount, Groupie, group_adset
from fastapi import FastAPI

url = "postgresql://postgres:tester@localhost/adden"
engine = create_engine(url)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
app = FastAPI()


# create adaccount
@app.post("/adaccount/{adaccount_id}")
async def create_account(adacount_id: int, content: str):
    db = SessionLocal()
    db_adset = AdAccount(id=adacount_id, content=content)
    db.add(db_adset)
    db.commit()
    db.refresh(db_adset)
    return db_adset


# create campaign for any adaccount
@app.post("/adaccount/{adaccount_id}/campaign/{campaign_id}/")
async def create_campaign(
    adacount_id: int,
    content: str,
    budget: int,
    campaign_id: int,
):
    db = SessionLocal()
    db_adset = Campaign(
        id=campaign_id, account_id=adacount_id, content=content, budget=budget
    )
    db.add(db_adset)
    db.commit()
    db.refresh(db_adset)
    return db_adset


# create adset for any campaign
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


# create groups for any adacount
@app.post("/{account_id}/groups/create/")
async def create_group(group_id: int, account_id: int, content: str, name: str):
    db = SessionLocal()
    db_group = Groupie(id=group_id, account_id=account_id, content=content, name=name)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group


# add an adset to a group
@app.post("/groups-adset/")
async def link_group_adset(adset_id: int, group_id: int):
    db = SessionLocal()
    db_group = db.query(Groupie).filter(Groupie.id == group_id).first()
    adset = db.query(Adset).filter(Adset.id == adset_id).first()
    db_group.adsets.append(adset)

    db.commit()
    db.refresh(db_group)
    return db_group, adset


# read all adsets
@app.get("/adsets/")
async def read_all_adsets():
    db = SessionLocal()
    adsets = db.query(Adset).all()
    return adsets


# read all adsets belonging to a campaign
@app.get("/campaign/{campaign_id}/adsets")
async def adsets_of_campaign(campaign_id: int):
    db = SessionLocal()
    adsets = db.query(Adset).filter(Adset.campaign_id == campaign_id).all()
    return adsets


# read all adsets belonging to a group
@app.get("/groups/{group_id}/adsets")
async def adsets_of_group(group_id: int):
    db = SessionLocal()
    adsets = db.query(group_adset).filter(group_adset.c.groupId == group_id).all()
    adset_list = []
    print(adsets)
    for row in adsets:
        adset_list.append(row[0])
    return adset_list


# update campaign of an adset
@app.put("/update-adset-campaign")
async def update_adset_campaign(adset_id: int, campaign_id: int):
    db = SessionLocal()
    adset = db.query(Adset).filter(Adset.id == adset_id).first()
    adset.campaign_id = campaign_id
    db.commit()
    return adset


# delete an adset
@app.delete("/delete-adset")
async def delete_adset(adset_id: int):
    db = SessionLocal()
    adset = db.query(Adset).filter(Adset.id == adset_id).first()
    db.delete(adset)
    db.commit()
    return {"message": "{adset_id} deleted successfully"}
