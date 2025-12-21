from pydantic import BaseModel, ConfigDict
from models.git import Git
from models.whois import Whois

class AnalysisResponse(BaseModel):
    whois_data: Whois
    github_data: Git
    model_config = ConfigDict(from_attributes=True)