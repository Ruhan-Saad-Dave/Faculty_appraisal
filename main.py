from fastapi import FastAPI
from src.setup.database import engine, Base

# Part B Routers
from src.api.Part_B.v1 import (
    journal_publication, book_publication, ict_pedagogy,
    research_guidance, research_project, ipr, research_award,
    conference_paper, research_proposal, product_development,
    self_development_fdp, industrial_training
)

# Part A Routers
from src.api.Part_A.v1 import (
    teaching_process, course_file, teaching_methods,
    student_feedback, departmental_activities, university_activities,
    social_contributions, industry_connect, qualification_enhancement,
    project, acr, part_a_summary
)

# Overall Routers
from src.api.overall.v1 import appraisal_summary, remarks, finalization

# Create all tables defined in Base
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Faculty Appraisal API",
    description="API for managing faculty appraisal data.",
    version="1.0.0",
)

# Part B Endpoints
app.include_router(journal_publication.router, prefix="/api", tags=["Journal Publications"])
app.include_router(book_publication.router, prefix="/api", tags=["Book Publications"])
app.include_router(ict_pedagogy.router, prefix="/api", tags=["ICT Pedagogies"])
app.include_router(research_guidance.router, prefix="/api", tags=["Research Guidance"])
app.include_router(research_project.router, prefix="/api", tags=["Research Projects"])
app.include_router(ipr.router, prefix="/api", tags=["IPR Entries"])
app.include_router(research_award.router, prefix="/api", tags=["Research Awards"])
app.include_router(conference_paper.router, prefix="/api", tags=["Conference Papers"])
app.include_router(research_proposal.router, prefix="/api", tags=["Research Proposals"])
app.include_router(product_development.router, prefix="/api", tags=["Product Developments"])
app.include_router(self_development_fdp.router, prefix="/api", tags=["Self-Development FDP"])
app.include_router(industrial_training.router, prefix="/api", tags=["Industrial Trainings"])

# Part A Endpoints
app.include_router(teaching_process.router, prefix="/api", tags=["Part A - Teaching Process"])
app.include_router(course_file.router, prefix="/api", tags=["Part A - Course File"])
app.include_router(teaching_methods.router, prefix="/api", tags=["Part A - Teaching Methods"])
app.include_router(student_feedback.router, prefix="/api", tags=["Part A - Student Feedback"])
app.include_router(departmental_activities.router, prefix="/api", tags=["Part A - Departmental Activities"])
app.include_router(university_activities.router, prefix="/api", tags=["Part A - University Activities"])
app.include_router(social_contributions.router, prefix="/api", tags=["Part A - Social Contributions"])
app.include_router(industry_connect.router, prefix="/api", tags=["Part A - Industry Connect"])
app.include_router(qualification_enhancement.router, prefix="/api", tags=["Part A - Qualification Enhancement"])
app.include_router(project.router, prefix="/api", tags=["Part A - Project"])
app.include_router(acr.router, prefix="/api", tags=["Part A - ACR"])
app.include_router(part_a_summary.router, prefix="/api", tags=["Part A - Summary"])

# Overall Endpoints
app.include_router(appraisal_summary.router, prefix="/api", tags=["Appraisal Summary"])
app.include_router(remarks.router, prefix="/api", tags=["Appraisal Remarks"])
app.include_router(finalization.router, prefix="/api", tags=["Finalization (Enclosures & Declaration)"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Faculty Appraisal API"}
