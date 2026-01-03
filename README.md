# Dev Docker Compose Library

A curated collection of **docker-compose stacks for local development**, organized by technology (Kafka, Redis,
databases, observability, etc.).  
Each folder contains **one or more compose YAML files** that you can run standalone or combine.

---

## Repo Structure

Each technology has its own folder:

### Naming convention (recommended)

- `docker-compose.yml` → default stack (most common)
- `docker-compose.<feature>.yml` → add-ons (ui, exporter, init-job, etc.)
- Or: `standalone.yml`, `cluster.yml`, `with-ui.yml` (whatever you prefer—just be consistent)

---

## Requirements

- Docker Engine + Docker Compose v2 (`docker compose version`)
- Recommended: GNU Make (optional)

---

## Quick Start

### Run a stack

From repo root:

```bash
docker compose -f kafka/docker-compose.yml up -d
```

Combine multiple files (base + addon)

```bash
docker compose \
  -f kafka/docker-compose.yml \
  -f kafka/docker-compose.ui.yml \
  up -d

```