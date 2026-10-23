# HousingCoop

Research and legal-planning repo for a friend-group self-build community ("Friendstead") on 20-40 acres near Austin, Texas. No code lives here.

## How work is delivered
- Written deliverables (analyses, term sheets, contingency matrices, market models) are Claude Docs, linked from `README.md`. Do not write long reports as local Markdown unless the user asks for a file.
- `sources/` holds pasted or downloaded source material, one file each, dated in the filename.
- `notes/` holds short working notes and decision logs.
- `drafts/` holds exported copies of docs when the user wants a file in the repo.
- `designs/` holds the Blender and IFC building models made with Bonsai, one folder per building with a `BRIEF.md`, a parametric generator script, versioned `.ifc` and `.blend` files, and `exports/` for renders. The IFC is the source of truth. See `designs/README.md`.

## Conventions
- Cite statutes by code and section (for example Tex. Loc. Gov't Code § 232.0015(f)) and link the official text at statutes.capitol.texas.gov.
- Market figures carry an as-of date and a source link. Listing prices are asking prices, not closed sales, and are labeled as such.
- Nothing here is legal advice; the goal is a package a Texas real-estate attorney can work from.
