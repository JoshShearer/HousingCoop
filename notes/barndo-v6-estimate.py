"""Itemised cash estimate for the v6 barndominium: 56 x 40 ft, 20 ft eave, post-frame, two-storey house block, rough interior.

    python3 -I notes/barndo-v6-estimate.py            # prints the summary and writes designs/barndominium/ESTIMATE-v6.md

Model figures [M], not quotes: quantities from the v6 IFC parameters, unit prices at the Texas 2026 level. Kinds:
M = material the members buy (8.25% sales tax added per section), S = subbed or installed price, R = rental, fee or permit.
Anchors, cited in the vault Sources note: S86 (the Cedar, Iowa 2024, itemised self-build), S118 (BC lumber prices,
9 Oct 2026), S119 (HomeWyse insulated garage door, May 2026), S120 (HomeAdvisor and BuilderMuse Texas slab guides).
"""
import math, pathlib

TAX = 0.0825
L, W, H, PITCH, OV = 56, 40, 20, 4 / 12, 1
SLAB = L * W                                                 # 2,240 sq ft
PERIM = 2 * (L + W)                                          # 192 ft
WALL = PERIM * H + W * (PITCH * W / 2)                       # 4,107 sq ft incl. both gables
OPENINGS = 2 * 144 + 3 * 20 + 12 * 12                        # two 12x12 doors, three walk doors, twelve 3x4 windows: 492
ROOF = 2 * (L + 2 * OV) * ((W / 2 + OV) * math.sqrt(1 + PITCH**2))   # 2,568 sq ft
FLOOR2 = 32 * 40                                             # 1,280 sq ft gross
PART_LF = 177                                                # temporary partitions, both floors (from the plan)

