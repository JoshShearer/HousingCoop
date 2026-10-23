"""Build the first-person browser walkthrough for a design version.

    python3 designs/make_walkthrough.py designs/barndominium/exports/barndominium-v3-plan.json <model.glb>

Writes exports/<stem>-walkthrough.html (standalone, opens from disk; three.js comes from a CDN) and a
headerless copy next to the GLB for publishing as a Claude artifact. The GLB comes from export_glb.py:

    ~/.local/bin/blender -b designs/barndominium/barndominium-v3.blend --python designs/export_glb.py -- /path/to/barndominium-v3.glb
"""
import base64, json, pathlib, sys
FT = 0.3048
plan_path, glb_path = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
plan = json.loads(plan_path.read_text()); P = plan["params"]
rooms = [[n, round(x0 / FT, 2), round(y0 / FT, 2), round(x1 / FT, 2), round(y1 / FT, 2)] for n, x0, y0, x1, y1 in plan["rooms"]]
stem = plan_path.stem.replace("-plan", "")
L, W, PD = P["length_ft"], P["width_ft"], P["porch_depth_ft"]
page = pathlib.Path(__file__).with_name("walkthrough_template.html").read_text()
for k, v in {"GLB_B64": base64.b64encode(glb_path.read_bytes()).decode(), "ROOMS": json.dumps(rooms), "L_FT": f"{L:g}", "W_FT": f"{W:g}",
             "PORCH_FT": f"{PD:g}", "START_X_FT": f"{plan.get('start_x_ft', L / 2):.2f}", "VERSION": stem.split("-")[-1],
             "MAP_W": "480", "MAP_H": str(round(480 * (W + PD) / L) + 40)}.items():
    page = page.replace("{{" + k + "}}", v)
assert "{{" not in page
bare = glb_path.with_name(f"{stem}-walkthrough.html"); bare.write_text(page)
full = plan_path.with_name(f"{stem}-walkthrough.html")
full.write_text('<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>[hidden]{display:none!important}</style></head><body>\n' + page + "</body></html>\n")
print("wrote", bare, "and", full)
