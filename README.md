# HousingCoop

Planning repo for a cooperative self-build community near Austin, TX.

## Documents (Claude Docs)
- Friendstead Structure and Market Analysis (2026-10-22), two tabs: "Structure and market" and "Build systems, labor and tax": https://claude.ai/artifact/GPnPpzM6q64GkTv3kwCPKM
- Zero Energy Passive Design Feasibility for Friendstead (2026-10-24), three tabs: "Feasibility" (ZERH-grade envelope recommended, Phius optional, co-op solar economics after the 2025 credit sunset), "Cost-effective design" (cheapest net-zero form, build system and package for the member homes) and "Prefab walls" (factory wall panels buy back member hours at $15 to $30 an hour but save no cash; exterior walls yes, interior as an option): https://claude.ai/artifact/6EXUtrMb4YmZxhAid7Ex2b
- Friendstead Community App: Rough Design (2026-10-28): invite-only PWA on pop-os for the exploration year (invites, learn pages, interest and fair-housing-safe fit check, ideas with evidence review, household ballots on the governance thresholds, upcoming and past events with meeting notes, catalogs of community structures and features seeded from the research), stack, hosting, milestones and open decisions: https://claude.ai/artifact/Y2wK5PzciUALpNv46X5AFv
  - Built and running on pop-os, public through Tailscale Funnel: https://pop-os.tail89465a.ts.net:10000. Source in /data/Dev/friendstead-app (separate repo; no code lives here), deploy with `bash scripts/deploy.sh` from there.

## Tools
- Member finance calculator (2026-10-25): per-household cash timeline, construction-loan and income requirements, founder scenario, candidate pass/fail check and a headcount sweep. Source `tools/member-finance-calculator.html`, published at https://claude.ai/artifact/9JMzkMfRNipFKTboQC2Tbc

## Walkthrough
- Barndominium v5 walkthrough (Three.js, from the IFC): https://claude.ai/artifact/HsUtQdhz5YpM2NvhuqUwLT

## Layout
- `vault/` versioned copy of the Friendstead notes from the Obsidian vault (`Friendstead/`, `Library/`, `Attachments/`). Edit in the vault, then run `vault/sync-from-vault.sh`. Start at `vault/Friendstead/Friendstead.md`.
- `sources/` source material, one file each, dated; includes the archived Texas statute and court-opinion excerpts (2026-10-23)
- `notes/` working notes and decision logs (`notes/2026-10-22-decisions.md`, `notes/2026-10-23-decisions.md`)
- `drafts/` exported copies of documents
- `tools/` single-file HTML calculators; the published copies are linked under Tools above

## Designs

Blender and IFC models live in `designs/` (Bonsai in Blender 4.5 LTS). Start with `designs/README.md`; the first building is the shared barndominium in `designs/barndominium/`.
