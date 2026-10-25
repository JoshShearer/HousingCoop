# Designs

Blender and IFC models of the Friendstead buildings, authored with Bonsai (the BIM add-on) in Blender 4.5 LTS. One folder per building.

## Layout

```
designs/
  README.md
  <building>/
    BRIEF.md                 what the building has to do, from the analysis
    make_<building>.py       parametric starter that generates the first IFC and .blend
    <building>-vNN.ifc       the model; the IFC is the source of truth
    <building>-vNN.blend     Bonsai working file for the same version
    exports/                 renders, drawings, PDFs for the vault and the doc
```

## Conventions

- **IFC first.** Bonsai stores the building in the `.ifc`; the `.blend` is the editing session. Save both together and keep the same version suffix.
- **Versions, not overwrites.** `v0` is the generated massing. Bump the number when a design decision changes the model; note the decision in `notes/2026-10-22-decisions.md` or the vault decision log.
- **Units.** Models are in metres (IFC default); the generator scripts take feet. Bonsai's unit display can be switched to imperial in Project Setup.
- **Parameters travel with the file.** Each generator writes a `Friendstead_Parameters` property set on the IfcBuilding so the numbers can be read back from the model.
- **Large files.** `.blend` and `.ifc` files are binary-ish and can get large; if this folder is ever put under git, use git LFS for them.
- **Rendering.** Put images in `exports/` and reference them from the vault note for that building.

## Running a generator

```
~/.local/bin/blender -b --python designs/barndominium/make_barndominium.py            # writes barndominium-v6.ifc, .blend and exports/barndominium-v6-plan.json
~/.local/bin/blender -b --python designs/barndominium/make_barndominium.py -- barndominium-v6
uv run --with matplotlib python -I designs/draw_plan.py designs/barndominium/exports/barndominium-v6-plan.json   # dimensioned 2D plan PNG
uv run --with matplotlib python -I designs/draw_plan.py designs/barndominium/exports/barndominium-v6-plan-upper.json   # second-floor plan
~/.local/bin/blender -b designs/barndominium/barndominium-v6.blend --python designs/render_massing.py -- designs/barndominium/exports/barndominium-v6-massing.png   # isometric massing render
~/.local/bin/blender -b designs/barndominium/barndominium-v6.blend --python designs/export_glb.py -- /tmp/barndominium-v6.glb   # coloured GLB for the web
python3 designs/make_walkthrough.py designs/barndominium/exports/barndominium-v6-plan.json /tmp/barndominium-v6.glb          # first-person walkthrough page
```

Open the result with `~/.local/bin/blender designs/barndominium/barndominium-v6.blend`, or File > Open IFC Project in Bonsai.

## Buildings

| Building | Status | Note |
|---|---|---|
| [Barndominium](barndominium/BRIEF.md) | v6 shell | 56 x 40 ft, 20 ft eave, two-storey house block with a member-built wood floor, 24 ft shop bay with two 12 x 12 insulated doors, foam, temporary rooms, no porch; about 3,500 sq ft; v5 (70 x 40 finished single storey with porch and vault) kept as the alternative |
