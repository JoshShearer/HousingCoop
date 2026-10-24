---
tags: [friendstead]
type: analysis
updated: 2026-10-24
---

# Tax and Code Savings

The durable savings come from the homestead cap, the exemptions and ag valuation on the common tract; the unfinished-house move saves one year of tax on the house's incomplete value and nothing after. Part of [[Friendstead]]; ag detail in [[Agricultural Valuation]].

| Lever | What it does | Worth per household | How to use it | Source |
|---|---|---|---|---|
| Percent complete on January 1 | An unfinished house goes on the roll at market value times its percent complete on January 1; land is valued separately | One year's tax on the unbuilt share: a house 40% complete at a $300,000 finished value saves about $3,600 at a 2% rate, once **[M]** | Schedule slab and framing after January 1 or hold exterior completion until January; do not leave siding off a lived-in house, the appraiser values market value and the insurer will not cover it | **[S38]** (search result) |
| Homestead cap | After the first full year of homestead, appraised value rises at most 10% a year plus new improvements | The main long-run lever in a rising market | File homestead the year of the deed; the cap starts the next January 1. A low first-year value sets the base, but the completed house is added at market value as a new improvement, so the reset is partial | **[S24]** |
| School homestead exemption $140,000 | Proposition 13 (Nov 2025) raised it from $100,000; over-65 or disabled add $60,000 under Proposition 11 | About $1,400 a year on the $40,000 increase at a 1.0% school rate; about $4,900 total **[M]** | Automatic with the homestead | **[S35]** |
| No county building permit | Counties have no building-code authority unless they opt into Loc. Gov't Code ch. 233 subch. F; an opted-in county requires three inspections (foundation, framing and mechanical, completion) by a licensed engineer, architect, TREC inspector or ICC residential inspector that the builder hires | Weeks of review time and city-level permit fees | Confirm the county's status; Travis still requires a development permit for any earth disturbance, plus floodplain, septic and driveway permits | **[S32]** |
| Energy code | State code for single-family homes is the IRC energy chapter as of May 1, 2015; SECO may substitute a newer edition no more than every six years | Nothing to save; sets the floor in [[Energy Costs by Envelope]] | Build to 2015 IRC chapter 11 as a minimum | **[S33]** |
| Owner-occupant trade exemptions | No electrician license for work on a dwelling you own and reside in; a homeowner may plumb their own homestead; HVAC on a home you solely own | Licensed-trade labor on your own house, roughly $20,000 to $30,000 per house if the owner is competent **[M]** | Local rules can override; insurer or lender may still require licensed work; never covers helpers | **[S31]**; 16 TAC 75.30 and Occ. Code 1301.051 from search results |
| Sales tax on materials | Materials taxed at 8.25% whoever buys them; labor for new residential construction is never taxed; a homeowner acting as their own general contractor is a homebuilder and can issue exemption certificates for otherwise-taxable real property services (surveying, landscaping, cleanup) | Tax on services: a few hundred to a few thousand dollars | Issue the homebuilder certification to surveyors and site-service vendors | **[S34]** (dated 2001, verify) |
| Solar | Federal 25D credit ended for systems completed after 31 Dec 2025; leased or PPA systems can still use 48E through 2027; Texas exempts the added value of a solar system from property tax (Tax Code 11.27), filed by April 30 the year after installation | Property-tax exemption about $500 a year on a $25,000 system at 2%; no federal credit for purchased systems in 2026 | Decide early whether a co-op-owned array on the common tract leased to members fits the 48E path; ask a tax professional | **[S36]** |
| Rainwater | Equipment, supplies and installation labor exempt from sales tax with Form 01-339 (Tax Code 151.355, 34 TAC 3.318); 2025 HJR 88 proposed a local property-tax exemption, status unconfirmed | 8.25% of a $15,000 system, about $1,200; a rainwater supply also unlocks smaller lots in Travis and Hays | Hand the exemption certificate to tank and gutter suppliers | **[S37]** |
| Member labor kept out of barter income | Hours ledger with no dollar price and no cash between households; a shortfall raises that household's cash share of shared costs. Work on your own house is never income; the barter-exchange regulation excludes informal noncommercial exchanges of similar services | Avoids income tax on roughly $45,000 to $90,000 of labor value per household **[M]** | Strike credit rates and true-ups from the labor agreement; CPA sign-off | **[S73]** **[S75]**, [[Entity and Ownership Design#Labor without a tax bill]] |
| Common tract appraised at a nominal value | The POA's road, well, barndominium and common land go on the roll at a nominal value instead of market value, because the lots already carry the value of the right to use them | On a 10-acre common tract with a $275,000 barndominium, roughly the tax on $400,000 to $550,000 of value **[M]**, which would otherwise be assessed to the POA and paid through dues; the appraiser may add some of that value back onto the lots | Qualify the POA under Tax Code § 23.18: nonprofit, 60% of income from dues, 90% of spending on the common property, every lot holding an equal nonrevocable easement that runs with the lot, and federal § 528 homeowners-association status. Record the easements in the declaration | [Tax Code § 23.18](https://statutes.capitol.texas.gov/Docs/TX/htm/TX.23.htm#23.18) **[S79]** |
| Ag and wildlife valuation | Land, not the house, taxed on productivity value | On a 10-acre common tract east of Austin, roughly $5,000 a year for the group **[M]** | Buy a tract already under ag valuation and keep the use going | [[Agricultural Valuation]] |

Two moves that are not worth it: deliberately leaving a house unfinished to hold value down (the appraiser uses market value, the insurer and lender will object, and the homestead cap adds the completed value as a new improvement anyway), and skipping engineering because no permit requires it (a lender's appraiser, a buyer's inspector and the chapter 233 inspector all will) **[J]**.

