from typing import Set

def coverage_score(job_skills: Set[str], cand_skills: Set[str]) -> float:
    # quanto dos requisitos da vaga o candidato cobre: len(inter)/len(job_skills)
    if not job_skills:
        return 0.0
    inter = job_skills.intersection(cand_skills)
    return len(inter) / len(job_skills)*100