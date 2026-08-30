"""First functional onboarding flow for Bitey Enterprise."""
from __future__ import annotations
from typing import Any
from .enterprise_context import Evidence, EnterpriseContext, create_enterprise_context

STEPS = ("company", "study", "assistant", "sources", "context")

def start_onboarding(company_name: str, assistant_name: str) -> EnterpriseContext:
    return create_enterprise_context(company_name, assistant_name)

def apply_study(ctx: EnterpriseContext, study: dict[str, Any]) -> EnterpriseContext:
    ctx.business_study.update(study)
    return ctx

def add_document(ctx: EnterpriseContext, filename: str, claims: list[dict[str, Any]]) -> EnterpriseContext:
    ctx.sources.append({"type": "document", "ref": filename})
    for item in claims:
        evidence = Evidence("document", filename, str(item["claim"]), bool(item.get("verified", False)))
        if evidence.verified:
            ctx.add_fact(str(item["key"]), item.get("value"), evidence)
        else:
            ctx.add_hypothesis(evidence.claim, float(item.get("confidence", 0.0)), "unverified document claim")
    return ctx

def add_website(ctx: EnterpriseContext, url: str) -> EnterpriseContext:
    ctx.sources.append({"type": "website", "ref": url, "status": "pending_fetch"})
    return ctx

def generate_context(ctx: EnterpriseContext) -> dict[str, Any]:
    return ctx.to_dict()