# (section, [(item, qty, unit, unit_cost, kind, note)])
SECTIONS = [
 ("Site and preparation", [
  ("Scrape, grade and compact the pad, dozer or skid steer with operator", 2, "day", 1_200, "S", "about 4,000 sq ft, 6 in select fill under the slab"),
  ("Select fill, delivered", 55, "cu yd", 35, "S", "6 in over the slab footprint plus edges"),
  ("Crushed limestone base, 4 in under the slab", 28, "cu yd", 55, "S", ""),
  ("Drainage swale and a 20 ft culvert at the drive", 1, "lot", 1_200, "S", "clay soils east of Austin; keep water off the post line"),
  ("Gravel apron at the shop doors, 20 tons", 20, "ton", 38, "S", ""),
  ("Temporary power pole and well hookup for construction", 1, "lot", 1_000, "S", ""),
  ("Dumpster, three pulls", 3, "pull", 500, "R", ""),
  ("Portable toilet, six months", 6, "month", 150, "R", ""),
 ]),
 ("Slab on grade, 6 in, 4,000 psi", [
  ("Ready-mix 4,000 psi, delivered", 58, "cu yd", 165, "M", "41.5 yd slab, 10.7 yd thickened edges, 1 yd post footings, 8% waste"),
  ("Pump truck, half day", 1, "lot", 1_200, "S", ""),
  ("Rebar #4 at 18 in both ways, chairs and ties", 1.2, "ton", 1_450, "M", "about 3,600 lf"),
  ("Vapor barrier, 15 mil", 2_500, "sq ft", 0.25, "M", ""),
  ("Forms, placing and finishing crew", SLAB, "sq ft", 4.50, "S", "subbed; the Cedar's 55 yd slab was $32,700 all-in in 2024 [S86]"),
  ("Sawcut control joints", 1, "lot", 500, "S", ""),
  ("Termite pretreatment", 1, "lot", 500, "S", ""),
  ("Compaction test and engineer's slab inspection", 1, "lot", 800, "S", ""),
 ]),
 ("Post-frame structure package, 56 x 40 x 20", [
  ("Laminated 3-ply 2x8 columns, 24 ft, treated or on wet-set brackets", 26, "each", 220, "M", "8 ft bays on the long walls, 8 ft on the gables"),
  ("Wet-set post brackets and hardware", 26, "each", 60, "M", "keeps the posts out of the ground"),
  ("40 ft clear-span trusses, 4:12, 4 ft on centre", 15, "each", 450, "M", "engineered for the second-floor-free shop and 115 mph wind"),
  ("Gable-end trusses with studs, two", 2, "each", 600, "M", ""),
  ("Truss carriers, double 2x12, long walls", 224, "lf", 2.20, "M", "2 x 56 ft x 2 ply"),
  ("Roof purlins 2x6 on edge, 2 ft on centre", 1_232, "lf", 0.95, "M", "11 rows per slope"),
  ("Wall girts 2x6, 2 ft on centre", 1_920, "lf", 0.95, "M", "10 rows round 192 ft"),
  ("Treated 2x8 splash plank", 192, "lf", 2.60, "M", ""),
  ("Wind bracing, strapping, hurricane ties, purlin blocking", 1, "lot", 1_600, "M", ""),
  ("Roof steel, 26 ga PBR, PVDF bright white", 2_700, "sq ft", 2.40, "M", f"{ROOF:,.0f} sq ft plus 5%; steel mill products up 28% on 2025"),
  ("Wall steel, 26 ga PBR, PVDF bone white", 3_800, "sq ft", 2.20, "M", f"{WALL - OPENINGS:,.0f} sq ft net of openings plus 5%"),
  ("Trim: ridge cap, eave, rake, corner, base, J-trim", 600, "lf", 4.00, "M", ""),
  ("Screws, closures, butyl, sealant", 1, "lot", 1_200, "M", ""),
  ("House wrap on the walls", 4_200, "sq ft", 0.15, "M", "no roof underlayment: the roof deck is foamed"),
  ("Vented soffit and fascia, both eaves", 112, "lf", 11.00, "M", "18 in; the Cedar paid $4.69 per ft for soffit alone [S86]"),
  ("Gutters and downspouts, both eaves", 112, "lf", 13.00, "S", "keeps roof water off the post line"),
  ("Framed openings: LVL headers and jambs for two 12 ft doors, walk doors, windows", 1, "lot", 1_300, "M", ""),
  ("Bolts, nails, hangers, misc hardware", 1, "lot", 800, "M", ""),
  ("Freight", 1, "lot", 2_000, "S", ""),
 ]),
 ("Shop doors, walk doors and windows", [
  ("12 x 12 ft commercial sectional door, 2 in polyurethane, R-16, torsion springs", 2, "each", 3_600, "M", "e.g. Clopay 3720 or Wayne Dalton 5255 class"),
  ("Chain hoist", 2, "each", 350, "M", "no openers in the rough build"),
  ("Door installation by a commercial door company", 2, "each", 900, "S", "residential doors install at $1,300 to $2,050 all-in [S119]"),
  ("Steel prehung exterior doors, 3/0 x 6/8, insulated, with locksets", 3, "each", 530, "M", ""),
  ("Vinyl single-hung windows 3 x 4 ft", 7, "each", 260, "M", ""),
  ("Vinyl egress windows 3 x 5 ft for the five upstairs bunk rooms", 5, "each", 350, "M", "IRC R310 egress for sleeping rooms"),
  ("Flashing tape, sealant, shims, screws", 1, "lot", 400, "M", "members install the doors and windows"),
 ]),
 ("Closed-cell spray foam and thermal barrier", [
  ("Walls, 2 in closed-cell, about R-14", round((WALL - OPENINGS) * 2), "board ft", 1.90, "S", "the Cedar paid $1.75 per board foot in 2024 [S86]"),
  ("Roof deck, 3 in closed-cell, about R-21, unvented", round(ROOF * 3), "board ft", 1.90, "S", ""),
  ("Intumescent thermal-barrier coating over exposed foam in occupied space", 6_200, "sq ft", 1.05, "S", "IRC R316.4: foam in a lived-in building needs a 15-minute thermal barrier; coating is cheaper than drywalling the shell"),
 ]),
 ("Second floor and stair, member-built", [
  ("I-joists 11-7/8 in, 16 in on centre, 20 ft", 50, "each", 76, "M", "25 each side of the centre beam; SPF 2x4 at $454 per mbf in Oct 2026 [S118]"),
  ("LVL rim and ledger 1-3/4 x 11-7/8 on the posts", 144, "lf", 9.00, "M", ""),
  ("Centre beam, 2-ply 1-3/4 x 14 LVL, flush", 64, "lf", 13.00, "M", ""),
  ("6x6 posts under the beam with bases and caps", 3, "each", 120, "M", ""),
  ("Joist hangers, ledger bolts, squash blocks", 1, "lot", 900, "M", ""),
  ("Subfloor 23/32 T&G OSB", 42, "sheet", 42, "M", "1,280 sq ft plus 5%; OSB CDN$390 per msf at the mill [S118]"),
  ("Subfloor glue and screws", 1, "lot", 250, "M", ""),
  ("U-stair: 2x12 stringers, OSB treads, landing frame", 1, "lot", 650, "M", ""),
  ("Temporary 2x4 guards and handrails, both floors", 1, "lot", 400, "M", ""),
 ]),
 ("Temporary partitions, both floors", [
  ("2x4 studs, 10 ft, 16 in on centre", 150, "each", 4.20, "M", f"{PART_LF} lf of wall"),
  ("2x4 plates and door headers", 560, "lf", 0.70, "M", ""),
  ("7/16 OSB both sides of the bunk rooms, one side elsewhere", 100, "sheet", 15.00, "M", ""),
  ("Hollow-core prehung interior doors with passage sets", 8, "each", 150, "M", ""),
  ("5/8 in type X drywall on the shop side of the partition and a 20-minute door", 1, "lot", 1_050, "M", "IRC R302.6 separation between the shop and the dwelling"),
  ("Nails, screws, shims", 1, "lot", 200, "M", ""),
 ]),
 ("Equipment, tools and consumables", [
  ("Telehandler rental, three months, delivered", 3, "month", 2_800, "R", "the Cedar's builder erected the shell solo with one [S86]"),
  ("Telehandler delivery and pickup", 1, "lot", 600, "R", ""),
  ("Screw guns, bits, blades, ladders, fall protection, consumables", 1, "lot", 1_500, "M", ""),
 ]),
 ("Engineering, permits and inspections", [
  ("Texas PE stamp: post-frame with the second-floor load and 115 mph wind", 1, "lot", 2_500, "R", ""),
  ("Foundation engineering", 1, "lot", 1_000, "R", ""),
  ("County development permit, address, driveway permit", 1, "lot", 500, "R", "rural county; the Cedar's permits were about $1,500 [S86]"),
  ("Electrical and plumbing permits", 1, "lot", 400, "R", ""),
  ("Third-party inspections", 1, "lot", 500, "R", ""),
 ]),
]
SERVICES = [
 ("Electrical", [
  ("Utility meter and service connection fees", 1, "lot", 1_500, "R", "line extension is in the shared electric backbone"),
  ("200 A meter base and main panel", 1, "lot", 900, "M", ""),
  ("100 A shop subpanel and 60 ft SER feeder", 1, "lot", 750, "M", ""),
  ("Branch wire: 12/2, 14/2, 10/2, 6/3 for about 40 circuits", 1, "lot", 2_000, "M", ""),
  ("AFCI and GFCI breakers", 30, "each", 45, "M", ""),
  ("Boxes, devices, plates", 80, "each", 4, "M", ""),
  ("LED shop and keyless fixtures, exterior lights", 64, "each", 20, "M", ""),
  ("Mini-split circuits and disconnects", 3, "each", 250, "M", ""),
  ("Interconnected smoke and CO alarms", 8, "each", 40, "M", ""),
  ("Grounding electrode and bonding", 1, "lot", 200, "M", ""),
  ("Licensed electrician: service, rough-in oversight, trim and inspections", 60, "hour", 110, "S", "members pull wire under the license; the Cedar paid $14,000 all-in [S86]"),
 ]),
 ("Plumbing", [
  ("Under-slab DWV: 3 and 4 in PVC and fittings, one north-south trench", 1, "lot", 1_100, "M", ""),
  ("Sewer line to the septic tank, 80 ft 4 in", 1, "lot", 400, "M", "septic itself is in the shared pot"),
  ("Water service from the well, 100 ft 1 in PE", 1, "lot", 300, "M", ""),
  ("PEX manifold, 500 ft PEX, fittings, hose bibs", 1, "lot", 920, "M", ""),
  ("Fiberglass tub-shower units", 2, "each", 600, "M", ""),
  ("Toilets", 2, "each", 350, "M", ""),
  ("Lavatories with faucets", 2, "each", 250, "M", ""),
  ("Kitchen sink and faucet, laundry box", 1, "lot", 480, "M", ""),
  ("Heat-pump water heater, 50 gal", 1, "each", 1_900, "M", "rebate possible under the energy incentives note"),
  ("Roof vents and flashings", 2, "each", 75, "M", ""),
  ("Licensed plumber: under-slab, top-out, trim and inspections", 50, "hour", 100, "S", "the Cedar paid $10,000 [S86]"),
 ]),
 ("Heating, cooling and ventilation", [
  ("Mini-split, 18k BTU, common room", 1, "each", 1_700, "M", ""),
  ("Mini-split, 12k BTU, bunk 1 and baths zone", 1, "each", 1_300, "M", ""),
  ("Mini-split, 24k BTU, upstairs hall", 1, "each", 2_000, "M", "bunk-room doors stay open or get transfer grilles"),
  ("Line sets, pads, whips, condensate", 3, "each", 200, "M", ""),
  ("Licensed HVAC: hang, vacuum, charge, start up", 3, "each", 700, "S", "the Cedar's five heads were $12,000 installed [S86]"),
  ("Ventilating dehumidifier, 70 pint, with ducting", 1, "each", 2_700, "M", "humidity is the hard load in zone 2A once the shell is tight"),
  ("Dehumidifier install", 1, "lot", 500, "S", ""),
  ("Bath exhaust fans and a range hood", 1, "lot", 400, "M", ""),
 ]),
]

