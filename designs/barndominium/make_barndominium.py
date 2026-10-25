"""Parametric starter for the Friendstead shared barndominium (v6: cheap two-storey shell).

Reworked 24 Oct 2026 to the cheapest functional brief: a dried-in post-frame or
red-iron shell, closed-cell foam, rough but usable interiors until the houses are
built, then a decision on the final fit-out (guest house plus shop, or whatever the
group wants). 56 x 40 ft footprint, 20 ft eave, 4:12 gable, no porch, no vault, no
timber entry. The west 24 ft bay is the shop, open to the roof, with two 12 x 12 ft
insulated sectional doors in the west gable. The east 32 x 40 ft block carries a
member-built wood second floor on a centre beam line, so the building has about
3,500 sq ft of floor on a 2,240 sq ft slab. Temporary 2x4 partitions make six bunk
rooms, two baths and a laundry on one plumbing trench. v5 (70 x 40 single storey
with the vaulted great room and porch) lives on as its IFC and in git history.

Builds an IFC4 model with ifcopenshell (bundled with Bonsai), then opens it in
Bonsai and saves a .blend beside it. Run through the Bonsai-enabled Blender:

    ~/.local/bin/blender -b --python designs/barndominium/make_barndominium.py -- [out-stem]

Dimensions in PARAMS are feet and are converted to metres for the IFC.
This is a massing model: openings are voids with no door or window objects yet.
"""
import sys, math, pathlib, json
import numpy as np
import ifcopenshell, ifcopenshell.api
import ifcopenshell.api.project, ifcopenshell.api.root, ifcopenshell.api.unit, ifcopenshell.api.context
import ifcopenshell.api.aggregate, ifcopenshell.api.spatial, ifcopenshell.api.geometry, ifcopenshell.api.attribute
import ifcopenshell.api.pset, ifcopenshell.api.feature

FT = 0.3048
PARAMS = dict(
    length_ft=56.0,        # east-west, the long side; 56 x 40 = 2,240 sq ft slab
    width_ft=40.0,         # north-south, gable-end width; 40 ft clear span is a stock size
    eave_ft=20.0,          # wall height to the eave: 10 ft clear below the second floor, 8.75 ft above it
    pitch=4 / 12,          # main roof pitch, metal roof
    porch_depth_ft=0.0,    # no porch in the cheap shell; a later add-on
    shop_length_ft=24.0,   # west gable bay, full 40 ft depth, open to the roof, 960 sq ft
    wall_thk_ft=0.667,     # 8 in: girts or posts, foam, metal skin
    partition_thk_ft=0.5,  # 6 in wall between shop and house block, full height
    slab_thk_ft=0.5,       # 6 in slab on grade with thickened edges (engineer to confirm)
    overhang_ft=1.0,       # roof overhang on all four sides
    rollup_w_ft=12.0, rollup_h_ft=12.0, rollup_count=2,   # two insulated sectional doors in the west gable
    rollup_gap_ft=3.0,     # wall between the two doors
    man_door_w_ft=3.0, man_door_h_ft=6.67,
    window_w_ft=3.0, window_h_ft=4.0, window_sill_ft=3.0,   # small vinyl windows, few of them
    # Second floor over the house block (east of the shop), member-built
    floor_to_floor_ft=11.25,   # top of the second-floor deck
    deck_thk_ft=1.25,          # 11-7/8 in I-joists, 3/4 in subfloor, flush 14 in LVL centre beam
    beam_post_spacing_ft=8.0,  # 6x6 posts under the centre beam
    stair_w_ft=3.5, stair_run_ft=6.67, stair_landing_ft=3.5,   # U-stair in the core band: two flights of 8 treads at 10 in, 9 risers at 7.5 in
    # Temporary partitions (2x4, OSB one side), feet from inside faces
    int_thk_ft=0.375,
    core_band_ft=10.0,     # band against the shop partition: bunk room, two baths, laundry
    bunk_a_depth_ft=12.0,  # ground-floor bunk room on the south wall
    bath_depth_ft=7.0,     # each of the two baths
    laundry_depth_ft=2.5,  # stacked washer closet; panels and water heater live in the shop. The U-stair takes the rest of the band at the north wall
    upper_room_depth_ft=12.0,   # bunk rooms along the south and north walls upstairs; open hall between
    upper_rooms_per_row=3,
)
FINISHES = dict(   # cool exterior: high solar reflectance and high emittance, Austin is climate zone 2A
    roof="Standing-seam or screw-down steel, PVDF (Kynar 500) bright white: initial SR about 0.68-0.72, emittance 0.85, SRI 82-88",
    walls="PVDF bone white or light stone wall panel: SRI about 80; any colour with SRI above 65 is acceptable",
    avoid="Bare Galvalume (SRI about 62, low emittance) and dark bronze or charcoal (SRI about 25)",
    source="McElroy Metal cool-roof tables and ORNL/FSEC Fort Myers field study, checked 2026-10-22",
)

