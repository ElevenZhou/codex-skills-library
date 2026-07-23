---
name: domain-brand-finder
description: Project naming, brand-domain strategy, and domain availability workflow. Use when the user asks to name a project/product/company, brainstorm brand names, check domain availability, compare .com/.ai/.io/etc domains, avoid low-quality naming, rank registrable domains, or produce a naming/domain recommendation report.
---

# Domain Brand Finder

Skill version: `2026.07.24`

## Workflow

1. **Understand the product**
   - Identify category, audience, geography, trust requirements, and business model.
   - Extract hard constraints: preferred TLDs, max length, language, required words, banned words, company-name linkage, ICP/hosting constraints.
   - If context is missing, infer a reasonable naming direction and say the assumption.

2. **Define naming lanes**
   - Create 3-6 lanes before searching: e.g. descriptive, coined, company-linked, infrastructure-grade, premium SaaS, local-language.
   - Avoid low-trust terms for infrastructure products unless the user wants them: `relay`, `proxy`, `reseller`, `cheap`, `mirror`, `中转站`, `代理站`, `倒接口`.
   - Prefer names that can be explained in one sentence and survive product expansion.

3. **Generate candidates**
   - Prioritize `.com`; consider `.ai`, `.io`, `.app`, `.dev`, local ccTLDs, and defensive variants when useful.
   - Generate enough candidates to account for likely domain scarcity. For short `.com`, expect most good names to be taken.
   - Include spelling, pronunciation, negative connotations, and trademark-search risk notes.

4. **Check availability**
   - Use direct RDAP/WHOIS/registrar checks. For `.com` and `.net`, Verisign RDAP 404 usually means the registry has no domain object.
   - If available, still label it as “appears available now” because registrar premium/reserved status can differ and availability changes quickly.
   - If network access is unavailable, provide candidate lists and a command or script the user can run later.
   - Use `scripts/check_domains.py` for repeatable checks when possible.

5. **Rank recommendations**
   - Only recommend domains that appear available unless the user explicitly asks for taken/premium ideas.
   - Rank by: brand fit, memorability, spelling, business expansion, trust, TLD quality, and risk.
   - Present a short final shortlist. State what to buy first, what to buy defensively, and what can be skipped.

6. **Produce deliverables when asked**
   - Naming memo: chosen name, domain, rationale, slogan, brand story, brand voice, homepage copy.
   - Domain report: checked candidates, availability evidence, risk notes, final recommendation.
   - Implementation handoff: requirements for a standalone agent or CLI.

## Evidence standards

- Include the check date when domain availability matters.
- Record check source when possible: RDAP endpoint, registrar page, or WHOIS provider.
- Do not claim legal trademark clearance from domain checks. Recommend trademark search separately when the brand will be public.
- Separate domain purchase, DNS, hosting location, ICP filing, HTTPS, and product naming decisions.

## RDAP helper

Use the bundled script for common TLD checks:

```powershell
python C:\Users\AprilWu\.codex\skills\domain-brand-finder\scripts\check_domains.py flaios.com timenovai.com example.ai --json
```

Output statuses:

- `available`: RDAP returned 404 / not found.
- `registered`: RDAP returned 200.
- `unknown`: timeout, unsupported TLD, or ambiguous response; verify manually.

## Reference files

- `references/domain-strategy.md`: naming heuristics, scoring rubric, report format, and risk checklist.
