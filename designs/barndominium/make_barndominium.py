"""Parametric starter for the Friendstead shared barndominium (v5 layout).

Long sides run east-west, 70 x 40 ft. A covered porch runs the full south
side. The shop is a 20 ft full-depth bay at the west gable with a roll-up
door on the gable and a man door on the porch side. The 50 x 40 house is a
split plan with a shared wet core: bath 1, laundry, kitchen, master bath and
the utility room all sit on one east-west line in the north half so one
sewer trench and one water manifold serve everything. Walls are 10 ft to the
eave; the great room is vaulted to the ridge, the wings get 9 ft flat ceilings. Exterior finish is a cool white roof and light walls (pset
Friendstead_Finishes). v3 (72 ft, separate baths) lives on as its IFC.

Builds an IFC4 model with ifcopenshell (bundled with Bonsai), then opens it in
Bonsai and saves a .blend beside it. Run through the Bonsai-enabled Blender:

    ~/.local/bin/blender -b --python designs/barndominium/make_barndominium.py -- [out-stem]

Dimensions in PARAMS are feet and are converted to metres for the IFC.
This is a massing model: openings are voids with no door or window objects yet.
"""
import sys, math, pathlib
import numpy as np
import ifcopenshell, ifcopenshell.api
import ifcopenshell.api.project, ifcopenshell.api.root, ifcopenshell.api.unit, ifcopenshell.api.context
import ifcopenshell.api.aggregate, ifcopenshell.api.spatial, ifcopenshell.api.geometry, ifcopenshell.api.attribute
import ifcopenshell.api.pset, ifcopenshell.api.feature

FT = 0.3048
PARAMS = dict(
    length_ft=70.0,        # east-west, the long side; 40 x 70 = 2,800 sq ft (60 ft was too tight: 15 ft great room)
    width_ft=40.0,         # north-south, gable-end width
    eave_ft=10.0,          # wall height to the eave
    pitch=4 / 12,          # main roof pitch, metal roof
    porch_depth_ft=10.0,   # covered porch along the whole south side
    porch_pitch=2 / 12,    # shed roof over the porch, tied in under the eave
    shop_length_ft=20.0,   # west gable bay, full 40 ft depth, 800 sq ft
    wall_thk_ft=0.667,     # 8 in: girts, foam, liner and metal skin
    partition_thk_ft=0.5,  # 6 in interior wall between living and shop
    slab_thk_ft=0.5,       # 6 in slab on grade (engineer to confirm)
    overhang_ft=1.0,       # roof overhang at north eave and both gables
    rollup_w_ft=12.0, rollup_h_ft=8.0,   # shop roll-up door, west gable; 8 ft is the most a 10 ft eave carries with a header
    man_door_w_ft=3.0, man_door_h_ft=6.67,
    window_w_ft=4.0, window_h_ft=4.0, window_sill_ft=3.0,
    porch_post_count=8,
    ceiling_ft=9.0,          # flat ceilings over the two wings; the great room is open to the ridge
    entry_gable_w_ft=24.0,   # timber-frame cross gable over the porch in front of the great room door and windows
    entry_gable_pitch=4 / 12,
    entry_gable_ov_ft=1.0,   # side overhang of the entry gable roof
    # Split floor plan with a shared wet core (feet, measured from the inside faces)
    int_thk_ft=0.375,        # 4.5 in interior partitions (2x4 + drywall)
    bed_wing_ft=12.0,        # beside the shop: bedroom 1 (south), hall, bath 1 + laundry, bedroom 2 (north)
    bedroom_depth_ft=13.0,   # bedroom 1 on the porch wall
    hall_w_ft=4.0,           # east-west hall from the great room to the shop door
    core_depth_ft=9.5,       # bath 1 and laundry band north of the hall; master bath sits on the same line
    bath_w_ft=7.0,           # bath 1 width, laundry takes the rest of the wing
    master_wing_ft=11.0,     # east end: master bedroom (south), closet, master bath, utility (north)
    master_depth_ft=15.0,
    closet_depth_ft=5.0,     # walk-through closet between bedroom and bath
    master_bath_depth_ft=9.0,
)
FINISHES = dict(   # cool exterior: high solar reflectance and high emittance, Austin is climate zone 2A
    roof="Standing-seam steel, PVDF (Kynar 500) bright white: initial SR about 0.68-0.72, emittance 0.85, SRI 82-88",
    walls="PVDF bone white or light stone wall panel: SRI about 80; any colour with SRI above 65 is acceptable",
    avoid="Bare Galvalume (SRI about 62, low emittance) and dark bronze or charcoal (SRI about 25)",
    source="McElroy Metal cool-roof tables and ORNL/FSEC Fort Myers field study, checked 2026-10-22",
)