HERE = pathlib.Path(__file__).resolve().parent
stem = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv and len(sys.argv) > sys.argv.index("--") + 1 else "barndominium-v6"
ifc_path, blend_path = HERE / f"{stem}.ifc", HERE / f"{stem}.blend"

m = lambda ft: ft * FT
L, W, H = m(PARAMS["length_ft"]), m(PARAMS["width_ft"]), m(PARAMS["eave_ft"])
SL, T, PT, S, OV = (m(PARAMS[k]) for k in ("shop_length_ft", "wall_thk_ft", "partition_thk_ft", "slab_thk_ft", "overhang_ft"))
RISE = PARAMS["pitch"] * (W / 2)
ROOF_T = 0.25
FL, DK = m(PARAMS["floor_to_floor_ft"]), m(PARAMS["deck_thk_ft"])

api = ifcopenshell.api.run
f = ifcopenshell.api.project.create_file(version="IFC4")
project = api("root.create_entity", f, ifc_class="IfcProject", name="Friendstead barndominium")
api("unit.assign_unit", f, length={"is_metric": True, "raw": "METERS"})
model_ctx = api("context.add_context", f, context_type="Model")
body = api("context.add_context", f, context_type="Model", context_identifier="Body", target_view="MODEL_VIEW", parent=model_ctx)
site = api("root.create_entity", f, ifc_class="IfcSite", name="Common tract")
building = api("root.create_entity", f, ifc_class="IfcBuilding", name="Barndominium")
ground = api("root.create_entity", f, ifc_class="IfcBuildingStorey", name="Ground floor")
upper = api("root.create_entity", f, ifc_class="IfcBuildingStorey", name="Second floor")
api("attribute.edit_attributes", f, product=upper, attributes={"Elevation": FL})
api("aggregate.assign_object", f, relating_object=project, products=[site])
api("aggregate.assign_object", f, relating_object=site, products=[building])
api("aggregate.assign_object", f, relating_object=building, products=[ground, upper])

ALONG_X = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=float)  # profile drawn in (y, z), extruded along world +X

def place(product, x=0.0, y=0.0, z=0.0, rot_z_deg=0.0, rot=None):
    mat = np.eye(4)
    if rot is None:
        c, s = math.cos(math.radians(rot_z_deg)), math.sin(math.radians(rot_z_deg))
        rot = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
    mat[:3, :3] = rot
    mat[:3, 3] = [x, y, z]
    api("geometry.edit_object_placement", f, product=product, matrix=mat, is_si=True)

def add(ifc_class, name, rep, predefined=None, storey=None, **pl):
    e = api("root.create_entity", f, ifc_class=ifc_class, name=name)
    api("geometry.assign_representation", f, product=e, representation=rep)
    place(e, **pl)
    api("spatial.assign_container", f, relating_structure=storey or ground, products=[e])
    if predefined:
        api("attribute.edit_attributes", f, product=e, attributes={"PredefinedType": predefined})
    return e

