#!/usr/bin/env python3
"""20-year property-tax comparison per household. Modelled figures [M]; rates as cited in the vault Sources (S81-S83).
Timeline: land closes January of year 1; lots deeded after plat late in year 1; house 40% complete on 1 Jan year 2;
move-in at month 18 (July year 2); first full homestead year 3; 10% cap effective year 4 (Tax Code 23.23(c), (c-1))."""
GROWTH = 0.04          # market appreciation, all scenarios
YEARS = 20
# 2025 rates per $100 (see sources): east side = Bastrop County (derived 0.4287) + Bastrop ISD 1.0679 + ESD 0.10
EAST = {"isd": 1.0679, "other": 0.4287 + 0.10}
# Austin 2025: AISD 0.9252, City 0.524017, Travis 0.375845, Central Health 0.118023, ACC 0.1034
AUS = {"isd": 0.9252, "city": 0.524017, "county": 0.375845, "ch": 0.118023, "acc": 0.1034}
SCHOOL_EX = 140_000    # Prop 13, Nov 2025
LOCAL_PCT = 0.20       # Austin, Travis County, Central Health local-option homestead exemption (11.13(n))

def east_tax(value, homestead=True, frac=1.0):
    isd = max(value - (SCHOOL_EX if homestead else 0), 0) * EAST["isd"] / 100
    other = value * EAST["other"] / 100
    return (isd + other) * frac

def austin_tax(value):
    isd = max(value - SCHOOL_EX, 0) * AUS["isd"] / 100
    loc = value * (1 - LOCAL_PCT) * (AUS["city"] + AUS["county"] + AUS["ch"]) / 100
    acc = max(value - 5_000, 0) * AUS["acc"] / 100
    return isd + loc + acc

def grow(v, yrs): return v * (1 + GROWTH) ** yrs

def scenario_austin_median():
    """Existing metro-median home, $421,000, bought January year 1, homestead from year 1."""
    return [austin_tax(grow(421_000, y)) for y in range(YEARS)]

def scenario_solo_rural(house_mv=450_000, lot_mv=200_000):
    """Solo 5-acre lot at $40,000/acre, contractor-built; same 18-month timeline, no ag on the lot."""
    out = []
    for y in range(YEARS):
        if y == 0: out.append(east_tax(lot_mv, homestead=False))
        elif y == 1:  # 40% complete on Jan 1, move-in July: partial-year school exemption on the Jan 1 value
            v = lot_mv + 0.4 * house_mv
            out.append(east_tax(v, homestead=False) - 0.5 * min(SCHOOL_EX, v) * EAST["isd"] / 100)
        else: out.append(east_tax(grow(lot_mv + house_mv, y - 2)))
    return out

def scenario_coop(house_mv=450_000, lot_mv=100_000, households=6, ag_value_per_acre=150, rollback=5_000,
                  barndo_mv=275_000, poa_nominal=True):
    """Co-op household, 3-acre lot. Year 1: 30-acre tract under 1-d-1 ag. Year 2: lot deeded, 40% complete,
    rollback on the lot, LLC-owned barndominium half built. Year 3 on: full value, homestead; POA common tract
    and barndominium at nominal value under Tax Code 23.18 if the POA qualifies, else at market."""
    out = []
    for y in range(YEARS):
        if y == 0:
            out.append(east_tax(30 * ag_value_per_acre, homestead=False) / households)
        elif y == 1:
            v = lot_mv + 0.4 * house_mv
            own = east_tax(v, homestead=False) - 0.5 * min(SCHOOL_EX, v) * EAST["isd"] / 100
            barndo = east_tax(0.5 * barndo_mv, homestead=False) / households
            out.append(own + barndo + rollback)
        else:
            own = east_tax(grow(lot_mv + house_mv, y - 2))
            common = (east_tax(10 * ag_value_per_acre + 1_000, homestead=False) if poa_nominal
                      else east_tax(grow(barndo_mv + 10 * 28_000, y - 2), homestead=False)) / households
            out.append(own + common)
    return out

if __name__ == "__main__":
    S = {
        "Austin metro median existing home, $421,000": scenario_austin_median(),
        "Solo rural lot + contractor-built, $650,000 market": scenario_solo_rural(),
        "Co-op household, $550,000 market, POA at nominal value": scenario_coop(),
        "Co-op household, POA common property taxed at market": scenario_coop(poa_nominal=False),
        "Co-op household, home appraised at $450,000 market": scenario_coop(house_mv=350_000),
    }
    print(f"{'Scenario':62} {'Yr1':>8} {'Yr2':>8} {'Yr3':>8} {'Yr10':>8} {'Yr20':>8} {'20-yr total':>12}")
    for k, v in S.items():
        print(f"{k:62} {v[0]:8,.0f} {v[1]:8,.0f} {v[2]:8,.0f} {v[9]:8,.0f} {v[19]:8,.0f} {sum(v):12,.0f}")
