# OpenApplyBot Jobs

A local-first job discovery index that collects public listings from official company career sites, normalizes and deduplicates them, and serves them through a searchable API and dashboard.

> **Active scraper policy:** only sources that returned at least one valid job in the latest recorded local validation run are registered in the scraper manifest. A passing test means the source returned valid listings at test time; it is not a guarantee of future availability.

## Features

- Company-specific scraper modules with a central manifest.
- Public listing discovery and pagination for supported career sites and ATS platforms.
- Normalized job records with title and source URL validation.
- PostgreSQL, Redis-backed workers, API, scheduler, and frontend in Docker Compose.
- Local testing and operation; GitHub Actions is not required.

## Quick start

Requirements: Docker Engine with the Docker Compose plugin, Git, and a Linux/macOS shell.

    git clone https://github.com/OpenApplyBot/jobs.git
    cd jobs
    bash run.sh

The launcher checks prerequisites and starts the local stack. See its output for local service URLs and diagnostics. To stop services, use docker compose down from the repository root. Persistent volumes are not removed automatically.

## Repository layout

    backend/
      app/scrapers/
        manifest.json       # Registered and validated scraper sources
        companies/          # Company-specific scraper modules
        ...                 # Shared adapters and HTTP helpers
    frontend/                 # Search/dashboard UI
    scripts/                  # Local audit and maintenance utilities
    docs/                     # Project and scraper documentation
    docker-compose.yml        # Local service orchestration
    run.sh                    # Local setup and launcher

## Scraper validation

The manifest at backend/app/scrapers/manifest.json is the source of truth for active scrapers. A source is retained only if the recorded local test returned at least one job with valid title and URL fields.

Run the local audit from the repository root:

    bash scripts/audit-scrapers-local.sh

The audit writes generated reports under backend/. Do not commit generated logs, reports, virtual environments, secrets, database files, or build outputs.

**Important:** career sites change frequently, rate-limit requests, and may block automated traffic. A timeout is not proof that a site has no jobs; the active list is intentionally conservative and excludes sources that did not pass the recorded validation. Re-test excluded sources individually before re-registering them.

## Configuration and data

- Never commit real API keys, cookies, credentials, or .env files.
- Local database state is disposable only when you intentionally remove the relevant Docker volume.
- Job listings link to their original employer or applicant-tracking-system page. OpenApplyBot does not guarantee that a listing remains open.

## Development

1. Read CONTRIBUTING.md.
2. Make changes in the relevant company module and shared adapter only when necessary.
3. Test the affected scraper locally before registering it in the manifest.
4. Keep source URLs official, preserve pagination, and validate that each returned record has a non-empty title and a valid URL.
5. Update documentation when commands, architecture, or manifest behavior changes.

## Documentation

- Active sources: docs/DOMAINS_COVERED.md
- Contribution guide: CONTRIBUTING.md

## License

No license file is currently defined in this repository. Unless and until a license is added by the maintainers, all rights remain with the copyright holder.
