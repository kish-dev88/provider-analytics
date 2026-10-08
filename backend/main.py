from pathlib import Path
from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .models import ProposedChange,BulkApproval,SourceRefreshResponse
from .service import get_providers,get_provider,submit_change,bulk_approve,SOURCE_HEALTH,CHANGE_EVENTS,refresh_source
app=FastAPI(title="Provider Data Change Monitoring API",version="1.0.0")
app.add_middleware(CORSMiddleware,allow_origins=["http://localhost:5173","http://127.0.0.1:5173"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
@app.get("/api/health")
def health(): return {"status":"ok"}
@app.get("/api/metrics")
def metrics(): return {"providers_monitored":24862,"providers_with_changes":120,"change_events":CHANGE_EVENTS,"require_human_review":42,"pending_approvals":12}
@app.get("/api/providers")
def providers(): return {"items":get_providers(),"total":len(get_providers())}
@app.get("/api/providers/{provider_id}")
def provider(provider_id:int):
    p=get_provider(provider_id)
    if not p: raise HTTPException(404,"Provider not found")
    return p
@app.post("/api/providers/{provider_id}/submit")
def submit(provider_id:int,c:ProposedChange):
    p=submit_change(provider_id,c.proposed_value)
    if not p: raise HTTPException(404,"Provider not found")
    return {"message":"Submitted for review","provider":p}
@app.post("/api/reviewer/bulk-approve")
def approve_many(payload:BulkApproval):
    a=bulk_approve(payload.provider_ids)
    return {"message":f"{len(a)} changes approved","approved_provider_ids":a}
@app.get("/api/source-health")
def source_health(): return {"sources":[{"name":n,"last_refreshed":v,"status":"Current"} for n,v in SOURCE_HEALTH.items()]}
@app.post("/api/source-health/{source}/refresh",response_model=SourceRefreshResponse)
def refresh(source:str):
    if source not in SOURCE_HEALTH: raise HTTPException(404,"Unknown source")
    return SourceRefreshResponse(source=source,last_refreshed=refresh_source(source),status="Current")
DIST=Path(__file__).resolve().parents[1]/"frontend"/"dist"
if DIST.exists(): app.mount("/",StaticFiles(directory=DIST,html=True),name="frontend")
