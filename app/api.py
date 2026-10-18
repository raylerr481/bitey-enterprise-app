"""Minimal HTTP API for Bitey Enterprise onboarding.

Security note: all stateful onboarding routes fail closed unless BE_API_TOKEN is
configured and supplied as a Bearer token. This is a deployment gate, not a
replacement for per-user authentication and tenant-level authorization.
"""
from __future__ import annotations

import hmac
import os
from typing import Any

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field, HttpUrl

from .onboarding import (
    add_document,
    add_website,
    apply_study,
    generate_context,
    start_onboarding,
)

app = FastAPI(title="Bitey Enterprise App", version="0.2.0")
_SESSIONS: dict[str, Any] = {}
_bearer = HTTPBearer(auto_error=False)


class StartRequest(BaseModel):
    company_name: str = Field(min_length=1, max_length=200)
    assistant_name: str = Field(min_length=1, max_length=80)


class StudyRequest(BaseModel):
    study: dict[str, Any]


class DocumentClaim(BaseModel):
    key: str = Field(min_length=1, max_length=160)
    claim: str = Field(min_length=1, max_length=2000)
    value: Any = None
    verified: bool = False
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class DocumentRequest(BaseModel):
    filename: str = Field(min_length=1, max_length=255)
    claims: list[DocumentClaim] = Field(default_factory=list, max_length=500)


class WebsiteRequest(BaseModel):
    url: HttpUrl


def require_api_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
) -> None:
    """Fail closed; never permit anonymous access to stateful endpoints."""
    expected = os.getenv("BE_API_TOKEN", "").strip()
    if not expected:
        raise HTTPException(
            status_code=503,
            detail="Enterprise API is not configured for authenticated access",
        )
    supplied = credentials.credentials if credentials else ""
    if (
        credentials is None
        or credentials.scheme.lower() != "bearer"
        or not hmac.compare_digest(supplied, expected)
    ):
        raise HTTPException(status_code=401, detail="Valid bearer token required")


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "bitey-enterprise-app",
        "version": "0.2.0",
        "authenticated_api_configured": bool(os.getenv("BE_API_TOKEN", "").strip()),
    }


@app.post("/onboarding/start", dependencies=[Depends(require_api_token)])
def onboarding_start(req: StartRequest):
    ctx = start_onboarding(req.company_name, req.assistant_name)
    # Current storage is process-local and is not suitable for production scale.
    _SESSIONS[ctx.assistant_id] = ctx
    return generate_context(ctx)


def _ctx(assistant_id: str):
    ctx = _SESSIONS.get(assistant_id)
    if not ctx:
        raise HTTPException(status_code=404, detail="assistant_id not found")
    return ctx


@app.post("/onboarding/{assistant_id}/study", dependencies=[Depends(require_api_token)])
def onboarding_study(assistant_id: str, req: StudyRequest):
    return generate_context(apply_study(_ctx(assistant_id), req.study))


@app.post("/onboarding/{assistant_id}/document", dependencies=[Depends(require_api_token)])
def onboarding_document(assistant_id: str, req: DocumentRequest):
    return generate_context(
        add_document(
            _ctx(assistant_id),
            req.filename,
            [claim.model_dump() for claim in req.claims],
        )
    )


@app.post("/onboarding/{assistant_id}/website", dependencies=[Depends(require_api_token)])
def onboarding_website(assistant_id: str, req: WebsiteRequest):
    return generate_context(add_website(_ctx(assistant_id), str(req.url)))


@app.get("/onboarding/{assistant_id}/context", dependencies=[Depends(require_api_token)])
def onboarding_context(assistant_id: str):
    return generate_context(_ctx(assistant_id))
