# Web + n8n deployment

The repository now includes a Docker Compose stack with the CleanFrame web app and n8n. The n8n workflow is `n8n/cleanframe-webhook.json`.

## Start locally

```powershell
docker compose up --build -d
```

- Web UI: `http://localhost:8765`
- n8n: `http://localhost:5678`

Import the workflow in n8n, activate it, and call the production webhook URL with a multipart `video` field plus `x`, `y`, `width`, `height`, and `rights_attested=true`. The workflow defaults to the sample icon region only as a convenience; editors should verify the region in the UI.

## Production notes

- Set `N8N_HOST`, `N8N_PROTOCOL`, and `N8N_WEBHOOK_URL` in a private `.env` file; never commit credentials.
- Put TLS/reverse proxy in front of n8n and use secure cookies.
- The Compose stack pins n8n `2.34.4`; review upgrades deliberately and back up the named `n8n_data` volume first.
- The workflow must remain inactive until rights and compliance review are complete.

## Current status

- Web app: implemented and tested locally.
- n8n workflow: authored and importable JSON; requires a running n8n instance for smoke testing.
- Public deployment: not performed from this workstation.