## Property tax over 20 years

Per household, east side, 4% a year market appreciation in every case, 2025 rates held flat, 18-month build with move-in in July of year 2 **[M]**. Model: `notes/tax-20yr.py` in the repo. Numbers rounded.

**Rates, 2025, per $100 of taxable value**

| Where | Posted rate | What a homestead actually pays after exemptions | Source |
|---|---|---|---|
| Austin (AISD, city, Travis County, Central Health, ACC) | $2.05 | about 1.53% of market on a $421,000 home | **[S82]** |
| East side (Bastrop ISD, Bastrop County, ESD) | $1.60 | about 1.32% of market on a $550,000 home | **[S81]** |

The effective rate is below the posted rate because the first $140,000 is exempt from school tax (§ 11.13(b)) **[S35]** and Austin's city, county and Central Health each take 20% off before applying their rates (§ 11.13(n)). The Bastrop County rate is derived from reported figures and needs checking against the county's adopted rate order.

**Tax burden per household**

| Scenario | Market value | 20-year total | Average per year | Average per month | Effective rate once settled (year 3) |
|---|---|---|---|---|---|
| Buy the Austin metro median existing home | $421,000 | $205,000 | $10,250 | $854 | 1.68% |
| Build alone on a 5-acre rural lot, contractor-built | $650,000 | $248,000 | $12,390 | $1,032 | 1.37% |
| **Co-op household, 3-acre lot plus home, POA common property nominal under § 23.18** | **$550,000** | **$208,000** | **$10,375** | **$865** | **1.33%** |
| Co-op household, POA common property taxed at market instead | $550,000 | $245,000 | $12,260 | $1,022 | 1.59% |
| Co-op household, home appraised at $450,000 on rural comparables | $450,000 | $166,000 | $8,300 | $691 | 1.27% |

The effective rate rises slowly after year 3 because the $140,000 exemption does not grow with the house (about 1.40% by year 20 for the co-op base case).

**Delta, 20-year total**

| Scenario | Against buying in Austin | Against building alone |
|---|---|---|
| Co-op, POA nominal under § 23.18 | +$2,500 (a wash) | −$40,200 |
| Co-op, POA common property at market | +$40,200 | −$2,500 (a wash) |
| Co-op, home appraised at $450,000 | −$39,100 | −$81,800 |

**Year by year**

| Scenario | Year 1 | Year 2 | Year 3 | Year 10 | Year 20 |
|---|---|---|---|---|---|
| Austin metro median, bought January year 1 | $6,500 | $6,800 | $7,100 | $9,700 | $15,000 |
| Solo rural lot plus contractor-built home | $3,200 | $5,300 | $8,900 | $12,200 | $18,700 |
| **Co-op, POA nominal** | **$12** | **$9,100** | **$7,300** | **$10,100** | **$15,600** |
| Co-op, POA at market | $12 | $9,100 | $8,800 | $12,000 | $18,500 |
| Co-op, home appraised at $450,000 | $12 | $8,500 | $5,700 | $8,000 | $12,500 |

How to read it:

- **What the deltas say.** The co-op pays a lower rate than Austin on a more valuable house, so the dollar bill comes out the same. Against a solo rural build it saves about $40,000, almost all of it from the § 23.18 treatment of the common tract; if the POA does not qualify, the co-op saves nothing over building alone. The only scenario that beats Austin in dollars is the one where the district values a member-built home at $450,000 rather than $550,000, which is a protest to win year by year, not a design feature.
- **What each household's bill is made of.** Its own house and lot at market with the homestead exemption, plus one sixth of the common tract. The common land stays under 1-d-1 agricultural valuation the whole time; a house does not end ag valuation, it only takes the homesite acres out of it ([[Agricultural Valuation]]). What § 23.18 adds is the shared barndominium, which ag valuation never covers because it is a building **[S79]**.
- **Year 1, before anything is built.** The LLC owns 30 acres under ag valuation, so the whole tract carries a productivity value of a few thousand dollars and the tax is about $12 per household **[S84]**. A tract bought without ag valuation would cost about $2,200 per household that year.
- **Year 2, the build year, is the most expensive year.** The lot is deeded after plat and the house is about 40% complete on 1 January, so it is taxed at the lot plus 40% of the home's value **[S38]**. Moving in during the year earns the school exemption for the rest of that year (§ 11.42(f)) **[S83]**. The year also carries the one-time rollback on the lot (about $5,000: the difference between ag and market tax for the three preceding years, no interest since 2021, and only on the acres whose use changed, § 23.55(a), (d) **[S85]**) and a share of the half-built barndominium.
- **Year 3 on.** Full market value with the $140,000 school exemption. The 10% homestead cap starts the year after the first qualifying year, so from year 4 (§ 23.23(c), (c-1)); at 4% appreciation it never binds, but it is the insurance against a jump.
- **Why the co-op is level with Austin rather than far below it.** East-side rates total about $1.60 per $100 against Austin's $2.05, but Austin's 20% local-option exemptions and Austin ISD's lower rate close the gap, so a $550,000 home east of Austin pays about what a $421,000 home in Austin pays.
- **Design point.** Smaller deeded lots (about one acre) with the rest held in the common tract as one ag operation keep more acres under ag, shrink the rollback and make the five-of-seven-years history easier to hold. The new owner must file a new application before 1 May of the first year after the ownership change or lose the valuation for that year (§ 23.54(d), (e)) **[S85]**, so that goes on the closing checklist.