def rect(xdim, ydim):
    return f.create_entity("IfcRectangleProfileDef", ProfileType="AREA", XDim=xdim, YDim=ydim)

def polygon(pts):
    poly = f.create_entity("IfcPolyline", Points=[f.create_entity("IfcCartesianPoint", Coordinates=p) for p in pts + [pts[0]]])
    return f.create_entity("IfcArbitraryClosedProfileDef", ProfileType="AREA", OuterCurve=poly)

PLAN = {"walls": [], "openings": [], "rooms": [], "posts": []}        # ground floor, for draw_plan.py
UPPER = {"walls": [], "openings": [], "rooms": [], "posts": []}       # second floor, same format

def wall(name, length, x, y, rot, thk=T, z=0.0, height=None, plan=PLAN, storey=None):
    plan["walls"].append(dict(name=name, length=length, x=x, y=y, rot=rot, thk=thk))
    return add("IfcWall", name, api("geometry.add_wall_representation", f, context=body, length=length, height=H if height is None else height, thickness=thk),
               storey=storey, x=x, y=y, z=z, rot_z_deg=rot)

def iwall(name, p0, p1, thk=None, z=0.0, height=None, plan=PLAN, storey=None):
    """Interior partition centred on the line p0 -> p1 (metres); the line must be east-west or north-south."""
    t = m(PARAMS["int_thk_ft"]) if thk is None else thk
    (x0, y0), (x1, y1) = p0, p1
    if y0 == y1:   # east-west: thickness toward local +Y, so shift the start south by t/2
        return wall(name, x1 - x0, x0, y0 - t / 2, 0, thk=t, z=z, height=height, plan=plan, storey=storey)
    return wall(name, y1 - y0, x0 + t / 2, y0, 90, thk=t, z=z, height=height, plan=plan, storey=storey)   # north-south: local +Y is world -X

def opening(name, host, width, height, sill, x=None, y=None, along="x", plan=PLAN):
    """Rectangular void through a wall. along='x': wall runs east-west, x is the opening centre; along='y': wall runs north-south, y is the centre."""
    prof = rect(width, T + 0.1) if along == "x" else rect(T + 0.1, width)
    rep = api("geometry.add_profile_representation", f, context=body, profile=prof, depth=height)
    o = api("root.create_entity", f, ifc_class="IfcOpeningElement", name=name)
    api("geometry.assign_representation", f, product=o, representation=rep); place(o, x=x, y=y, z=sill)
    api("feature.add_feature", f, feature=o, element=host)
    plan["openings"].append(dict(name=name, width=width, x=x, y=y, along=along, kind="window" if (sill > 0.3 and abs(sill - FL) > 0.3) else "door"))

# Slab on grade
add("IfcSlab", "Slab on grade, 6 in", api("geometry.add_profile_representation", f, context=body, profile=rect(L, W), depth=S),
    predefined="BASESLAB", x=L / 2, y=W / 2, z=-S)

# Exterior walls (wall representation runs along local +X, thickness toward local +Y)
south = wall("South wall", L, 0, 0, 0)
north = wall("North wall", L, 0, W - T, 0)
west = wall("West wall (gable, shop doors)", W, T, 0, 90)
east = wall("East wall (gable)", W, L, 0, 90)
for d in (south, north, west, east): UPPER["walls"].append(PLAN["walls"][[w["name"] for w in PLAN["walls"]].index(d.Name)])
X0, X1, Y0, Y1 = T, L - T, T, W - T
XS = X0 + SL                                   # shop partition centreline
partition = wall("Shop partition (full height)", W - 2 * T, XS + PT / 2, Y0, 90, thk=PT)
UPPER["walls"].append(PLAN["walls"][-1])
XL = XS + PT / 2                               # house block starts here

