from fastapi import FastAPI
from .setup.database import engine, Base
from .models.Part_B import faculty # Import faculty model to ensure table creation
from .models.Part_B.journal_publication import JournalPublication # Import journal_publication model to ensure table creation
from .models.Part_B.book_publication import BookPublication # Import book_publication model to ensure table creation
from .models.Part_B.ict_pedagogy import ICTPedagogy # Import ict_pedagogy model to ensure table creation
from .models.Part_B.research_guidance import ResearchGuidance # Import research_guidance model to ensure table creation
from .models.Part_B.research_project import ResearchProject # Import research_project model to ensure table creation
from .models.Part_B.ipr import IPR # Import ipr model to ensure table creation
from .models.Part_B.research_award import ResearchAward # Import research_award model to ensure table creation
from .models.Part_B.conference_paper import ConferencePaper # Import conference_paper model to ensure table creation
from .models.Part_B.research_proposal import ResearchProposal # Import research_proposal model to ensure table creation
from .models.Part_B.product_development import ProductDevelopment # Import product_development model to ensure table creation
from .models.Part_B.self_development_fdp import SelfDevelopmentFDP # Import self_development_fdp model to ensure table creation
from .models.Part_B.industrial_training import IndustrialTraining # Import industrial_training model to ensure table creation


from .api.Part_B.v1 import journal_publication
from .api.Part_B.v1 import book_publication
from .api.Part_B.v1 import ict_pedagogy
from .api.Part_B.v1 import research_guidance
from .api.Part_B.v1 import research_project
from .api.Part_B.v1 import ipr
from .api.Part_B.v1 import research_award
from .api.Part_B.v1 import conference_paper
from .api.Part_B.v1 import research_proposal
from .api.Part_B.v1 import product_development
from .api.Part_B.v1 import self_development_fdp
from .api.Part_B.v1 import industrial_training
from .api.overall.v1 import appraisal_summary # New import

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
