# Bitey Enterprise App

**Create, personalize, test and operate a dedicated AI assistant for each business.**

Bitey Enterprise App is the business-facing application for the Bitey platform. It guides a company through creating its own personalized AI assistant, importing business knowledge, configuring its identity and behavior, connecting communication channels, testing the assistant, and activating it for customers.

> **Core idea:** Bitey is the platform. Each business gets its own isolated AI assistant with its own name, personality, knowledge, rules, customers, conversations, channels, and configuration.

## Vision

Turn business AI deployment from a technical integration project into a guided product that a business owner can configure from a phone or web interface without needing to understand APIs, webhooks, databases, or AI infrastructure.

A company should be able to:

1. Create its business profile.
2. Create an AI assistant and give it a personalized name.
3. Configure personality, tone, language and business role.
4. Import information from its website and documents.
5. Connect WhatsApp, Telegram and a dedicated web experience.
6. Run context-aware and randomized tests generated from the company's actual knowledge.
7. Detect unsupported answers and contradictions.
8. Review an AI readiness score.
9. Activate the assistant.
10. Continue improving the assistant after deployment.

## Product Model

```text
                         BITEY PLATFORM
                               |
              +----------------+----------------+
              |                                 |
          Company A                         Company B
              |                                 |
        Assistant A                       Assistant B
          "Bitey"                            "Sofia"
              |                                 |
       +------+------+                   +------+------+
       |      |      |                   |      |      |
      Web  WhatsApp Telegram            Web  WhatsApp Telegram
```

The underlying Bitey Core is shared infrastructure. Business data and assistant configuration are tenant-isolated by `company_id` and each assistant has a stable `assistant_id`.

## Personalized AI Identity

The assistant is a first-class product object, not merely a prompt.

Each assistant can have:

- Name
- Avatar/branding
- Greeting
- Personality
- Tone
- Languages
- Business role
- System instructions
- Business rules
- Escalation behavior
- Knowledge sources
- Services/products
- Channel configuration
- Memory/context policy
- Feature entitlements
- Test history
- Activation state

Example:

```text
Company: BiteFixes
Assistant: Bitey

Company: Example Dental
Assistant: Sofia

Company: Auto Center ABC
Assistant: Alex
```

## Guided Enterprise Onboarding

The mobile/web application should configure the company progressively rather than presenting one large technical form.

```text
Create account
    -> Create company
    -> Name the AI
    -> Configure identity
    -> Import website/documents
    -> Review extracted knowledge
    -> Configure business rules
    -> Connect WhatsApp
    -> Connect Telegram
    -> Enable Web
    -> Run tests
    -> Readiness assessment
    -> Activate
```

The onboarding flow should remember completed information and only ask for missing or ambiguous data.

## Business Knowledge

Authorized business sources can include:

- Company website
- PDF
- DOCX
- TXT
- CSV
- FAQ
- Product catalog
- Service catalog
- Policies
- Manually entered information

Knowledge extraction should identify structured information such as:

```text
Products
Services
Prices
Schedules
Locations
Policies
Guarantees
FAQs
Contact information
Business terminology
```

Every important answer should be traceable to a business source or a configured business rule. When information is unavailable, the assistant must prefer `UNKNOWN` or human escalation over invention.

## Multichannel Architecture

One personalized assistant operates across supported channels.

```text
                       Company Assistant
                              |
                         Bitey Core
                              |
              +---------------+---------------+
              |               |               |
           WhatsApp        Telegram          Web
              |               |               |
              +---------------+---------------+
                              |
                    Shared business context
```

Initial channel targets:

- WhatsApp Business Platform
- Telegram Bot
- Dedicated business web experience

Future channels must reuse the same assistant identity and business context instead of creating separate AI implementations.

## WhatsApp Onboarding

The app should guide the business through the required WhatsApp Business Platform configuration, including business account, number, webhook, verification and connection testing.

Sensitive credentials must never be embedded in the mobile application. They belong in secure backend/secret infrastructure.