# Shell openings: two 12 x 12 insulated sectional doors in the west gable, man doors, a few windows
rw, rh = m(PARAMS["rollup_w_ft"]), m(PARAMS["rollup_h_ft"])
gap = m(PARAMS["rollup_gap_ft"])
for i, cy in enumerate([W / 2 - (rw + gap) / 2, W / 2 + (rw + gap) / 2]):
    opening(f"Shop door {i + 1}, 12 x 12 insulated sectional, west gable", west, rw, rh, 0, x=T / 2, y=cy, along="y")
dw, dh = m(PARAMS["man_door_w_ft"]), m(PARAMS["man_door_h_ft"])
ww, wh, ws = m(PARAMS["window_w_ft"]), m(PARAMS["window_h_ft"]), m(PARAMS["window_sill_ft"])
opening("Shop man door, south", south, dw, dh, 0, x=X0 + m(4), y=T / 2, along="x")
opening("Shop to house door", partition, dw, dh, 0, x=XS, y=Y1 - m(3), along="y")
XK = XL + m(PARAMS["core_band_ft"])           # east edge of the core band
opening("Front door, south", south, dw, dh, 0, x=XK + m(6), y=T / 2, along="x")
opening("Back door, north", north, dw, dh, 0, x=X1 - m(5), y=W - T / 2, along="x")
# Ground-floor windows: common room south and north, bunk room A, one on the east gable
for name, host, xx, yy, along in [
    ("Window, common south 1", south, XK + m(14), T / 2, "x"), ("Window, common south 2", south, X1 - m(5), T / 2, "x"),
    ("Window, bunk A south", south, XL + m(5), T / 2, "x"),
    ("Window, kitchen north", north, XK + m(8), W - T / 2, "x"), ("Window, common north", north, X1 - m(12), W - T / 2, "x"),
    ("Window, common east", east, L - T / 2, W / 2, "y"),
]:
    opening(name, host, ww, wh, ws, x=xx, y=yy, along=along)

# Second floor over the house block: wood deck on a flush centre beam and 6x6 posts
HB = X1 - XL                                   # house block length, east-west
deck = add("IfcSlab", "Second floor, wood joists and subfloor", api("geometry.add_profile_representation", f, context=body, profile=rect(HB, Y1 - Y0), depth=DK),
           predefined="FLOOR", storey=upper, x=XL + HB / 2, y=(Y0 + Y1) / 2, z=FL - DK)
sw, sr, sl = m(PARAMS["stair_w_ft"]), m(PARAMS["stair_run_ft"]), m(PARAMS["stair_landing_ft"])
IT = m(PARAMS["int_thk_ft"])
YA = Y0 + m(PARAMS["bunk_a_depth_ft"])        # bunk room A north wall
YB1 = YA + m(PARAMS["bath_depth_ft"])         # bath 1 north wall
YB2 = YB1 + m(PARAMS["bath_depth_ft"])        # bath 2 north wall
YLD = YB2 + m(PARAMS["laundry_depth_ft"])     # laundry north wall; the U-stair takes YLD..Y1 at the north end of the band
stair_y0 = YLD + IT / 2                       # bottom riser of flight 1 (west), landing against the north wall, flight 2 (east) rises back south
void = api("root.create_entity", f, ifc_class="IfcOpeningElement", name="Stair void")
api("geometry.assign_representation", f, product=void, representation=api("geometry.add_profile_representation", f, context=body, profile=rect(2 * sw, Y1 - stair_y0), depth=DK + 0.1))
place(void, x=XL + sw, y=(stair_y0 + Y1) / 2, z=FL - DK - 0.05)
api("feature.add_feature", f, feature=void, element=deck)
def flight(name, x, y_start, rise0, northward):
    """Sloped slab for one flight of sr run and FL/2 rise, starting at (x, y_start, rise0) and climbing north or south."""
    run_len = math.hypot(sr, FL / 2); ang = math.atan2(FL / 2, sr) * (1 if northward else -1)
    rot = np.array([[1, 0, 0], [0, math.cos(ang), -math.sin(ang)], [0, math.sin(ang), math.cos(ang)]])   # tilt about X so +Y climbs (or -Y)
    e = api("root.create_entity", f, ifc_class="IfcStairFlight", name=name)
    api("geometry.assign_representation", f, product=e, representation=api("geometry.add_profile_representation", f, context=body, profile=rect(sw, run_len), depth=0.25))
    yc = y_start + (sr / 2 if northward else -sr / 2)
    mat = np.eye(4); mat[:3, :3] = rot; mat[:3, 3] = [x + sw / 2, yc, rise0 + FL / 4 - 0.125]
    api("geometry.edit_object_placement", f, product=e, matrix=mat, is_si=True)
    api("spatial.assign_container", f, relating_structure=ground, products=[e])