HERE = pathlib.Path(__file__).resolve().parent
stem = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv and len(sys.argv) > sys.argv.index("--") + 1 else "barndominium-v5"
ifc_path, blend_path = HERE / f"{stem}.ifc", HERE / f"{stem}.blend"

m = lambda ft: ft * FT
L, W, H = m(PARAMS["length_ft"]), m(PARAMS["width_ft"]), m(PARAMS["eave_ft"])
P, SL, T, PT, S, OV = (m(PARAMS[k]) for k in ("porch_depth_ft", "shop_length_ft", "wall_thk_ft", "partition_thk_ft", "slab_thk_ft", "overhang_ft"))
RISE = PARAMS["pitch"] * (W / 2)
ROOF_T = 0.25

api = ifcopenshell.api.run
f = ifcopenshell.api.project.create_file(version="IFC4")
project = api("root.create_entity", f, ifc_class="IfcProject", name="Friendstead barndominium")
api("unit.assign_unit", f, length={"is_metric": True, "raw": "METERS"})
model_ctx = api("context.add_context", f, context_type="Model")
body = api("context.add_context", f, context_type="Model", context_identifier="Body", target_view="MODEL_VIEW", parent=model_ctx)
site = api("root.create_entity", f, ifc_class="IfcSite", name="Common tract")
building = api("root.create_entity", f, ifc_class="IfcBuilding", name="Barndominium")
storey = api("root.create_entity", f, ifc_class="IfcBuildingStorey", name="Ground floor")
api("aggregate.assign_object", f, relating_object=project, products=[site])
api("aggregate.assign_object", f, relating_object=site, products=[building])
api("aggregate.assign_object", f, relating_object=building, products=[storey])

ALONG_X = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=float)  # profile drawn in (y, z), extruded along world +X

def place(product, x=0.0, y=0.0, z=0.0, rot_z_deg=0.0, rot=None):
    mat = np.eye(4)
    if rot is None:
        c, s = math.cos(math.radians(rot_z_deg)), math.sin(math.radians(rot_z_deg))
        rot = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
    mat[:3, :3] = rot
    mat[:3, 3] = [x, y, z]
    api("geometry.edit_object_placement", f, product=product, matrix=mat, is_si=True)

def add(ifc_class, name, rep, predefined=None, **pl):
    e = api("root.create_entity", f, ifc_class=ifc_class, name=name)
    api("geometry.assign_representation", f, product=e, representation=rep)
    place(e, **pl)
    api("spatial.assign_container", f, relating_structure=storey, products=[e])
    if predefined:
        api("attribute.edit_attributes", f, product=e, attributes={"PredefinedType": predefined})
    return e

def rect(xdim, ydim):
    return f.create_entity("IfcRectangleProfileDef", ProfileType="AREA", XDim=xdim, YDim=ydim)

def polygon(pts):
    poly = f.create_entity("IfcPolyline", Points=[f.create_entity("IfcCartesianPoint", Coordinates=p) for p in pts + [pts[0]]])
    return f.create_entity("IfcArbitraryClosedProfileDef", ProfileType="AREA", OuterCurve=poly)

PLAN = {"walls": [], "openings": [], "rooms": [], "posts": []}

