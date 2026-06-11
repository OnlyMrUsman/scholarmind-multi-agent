# ScholarMind — Startup Checklist (after reboot)

Follow these steps to bring the system back up. Total time: ~3-5 minutes.

## 1. Start Docker Desktop
- Open Docker Desktop on Windows.
- Wait until it says "Engine running" (bottom-left green).

## 2. Wait for Dify containers to auto-start
- The Dify containers and the scholarmind-tools container start automatically
  (restart policy = always). Give them 2-3 minutes.
- DO NOT run "docker compose down -v" ever — the -v deletes the database.

## 3. Open Dify
- Go to http://localhost in the browser.
- If it looks empty or won't load, WAIT and refresh (Ctrl+Shift+R). It is still starting.

## 4. Quick health check (optional, in WSL)
    docker ps | grep scholarmind        # should show "Up"
    docker exec docker-api-1 curl -s http://scholarmind-tools/health

## 5. Open and run ScholarMind
- Studio -> ScholarMind -> Preview (or open the published app).
- Ask a question to confirm it works.

## If anything is missing (rare)
- The whole app is backed up as dify-export/ScholarMind.yml.
- In Dify Studio: Import DSL -> select that file -> the full 5-agent app returns.

## Notes
- The arXiv search runs INSIDE Dify (Code node) — no manual app.py needed.
- DeepSeek API key must be present under Settings -> Model Provider.
