# Enterprise API security deployment gate

## Required environment variable

Set `BE_API_TOKEN` as a secret in the backend deployment environment. Generate a long, random token using a trusted password manager or secret generator. Do not commit the token, expose it in frontend JavaScript, or paste it into chat.

When `BE_API_TOKEN` is absent, all stateful `/onboarding/*` endpoints return HTTP 503. Requests without a matching `Authorization: Bearer <token>` header return HTTP 401. `GET /health` remains public and reports whether the token is configured, without disclosing its value.

## Important limitation

This token is a temporary fail-closed deployment gate, not complete multi-tenant authentication. Every caller possessing the same token has the same API authority. The current `_SESSIONS` store is process-local, may be lost on restart, and is not durable or tenant-isolated. Assistant identifiers must not be treated as authorization.

**Do not expose this API as a production multi-tenant service yet.** Before production, implement per-user identity (for example, verified Supabase Auth JWTs), derive `company_id` from the verified identity rather than request input, check ownership for every assistant/resource, enforce database Row Level Security, and move state to a durable database. Do not put `BE_API_TOKEN` in the Cloudflare Pages frontend.

## Verify

Install dependencies, then run:

```sh
pip install -r requirements.txt
pip install -r requirements-dev.txt
pytest -q
```

Expected checks include public health, fail-closed behavior when the token is unset, rejection of missing/incorrect bearer tokens, and access with the configured token.

## Frontend integration

The static Pages frontend currently has no proven authenticated API adapter for this backend. Do not enable its login/register UI by embedding the shared token in browser code. Integrate a real user-authentication flow and a server-side API proxy before enabling end-user access.