def wall(name, length, x, y, rot, thk=T):
    PLAN["walls"].append(dict(name=name, length=length, x=x, y=y, rot=rot, thk=thk))
    return add("IfcWall", name, api("geometry.add_wall_representation", f, context=body, length=length, height=H, thickness=thk), x=x, y=y, rot_z_deg=rot)

def iwall(name, p0, p1, thk=None):
    """Interior partition centred on the line p0 -> p1 (metres); the line must be east-west or north-south."""
    t = m(PARAMS["int_thk_ft"]) if thk is None else thk
    (x0, y0), (x1, y1) = p0, p1
    if y0 == y1:   # east-west: thickness toward local +Y, so shift the start south by t/2
        return wall(name, x1 - x0, x0, y0 - t / 2, 0, thk=t)
    return wall(name, y1 - y0, x0 + t / 2, y0, 90, thk=t)   # north-south: local +Y is world -X

def opening(name, host, width, height, sill, x=None, y=None, along="x"):
    """Rectangular void through a wall. along='x': wall runs east-west, x is the opening centre; along='y': wall runs north-south, y is the centre."""
    if along == "x":
        rep = api("geometry.add_profile_representation", f, context=body, profile=rect(width, T + 0.1), depth=height)
        o = api("root.create_entity", f, ifc_class="IfcOpeningElement", name=name)
        api("geometry.assign_representation", f, product=o, representation=rep); place(o, x=x, y=y, z=sill)
    else:
        rep = api("geometry.add_profile_representation", f, context=body, profile=rect(T + 0.1, width), depth=height)
        o = api("root.create_entity", f, ifc_class="IfcOpeningElement", name=name)
        api("geometry.assign_representation", f, product=o, representation=rep); place(o, x=x, y=y, z=sill)
    api("feature.add_feature", f, feature=o, element=host)
    PLAN["openings"].append(dict(name=name, width=width, x=x, y=y, along=along, kind="window" if sill > 0 else "door"))
    return o

# Slab on grade: main footprint plus the south porch
add("IfcSlab", "Slab on grade", api("geometry.add_profile_representation", f, context=body, profile=rect(L, W + P), depth=S),
    predefined="BASESLAB", x=L / 2, y=(W + P) / 2 - P, z=-S)

# Exterior walls (wall representation runs along local +X, thickness toward local +Y)
south = wall("South wall (porch side)", L, 0, 0, 0)
north = wall("North wall", L, 0, W - T, 0)
west = wall("West wall (gable, shop door)", W, T, 0, 90)
east = wall("East wall (gable)", W, L, 0, 90)
X0, X1, Y0, Y1 = T, L - T, T, W - T
XS = X0 + SL                                   # shop partition centreline
partition = wall("Shop partition", W - 2 * T, XS + PT / 2, Y0, 90, thk=PT)
XL = XS + PT / 2                               # living side starts here

# Openings in the shell
rw, rh = m(PARAMS["rollup_w_ft"]), m(PARAMS["rollup_h_ft"])
dw, dh = m(PARAMS["man_door_w_ft"]), m(PARAMS["man_door_h_ft"])
ww, wh, ws = m(PARAMS["window_w_ft"]), m(PARAMS["window_h_ft"]), m(PARAMS["window_sill_ft"])
opening("Shop roll-up door, west gable", west, rw, rh, 0, x=T / 2, y=W / 2, along="y")
opening("Shop man door, south", south, dw, dh, 0, x=XS - m(4), y=T / 2, along="x")

# Split floor plan with the wet core on one east-west line
IT = m(PARAMS["int_thk_ft"])
XB = XL + m(PARAMS["bed_wing_ft"])           # bedroom wing / great room
XM = X1 - m(PARAMS["master_wing_ft"])        # great room / master wing
YB1 = Y0 + m(PARAMS["bedroom_depth_ft"])     # bedroom 1 back wall
YH = YB1 + m(PARAMS["hall_w_ft"])            # hall north wall
YC = YH + m(PARAMS["core_depth_ft"])         # bath 1 and laundry north wall, bedroom 2 south wall
XBA = XL + m(PARAMS["bath_w_ft"])            # bath 1 / laundry
YM = Y0 + m(PARAMS["master_depth_ft"])       # master back wall
YCL = YM + m(PARAMS["closet_depth_ft"])      # closet north wall
YMB = YCL + m(PARAMS["master_bath_depth_ft"]) # master bath north wall; utility beyond

