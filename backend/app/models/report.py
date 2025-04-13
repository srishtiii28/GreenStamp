from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ReportBase(BaseModel):
    report_id: str
    ipfs_hash: str
    report_hash: str
    esg_score: int
    summary: str
    greenwashing_risk: str
    missing_disclosures: List[str]

class ReportCreate(ReportBase):
    pass

class Report(ReportBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Mock database
reports_db = {}

def create_report(report: ReportCreate) -> Report:
    report_id = len(reports_db) + 1
    now = datetime.utcnow()
    db_report = Report(
        id=report_id,
        created_at=now,
        updated_at=now,
        **report.dict()
    )
    reports_db[report_id] = db_report
    return db_report

def get_report(report_id: int) -> Optional[Report]:
    return reports_db.get(report_id)

def get_reports() -> List[Report]:
    return list(reports_db.values()) 