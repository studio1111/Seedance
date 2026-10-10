import bpy, os, re

OUT = os.path.dirname(bpy.data.filepath)
os.makedirs(OUT, exist_ok=True)

scenes = sorted(
    [s for s in bpy.data.scenes if re.match(r"CLIP_\d\d_", s.name)],
    key=lambda s: s.name
)
if len(scenes) != 10:
    raise RuntimeError(f"Expected 10 clip scenes, found {len(scenes)}")

for scene in scenes:
    match = re.match(r"CLIP_(\d\d)_", scene.name)
    clip = match.group(1)
    scene.render.engine = "BLENDER_EEVEE_NEXT" if "BLENDER_EEVEE_NEXT" in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items.keys() else "BLENDER_EEVEE"
    scene.render.resolution_x = 480
    scene.render.resolution_y = 270
    scene.render.resolution_percentage = 100
    scene.render.fps = 6
    scene.frame_step = 4
    scene.render.image_settings.file_format = "FFMPEG"
    scene.render.ffmpeg.format = "MPEG4"
    scene.render.ffmpeg.codec = "H264"
    scene.render.filepath = os.path.join(OUT, f"clip_{clip}")
    scene.frame_start = 1
    scene.frame_end = 720
    print(f"RENDERING {scene.name}: 30s at 6 fps, 480x270", flush=True)
    with bpy.context.temp_override(scene=scene, view_layer=scene.view_layers[0]):
        bpy.ops.render.render(animation=True)
    print(f"FINISHED {scene.name}", flush=True)
