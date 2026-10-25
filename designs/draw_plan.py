"""Draw a dimensioned 2D floor plan from the JSON a generator writes to exports/.

    uv run --with matplotlib python -I designs/draw_plan.py designs/barndominium/exports/barndominium-v2-plan.json
"""
import json, sys, pathlib
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Arc, Polygon

plt.rcParams["text.parse_math"] = False
FT = 0.3048
src = pathlib.Path(sys.argv[1]); plan = json.loads(src.read_text())
ft = lambda v: v / FT
INK, MUTED, SURFACE, WALL, OPEN = "#0b0b0b", "#52514e", "#fcfcfb", "#2b2b2b", "#fcfcfb"

fig, ax = plt.subplots(figsize=(14, 10.5), dpi=150); fig.patch.set_facecolor(SURFACE); ax.set_facecolor(SURFACE)
for w in plan["walls"]:
    L, t = ft(w["length"]), ft(w["thk"]); x, y = ft(w["x"]), ft(w["y"])
    if w["rot"] == 0: ax.add_patch(Rectangle((x, y), L, t, color=WALL, lw=0))
    else: ax.add_patch(Rectangle((x - t, y), t, L, color=WALL, lw=0))
# openings: doors as gaps with a swing, windows as gaps with a thin line
for o in plan["openings"]:
    wdt, x, y = ft(o["width"]), ft(o["x"]), ft(o["y"])
    host = min(plan["walls"], key=lambda w: (abs(ft(w["y"]) + ft(w["thk"]) / 2 - y) if w["rot"] == 0 else abs(ft(w["x"]) - ft(w["thk"]) / 2 - x)) + (0 if (w["rot"] == 0) == (o["along"] == "x") else 99))
    t = ft(host["thk"]) + 0.2
    if o["along"] == "x":
        ax.add_patch(Rectangle((x - wdt / 2, y - t / 2), wdt, t, color=OPEN, lw=0, zorder=3))
        if o["kind"] == "window": ax.plot([x - wdt / 2, x + wdt / 2], [y, y], color=INK, lw=0.8, zorder=4)
        else:
            ax.plot([x - wdt / 2, x - wdt / 2], [y, y + wdt], color=INK, lw=0.8, zorder=4)
            ax.add_patch(Arc((x - wdt / 2, y), 2 * wdt, 2 * wdt, theta1=0, theta2=90, color=MUTED, lw=0.6, zorder=4))
    else:
        ax.add_patch(Rectangle((x - t / 2, y - wdt / 2), t, wdt, color=OPEN, lw=0, zorder=3))
        if o["kind"] == "window": ax.plot([x, x], [y - wdt / 2, y + wdt / 2], color=INK, lw=0.8, zorder=4)
        else:
            ax.plot([x, x - wdt], [y - wdt / 2, y - wdt / 2], color=INK, lw=0.8, zorder=4)
            ax.add_patch(Arc((x, y - wdt / 2), 2 * wdt, 2 * wdt, theta1=90, theta2=180, color=MUTED, lw=0.6, zorder=4))
for name, x0, y0, x1, y1 in plan.get("wet_core", []):
    ax.add_patch(Rectangle((ft(x0), ft(y0)), ft(x1 - x0), ft(y1 - y0), facecolor="#1baf7a", alpha=0.14, lw=0, zorder=0))
if plan.get("trench"):
    (tx0, ty0), (tx1, ty1) = plan["trench"]
    ax.plot([ft(tx0), ft(tx1)], [ft(ty0), ft(ty1)], color="#1baf7a", lw=2.2, ls=(0, (6, 3)), zorder=0.5)
    ax.text(ft(tx1) + 0.6, ft(ty1), f"sewer trench {ft(((tx1 - tx0) ** 2 + (ty1 - ty0) ** 2) ** 0.5):.0f}'", color="#1baf7a", fontsize=8, va="center")
if plan.get("gable"):
    gx0, gy0, gx1, gy1, glabel = plan["gable"]
    ax.add_patch(Rectangle((ft(gx0), ft(gy0)), ft(gx1 - gx0), ft(gy1 - gy0), fill=False, ls=(0, (4, 3)), lw=1, edgecolor=INK, zorder=1))
    ax.plot([ft((gx0 + gx1) / 2)] * 2, [ft(gy0), ft(gy1)], color=INK, lw=0.6, ls=(0, (2, 2)))
    ax.text(ft((gx0 + gx1) / 2) + 0.6, ft(gy0) + 1.6, glabel, ha="center", va="bottom", fontsize=7.5, color=INK, style="italic", bbox=dict(facecolor=SURFACE, edgecolor="none", pad=1.5))
for nx, ny, text in plan.get("notes", []):
    ax.text(ft(nx), ft(ny), text, ha="center", va="center", fontsize=7.5, color=MUTED, style="italic")
for px, py in plan["posts"]:
    ax.add_patch(Rectangle((ft(px) - 0.25, ft(py) - 0.25), 0.5, 0.5, color=WALL, lw=0))
for name, x0, y0, x1, y1 in plan["rooms"]:
    x0, y0, x1, y1 = map(ft, (x0, y0, x1, y1)); area = (x1 - x0) * (y1 - y0)
    ax.text((x0 + x1) / 2, (y0 + y1) / 2 + 0.6, name, ha="center", va="center", fontsize=9.5, color=INK, weight="bold")
    small = (x1 - x0) < 8
    ax.text((x0 + x1) / 2, (y0 + y1) / 2 - 0.8, f"{x1 - x0:.0f}' x {y1 - y0:.0f}'" + ("" if small else f"  ·  {area:,.0f} sq ft"), ha="center", va="center", fontsize=7 if small else 8, color=MUTED)
P = plan["params"]; L, W, PD = P["length_ft"], P["width_ft"], P["porch_depth_ft"]
def dim(x0, x1, y, label, vertical=False):
    if vertical: ax.annotate("", (y, x1), (y, x0), arrowprops=dict(arrowstyle="|-|", lw=0.7, color=MUTED, mutation_scale=4)); ax.text(y - 0.5, (x0 + x1) / 2, label, rotation=90, ha="center", va="center", fontsize=8, color=MUTED)
    else: ax.annotate("", (x1, y), (x0, y), arrowprops=dict(arrowstyle="|-|", lw=0.7, color=MUTED, mutation_scale=4)); ax.text((x0 + x1) / 2, y + 0.5, label, ha="center", va="center", fontsize=8, color=MUTED)
for x0, x1, off, label, vert in plan.get("dims", []): dim(x0, x1, off, label, vertical=vert)
ax.annotate("N", (L + 4, W - 2), (L + 4, W - 6), ha="center", fontsize=10, color=INK, arrowprops=dict(arrowstyle="-|>", color=INK, lw=1))
ax.set_xlim(-5, L + 7); ax.set_ylim(-PD - 5, W + 5); ax.set_aspect("equal"); ax.axis("off")
ax.set_title(plan.get("title") or f"{src.stem.replace('-plan', '')}: floor plan, {P['eave_ft']:.0f} ft walls, {L:.0f} x {W:.0f} ft" + (f" plus {PD:.0f} ft south porch" if PD else ""), loc="left", fontsize=12, color=INK, pad=12)
fig.text(0.01, 0.01, "Massing model, not a construction drawing. Dimensions are to outside faces; doors are 3 ft, interior walls 4.5 in. Green: wet core on one sewer trench. Generated from the IFC parameters.", fontsize=7.5, color=MUTED)
out = src.with_name(src.stem + ".png"); fig.savefig(out, bbox_inches="tight", facecolor=SURFACE); print("wrote", out)
