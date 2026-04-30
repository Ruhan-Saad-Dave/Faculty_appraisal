from fastapi import FastAPI 

# uvicorn main:app --reloadfrom fastapi import FastAPI

from src.setup.database import engine, Base
from src.api.Part_B.v1 import journal_publication
from src.api.Part_B.v1 import book_publication
from src.api.Part_B.v1 import ict_pedagogy
from src.api.Part_B.v1 import research_guidance
from src.api.Part_B.v1 import research_project
from src.api.Part_B.v1 import ipr
from src.api.Part_B.v1 import research_award
from src.api.Part_B.v1 import conference_paper
from src.api.Part_B.v1 import research_proposal
from src.api.Part_B.v1 import product_development
from src.api.Part_B.v1 import self_development_fdp
from src.api.Part_B.v1 import industrial_training
from src.api.overall.v1 import appraisal_summary # New import

# Create all tables defined in Base
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Faculty Appraisal API",
    description="API for managing faculty appraisal data.",
    version="1.0.0",
)

app.include_router(journal_publication.router, prefix="/api/v1", tags=["Journal Publications"])
app.include_router(book_publication.router, prefix="/api/v1", tags=["Book Publications"])
app.include_router(ict_pedagogy.router, prefix="/api/v1", tags=["ICT Pedagogies"])
app.include_router(research_guidance.router, prefix="/api/v1", tags=["Research Guidance"])
app.include_router(research_project.router, prefix="/api/v1", tags=["Research Projects"])
app.include_router(ipr.router, prefix="/api/v1", tags=["IPR Entries"])
app.include_router(research_award.router, prefix="/api/v1", tags=["Research Awards"])
app.include_router(conference_paper.router, prefix="/api/v1", tags=["Conference Papers"])
app.include_router(research_proposal.router, prefix="/api/v1", tags=["Research Proposals"])
app.include_router(product_development.router, prefix="/api/v1", tags=["Product Developments"])
app.include_router(self_development_fdp.router, prefix="/api/v1", tags=["Self-Development FDP"])
app.include_router(industrial_training.router, prefix="/api/v1", tags=["Industrial Trainings"])
app.include_router(appraisal_summary.router, prefix="/api", tags=["Appraisal Summary"]) # New router inclusion

@app.get("/")
def read_root():
    return {"message": "Welcome to the Faculty Appraisal API"}
