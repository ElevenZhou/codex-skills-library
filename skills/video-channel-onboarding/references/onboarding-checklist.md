# Video Channel Onboarding Checklist

## 1. Intake

- Create raw resource folder: `渠道接入资料/<channel-name>/` (gitignored, credentials OK).
- Create adapter/decision folder: `渠道接入/<family>/<channel-name>/`.
- Store original source materials:
  - DOCX/PDF/TXT exports
  - API links and passwords as private notes only when allowed
  - screenshots
  - upstream sample code
  - pricing/model notes from business
- Write a `渠道接入资料/<channel-name>/README.md` summarizing: endpoints, credentials (types only, values in separate file), models, what's tested vs unconfirmed.
- Convert DOCX/PDF to text for search.
- Record known-good/known-bad historical conclusions.

## 2. Contract Analysis

Identify:

- endpoint and region
- auth type: bearer key, AK/SK signing, SDK, cookie, custom headers
- submit/query/cancel/result actions
- async states and terminal states
- request body shape
- model names and aliases
- required media URL accessibility rules
- casing-sensitive fields
- billing parameters and non-billable probe method

Compare against existing adapters:

- Seedance/Doubao official task adaptor
- NewAPI/OpenAI video endpoints
- existing special adapter services
- vendor-specific adapter packages

Decide:

- new channel type
- existing task adaptor
- special channel config
- standalone adapter service
- temporary compatibility shim

## 3. Repo Implementation

Checklist:

- constants/channel registration
- relay adaptor registration
- task adaptor package or adapter service
- frontend channel type labels
- model ratio/fixed price defaults
- model list exposure
- group/ability implications
- request mapping tests
- response parsing tests
- error handling tests
- no full secrets in repo

Use existing patterns in the codebase. Avoid broad refactors.

## 4. Production Configuration

Configure:

- channel name
- type
- base URL
- key format
- models
- groups
- abilities
- priority/weight
- auto ban policy during smoke
- channel remark summarizing endpoint/model/pricing/key format

For NewAPI memory cache, restart or wait for sync after DB channel/ability changes.

## 5. Pricing

Record business instruction and implement:

- model ratio or fixed model price
- completion ratio when applicable
- group ratio
- hidden vs exposed models
- discount/no-discount rule

Verify pricing failure modes before live smoke. A `model_price_error` means routing may already be working but pricing is missing.

## 6. Smoke Tests

Minimum tests:

- route/pricing smoke: ensure request selects the intended channel
- text-to-video: low duration/resolution, poll to terminal status when feasible
- image/reference-to-video: use a public URL verified by GET
- query endpoint: verify customer-facing shape and upstream task data

### Asset Action Tests (if upstream supports asset management)

Test each of the 12 Seedance-compatible Actions individually against the new upstream. Record which succeed and which return errors (e.g., 401). **Missing Actions are expected and acceptable** — the goal is honest testing, not forcing all 12 to work. Do NOT borrow another channel's upstream to fill gaps.

Use the latest dated upstream document as the expected capability baseline. For kmood, the 2026-07-13 document defines all 12 Actions, so test all 12 against kmood after the matching upstream release.

Record results in a per-Action table:

| Action | HTTP Status | Result | Note |
|--------|-------------|--------|------|
| CreateAsset | 200 | ✅ | |
| GetAsset | 200 | ✅ | |
| UpdateAsset | 200 | ✅ | |
| DeleteAsset | 401 | ❌ | upstream not supported |
| ... | ... | ... | ... |

If asset creation is supported, the asset:// end-to-end flow is a release-critical acceptance test:
1. CreateAssetGroup → retain our own group-id
2. CreateAsset with a known image URL and that exact GroupId/group_id → get asset-id
3. Poll GetAsset until status=Active
4. CreatedVideo with `asset://asset-id` in content[] → get task-id
5. QueryTask until terminal status
6. Clean up the test asset and asset group when supported

