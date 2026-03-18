from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class ArticleCategory(str, Enum):
    SCHEDULING = "scheduling"
    BILLING_CODING = "billing_coding"
    INSURANCE_CLAIMS = "insurance_claims"
    PATIENT_RECORDS = "patient_records"
    REPORTING_ANALYTICS = "reporting_analytics"
    TECHNICAL_TROUBLESHOOTING = "technical_troubleshooting"
    ACCOUNT_PLANS = "account_plans"


@dataclass
class Article:
    id: int
    title: str
    slug: str
    category: ArticleCategory
    content: str
    created_by: int | None
    updated_at: datetime
    created_at: datetime


@dataclass
class ArticleSearchResult:
    id: int
    title: str
    category: ArticleCategory
    content: str
    rank: float
