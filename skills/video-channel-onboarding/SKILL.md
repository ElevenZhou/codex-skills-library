---
name: video-channel-onboarding
description: End-to-end workflow for onboarding new video generation channels into video.flaios.com/NewAPI, especially when a user provides upstream docs, API keys, channel pricing, Seedance-compatible request requirements, or asks to create a channel folder, inspect docs, implement/configure an adapter, deploy to Tokyo, run text and image/reference smoke tests, and write usage docs, online docs, and colleague handoff notes.
---

# Video Channel Onboarding

Skill version: `2026.07.25`

Use this skill to handle a new video generation provider from first document intake through production smoke validation and handoff documentation.

## Core Rule

Treat a new channel as incomplete until all of these are true:

- Source materials are copied into a durable channel folder.
- The upstream API contract is summarized and reconciled against existing NewAPI/video adapters.
- The chosen integration shape is explicit: new channel type, special channel under an existing provider, standalone adapter service, or existing task adaptor config.
- Secrets are configured only in channel key/secret storage or production env, never committed to code, README, logs, or screenshots.
- At least one text video task and one image/reference video task have been submitted or a blocker is recorded with exact upstream response.
- Customer-facing usage docs, online docs, and an internal handoff summary are written.

## Channel Isolation Rule (Critical)

**Different channels' upstream APIs must never be mixed.** Each channel's asset management, video generation, and all other operations must route to that channel's own upstream only.

This rule exists because of a real production incident (2026-07-10): the kmood adapter had Volcengine AK/SK configured, causing `CreateAsset` to route to Volcengine while `CreatedVideo` went to kmood. Assets were created in the Volcengine namespace but `asset://` references were sent to kmood, which could not find them.

Enforcement:

1. **One adapter = one upstream.** Do not configure a second upstream's credentials on an adapter that serves a different upstream.
2. **Credentials do not cross channels.** Each channel's AK/SK/API Key is used only for that channel.
3. **asset:// must stay in the same namespace as video generation.** If video generation goes to upstream A, assets must also be created on upstream A.
4. **Do not auto-inject upstream-specific fields.** For example, `ProjectName` is a Volcengine concept; injecting it into a kmood payload caused HTTP/2 stream resets. Only pass fields the target upstream accepts.
5. **Different upstreams' capability gaps are not filled by borrowing from each other.** If a channel lacks an Action, do not route that Action to another upstream to "complete the set." Document the gap honestly.
6. **Shared upstream accounts require local tenant isolation.** If multiple platform users share one upstream UID/account, upstream ownership checks do not separate those users. Derive an opaque principal from the authenticated platform `user_id`, persist group/asset/session ownership, and enforce it for create/get/list/update/delete, visual-validation results, and `asset://` generation.
7. **Never use a global shared default asset group.** User-created groups are reusable. If `CreateAsset` omits GroupId, lazily create one personal default group for that principal and reuse it. Prefer `user_id` over raw API key text so key rotation and multiple keys do not orphan assets.
8. **Asset ownership is two-dimensional: `(channel, principal)`.** First isolate each channel's upstream, credentials, group IDs, asset IDs, visual sessions, and `asset://` namespace; then isolate users inside that channel. A group, asset, session, or `asset://` created through channel A must never be queried, modified, deleted, or used for generation through channel B. Dedicated adapters may make channel implicit through the service instance; shared controllers and ownership databases must include a stable channel identifier in every ownership key and check.

Capability statements must follow the latest dated upstream document and live verification. For kmood, the 2026-07-13 document defines all 12 Seedance-compatible asset and visual-validation Actions; all 12 must route to kmood after its corresponding upstream release.

For the full checklist, read `references/onboarding-checklist.md`.

## Default Workflow

1. Create or update `渠道接入资料/<channel-name>/` for raw source materials (gitignored, credentials OK).
2. Create or update `渠道接入/<family>/<channel-name>/` for adapter code and decision notes.
3. Copy every upstream doc, screenshot, PDF, DOCX, TXT export, API link note, and local test result into the resource folder.
4. Convert DOCX/PDF sources to searchable text when needed, then inspect them before coding.
5. Decide the integration shape by comparing auth, endpoint style, async task semantics, request/response fields, model naming, and billing behavior with existing adapters.
6. Implement or configure the smallest compatible path for `video.flaios.com` first. Do not connect to `flaios.com` main site unless explicitly requested.
7. Configure channel metadata, model list, groups, abilities, model ratio/fixed price, remarks, and key format.
8. Deploy with a visible version header and keep a QA ledger.
9. Run smoke tests:
   - text-to-video, low duration/resolution
   - image/reference-to-video using a confirmed public URL, preferably domestic or self-hosted
   - asset:// end-to-end if the upstream supports asset management (CreateAssetGroup → CreateAsset with that GroupId → poll Active → CreatedVideo)
   - query until terminal status or a documented timeout
