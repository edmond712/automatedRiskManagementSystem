from dataclasses import dataclass

Priority = {
    "NO": 0,
    "CRITICAL": 1,
    "MAJOR": 2,
    "HIGHEST": 4,
    "HIGH": 8,
    "MEDIUM": 16,
    "LOW": 32,
    "LOWEST": 64,
    "TRIVIAL": 128,
}


@dataclass
class RiskLevel:
    id: str
    name: str
    description: str


@dataclass
class Risk:
    id: str
    name: str
    description: str
    riskAnswersValue: float
    riskLevel: RiskLevel


@dataclass
class Requirement:
    id: str
    shortName: str
    description: str
    categoryId: str
    risksIds: list[list[str]]
    status: str = "ACTIVE"
    priority: str = "No"


@dataclass
class Project:
    name: str
    id: str
    firstCreateDate: str
    lastUpdateDate: str
    downloadDate: str
    risks: list[Risk]
    requirements: list[Requirement]
