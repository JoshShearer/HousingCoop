"""Render an isometric massing view of a Bonsai .blend from the southwest.

    ~/.local/bin/blender -b designs/barndominium/barndominium-v6.blend --python designs/render_massing.py -- designs/barndominium/exports/barndominium-v6-massing.png

Workbench render, flat white studio light, so it runs in seconds without a GPU.
"""
import sys, math, pathlib
import bpy
from mathutils import Vector

out = pathlib.Path(sys.argv[sys.argv.index("--") + 1]).resolve()
scene = bpy.context.scene
meshes = [o for o in scene.objects if o.type == "MESH" and not o.hide_render]
lo = Vector((min(v.x for o in meshes for v in [o.matrix_world @ Vector(c) for c in o.bound_box]),
             min(v.y for o in meshes for v in [o.matrix_world @ Vector(c) for c in o.bound_box]),
             min(v.z for o in meshes for v in [o.matrix_world @ Vector(c) for c in o.bound_box])))
hi = Vector((max(v.x for o in meshes for v in [o.matrix_world @ Vector(c) for c in o.bound_box]),
             max(v.y for o in meshes for v in [o.matrix_world @ Vector(c) for c in o.bound_box]),
             max(v.z for o in meshes for v in [o.matrix_world @ Vector(c) for c in o.bound_box])))
centre, size = (lo + hi) / 2, (hi - lo).length

cam_data = bpy.data.cameras.new("MassingCam"); cam_data.type = "ORTHO"; cam_data.ortho_scale = size * 1.15
cam = bpy.data.objects.new("MassingCam", cam_data); scene.collection.objects.link(cam)
direction = Vector((-1.0, -1.0, 0.75)).normalized()        # from the southwest, looking down
cam.location = centre + direction * size * 3
cam.rotation_euler = (-direction).to_track_quat("-Z", "Y").to_euler()
scene.camera = cam

sun = bpy.data.objects.new("Sun", bpy.data.lights.new("Sun", "SUN")); scene.collection.objects.link(sun)
sun.rotation_euler = (math.radians(50), 0, math.radians(-30))

scene.render.engine = "BLENDER_WORKBENCH"
sh = scene.display.shading
sh.light = "STUDIO"; sh.color_type = "SINGLE"; sh.single_color = (0.82, 0.80, 0.76); sh.show_shadows = True; sh.show_cavity = True
sh.background_type = "VIEWPORT"; sh.background_color = (0.97, 0.97, 0.96)
scene.display.render_aa = "8"
scene.view_settings.view_transform = "Standard"; scene.view_settings.look = "None"
scene.render.resolution_x, scene.render.resolution_y = 1800, 1200
scene.render.film_transparent = False
scene.world = scene.world or bpy.data.worlds.new("World")
scene.world.color = (0.97, 0.97, 0.96)
scene.render.filepath = str(out); scene.render.image_settings.file_format = "PNG"
bpy.ops.render.render(write_still=True); print("wrote", out)