flight("Stair flight 1 (west, up to the landing)", XL, stair_y0, 0, True)
add("IfcSlab", "Stair landing", api("geometry.add_profile_representation", f, context=body, profile=rect(2 * sw, sl), depth=0.25), predefined="LANDING",
    x=XL + sw, y=Y1 - sl / 2, z=FL / 2 - 0.25)
flight("Stair flight 2 (east, landing to the second floor)", XL + sw, Y1 - sl, FL / 2, False)
beam_y = (Y0 + Y1) / 2
add("IfcBeam", "Centre beam, 14 in LVL, flush", api("geometry.add_profile_representation", f, context=body, profile=rect(HB, m(0.3)), depth=m(1.17)),
    x=XL + HB / 2, y=beam_y, z=FL - m(1.17) - m(0.08))
n_posts = int(round(HB / m(PARAMS["beam_post_spacing_ft"]))) - 1
for i in range(n_posts):
    px = XL + (i + 1) * HB / (n_posts + 1)
    add("IfcColumn", f"Beam post {i + 1}, 6x6", api("geometry.add_profile_representation", f, context=body, profile=rect(m(0.5), m(0.5)), depth=FL - DK), x=px, y=beam_y, z=0)
    PLAN["posts"].append((float(px), beam_y))

# Ground-floor temporary partitions: a 10 ft core band against the shop partition
band = iwall("Core band east wall", (XK, Y0), (XK, Y1), height=FL - DK)
iwall("Bunk A north wall", (XL, YA), (XK, YA), height=FL - DK)
iwall("Bath 1 north wall", (XL, YB1), (XK, YB1), height=FL - DK)
iwall("Bath 2 north wall", (XL, YB2), (XK, YB2), height=FL - DK)
iwall("Laundry north wall", (XL, YLD), (XK, YLD), height=FL - DK)
for name, yy in [("Bunk A door", Y0 + (YA - Y0) / 2), ("Bath 1 door", YA + (YB1 - YA) / 2), ("Bath 2 door", YB1 + (YB2 - YB1) / 2), ("Laundry door", YB2 + (YLD - YB2) / 2)]:
    opening(name, band, dw, dh, 0, x=XK, y=yy, along="y")

# Second-floor temporary partitions: bunk rooms along the south and north walls, open hall and landing between
URD = m(PARAMS["upper_room_depth_ft"]); n = PARAMS["upper_rooms_per_row"]
UH = H - FL                                   # partition height to the eave line (roof slope above is open)
ys, yn = Y0 + URD, Y1 - URD
iwall("Upper south row wall", (XL, ys), (X1, ys), z=FL, height=UH, plan=UPPER, storey=upper)
north_row_x0 = XK                             # north row starts east of the core band; the stair arrives in the band's north end
iwall("Upper north row wall", (north_row_x0, yn), (X1, yn), z=FL, height=UH, plan=UPPER, storey=upper)
iwall("Upper stair guard wall", (XL + 2 * sw, stair_y0), (XL + 2 * sw, Y1), z=FL, height=m(3.5), plan=UPPER, storey=upper)
rw_s = HB / n
upper_rooms = []
for i in range(n):
    xa, xb = XL + i * rw_s, XL + (i + 1) * rw_s
    if i < n - 1: iwall(f"Upper south room wall {i + 1}", (xb, Y0), (xb, ys), z=FL, height=UH, plan=UPPER, storey=upper)
    upper_rooms.append((f"Bunk {i + 2}", xa, Y0, xb, ys))
