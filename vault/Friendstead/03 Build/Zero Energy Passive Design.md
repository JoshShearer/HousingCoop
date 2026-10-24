---
tags: [friendstead]
type: analysis
updated: 2026-10-24
---

# Zero Energy Passive Design

A net-zero house is feasible near Austin; a certified Passive House is feasible but the wrong tool for a self-built metal barndominium in a hot-humid climate. Build the barndominium to DOE Zero Energy Ready Home (ZERH) grade, make it solar-ready, and size the array and battery after the co-op is known and the house has been metered for a season. Full analysis with the cost table and sources: [Zero Energy Passive Design Feasibility for Friendstead](https://claude.ai/artifact/6EXUtrMb4YmZxhAid7Ex2b) (Claude Doc, 24 Oct 2026). Part of [[Friendstead]]; baseline kWh in [[Energy Costs by Envelope]]; what still pays in [[Energy Incentives]]; the building in the barndominium brief at `designs/barndominium/BRIEF.md`.

## What the phrase means here

| Term | Requires | Fit for Austin |
|---|---|---|
| Passive solar | Orientation, south glass, mass, overhangs | Partly: Austin needs sun exclusion, not collection; the brief's east-west axis, white roof and 10 ft south porch are the right moves, mass and big glass are wrong |
| Passive House (Phius CORE or PHI) | 0.6 ACH50, modeled demand limits, balanced ventilation, listed windows | Achievable with a few Austin precedents **[S100]**, but humidity is the limiting load and airtightness and windows are the costly parts in a metal building |
| DOE Zero Energy Ready Home | ENERGY STAR baseline, 3 ACH50 in zone 2, ducts inside, solar-ready, HERS in the 40s | The right target: the same building-science moves at about a third of the premium, through the HERS raters already in the market |
| Net-zero energy | Annual generation equals consumption | A result, not a design; any of the above plus a big enough array |

## Climate

Austin is IECC 2A: 1% cooling design 98 °F dry bulb / 75 °F wet bulb, 99% heating design 28 °F, 3,016 cooling degree days against 1,688 heating **[S104]**. Consequences: keep the sun out (SHGC 0.20 or less, no west glass, deep overhangs); humidity is the hard load once the shell is tight, so plan a dedicated dehumidifier and about 50% RH **[S101]** **[S102]**; put the envelope money into the roof, windows and air sealing, not wall thickness (DOE's hot-humid ZERH package is only R-30 unvented roof, R-13 + R-5 continuous walls, uninsulated slab, U 0.33 / SHGC 0.2 windows, 2.5 ACH50, 18 SEER, ducts inside) **[S98]**. Resilience cuts the other way: an Austin retrofit at 0.4 ACH50 held 62 °F after a night at 9 °F without power in February 2021 and 53 °F after three days, while the identical house next door hit 36 °F; CO2 reached 3,200 ppm because the ventilation had no power, which is the case for a battery **[S101]**.

## The metal-building problem

Girts and purlins cross the insulation; the foam-only barndominium in [[Energy Costs by Envelope]] only gets back to code. Lstiburek's rules for metal buildings in hot-humid climates: a vapor retarder that keeps humid interior air off cold steel, controlled mechanical ventilation, no interior polyethylene, unvented roof with the HVAC inside **[S102]**. Post-frame builders reach 0.6 ACH50 only when the slab-to-wall joint is detailed, and that joint is where most attempts fail **[S102]**. The practical answer: an inboard 2x6 infill wall with R-5 continuous foam between it and the girts, which members frame themselves, and foam only the house half and its roof deck, not the unconditioned shop bay (about $4,000 of foam saved **[M]**). The shop partition and hall door become exterior walls for energy purposes.

## Cost and payback

Figures are model estimates **[M]** on the $256,000 v5 estimate; a co-op all-in retail rate of 14 to 15 cents is assumed.

| Step | Added cost | Annual kWh | Saving a year | Simple payback |
|---|---|---|---|---|
| Code-minimum barndominium, closed-cell foam | 0 | 13,000 | baseline, about $1,900 | |
| ZERH-grade: infill wall + R-5 continuous, roof to R-30+, SHGC 0.20 windows, slab-edge sealing and blower door, 2-ton inverter heat pump instead of 3.5 tons, ventilating dehumidifier, heat-pump water heater, HERS rating | $14,000 to $18,000 | 9,000 to 9,800 | $500 to $600 | 8 to 10 years; the downsized heat pump recovers about $3,000 |
| Rooftop solar 9 to 10 kW at $2.17 a watt (Austin, Oct 2026) + $500 PEC interconnection | $20,000 to $22,000 | net zero on paper | $850 to $1,100 | 18 to 24 years: only the 35 to 40% self-consumed earns retail, exports earn 6.7 to 7.2 cents **[S96]** **[S97]** **[S103]** |
| Battery, one 13.5 kWh | $12,000 to $16,000 | | $150 to $250 | Outage cover, not an energy investment **[S103]** |
| Phius CORE on top: listed windows, membrane + AeroBarrier to 0.6 ACH50, ERV, WUFI model, consultant, rater | $30,000 to $45,000 | 7,500 to 8,500 | $100 to $200 | Never. Auburn's Alabama twins: Phius cost $10,600 more than its ZERH twin, used 30% less heating and cooling, worth about $7 a month **[S99]** |

## Utility rules that set the solar economics

Austin Energy's 12.89 cent Value of Solar and $4,000 rebate **[S105]** do not reach a rural tract. PEC: Sustainable Power Credit 7.19 cents per exported kWh from 1 Mar 2026 (8.27 before; about 9, 5.4, 6.1 cents in 2022 to 2024), offsets only the 6.59 cent base power charge, unused credit expires 31 December, $500 interconnection under 50 kW, and a time-of-use interconnect option paying 16.18 cents for 4 to 8 pm summer exports and 4.35 cents off-peak **[S96]**. Bluebonnet: Member Production credit 6.70 cents, updated annually, against about 15.5 cents all-in retail (3.30 service + 5.89 wholesale + 6.29 variable power-cost factor) plus $22.50 a month; its own example of 1,000 kWh used and 500 produced bills $85.01 **[S97]**. On both, size the array to self-consumption plus what a battery can shift; a west bias or a battery on PEC's TOU rate beats a south array on the flat credit.

## Fit with the v5 barndominium

Orientation, roof and porch are already right. Gaps: the shop partition as thermal boundary; a tested air barrier at the slab; an attic pocket over a wing for the ducts and dehumidifier; a 10 kW array fits on the south slope either side of the 24 ft timber entry gable, on S-5 clamps with no penetrations; Phase 2 occupancy (community kitchen, meeting room, shop next door) needs ventilation sized for the crowd case and a dedicated shop exhaust. All-electric is implicit. Member labor covers the infill wall, foam board, air sealing, drywall and racking under the existing [[Member Labor Matrix]] and the owner-occupant trade exemptions in [[Tax and Code Savings]]; the Manual J and S and the dehumidifier commissioning are the one professional fee not to skip. The barndominium is the test build; meter it for a year and set the member-home spec from what it measures.

## Next steps

1. Add the ZERH spec and the solar-ready items to the barndominium brief and the v6 generator before the frame vendor quotes.
2. Identify the serving co-op for each candidate tract and get the tariff, buyback and line-extension allowance in writing (open item in [[Further Cost Levers]]).
3. Commission a Manual J and S and ventilation design from a designer who has done tight zone 2A houses ($1,500 to $3,000 **[J]**).
4. Two blower-door tests from a HERS rater, at rough-in and completion.
5. Start the array at 6 to 8 kW with mounting laid out for 12 kW; revisit after a year of data.
6. Battery on resilience grounds only.
7. Carry the $16,000 envelope premium and the array as separate opt-in lines in [[Per-Member Cost Model]] and [[Build Systems Compared]].

Open: which county and co-op; battery or generator and transfer switch; whether any member wants Phius on their own house at their own cost.
