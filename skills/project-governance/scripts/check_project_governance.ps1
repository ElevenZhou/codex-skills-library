param([string]$Root = (Get-Location).Path)
$required = @('AGENTS.md','README.md','CHANGELOG.md','AI_PROJECT_HANDOFF.md','project-governance.yml','docs/project/overview.md','docs/project/architecture.md','docs/project/decisions.md','docs/project/milestones.md','docs/project/intake.md')
$missing = @($required | Where-Object { -not (Test-Path (Join-Path $Root $_)) })
$git = git -C $Root status --short --branch 2>&1
[pscustomobject]@{ root=$Root; missing=$missing; git_status=@($git); pass=($missing.Count -eq 0) } | ConvertTo-Json -Depth 4