def gable_wall(name, x, thk):
    """North-south partition whose top follows the roof underside: 10 ft at the eaves, ridge height at mid-span."""
    span = Y1 - Y0
    prof = polygon([(0, 0), (span, 0), (span, H + PARAMS["pitch"] * (W - Y1)), (W / 2 - Y0, H + RISE), (0, H + PARAMS["pitch"] * Y0)])
    return add("IfcWall", name, api("geometry.add_profile_representation", f, context=body, profile=prof, depth=thk), x=x - thk / 2, y=Y0, z=0, rot=ALONG_X)
w_wing = gable_wall("Bedroom wing wall (to the roof)", XB, IT)
w_b1 = iwall("Bedroom 1 back wall", (XL, YB1), (XB, YB1))
w_hall = iwall("Hall north wall", (XL, YH), (XB, YH))
w_core = iwall("Core north wall", (XL, YC), (XB, YC))
w_bl = iwall("Bath 1 / laundry wall", (XBA, YH), (XBA, YC))
e_wing = gable_wall("Master wing wall (to the roof)", XM, IT)
e_back = iwall("Master back wall", (XM, YM), (X1, YM))
e_cl = iwall("Closet north wall", (XM, YCL), (X1, YCL))
e_mb = iwall("Master bath north wall", (XM, YMB), (X1, YMB))

# Doors (centres)
GRW = XM - XB
opening("Porch door", south, dw, dh, 0, x=XB + GRW / 2, y=T / 2, along="x")
opening("Hall door", w_wing, dw, dh, 0, x=XB, y=YB1 + (YH - YB1) / 2, along="y")
opening("Hall to shop door", partition, dw, dh, 0, x=XS, y=YB1 + (YH - YB1) / 2, along="y")
opening("Bedroom 1 door", w_b1, dw, dh, 0, x=XB - m(3), y=YB1, along="x")
opening("Bath 1 door", w_hall, dw, dh, 0, x=XL + m(3), y=YH, along="x")
opening("Laundry door", w_hall, dw, dh, 0, x=XB - m(2.5), y=YH, along="x")
opening("Bedroom 2 door", w_wing, dw, dh, 0, x=XB, y=YC + m(3), along="y")
opening("Master door", e_wing, dw, dh, 0, x=XM, y=YM - m(3), along="y")
opening("Closet door", e_back, dw, dh, 0, x=XM + m(3), y=YM, along="x")
opening("Master bath door", e_cl, dw, dh, 0, x=XM + m(3), y=YCL, along="x")
opening("Utility door", e_wing, dw, dh, 0, x=XM, y=YMB + (Y1 - YMB) / 2, along="y")

# Windows
opening("South window, bedroom 1", south, ww, wh, ws, x=XL + (XB - XL) / 2, y=T / 2, along="x")
opening("South window, great room west", south, ww, wh, ws, x=XB + GRW * 0.22, y=T / 2, along="x")
opening("South window, great room east", south, ww, wh, ws, x=XM - GRW * 0.22, y=T / 2, along="x")
opening("South window, master", south, ww, wh, ws, x=XM + (X1 - XM) / 2, y=T / 2, along="x")
opening("North window, bedroom 2", north, ww, wh, ws, x=XL + (XB - XL) / 2, y=W - T / 2, along="x")
opening("North window, kitchen", north, ww, wh, ws, x=XM - GRW * 0.22, y=W - T / 2, along="x")
opening("North window, dining", north, ww, wh, ws, x=XB + GRW * 0.22, y=W - T / 2, along="x")