10. Preserve raw upstream errors when a smoke fails. Do not paraphrase away request IDs or error codes.
11. Write final docs:
    - internal README/update notes
    - customer usage guide
    - online HTML page under `video.flaios.com/docs/.../`
    - colleague summary suitable for forwarding

## Deployment Notes

For adapters with bind mounts (e.g., kmood-adapter): the source file on the host IS the container file. Deploy by copying to the host path and restarting the container. Do not use `docker cp` on bind-mounted files — it fails with "device or resource busy".

```bash
sudo cp /tmp/app.py /opt/new-api/<adapter>/app.py
sudo docker restart flaios-<adapter>
```

Batch SSH commands to avoid triggering fail2ban. Avoid many rapid successive SSH connections.

## Testing Standards

Prefer live tests only after key, pricing, group, and routing are verified. For paid upstreams, use the cheapest safe model/duration/resolution that still exercises the real path. If upstream docs warn that a full request creates a billable task, do non-billable probes only until credentials and model availability are confirmed.

For image/reference tests, verify the media URL with an actual `GET`, not only `HEAD`. Some signed OSS URLs reject `HEAD`. When in doubt, upload a known image to `video.flaios.com/brand/<channel>/...` and use that URL.

### Asset Action Testing

If the upstream provides asset management APIs, test each of the 12 Seedance-compatible Actions individually against that upstream before exposing them. Different upstreams support different subsets:

- kmood: all 12 are defined by the 2026-07-13 upstream document; verify all 12 live after the upstream release
- 中国移动 AICC: 10 (all group/asset CRUD, no visual validation API)
- Volcengine ark: all 12

**Missing Actions are expected and acceptable.** The goal is not to force all 12 to work, but to test each one honestly and record the result. If an Action returns 401 or is not provided by the upstream, mark it as unsupported. Never borrow another channel's upstream to fill the gap.

For each Action, record: Action name, HTTP status, pass/fail, brief note. Use this table format in the channel's internal docs.

For providers whose `CreateAsset` requires a group, do not reuse a provider sample, default, or foreign group. First call `CreateAssetGroup`, retain the returned group ID, and pass that exact ID as `GroupId`/`group_id` to `CreateAsset`.

For a shared upstream account, distinguish the provider's account-level group from the platform user's logical ownership. The adapter may auto-create a reusable per-user default group, but it must still verify every explicit group ID and asset ID against the authenticated principal. Persist mappings on a durable volume and fail closed if the trusted identity signature or ownership database is unavailable.

For asset:// end-to-end (required when the upstream supports asset creation): CreateAssetGroup → CreateAsset with the newly created own GroupId → poll GetAsset until Active → CreatedVideo with asset:// → query until succeeded. Treat this as a release-critical acceptance test, not an optional follow-up.

Visual validation requires live manual participation. Test both `CreateVisualValidateSession` and `GetVisualValidateResult` with a real person completing the H5 flow; adapter/unit tests alone do not count as acceptance.

## Documentation Completion Rule

A channel is not complete until ALL related documents are written and updated after smoke tests pass:

1. **使用说明** (`docs/<slug>/使用说明.md` or `渠道接入/<adapter>/README.md`) — internal/coworker usage guide with endpoints, auth, models, known constraints.
2. **线上说明** (`渠道接入/<adapter>/docs/<slug>/index.html`) — customer-facing online page, deployed to `video.flaios.com/docs/<slug>/`. Must not mention internal upstream names. Must list supported Actions and mark unsupported ones as 即将支持.
3. **关联文档更新** — after the channel goes live, update:
   - Root `README.md` (channel list, directory structure, production version)
   - `Seedance2.0官方兼容使用说明.md` (if the channel affects Seedance docs)
   - Any cross-reference docs that list channels or Actions
   - The channel's `渠道接入资料/<channel>/README.md` (mark confirmed items, remove 待确认 that are now resolved)

Customer-facing docs rule: use the channel label letter (e.g., K) to annotate capability limits. Never write the upstream's real name (kmood, ecloud, etc.) in customer-facing material.

## Handoff Format

Keep the final handoff concise:

