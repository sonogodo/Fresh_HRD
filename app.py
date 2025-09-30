from fastapi import Form
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil, os, json
from Matching.preparingJobs import load_and_filter_jobs, transform_jobs
from Matching.pipeline import match_jobs_candidates

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/", response_class=HTMLResponse)
def root():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read(), status_code=200)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>File not found</h1>", status_code=404)

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API de matching ativa"}

@app.post("/match_vaga")
async def match_vaga_text(descricao: str = Form(...)):
    try:
        # 1. Monta objeto de vaga temporário
        vaga = {"id": "vaga_unica", "descricao": descricao}

        # 2. Carrega candidatos
        candidates_path = "JSONs/candidates.json"
        if not os.path.exists(candidates_path):
            return JSONResponse({"erro": "Arquivo de candidatos não encontrado."}, status_code=400)
        
        with open(candidates_path, "r", encoding="utf-8") as f:
            candidates = json.load(f)

        # 3. Aplica o matching
        res = match_jobs_candidates([vaga], candidates)

        # 4. Monta resposta: top 3 candidatos para a vaga
        match = res["top_matches"][0]
        top_candidatos = [
            {"candidato": c["cand_id"], "score": c["match_score"]}
            for c in match["top"]
        ]
        return {"vaga": descricao, "top_candidatos": top_candidatos}
    
    except Exception as e:
        return JSONResponse({"erro": "Erro interno do servidor", "detalhes": str(e)}, status_code=500)

@app.post("/match_vagas")
async def match_vagas(file: UploadFile = File(...)):
    vagas_path = "/tmp/vagas.json"
    try:
        # 1. Recebe o JSON e salva como vagas.json
        with open(vagas_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 2. Faz as transformações corretas no JSON
        filtered_jobs = load_and_filter_jobs()
        if not filtered_jobs:
            return JSONResponse({"erro": "Erro ao carregar ou filtrar vagas."}, status_code=400)
        jobs_list = transform_jobs(filtered_jobs)

        # 3. Carrega candidatos
        candidates_path = "JSONs/candidates.json"
        if not os.path.exists(candidates_path):
            return JSONResponse({"erro": "Arquivo de candidatos não encontrado."}, status_code=400)
        
        with open(candidates_path, "r", encoding="utf-8") as f:
            candidates = json.load(f)

        # 4. Aplica o matching
        res = match_jobs_candidates(jobs_list, candidates)

        # 5. Monta resposta: top 3 candidatos para cada vaga
        top_matches = []
        for match in res["top_matches"]:
            top_matches.append({
                "vaga": match["job_id"],
                "top_candidatos": [
                    {"candidato": c["cand_id"], "score": c["match_score"]}
                    for c in match["top"]
                ]
            })

        return {"top_matches": top_matches}
    
    except Exception as e:
        return JSONResponse({"erro": "Erro interno do servidor", "detalhes": str(e)}, status_code=500)
    
    finally:
        # 6. Apaga o arquivo temporário de vagas
        if os.path.exists(vagas_path):
            try:
                os.remove(vagas_path)
            except:
                pass  # Ignore cleanup errors

app_handler = app  # Para garantir compatibilidade com Vercel