# Flat ceilings over the wings; the great room and shop stay open to the roof
CH = m(PARAMS["ceiling_ft"])
for name, xa, xb in [("Ceiling, bedroom wing", XL, XB), ("Ceiling, master wing", XM, X1)]:
    add("IfcCovering", name, api("geometry.add_profile_representation", f, context=body, profile=rect(xb - xa, Y1 - Y0), depth=0.05),
        predefined="CEILING", x=(xa + xb) / 2, y=(Y0 + Y1) / 2, z=CH)
opening("East window, master", east, ww, wh, ws, x=L - T / 2, y=Y0 + (YM - Y0) / 2, along="y")

# Main gable roof: a thin plate following both slopes, so the underside is the vault; ridge runs east-west,
# no south overhang because the porch roof ties in there
north_eave = H - PARAMS["pitch"] * OV
pts = [(0, H), (W / 2, H + RISE), (W + OV, north_eave), (W + OV, north_eave + ROOF_T), (W / 2, H + RISE + ROOF_T), (0, H + ROOF_T)]
# Gable infill above the 10 ft end walls
for name, gx in [("West gable infill", 0), ("East gable infill", L - T)]:
    add("IfcWall", name, api("geometry.add_profile_representation", f, context=body, profile=polygon([(0, H), (W, H), (W / 2, H + RISE)]), depth=T),
        x=gx, y=0, z=0, rot=ALONG_X)
add("IfcRoof", "Gable roof, 4:12 metal", api("geometry.add_profile_representation", f, context=body, profile=polygon(pts), depth=L + 2 * OV),
    predefined="GABLE_ROOF", x=-OV, y=0, z=0, rot=ALONG_X)

# Entry gable: a cross gable over the porch, centred on the porch door, eaves at the main eave, 10 ft projection
GW, GP, GOV = m(PARAMS["entry_gable_w_ft"]), PARAMS["entry_gable_pitch"], m(PARAMS["entry_gable_ov_ft"])
XC = XB + GRW / 2
XG0, XG1 = XC - GW / 2, XC + GW / 2
ZR = H + GP * GW / 2                      # ridge of the entry gable
ZE = H - GP * GOV                         # eave at the side overhang
ALONG_NEG_Y = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]], dtype=float)  # profile drawn in (x, z), extruded along world -Y

# Porch shed roof in two pieces, west and east of the entry gable
edge_h = H - (P + OV) * PARAMS["porch_pitch"]
ppts = [(0, H - ROOF_T), (-(P + OV), edge_h - ROOF_T), (-(P + OV), edge_h), (0, H)]
for name, px, depth in [("Porch roof west, 2:12 shed", -OV, XG0 - GOV + OV), ("Porch roof east, 2:12 shed", XG1 + GOV, L + OV - XG1 - GOV)]:
    add("IfcRoof", name, api("geometry.add_profile_representation", f, context=body, profile=polygon(ppts), depth=depth),
        predefined="SHED_ROOF", x=px, y=0, z=0, rot=ALONG_X)

gpts = [(XG0 - GOV, ZE), (XC, ZR), (XG1 + GOV, ZE), (XG1 + GOV, ZE + ROOF_T), (XC, ZR + ROOF_T), (XG0 - GOV, ZE + ROOF_T)]
add("IfcRoof", "Entry gable roof, 4:12", api("geometry.add_profile_representation", f, context=body, profile=polygon(gpts), depth=P + OV),
    predefined="GABLE_ROOF", x=0, y=0, z=0, rot=ALONG_NEG_Y)
# Back of the entry gable where it meets the main roof: a triangular panel in the plane of the south wall
add("IfcWall", "Entry gable back infill", api("geometry.add_profile_representation", f, context=body, profile=polygon([(XG0, H), (XG1, H), (XC, ZR)]), depth=T),
    x=0, y=T, z=0, rot=ALONG_NEG_Y)