- What is live
- Channel ID/type/group/model
- Which paths clients should call
- Which smoke tasks succeeded
- Where docs live
- Remaining risks or disabled pieces

Never include full API keys or AccessKey secrets in the handoff.

## Integration Shape Decision

There are two established patterns for channel integration on `video.flaios.com`. The choice must be made explicitly and recorded before implementation.

### Pattern A: Python Adapter Service (e.g., kmood-adapter)

A standalone FastAPI service under `渠道接入/<channel>-adapter/`. The service handles BOTH video generation AND asset management for that channel. It receives requests from NewAPI (which routes to it via the channel base URL) and forwards them to the upstream.

When to choose:
- The upstream has its own asset management API with a signing scheme different from Volcengine (e.g., HmacSHA1 V2.0, custom headers, AK/SK with different canonical request format).
- The upstream's video API is Seedance-compatible (same `content[]` format) but may have response quirks that need normalization.
- You want to avoid modifying the NewAPI Go source (no binary rebuild needed).
- The upstream wraps/proxies Seedance but adds its own layer (e.g., ecloud MaaS wraps Volcengine Seedance).

Characteristics:
- One Python service = one channel = one logical upstream (may have multiple endpoints, e.g., separate video + asset APIs, but all belong to the same provider).
- Asset management is handled inside the adapter, NOT in NewAPI's Go code.
- NewAPI treats it as an OpenAI-compatible or custom-type channel with base URL pointing to the adapter.
- Deploy: bind mount, cp + restart, no Go rebuild.

Existing examples: `kmood-adapter` (video + 12 documented asset/visual Actions → kmood.cn; live acceptance follows the upstream release).

### Pattern B: Go Native Channel Type (e.g., VolcengineSeedanceWangzhe type 61)

A new channel type constant + task adaptor in `new-api-source/relay/channel/task/<provider>/`. Video generation goes through the task adaptor. Asset management goes through a separate Go controller (e.g., `controller/volc_asset_proxy.go`) with its own signing.

When to choose:
- The upstream IS the official provider (e.g., Volcengine Ark direct), so the API format is guaranteed compatible.
- You need deep integration with NewAPI's billing, caching, and task management.
- Asset management uses the same signing scheme as an existing Go controller (or you are prepared to write a new one).

Characteristics:
- Video: new or reused task adaptor (e.g., `doubao` adaptor serves types 45/54/61).
- Asset management: separate Go proxy controller, gated by channel type (currently only type 61 passes `volc_asset_proxy.go`).
- Requires Go build + binary transfer + NewAPI restart.
- Most complete integration but highest implementation cost.

Existing examples: type 61 VolcengineSeedanceWangzhe (doubao adaptor + volc_asset_proxy, 12 Actions).

### Decision Checklist

Answer these to determine the pattern:

1. Does the upstream use Volcengine-compatible signing for assets? → If yes, consider Pattern B (reuse volc_asset_proxy). If no (custom signing), lean Pattern A.
2. Is the upstream the official Volcengine endpoint or a wrapper/proxy? → Official = Pattern B. Wrapper = Pattern A.
3. Do you want to avoid rebuilding NewAPI? → If yes, Pattern A.
4. Does the upstream's video response format exactly match Volcengine's? → If unsure, Pattern A (can normalize in Python). If confirmed identical, Pattern B may reuse doubao adaptor.
5. Does the channel need asset management? → If yes and signing differs from Volcengine, Pattern A is the only clean option (per channel isolation rule, do not modify volc_asset_proxy to accept non-Volcengine channels).

### Reference Table

| Channel | Pattern | Video | Asset | adaptor |
|---------|---------|-------|-------|---------|
| kmood (54) | A (Python) | kmood.cn/CreatedVideo | kmood.cn asset/visual API (12 documented Actions) | `渠道接入/kmood-adapter/` |
| 王者 (61) | B (Go native) | ark.cn-beijing.volces.com (doubao adaptor) | volc_asset_proxy → ark OpenAPI (12 Actions) | `new-api-source/relay/channel/task/doubao/` |
| JimmyAI (59) | B (Go native, video only) | jimmyai.cn/v1/seedance/videos | N/A | `new-api-source/relay/channel/task/jimmyai/` |
| AliYike (60) | B (Go native, video only) | yike.aliyuncs.com (RPC AK/SK) | N/A | `new-api-source/relay/channel/task/yike/` |
| 中国移动 (TBD) | A (Python, recommended) | ecloud MaaS (Bearer) | AICC (HmacSHA1 V2.0, 10 Actions) | `渠道接入/cmcc-adapter/` (planned) |
