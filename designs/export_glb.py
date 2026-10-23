import bpy, sys
out = sys.argv[sys.argv.index("--") + 1]
COL = {"IfcWall": (0.90, 0.88, 0.82), "IfcSlab": (0.62, 0.61, 0.58), "IfcRoof": (0.95, 0.95, 0.94), "IfcColumn": (0.90, 0.88, 0.82), "IfcCovering": (0.97, 0.96, 0.93), "Timber": (0.43, 0.29, 0.17)}
for o in list(bpy.data.objects):
    if o.type != 'MESH' or "IfcOpeningElement" in o.name:
        o.hide_set(True); o.hide_render = True
        continue
    cls = "Timber" if "Timber" in o.name else next((k for k in COL if o.name.startswith(k)), None)
    if cls is None:
        print("skip", o.name); o.hide_render = True; continue
    mat = bpy.data.materials.get(cls) or bpy.data.materials.new(cls)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*COL[cls], 1.0); bsdf.inputs["Roughness"].default_value = 0.85
    o.data.materials.clear(); o.data.materials.append(mat)
    o.select_set(True)
print([o.name for o in bpy.data.objects if o.select_get()])
bpy.ops.export_scene.gltf(filepath=out, export_format='GLB', use_selection=True, export_apply=True, export_yup=True)
print("exported", out)
