# Gmail API Setup

Create OAuth credentials:

1. Go to Google Cloud Console.
2. Create or select a project.
3. Enable Gmail API.
4. Configure OAuth consent screen.
5. Create OAuth Client ID with application type `Desktop app`.
6. Download the JSON and save it as:
   `%USERPROFILE%\.codex\gmail\credentials.json`

The first `auth` run opens a browser login. After successful consent, a token is saved at:
`%USERPROFILE%\.codex\gmail\token.json`

For multiple Gmail accounts, use:

```powershell
& "C:\Users\AprilWu\AppData\Local\Programs\Python\Python311\python.exe" "%USERPROFILE%\.codex\skills\gmail-mail\scripts\gmail_mail.py" auth --account personal
& "C:\Users\AprilWu\AppData\Local\Programs\Python\Python311\python.exe" "%USERPROFILE%\.codex\skills\gmail-mail\scripts\gmail_mail.py" auth --account work
```

Then use `--account personal` or `--account work` on later commands.

Common errors:

- `credentials file not found`: save the OAuth client JSON at the expected path or pass `--credentials`.
- `access_denied`: add yourself as a test user on the OAuth consent screen if the app is in testing mode.
- `invalid_scope` or scope changes: delete `token.json` and run `auth` again.
- Browser cannot open: copy the printed auth URL into Chrome manually.