## Telegram Onboarding

The app should guide the business through bot creation and connection:

```text
Create bot
   -> Obtain token
   -> Connect
   -> Configure webhook
   -> Verify
   -> Active
```

## Dedicated Business Web

Each assistant can receive a branded web experience, for example:

```text
business.bitey.ai
```

and, when supported later, a customer-owned domain such as:

```text
ai.business.com
```

The web experience can expose the business branding, services, contact information and AI chat while using the same assistant configuration as WhatsApp and Telegram.

## Context-Aware Random Test Engine

A central product requirement is that every new business AI is tested using the actual context of that business.

Tests must not be a fixed generic questionnaire.

```text
Website + Documents + Services + Policies + FAQs
                         |
                  Knowledge extraction
                         |
                Context test generator
                         |
              Randomized test scenarios
                         |
                    AI assistant
                         |
                 Response evaluator
                         |
                PASS / FAIL / REVIEW
```

Examples of generated scenarios for a computer repair business:

- Ask about a service that exists.
- Ask for a documented price.
- Ask about warranty.
- Ask about opening hours.
- Ask about location.
- Ask about a service that does not exist.
- Introduce a conflicting price.
- Ask an ambiguous question.
- Ask a question outside the company's scope.

The test corpus changes when the company's knowledge changes.

## Adversarial and Contradiction Testing

The evaluator must test difficult cases, not only happy paths.

Expected classifications include:

```text
SUPPORTED
UNKNOWN
UNSUPPORTED
CONTRADICTORY
AMBIGUOUS
REQUIRES_HUMAN
```

The assistant must not invent a service, price, policy, location, guarantee or business capability that is not supported by the company's authorized knowledge.

## Conversation Regression Testing

Real failures discovered in production or manual testing become regression scenarios.

Example:

```text
User: tengo mi pc lenta con windows
Assistant: ...

User: windows 10
Assistant: ...
```

The active context must retain:

```text
device = computer
problem = slow_performance
platform = Windows
os_version = Windows 10
```

Likewise:

```text
PC lenta
    -> Windows 10
    -> tambien se calienta
```

should remain one problem, while:

```text
PC lenta
    -> mi celular no enciende
```

must create a new problem.

## Domino State Model

Bitey Enterprise uses the state concepts already being developed in Bitey Core.

```text
Customer
   -> Conversation
   -> Active Problem
   -> Entities
   -> Intent
   -> Decision
   -> Ticket / Service
   -> Resolution
```

The system must distinguish at least:

- `CONTINUATION`
- `ENTITY_UPDATE`
- `NEW_PROBLEM`
- `RESOLUTION`
- `ESCALATION`

This prevents unrelated customer problems from being merged incorrectly.

## AI Readiness

Before activation, the assistant should receive an automated readiness assessment.

Example:

```text
BITEY READINESS

Knowledge Accuracy       96%
Context Retention        94%
Conversation Quality     92%
Contradiction Handling   98%
Safety                   100%
Channel Configuration    100%

Overall                   96%

STATUS: READY
```

Suggested lifecycle:

```text
DRAFT -> CONFIGURING -> TESTING -> READY -> ACTIVE
                                  |
                                  +-> NEEDS_REVIEW
```

Critical failures should block production activation until resolved or explicitly reviewed.

## Feature Entitlements

Capabilities must be controlled by business plan/entitlements rather than by separate codebases.

Possible tiers:

### Starter

- Web
- Basic AI
- Business knowledge

### Business

- Web
- WhatsApp
- Telegram
- CRM integration
- Tickets
- Memory/context

### Enterprise

- All supported channels
- Advanced memory
- Advanced contextual testing
- Analytics
- Automation
- API
- Advanced integrations

The final commercial plans remain configurable and should not be hard-coded into the application.

## Multi-Tenant Principles

Every business is a tenant.

