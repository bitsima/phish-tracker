import fastapi
from sqlalchemy import orm

from .schemas import PhishingSiteCreate, PhishingSite
from ..database import services
from .. import scraper
from ..database import models

app = fastapi.FastAPI()


@app.get("/start-checks", response_model=dict)
async def start_checks(db: orm.Session = fastapi.Depends(services.get_db)):
    error_occurred = scraper.get_main_page()
    if not error_occurred:
        new_sites = scraper.get_submissions()

    site = await services.get_last_saved(db=db)

    for new_site in new_sites:
        if site != None and new_site.PhishTank_id == site.PhishTank_id:
            break
        await services.create_site(new_site, db=db)

    return {"message": "Checks started."}


@app.get("/phishing-sites/{PhishTank_id}/", response_model=PhishingSite)
async def get_site(
    PhishTank_id: int, db: orm.Session = fastapi.Depends(services.get_db)
):
    site = await services.get_site(db=db, PhishTank_id=PhishTank_id)
    if site is None:
        raise fastapi.HTTPException(status_code=404, detail="Site does not exist.")

    return await services.get_site(PhishTank_id=PhishTank_id, db=db)


@app.get("/phishing-sites", response_model=list[PhishingSite])
async def get_sites(db: orm.Session = fastapi.Depends(services.get_db)):
    return await services.get_all_sites(db=db)


@app.get("/update-sites", response_model=dict)
async def update_sites(db: orm.Session = fastapi.Depends(services.get_db)):
    all_sites = await services.get_all_sites(db=db)
    update_messages = dict()
    for saved_site in all_sites:
        site_data = scraper.get_updated_data(saved_site.PhishTank_id)
        update_messages[saved_site.PhishTank_id] = await services.update_site(
            site_data=site_data,
            site=await services.get_site(saved_site.PhishTank_id, db=db),
            db=db,
        )
    return update_messages


@app.delete("/phishing-sites/{PhishTank_id}/", response_model=dict)
async def delete_site(
    PhishTank_id: int, db: orm.Session = fastapi.Depends(services.get_db)
):
    site = await services.get_site(db=db, PhishTank_id=PhishTank_id)
    if site is None:
        raise fastapi.HTTPException(status_code=404, detail="Site does not exist.")

    await services.delete_site(site, db=db)
    return {"message": "Phishing site deleted successfully"}
