---
tags: [friendstead]
type: plan
updated: 2026-10-28
---

# Community App

An invite-only progressive web app on pop-os carries people through the exploration year (Nov 2026 to Oct 2027): invited, explorer, interested household, candidate household, founding household. It holds the learn pages, the interest form and a private fit check, ideas with an evidence review by a second household, upcoming and past events with meeting notes, catalogs of community structures and features, and household ballots at the thresholds in [[Governance and Exit]] (4, 5 and 6 of 6, stored as fractions because the household count moves). Every vote is advisory until the LLC exists. Full design: [Friendstead Community App: Rough Design](https://claude.ai/artifact/Y2wK5PzciUALpNv46X5AFv). Part of [[Friendstead]].

## Rules the app must keep

- **Fair housing.** The fit check asks about the deal (budget, timing, hours, area, lot tier, the draft rules, decision style), never about children, religion, origin, disability, sex, marital status or age. Results go only to the person who took it; stewards see totals only. Admission stays on the objective criteria in [[Governance and Exit#The replacement household]] **[S80]**.
- **Securities.** No public landing page, no projected returns, "not an offer" on every page, invites only from members ([[Friendstead Risks]], **[S70]**).
- **Vault boundary.** Learn pages are rewritten copies in the HousingCoop repo, published by a steward; nothing syncs from the vault automatically.

## Events and meeting notes

Every in-person discussion is an event: scheduled with an agenda linked to ideas and RSVPs, then held with attendance by household, then notes published after attendees have 48 hours to correct the draft. Notes follow one template (attendance, summary, agenda outcomes, sense of the room, action items with owner and due date, new ideas) and are versioned and searchable. No decisions in the room: a sense of the room becomes a household ballot so absent households vote, the habit Chapter 209 will require of the association. Notes record positions and outcomes, never remarks about a prospective household's personal traits **[S80]**.

## Structures and features catalogs

Two catalogs, Structures (barndominium, member homes, road, water, septic, electric and solar) and Community features (common tract, workshop and tool sharing, agricultural use, guest quarters), seeded from [[Build Systems Compared]], [[Cost-Effective Net-Zero Design]], [[Per-Member Cost Model]], [[Further Cost Levers]], [[Agricultural Valuation]] and the barndominium design in the repo. Each entry carries a status, key numbers with markers and as-of dates, research links, open questions, attached ideas and the meetings that discussed it. Members add ideas to entries or propose new ones through the idea lifecycle; status changes only by household ballot; a running total shows cost per household and member hours of everything planned, with proposals shown beside it. Entries describe uses, never who a space suits **[S80]**.

## Build

Next.js and Postgres 16 in one Docker Compose project, magic-link email through a transactional provider, Cloudflare Tunnel to a subdomain (the pattern the Twenty CRM already uses on pop-os; Tailscale Funnel's three ports are taken), nightly pg_dump copied to the laptop and off-site. Milestones: invite-ready with events and meeting notes late Nov 2026, ideas Jan 2027, decisions Mar 2027, polish May 2027.

## Running

Built and running on pop-os since 28 Oct 2026 at https://pop-os.tail89465a.ts.net:10000, public through Tailscale Funnel (free; chosen 28 Oct 2026, genetic-health-web moved to tailnet port 9443). Source at /data/Dev/friendstead-app, deployed with `bash scripts/deploy.sh` to ~/apps/friendstead-app; Docker Compose project "friendstead"; cron jobs and nightly backups to ~/backups/friendstead. Invites stay closed until the attorney-review box on the steward screen is ticked. Also built: a schematic site map of the base-case tract with catalog entries placed on it, site-visit videos on events, and sign-in without email (an invite link signs the person in once, stewards can make one-time links, passkeys for return visits). Public access is free either way and one command (`scripts/go-public.sh`): Tailscale Funnel needs one of ports 443, 8443 or 10000 freed on pop-os; Cloudflare Tunnel needs a domain at about $10 a year.

## Open

- [ ] Optional email sender for notifications: a provider on a domain, or Gmail with an app password
- [ ] Stewards besides Josh, from different households
- [ ] Invite rights: stewards only, then three per interested household
- [ ] Attorney review of the questions, learn pages and "not an offer" wording before the first invite

Done 28 Oct 2026: public access through Funnel on port 10000; daily laptop copy of backups to ~/Backups/friendstead via a systemd user timer.
