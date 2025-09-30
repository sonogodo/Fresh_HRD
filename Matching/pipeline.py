import pandas as pd
from typing import List, Dict, Any
import re

from Matching.scoring import coverage_score

TOP_N = 3

# Lista simples de stopwords (pode expandir)
STOPWORDS = set(["de", "da", "do", "em", "com", "e", "a", "o", "para", "por", "um", "uma", "no", "na", "os", "as"])

def simple_tokenizer(text):
    tokens = re.findall(r'\b\w+\b', text.lower())
    return [t for t in tokens if t not in STOPWORDS and len(t) > 2]

def extract_skills(text: str):
    tokens = re.findall(r'\b\w+\b', text.lower())
    return set(t for t in tokens if t not in STOPWORDS and len(t) > 2)

# ----------------------------
# Pipeline principal
# ----------------------------

def match_jobs_candidates(jobs: List[Dict[str,Any]], candidates: List[Dict[str,Any]]) -> Dict[str,Any]:
    job_texts = [j.get("descricao","") or j.get("title","") or "" for j in jobs]
    cand_texts = [c.get("perfil","") or c.get("summary","") or "" for c in candidates]

    job_skills_list = [extract_skills(t) for t in job_texts]
    cand_skills_list = [extract_skills(t) for t in cand_texts]

    m = len(jobs)
    n = len(candidates)
    combined_matrix = []
    for i in range(m):
        row = []
        for j in range(n):
            score = coverage_score(job_skills_list[i], cand_skills_list[j])
            row.append(score)
        combined_matrix.append(row)

    # Monta resposta: top N candidatos para cada vaga
    top_matches = []
    for i, job in enumerate(jobs):
        row = combined_matrix[i]
        ranked_idx = sorted(range(len(row)), key=lambda k: row[k], reverse=True)
        top = []
        for k in ranked_idx[:TOP_N]:
            top.append({
                "cand_index": int(k),
                "cand_id": candidates[k].get("id"),
                "match_score": float(row[k]),
                "cand_skills": sorted(list(cand_skills_list[k])),
                "job_skills": sorted(list(job_skills_list[i]))
            })
        top_matches.append({
            "job_index": i,
            "job_id": job.get("id"),
            "top": top
        })

    return {
        "top_matches": top_matches
    }