def member(name, p0, p1, w, h, ifc_class="IfcBeam"):
    """Timber member of w x h section along the line p0 -> p1 (metres); w is horizontal, h is upright."""
    p0, p1 = np.array(p0, float), np.array(p1, float)
    d = p1 - p0; length = float(np.linalg.norm(d)); c3 = d / length
    up = np.array([0, 0, 1.0]) if abs(c3[2]) < 0.99 else np.array([0, 1.0, 0])
    c1 = np.cross(up, c3); c1 /= np.linalg.norm(c1); c2 = np.cross(c3, c1)
    rot = np.column_stack([c1, c2, c3])
    return add(ifc_class, name, api("geometry.add_profile_representation", f, context=body, profile=rect(w, h), depth=length), x=p0[0], y=p0[1], z=p0[2], rot=rot)

IN = 0.0254
yp = -P + m(0.5)                           # post line, same as the porch posts
beam_top = H
bz = beam_top - 5 * IN                     # centreline of the 8x10 beams
for name, gx in [("Timber post, entry west", XG0), ("Timber post, entry east", XG1)]:
    add("IfcColumn", name, api("geometry.add_profile_representation", f, context=body, profile=rect(8 * IN, 8 * IN), depth=beam_top - 10 * IN), x=gx, y=yp, z=0)
member("Timber beam, entry front (bottom chord)", (XG0, yp, bz), (XG1, yp, bz), 8 * IN, 10 * IN)
member("Timber beam, entry west eave", (XG0, yp, bz), (XG0, 0, bz), 8 * IN, 10 * IN)
member("Timber beam, entry east eave", (XG1, yp, bz), (XG1, 0, bz), 8 * IN, 10 * IN)
rz = 0.11                                  # drop of the rafter centreline below the roof underside
member("Timber rafter, entry west", (XG0 - GOV, yp, ZE - rz), (XC, yp, ZR - rz), 6 * IN, 8 * IN)
member("Timber rafter, entry east", (XG1 + GOV, yp, ZE - rz), (XC, yp, ZR - rz), 6 * IN, 8 * IN)
member("Timber king post, entry", (XC, yp, beam_top), (XC, yp, ZR - rz - 0.1), 6 * IN, 6 * IN, "IfcMember")
for name, gx in [("Timber strut, entry west", (XG0 - GOV + XC) / 2), ("Timber strut, entry east", (XG1 + GOV + XC) / 2)]:
    member(name, (XC, yp, beam_top + 0.15), (gx, yp, (ZE + ZR) / 2 - rz - 0.05), 4 * IN, 6 * IN, "IfcMember")
member("Timber ridge beam, entry", (XC, yp, ZR - rz), (XC, 0, ZR - rz), 6 * IN, 8 * IN)
member("Timber tie, entry west (wall end)", (XG0, 0, bz), (XG0, 0, bz), 1, 1) if False else None

# Porch posts along the south edge
post_y = -P + m(0.5)
post_h = H - (0 - post_y) * PARAMS["porch_pitch"] - ROOF_T
for i, px in enumerate(np.linspace(m(0.5), L - m(0.5), PARAMS["porch_post_count"])):
    add("IfcColumn", f"Porch post {i + 1}", api("geometry.add_profile_representation", f, context=body, profile=rect(m(0.5), m(0.5)), depth=post_h), x=float(px), y=post_y, z=0)