nn = n - 1; rw_n = (X1 - north_row_x0) / nn
for i in range(nn):
    xa, xb = north_row_x0 + i * rw_n, north_row_x0 + (i + 1) * rw_n
    if i < nn - 1: iwall(f"Upper north room wall {i + 1}", (xb, yn), (xb, Y1), z=FL, height=UH, plan=UPPER, storey=upper)
    upper_rooms.append((f"Bunk {n + 2 + i}", xa, yn, xb, Y1))
# Upstairs windows
for name, host, xx, yy, along in [
    ("Upper window, south 1", south, XL + rw_s / 2, T / 2, "x"), ("Upper window, south 2", south, XL + 1.5 * rw_s, T / 2, "x"), ("Upper window, south 3", south, XL + 2.5 * rw_s, T / 2, "x"),
    ("Upper window, north 1", north, north_row_x0 + rw_n / 2, W - T / 2, "x"), ("Upper window, north 2", north, north_row_x0 + 1.5 * rw_n, W - T / 2, "x"),
    ("Upper window, east", east, L - T / 2, W / 2, "y"),
]:
    opening(name, host, ww, wh, FL + ws, x=xx, y=yy, along=along, plan=UPPER)

# Main gable roof: a thin plate on both slopes, 1 ft overhang all round; ridge runs east-west
eave_z = H - PARAMS["pitch"] * OV
pts = [(-OV, eave_z), (W / 2, H + RISE), (W + OV, eave_z), (W + OV, eave_z + ROOF_T), (W / 2, H + RISE + ROOF_T), (-OV, eave_z + ROOF_T)]
for name, gx in [("West gable infill", 0), ("East gable infill", L - T)]:
    add("IfcWall", name, api("geometry.add_profile_representation", f, context=body, profile=polygon([(0, H), (W, H), (W / 2, H + RISE)]), depth=T),
        x=gx, y=0, z=0, rot=ALONG_X)
add("IfcRoof", "Gable roof, 4:12 metal", api("geometry.add_profile_representation", f, context=body, profile=polygon(pts), depth=L + 2 * OV),
    predefined="GABLE_ROOF", x=-OV, y=0, z=0, rot=ALONG_X)

# Plan data for draw_plan.py (ground floor and second floor as two drawings)
PLAN["rooms"] = [
    ("Shop, open to roof", X0, Y0, XS - PT / 2, Y1),
    ("Bunk 1", XL, Y0, XK, YA), ("Bath 1", XL, YA, XK, YB1), ("Bath 2", XL, YB1, XK, YB2), ("Laundry", XL, YB2, XK, YLD), ("Stair", XL, YLD, XK, Y1),
    ("Common room and kitchen", XK, Y0, X1, Y1),
]
PLAN["wet_core"] = [("Bath 1", XL, YA, XK, YB1), ("Bath 2", XL, YB1, XK, YB2), ("Laundry", XL, YB2, XK, YLD), ("Kitchen", XK, Y1 - m(8), XK + m(14), Y1)]
PLAN["trench"] = [(XL + m(2), YLD - m(0.5)), (XL + m(2), YA + m(0.8))]   # one north-south sewer line under the core band
PLAN["notes"] = [(XK + (X1 - XK) / 2, Y0 + m(5), "second floor above, 10 ft clear; 6x6 posts on the centre line"),
                 (X0 + SL / 2, Y0 + m(4), "two 12 x 12 insulated doors in the west gable; 20 ft eave")]
PLAN["dims"] = [(0, L / FT, W / FT + 2.5, f"{L / FT:.0f}'", False), (0, SL / FT, -2.5, f"{SL / FT:.0f}' shop", False),
                (XL / FT, XK / FT, -2.5, f"{(XK - XL) / FT:.0f}'", False), (XK / FT, L / FT, -2.5, f"{(L - XK) / FT:.0f}'", False),
                (0, W / FT, -2.5, f"{W / FT:.0f}'", True)]
