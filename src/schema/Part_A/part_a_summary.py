from pydantic import BaseModel

class PartASummaryResponse(BaseModel):
    teachingScore: float
    feedbackScore: float
    deptActivityScore: float
    universityActivityScore: float
    socialScore: float
    industryScore: float
    acrScore: float
    totalFacultyScore: float
    totalHodScore: float
    totalDirectorScore: float