PLAN["rooms"] = [
    ("Shop", X0, Y0, XS - PT / 2, Y1),
    ("Bedroom 1", XL, Y0, XB, YB1), ("Hall", XL, YB1, XB, YH), ("Bath 1", XL, YH, XBA, YC), ("Laundry", XBA, YH, XB, YC), ("Bedroom 2", XL, YC, XB, Y1),
    ("Kitchen / dining / living", XB, Y0, XM, Y1),
    ("Master bedroom", XM, Y0, X1, YM), ("Closet", XM, YM, X1, YCL), ("Master bath", XM, YCL, X1, YMB), ("Utility", XM, YMB, X1, Y1),
    ("Covered porch", 0, -P, L, 0),
]
PLAN["wet_core"] = [("Bath 1", XL, YH, XBA, YC), ("Laundry", XBA, YH, XB, YC), ("Kitchen", XB, Y1 - m(10), XM, Y1), ("Master bath", XM, YCL, X1, YMB), ("Utility", XM, YMB, X1, Y1)]
PLAN["trench"] = [(XL, YH + m(2)), (X1, YH + m(2))]   # one sewer line, east-west, under the core
PLAN["notes"] = [(XB + (XM - XB) / 2, Y0 + m(6), f"vaulted to the ridge, {PARAMS['eave_ft'] + PARAMS['pitch'] * PARAMS['width_ft'] / 2:.1f} ft"),
                 (XL + (XB - XL) / 2, Y0 + m(2.5), f"{PARAMS['ceiling_ft']:.0f} ft flat ceilings, both wings")]
PLAN["dims"] = [  # (start, end, offset, label, vertical) in feet, for the 2D drawing
    (0, L / FT, W / FT + 2.5, f"{L / FT:.0f}'", False),
    (0, SL / FT, -P / FT - 2.5, f"{SL / FT:.0f}' shop", False),
    (XL / FT, XB / FT, -P / FT - 2.5, f"{(XB - XL) / FT:.0f}'", False),
    (XB / FT, XM / FT, -P / FT - 2.5, f"{(XM - XB) / FT:.0f}'", False),
    (XM / FT, L / FT, -P / FT - 2.5, f"{(L - XM) / FT:.0f}'", False),
    (-P / FT, 0, -2.5, f"{P / FT:.0f}' porch", True), (0, W / FT, -2.5, f"{W / FT:.0f}'", True),
]
PLAN["start_x_ft"] = (XB + (XM - XB) / 2) / FT
PLAN["finishes"] = FINISHES
PLAN["posts"] = [(float(px), post_y) for px in np.linspace(m(0.5), L - m(0.5), PARAMS["porch_post_count"])] + [(XG0, yp), (XG1, yp)]
PLAN["gable"] = (XG0 - GOV, -(P + OV), XG1 + GOV, 0, f"timber entry gable, {PARAMS['entry_gable_w_ft']:.0f}' wide, ridge {ZR / FT:.0f}'")
PLAN["params"] = PARAMS
import json; (HERE / "exports" / f"{stem}-plan.json").write_text(json.dumps(PLAN, indent=1))

pset = api("pset.add_pset", f, product=building, name="Friendstead_Parameters")
api("pset.edit_pset", f, pset=pset, properties={k: float(v) for k, v in PARAMS.items()} | {
    "floor_area_sqft": PARAMS["width_ft"] * PARAMS["length_ft"],
    "shop_area_sqft": PARAMS["shop_length_ft"] * PARAMS["width_ft"],
    "living_area_sqft": (PARAMS["length_ft"] - PARAMS["shop_length_ft"]) * PARAMS["width_ft"],
    "porch_area_sqft": PARAMS["porch_depth_ft"] * PARAMS["length_ft"],
    "wet_core_trench_ft": round((X1 - XL) / FT),
    "ridge_height_ft": PARAMS["eave_ft"] + PARAMS["pitch"] * PARAMS["width_ft"] / 2,
} | {f"{n.lower().replace(' / ', '_').replace(' ', '_')}_sqft": round((x1 - x0) * (y1 - y0) / FT**2) for n, x0, y0, x1, y1 in PLAN["rooms"]})
fin = api("pset.add_pset", f, product=building, name="Friendstead_Finishes")
api("pset.edit_pset", f, pset=fin, properties=FINISHES)
f.write(str(ifc_path)); print(f"wrote {ifc_path}")

try:
    import bpy
    bpy.ops.wm.read_homefile(use_empty=True)
    bpy.ops.bim.load_project(filepath=str(ifc_path))
    bpy.ops.wm.save_as_mainfile(filepath=str(blend_path)); print(f"wrote {blend_path}")
except Exception as e:  # noqa: BLE001
    print(f"blend not written: {e}")
