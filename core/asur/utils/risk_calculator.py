import json

from .schemas import Risk, Requirement, Priority

try:
    import openpyxl
    import pandas as pd
except ImportError:
    raise ImportError("Please install openpyxl and pandas")


def find_requirement(x: str, requirements: list[Requirement]):
    for requirement in requirements:
        if requirement.shortName.split(".")[0].lower() == x.lower():
            return requirement


def calculate_effect(row: pd.Series, col: str) -> float:
    priority = row["requirement_obj"].priority.upper()
    if Priority[priority] == 0:
        return 0
    return row[col] / Priority[priority]


def calculate_impact(risks: list[Risk], requirements: list[Requirement], mitigation_matrix: pd.DataFrame):
    validate_inputs(risks, requirements, mitigation_matrix)
    df = mitigation_matrix.copy(deep=True)
    df["requirement_obj"] = df.index.map(lambda x: find_requirement(x, requirements))
    df.dropna(subset=["requirement_obj"], inplace=True)
    for risk in risks:
        col = risk.name
        df[col] = df.apply(lambda x: calculate_effect(x, col), axis=1)
        df[col] = df[col] * risk.riskAnswersValue * 0.8 / 2 / max(df[col].sum(), 1)
    return df.drop(["requirement_obj"], axis=1)


def validate_inputs(risks: list[Risk], requirements: list[Requirement], mitigation_matrix: pd.DataFrame):
    validate_risks(risks, mitigation_matrix)
    validate_requirements(requirements, mitigation_matrix)


def validate_risks(risks: list[Risk], mitigation_matrix: pd.DataFrame):
    missing_risks = [risk.name for risk in risks if risk.name not in mitigation_matrix.columns]
    if missing_risks:
        raise ValueError(f'Missing risks: {", ".join(missing_risks)}')


def validate_requirements(requirements: list[Requirement], mitigation_matrix: pd.DataFrame):
    missing_reqs = [
        req.shortName.split(".")[0]
        for req in requirements
        if req.shortName.split(".")[0] not in mitigation_matrix.index
    ]
    # TIP: Их тут не хватает, но вообще такого быть не должно
    # if missing_reqs:
    #     raise ValueError(f'Missing requirements: {", ".join(missing_reqs)}')


if __name__ == "__main__":
    with open("./augmented.json", "r", encoding="utf-8") as json_file:
        json_data = json.load(json_file)
    mitigation_matrix = pd.read_excel("./mitigation_matrix.xlsx", index_col=0)

    services_and_requirements_list = []
    for application in json_data["applications"]:
        services_and_requirements_list.extend(application["requirements"][:])

    risks = [Risk(**risk) for risk in json_data["riskManager"]["risks"]]
    services_and_requirements = [Requirement(**requirement) for requirement in services_and_requirements_list]

    services = [r for r in services_and_requirements if r.shortName.split(".")[0].startswith("SS")]
    rc = calculate_impact(risks, services, mitigation_matrix)

    print(rc.to_string())
    requirements = [r for r in services_and_requirements if not r.shortName.split(".")[0].startswith("SS")]
    rc = calculate_impact(risks, requirements, mitigation_matrix)
    print(rc.to_string())