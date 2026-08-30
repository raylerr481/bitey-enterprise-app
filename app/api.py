"""Minimal HTTP API for Bitey Enterprise onboarding."""
from __future__ import annotations
from dataclasses import asdict
from typing import Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, HttpUrl
from .onboarding import add_document, add_website, apply_study, generate_context, start_onboarding

app = FastAPI(title="Bitey Enterprise App", version="0.1.0")
_SESSIONS: dict[str, Any] = {}

class StartRequest(BaseModel):
    company_name: str = Field(min_length=1, max_length=200)
    assistant_name: str = Field(min_length=1, max_length=80)

class StudyRequest(BaseModel):
    study: dict[str, Any]

class DocumentClaim(BaseModel):
    key: str
    claim: str
    value: Any = None
    verified: bool = False
    confidence: float = 0.0

class DocumentRequest(BaseModel):
    filename: str
    claims: list[DocumentClaim] = []

class WebsiteRequest(BaseModel):
    url: HttpUrl

@app.get("/health")
def health():
    return {"status": "ok", "service": "bitey-enterprise-app", "version": "0.1.0"}

@app.post("/onboarding/start")
def onboarding_start(req: StartRequest):
    ctx = start_onboarding(req.company_name, req.assistant_name)
    _SESSIONS[ctx.assistant_id] = ctx
    return generate_context(ctx)

def _ctx(assistant_id: str):
    ctx = _SESSIONS.get(assistant_id)
    if not ctx:
        raise HTTPException(404, "assistant_id not found")
    return ctx

@app.post("/onboarding/{assistant_id}/study")
def onboarding_study(assistant_id: str, req: StudyRequest):
    return generate_context(apply_study(_ctx(assistant_id), req.study))

@app.post("/onboarding/{assistant_id}/document")
def onboarding_document(assistant_id: str, req: DocumentRequest):
    return generate_context(add_document(_ctx(assistant_id), req.filename, [x.model_dump() for x in req.claims]))

@app.post("/onboarding/{assistant_id}/website")
def onboarding_website(assistant_id: str, req: WebsiteRequest):
    return generate_context(add_website(_ctx(assistant_id), str(req.url)))

@app.get("/onboarding/{assistant_id}/context")
def onboarding_context(assistant_id: str):
    return generate_context(_ctx(assistant_id))
