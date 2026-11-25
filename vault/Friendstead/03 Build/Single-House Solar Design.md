---
tags: [friendstead]
type: analysis
updated: 2026-11-25
---

# Single-House Solar Design

Three member-installed solar designs for one 2,000 sq ft Friendstead house, built from the parts named in a 17 Nov 2026 podcast transcript **[S157]**: CW Energy 595 W bifacial panels, a Sol-Ark hybrid inverter, BigBattery NEXUS 2 batteries and, for the off-grid case, a Kubota diesel generator. At 25 Nov 2026 asking prices the designs cost about **$12,600** (critical loads), **$16,800** (net-zero with backup, recommended) and **$42,900** (off-grid) **[M]**. The recommended design is $6,000 to $13,000 below the $23,000 to $30,000 array-plus-battery allowance in [[Cost-Effective Net-Zero Design]], because the battery is $187 a kWh and members do the racking. Part of [[Friendstead]]; incentives and export rates in [[Energy Incentives]]; house loads in [[Energy Costs by Envelope]]. Prices are retail asking prices before sales tax and freight. Nothing here is engineering or legal advice.

## What the transcript says, checked

The transcript is a podcast conversation, not a technical source. Its part names and prices checked out; two of its claims do not hold for Central Texas.

| Claim in the transcript | Check | Source |
|---|---|---|
| BigBattery NEXUS 2, 16 kWh, about $3,000 | Right: [$2,990 on the maker's site](https://bigbattery.com/products/bigbattery-48v-nexus-16kwh-lifepo4-battery-off-grid-home/), 51.2 V, 314 Ah cells, 7.6 kW continuous, 12-year warranty. Other sellers ask [$3,200](https://offgridsource.com/products/bigbattery-48v-nexus-2-lifepo4-battery-314ah-16kwh-off-grid-home-back-up) to [$3,499](https://thesolarstore.com/products/big-battery-48v-15kwh-nexus-lifepo4-battery) | **[S158]** |
| BigBattery is a Texas company | Its own site gives a Commerce, Texas address; directories also list Chatsworth, California. Cells are Chinese, as the speaker says | **[S158]** |
| Sol-Ark is an American inverter maker | Partly. Firmware is written in Allen, Texas; a [Sol-Ark certification](https://sol-ark.com/wp-content/uploads/2024/06/V001-60K-3P_TUV_UL1741Ed3_Certificate_Redacted-1.pdf) names Ningbo Deye, China, as the manufacturing plant | **[S159]** |
| A pallet of 31 CW Energy 595 W bifacial panels is $7,000 and 18 kW | Right: 18.45 kW, [$5,650](https://a1solarstore.com/cw-energy-595w-solar-panel-144-cell-bifacial-cwt595-144tnb10-assembled-in-the-usa-wholesale-31-panels-per-pallet.html) to [$7,450](https://www.ecodirect.com/CW-Energy-450-Watt-Solar-Panel-Pallet-Quantity-p/cw-energy-cwt595-144tnb10.htm) a pallet ([$7,009 at Signature Solar](https://signaturesolar.com/pallet-of-cw-energy-595w-bifacial-solar-panels-31-panels/)), $0.31 to $0.40 a watt | **[S160]** |
| The panels are 90 in tall | Right: 2,278 x 1,134 mm (89.7 x 44.6 in), per the [maker's datasheet](https://cw-enerji.com/images/down_file/144tnb10-595-570wp-topcon-n-type-bifacial-solar-panels-1120-en.pdf) | **[S160]** |
| Mounted vertically like a fence, bifacial panels collect about 80% | Not here. At Bastrop a south-facing fence makes 62% of a tilted array and an east-west fence 77%. The speaker himself says flatter is better nearer the equator | **[S162]** |
| Install them on ordinary chain-link fence posts | No. A 90 in solid panel at the area's design wind needs about 3 in schedule-40 pipe in engineered footings (see Mounting) | **[M]** |
| A new tariff starts 4 Dec 2026 and panel prices will roughly double | The [tariff is real](https://pv-magazine-usa.com/2026/08/07/us-announces-tariffs-minimum-import-price-on-polysilicon-imports/): a $0.38 a watt minimum import price on modules plus 15%. Doubling is the speaker's forecast; a rise from about $0.35 to $0.50 to $0.70 a watt is plausible **[J]** | **[S161]** |
| One pallet covers a typical house "and then some" | Right: about 28,000 kWh a year tilted against a 9,500 kWh house | **[S162]** |
| Kubota 11 kW diesel generator | [GL11000 Lowboy II](https://www.mowersatjacks.com/product-details/kubota/gl11000), 10 kW rated, [$9,800](https://www.pdgenerators.com/product-page/kubota-diesel-generator-gl11000-lowboy-ii) to [$10,700](https://www.machinerytrader.com/listings/for-sale/kubota/gl11000/stationary-generators-power-systems/153003) before freight | **[S163]** |

## Load

The recommended house in [[Cost-Effective Net-Zero Design]] uses about 9,500 kWh a year, 26 kWh a day on average, about 33 in July and 20 in November **[M]**. Critical loads (refrigerator, freezer, lights, internet and computers, well pump, ventilation) come to about 8 kWh a day, and 14 to 15 with the heat-pump water heater and one cooled room **[M]**.

## Output by mounting

PVWatts v8 at 30.11 N, 97.32 W, 14% losses, bifacial factor 0.8, ground albedo 0.2 **[S162]**.

| Mounting | kWh per kW a year | Share of tilted | December | July |
|---|---|---|---|---|
| Ground mount, 25 degree tilt, facing south | 1,525 | 100% | 99 | 149 |
| Metal roof at 4:12, facing south (rear side dark) | 1,461 | 96% | 89 | 148 |
| Vertical fence, faces east and west | 1,170 | 77% | 64 | 127 |
| Vertical fence, faces south | 950 | 62% | 100 | 55 |

A south-facing fence makes the least in summer, when a Texas house uses the most. If a fence is used, run it north to south so the faces look east and west.

## Three designs

| | A. Critical loads | B. Net-zero with backup (recommended) | C. Off-grid whole house |
|---|---|---|---|
| [Panels](https://signaturesolar.com/pallet-of-cw-energy-595w-bifacial-solar-panels-31-panels/) | 8 (4.76 kW) | 12 (7.14 kW) | 31, one pallet (18.45 kW) |
| Strings | 1 x 8 | 2 x 6, one per tracker | 2 x 8 in parallel, 1 x 8, 1 x 7 |
| Inverter | [Sol-Ark 12K](https://ressupply.com/inverters/sol-ark-12k-2p-n-sol-ark-12k-p-12k-2p-inverter) | [Sol-Ark 15K](https://www.currentconnected.com/product/sol-ark-15k-all-in-one-hybrid-inverter) | [Sol-Ark 15K](https://www.currentconnected.com/product/sol-ark-15k-all-in-one-hybrid-inverter) |
| Battery | 1 [NEXUS 2](https://bigbattery.com/products/bigbattery-48v-nexus-16kwh-lifepo4-battery-off-grid-home/) (16 kWh) | 1 [NEXUS 2](https://bigbattery.com/products/bigbattery-48v-nexus-16kwh-lifepo4-battery-off-grid-home/) (16 kWh) | 3 [NEXUS 2](https://bigbattery.com/products/bigbattery-48v-nexus-16kwh-lifepo4-battery-off-grid-home/) (48 kWh) |
| Generator | none | none | [Kubota GL11000](https://www.mowersatjacks.com/product-details/kubota/gl11000) |
| Grid | Connected, no export | Connected, export allowed | None |
| Output, tilted ground mount | 7,300 kWh | 10,900 kWh | 28,100 kWh |
| Output, east-west fence | 5,600 kWh | 8,400 kWh | 21,600 kWh |
| Share of the 9,500 kWh house | 76% | 115% | 296% |
| In an outage | Critical loads indefinitely | Critical loads indefinitely; whole house about 15 hours without sun | Normal operation |

**A** is the transcript's own brief: keep lights, communications and refrigeration running, and leave heating and cooling to the grid. **B** offsets the whole year's use and backs up the house through the 15K's 200 A pass-through. **C** is sized for December and July, not the annual total: the pallet makes 2.3 times the December load and 2.7 times the July load, the batteries hold about a day and a half of average use, and the generator covers long overcast spells.

String limits: panel open-circuit voltage is 51.58 V, about 57 V at -15 C, so 8 panels is the longest string under the Sol-Ark's 500 V input limit **[S159]** **[S160]**. The paired strings in C carry 27.3 A at full sun against the tracker's 26 A operating limit, which clips a little output at peak; short-circuit current is 29 A against a 44 A limit. The temperature coefficient is from a sister model's datasheet and needs confirming, as do the Sol-Ark 12K's input limits.

## Price

Member-installed, with a licensed electrician for the final connections. Asking prices, 25 Nov 2026.

| Part | Basis | A | B | C |
|---|---|---|---|---|
| Panels | $226 each at the [pallet price of $7,009](https://signaturesolar.com/pallet-of-cw-energy-595w-bifacial-solar-panels-31-panels/) **[S160]** | $1,800 | $2,700 | $7,000 |
| Racking and footings | $150 a panel **[M]** from [$70 to $230](https://solarpricelist.com/blog/solar-panel-ground-mount-installation-guide-2026) **[S164]** | $1,200 | $1,800 | $4,650 |
| Inverter | 12K [$4,126](https://ressupply.com/inverters/sol-ark-12k-2p-n-sol-ark-12k-p-12k-2p-inverter); 15K [$5,750](https://www.currentconnected.com/product/sol-ark-15k-all-in-one-hybrid-inverter) (sellers ask [$4,800](https://www.renvu.com/products/sol-ark-15k-48v-all-in-one-stackable-hybrid-inverter) to [$7,100](https://www.portlandiaelectric.supply/products/sol-ark-sa-15k-2p-n)) **[S159]** | $4,125 | $5,750 | $5,750 |
| Batteries | [$2,990 each](https://bigbattery.com/products/bigbattery-48v-nexus-16kwh-lifepo4-battery-off-grid-home/) **[S158]** | $3,000 | $3,000 | $8,950 |
| Wire, conduit, disconnects, subpanel | **[M]** | $1,500 | $2,000 | $3,500 |
| Electrician, interconnection, inspection | **[M]** | $1,000 | $1,500 | $1,500 |
| Generator, tank and wiring | [$10,300](https://www.mowersatjacks.com/product-details/kubota/gl11000) **[S163]** plus $1,200 **[M]** | | | $11,500 |
| **Total** | | **$12,600** | **$16,800** | **$42,900** |

A second battery on B adds $3,000 and raises battery-only output from 7.6 kW to the inverter's 12 kW. C without the generator is about $31,400. Six houses on design B need 72 panels: three pallets are 93, enough for 15 a house with three spares.

## Mounting

- **Ground mount, tilted.** Most output per panel and no roof penetrations. No rapid-shutdown devices are needed off a building.
- **Standing-seam roof.** Seam clamps cost about $0.17 a watt **[S127]**, but panels on a building need module-level rapid shutdown (NEC 690.12), about $50 a panel **[J]**, and the bifacial rear side adds nothing.
- **Vertical fence.** 8 panels in portrait make a fence 30 ft long, 12 make 45 ft and 31 make 115 ft, all about 8 ft tall. It gives up 23% of the output to gain a fence, easy cleaning and no hail-facing glass. Wind is the design problem: at a 115 mph design wind a solid 90 in panel loads each post with about 950 lb, a bending moment near 3,600 ft-lb, against roughly 1,500 ft-lb for a standard 2 3/8 in chain-link post **[M]**. Use 3 in schedule-40 pipe or a purpose-built fence rack, with footings sized by an engineer.

## Open before buying

- [ ] **Buy panels before 4 Dec 2026 or wait.** Three pallets cost about $21,000 now and might cost $8,000 to $19,000 more in 2027 **[J]**. Against that: no land yet, 18 to 24 months of storage, and warranties that start at purchase. A group decision.
- [ ] **NEXUS 2 with a Sol-Ark.** The manual lists Sol-Ark as compatible, but sellers confirm closed-loop communication only with EG4 and APEX inverters, and the UL 9540 listing is a battery-and-inverter pairing **[S158]**. Get the pairing in writing from both makers, or change the battery or the inverter.
- [ ] **Bluebonnet interconnection** for A and B: application, inspection and the co-op's equipment list **[S92]**. Exports earn a wholesale-based rate, so B is sized to barely exceed annual use.
- [ ] **Who may do the wiring.** Tex. Occ. Code [§ 1305.003](https://statutes.capitol.texas.gov/Docs/OC/htm/OC.1305.htm#1305.003) exempts some work by an owner on their own home; confirm with the attorney how it applies to a member-built house and to members helping each other.
- [ ] **Off-grid and the electric backbone.** Design C on every house could replace part of the $45,000 to $60,000 shared electric line in [[Per-Member Cost Model]], but lenders and insurers may require grid service. Not modeled.
- [ ] **File the solar property-tax exemption** (Tex. Tax Code [§ 11.27](https://statutes.capitol.texas.gov/Docs/TX/htm/TX.11.htm#11.27), Form 50-123), which covers batteries too **[S88]**. The covenants must allow the arrays: Tex. Prop. Code [§ 202.010](https://statutes.capitol.texas.gov/Docs/PR/htm/PR.202.htm#202.010).