```text
Company
 |
 +-- Assistant
 +-- Knowledge
 +-- Channels
 +-- Customers
 +-- Conversations
 +-- Problems
 +-- Tickets
 +-- Tests
 +-- Analytics
```

Minimum isolation identifiers:

- `company_id`
- `assistant_id`
- channel identity
- customer identity
- conversation identity

No company must be able to access another company's knowledge, customers, conversations, credentials or assistant configuration.

## Security Principles

- Never expose provider secrets in the APK.
- Never store API credentials as client-side constants.
- Authenticate backend requests.
- Enforce tenant isolation server-side.
- Protect channel credentials using secure secret infrastructure.
- Audit sensitive configuration changes.
- Minimize personal data collection.
- Keep customer data separate from company configuration.
- Validate channel ownership and connection status.
- Do not expose one company's knowledge to another company's assistant.

## Technology Direction

Initial direction:

```text
Bitey Enterprise App
        |
   React Native / Expo
        |
Enterprise API
        |
Bitey Backend
        |
Supabase
        |
Bitey Core
```

The app is intended to be mobile-first, with a web administration experience possible later. Backend contracts should remain independent of the mobile UI.

## Relationship With Existing Bitey Projects

```text
bitefixes-backend
    -> Bitey Core / Backend

bitey-web
    -> Web AI experience

bitey-enterprise-app
    -> Business onboarding and administration

bitey-system-bots-trading
    -> Trading module

JobIA
    -> Job intelligence product
```

BiteFixes should become the first real business tenant and reference implementation rather than hard-coding the whole Enterprise product around BiteFixes.

## Development Roadmap

### Phase 1 — Foundation

- [ ] Expo application scaffold
- [ ] Authentication
- [ ] Company profile
- [ ] Assistant creation
- [ ] Personalized assistant name
- [ ] Basic dashboard
- [ ] Backend API contract

### Phase 2 — Knowledge

- [ ] Website ingestion
- [ ] Document upload
- [ ] Knowledge extraction
- [ ] Source tracking
- [ ] Knowledge review/editing

### Phase 3 — AI Identity

- [ ] Personality
- [ ] Tone
- [ ] Languages
- [ ] Greeting
- [ ] Business rules
- [ ] Escalation configuration

### Phase 4 — Channels

- [ ] Web
- [ ] WhatsApp
- [ ] Telegram
- [ ] Connection status
- [ ] Channel verification

### Phase 5 — Testing

- [ ] Context-aware test generation
- [ ] Randomized scenarios
- [ ] Conversation regression tests
- [ ] Contradiction detection
- [ ] Unsupported-answer detection
- [ ] Readiness score

### Phase 6 — Production

- [ ] Feature entitlements
- [ ] Subscription integration
- [ ] Analytics
- [ ] Audit logs
- [ ] Enterprise controls
- [ ] Multi-business administration

## Definition of Done

A new business should be able to complete this lifecycle without developer intervention:

```text
Install App
    -> Create Account
    -> Create Company
    -> Name AI
    -> Configure Personality
    -> Provide Website/Documents
    -> Review Knowledge
    -> Connect WhatsApp
    -> Connect Telegram
    -> Enable Web
    -> Run Contextual Tests
    -> Pass Readiness
    -> Activate AI
```

## Strategic Intention

Bitey Enterprise is the control plane for creating many specialized business AI assistants from one common intelligence platform.

The business buys the service.

Bitey creates the assistant.

The business gives it identity and knowledge.

Bitey tests it against the real business context.

The business activates it across its selected channels.

Customers interact with the personalized assistant.

The assistant maintains business context, customer context and problem state according to the platform's policies.

```text
                    BITEY PLATFORM
                          |
          +---------------+---------------+
          |               |               |
       Company A       Company B       Company C
          |               |               |
        AI A             AI B             AI C
          |               |               |
       Web/WA/TG       Web/WA/TG       Web/WA/TG
```

**Bitey Enterprise App is the business control plane for provisioning, configuring, testing and operating personalized AI assistants.**