Never upload into a provider sample/default group or a group belonging to another account/channel.

For visual validation, live-test both Actions:
1. CreateVisualValidateSession → open the returned H5 URL
2. Have a real person complete the liveness flow
3. GetVisualValidateResult → verify the terminal result and response mapping

Unit tests and mocked responses do not replace this live verification.

### Channel Isolation Verification

- Confirm the adapter container only has this channel's credentials in env (no other channel's AK/SK).
- Confirm asset management routes to the same upstream as video generation (same namespace).
- Confirm no upstream-specific fields are auto-injected into payloads (e.g., ProjectName is Volcengine-only; kmood rejects it silently).
- If the upstream account/UID is shared, test platform-user isolation with two distinct users:
  - each user gets a different reusable default group when GroupId is omitted
  - user A cannot get/list/update/delete user B's group or asset
  - user A cannot use user B's `asset://` ID in video generation
  - visual-validation tokens and returned groups remain bound to their creator
  - raw API keys and raw user IDs are not stored or forwarded upstream
  - ownership mappings survive adapter/container restart on a persistent volume

Capture:

- public task ID
- upstream task ID if stored
- status sequence
- final status
- output URL presence
- raw upstream error body if failed
- per-Action pass/fail table for the 12 asset Actions

## 7. Documentation

After smoke tests pass, ALL of the following must be written or updated:

### Must-write (channel is incomplete without these):

1. **使用说明** — `docs/<slug>/使用说明.md` or `渠道接入/<adapter>/README.md`
   - Internal/coworker usage guide
   - Endpoints, auth, models, pricing, known constraints
   - Per-Action availability table

2. **线上说明** — `渠道接入/<adapter>/docs/<slug>/index.html`
   - Customer-facing online page
   - Deployed to `video.flaios.com/docs/<slug>/`
   - Must NOT mention internal upstream names (use channel label letter like K instead)
   - List supported Actions with examples
   - Mark unsupported Actions as 即将支持, not 暂不支持
   - Include asset:// workflow if CreateAsset is supported

3. **关联文档更新** — update all cross-referenced documents:
   - Root `README.md`: add channel to list, update directory structure, production version
   - `Seedance2.0官方兼容使用说明.md`: update if Seedance interface is affected
   - `渠道接入资料/<channel>/README.md`: mark confirmed items, remove resolved 待确认
   - Any other doc that references channels or Action availability

### Customer docs should show:

- base URL
- auth
- model names
- create/query endpoints
- text example
- image/reference example
- query result shape
- asset:// workflow (CreateAsset → poll Active → CreatedVideo) if supported
- known constraints (mark unsupported Actions as 即将支持, never mention the upstream name)

### Internal docs should additionally show:

- channel id/type/group
- upstream endpoint/action/version
- key format
- pricing config
- deploy version
- smoke task IDs
- per-Action availability table (which of 12 asset Actions work on this upstream)
- known pitfalls

## 8. Deployment

For Tokyo `video.flaios.com`:

- build Linux binary locally when appropriate
- upload to `/opt/new-api/new-api-bin/`
- update docker compose mount and `VERSION`
- restart only required services
- verify `x-new-api-version`
- deploy docs to `/opt/new-api/brand/docs/<slug>/index.html`
- update `/opt/new-api/brand/docs/index.html`

For Python adapters with bind mounts (e.g., kmood-adapter):

- copy source to `/opt/new-api/<adapter>/app.py` on the host (bind mount makes it visible in container)
- `sudo docker restart flaios-<adapter>`
- do NOT use `docker cp` on bind-mounted files (fails with "device or resource busy")

Keep production backups of changed compose/docs files.
Batch SSH commands to avoid fail2ban blocking.

## 9. Final Handoff

Include:

- live URL
- docs URL
- channel id/type/model/group
- deployed version
- successful smoke task IDs
- exact blockers if any
- files changed

Do not include full secrets.