def section_total(rows):
    mat = sum(q * u for _, q, _, u, k, _ in rows if k == "M")
    other = sum(q * u for _, q, _, u, k, _ in rows if k != "M")
    return mat, mat * TAX, other, mat * (1 + TAX) + other

def md_section(name, rows):
    out = [f"### {name}\n", "| Item | Qty | Unit | Unit cost | Total | Kind | Note |", "|---|---|---|---|---|---|---|"]
    for item, q, unit, u, k, note in rows:
        qs = f"{q:,.0f}" if float(q).is_integer() else f"{q:,.2f}"
        out.append(f"| {item} | {qs} | {unit} | ${u:,.2f} | ${q * u:,.0f} | {k} | {note} |")
    mat, tax, other, tot = section_total(rows)
    if mat: out.append(f"| Sales tax on materials, 8.25% | | | | ${tax:,.0f} | | on ${mat:,.0f} of materials |")
    out.append(f"| **Section total** | | | | **${tot:,.0f}** | | |\n")
    return "\n".join(out), tot

if __name__ == "__main__":
    lines = [f"# Barndominium v6, itemised estimate\n",
             "Model figures **[M]**, Texas 2026 price level, not quotes. Quantities come from the v6 parameters (56 x 40 ft slab, 20 ft eave, "
             f"{WALL:,.0f} sq ft of wall, {ROOF:,.0f} sq ft of roof, {FLOOR2:,} sq ft second floor, {PART_LF} lf of temporary partition). "
             "M = material the members buy, taxed at 8.25% per section; S = subbed or installed price; R = rental, fee or permit. "
             "Member labor is hours, never priced. Regenerated by `python3 -I notes/barndo-v6-estimate.py`.\n",
             "## Dried-in shell, foam, second floor and temporary rooms\n"]
    shell_tot, svc_tot = 0, 0
    summary = []
    for name, rows in SECTIONS:
        s, t = md_section(name, rows); lines.append(s); shell_tot += t; summary.append((name, t))
    lines.append("## Services to live in it\n")
    for name, rows in SERVICES:
        s, t = md_section(name, rows); lines.append(s); svc_tot += t; summary.append((name, t))
    dry = sum(t for n, t in summary if n in ("Site and preparation", "Slab on grade, 6 in, 4,000 psi", "Post-frame structure package, 56 x 40 x 20",
                                              "Shop doors, walk doors and windows", "Equipment, tools and consumables", "Engineering, permits and inspections"))
    allin = shell_tot + svc_tot
    lines += ["## Summary\n", "| Section | Total |", "|---|---|"] + [f"| {n} | ${t:,.0f} |" for n, t in summary] + [
        f"| **Shell, foam, floor and rooms** | **${shell_tot:,.0f}** |", f"| **Services** | **${svc_tot:,.0f}** |", f"| **All-in to occupy** | **${allin:,.0f}** |",
        f"| All-in with 10% contingency | **${round(allin * 1.1, -3):,.0f}** |", "",
        f"Dry shell only (site, slab, structure, doors and windows, equipment, permits): ${dry:,.0f}, ${round(dry * 1.1, -3):,.0f} with contingency. "
        f"Shell plus foam, floor and rooms: ${shell_tot:,.0f}, ${round(shell_tot * 1.1, -3):,.0f} with contingency. "
        f"All-in with contingency is ${allin * 1.1 / 3520:,.0f} per sq ft of floor and ${allin * 1.1 / SLAB:,.0f} per sq ft of slab. "
        "Septic (aerobic, 8 occupants, about $25,000) is in the shared pot, not here. Excluded: builder's risk insurance (LLC policy), the site road and electric line extension (shared pot), the well (shared), appliances, any finish beyond OSB.",
        "", "**Not in the base but worth pricing:** a 10 ft south porch later ($11,000 to $14,000); door openers ($600 each); a second bath upstairs (stack above bath 2, about $6,000); "
        "red iron instead of post-frame (kit $60,000 to $75,000 plus crane and crew $9,000 to $13,000, about $20,000 to $30,000 more than this package erected by members).",
    ]
    out = pathlib.Path(__file__).resolve().parent.parent / "designs" / "barndominium" / "ESTIMATE-v6.md"
    out.write_text("\n".join(lines) + "\n")
    print("\n".join(lines[-9:])); print("wrote", out)