PLAN["title"] = f"{stem}: ground floor, {PARAMS['eave_ft']:.0f} ft eave, {L / FT:.0f} x {W / FT:.0f} ft"
PLAN["start_x_ft"] = (XK + (X1 - XK) / 2) / FT
PLAN["finishes"] = FINISHES
PLAN["params"] = PARAMS
UPPER["rooms"] = [("Shop below, open to roof", X0, Y0, XS - PT / 2, Y1), ("Hall and landing", XL, ys, X1, yn), ("Stair down", XL, stair_y0, XL + 2 * sw, Y1), ("Open", XL + 2 * sw, yn, XK, Y1)] + upper_rooms
UPPER["notes"] = []
UPPER["dims"] = [(0, L / FT, W / FT + 2.5, f"{L / FT:.0f}'", False), (XL / FT, X1 / FT, -2.5, f"{HB / FT:.0f}' second floor", False), (0, W / FT, -2.5, f"{W / FT:.0f}'", True)]
UPPER["title"] = f"{stem}: second floor, deck at {PARAMS['floor_to_floor_ft']:.2f} ft, {(HB * (Y1 - Y0)) / FT**2:,.0f} sq ft"
UPPER["params"] = PARAMS
(HERE / "exports").mkdir(exist_ok=True)
(HERE / "exports" / f"{stem}-plan.json").write_text(json.dumps(PLAN, indent=1))
(HERE / "exports" / f"{stem}-plan-upper.json").write_text(json.dumps(UPPER, indent=1))

areas = {
    "slab_area_sqft": PARAMS["width_ft"] * PARAMS["length_ft"],
    "shop_area_sqft": PARAMS["shop_length_ft"] * PARAMS["width_ft"],
    "house_block_ground_sqft": round(HB * (Y1 - Y0) / FT**2),
    "second_floor_sqft": round(HB * (Y1 - Y0) / FT**2),
    "total_floor_sqft": round(PARAMS["shop_length_ft"] * PARAMS["width_ft"] + 2 * HB * (Y1 - Y0) / FT**2),
    "ridge_height_ft": PARAMS["eave_ft"] + PARAMS["pitch"] * PARAMS["width_ft"] / 2,
    "wall_area_sqft": round((2 * (PARAMS["length_ft"] + PARAMS["width_ft"]) * PARAMS["eave_ft"]) + PARAMS["width_ft"] * (PARAMS["pitch"] * PARAMS["width_ft"] / 2)),
    "roof_area_sqft": round(2 * (PARAMS["length_ft"] + 2 * PARAMS["overhang_ft"]) * ((PARAMS["width_ft"] / 2 + PARAMS["overhang_ft"]) / math.cos(math.atan(PARAMS["pitch"])))),
    "bunk_rooms": 1 + len(upper_rooms),
}
pset = api("pset.add_pset", f, product=building, name="Friendstead_Parameters")
api("pset.edit_pset", f, pset=pset, properties={k: float(v) for k, v in PARAMS.items()} | {k: float(v) for k, v in areas.items()}
    | {f"{n.lower().replace(' / ', '_').replace(', ', '_').replace(' ', '_')}_sqft": round((x1 - x0) * (y1 - y0) / FT**2) for n, x0, y0, x1, y1 in PLAN["rooms"] + upper_rooms})
fin = api("pset.add_pset", f, product=building, name="Friendstead_Finishes")
api("pset.edit_pset", f, pset=fin, properties=FINISHES)
f.write(str(ifc_path)); print(f"wrote {ifc_path}"); print(json.dumps(areas))

try:
    import bpy
    bpy.ops.wm.read_homefile(use_empty=True)
    bpy.ops.bim.load_project(filepath=str(ifc_path))
    bpy.ops.wm.save_as_mainfile(filepath=str(blend_path)); print(f"wrote {blend_path}")
except Exception as e:  # noqa: BLE001
    print(f"blend not written: {e}")
