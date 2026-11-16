from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import uuid

@dataclass
class InvestigationCase:
    transaction_id: str
    risk: dict
    evidence: dict
    case_id: str = field(default_factory=lambda: "CASE-" + uuid.uuid4().hex[:12])
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    review_status: str = "pending_human_review"
    analyst_decision: str | None = None

    def to_dict(self):
        return asdict(self)
