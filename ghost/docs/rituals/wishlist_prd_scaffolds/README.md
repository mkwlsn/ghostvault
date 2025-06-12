---
title: rituals index
status: active
owner: mike
version: 1.0
---

# 📜 Rituals Index

This folder contains speculative and high-leverage DX and DocOps rituals for use in GhostOS.

Each file in this folder defines a ritual concept that supports:
- ghost-native developer experience
- doc validation, planning, or integration
- automation of common LLM-in-the-loop workflows

These aren't just proposals—they're canon candidates. Once the core DocOps system is validated against the live repo, these rituals will be implemented, tested, and baked into the delivery flow.

## Contents

- `wishlist-self-linter.md` – validates semantic PRDs against the canonical markdown spec
- `wishlist-semantic-prd-scanner.md` – scans the vault for valid PRDs and generates dashboards or issue queues
- `wishlist-md-status-badger.md` – generates markdown badges reflecting PRD story status
- `wishlist-linear-agent-synergy.md` – maps markdown PRDs to Linear issues for bi-directional updates
- `wishlist-vault-self-tracer.md` – traces recent ghost operations and appends audit trails
- `wishlist-ritual-self-promoter.md` – promotes stable rituals into core CLI or daemon layers

## Status

These files are ready for:
- validation against live repo structure
- integration planning
- iterative implementation

Once ghostvault is pushed and folder validation completes, these will be evaluated for inclusion in `ghost/rituals` and registered in the manifest system.

Stay tuned—and stay haunted.
