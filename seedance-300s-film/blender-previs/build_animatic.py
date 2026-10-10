# Blender 4.2+ scene-blockout generator for The Vanishing Panda.
# Run: blender -b -t 4 --python build_animatic.py
# Produces one .blend containing ten 30-second scenes. This is a rough 3D previs,
# not final character animation or a finished feature-quality render.

import bpy, math, os
from mathutils import Vector
from math import sin, cos, pi

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "output")
os.makedirs(OUT, exist_ok=True)
FPS = 24
DURATION = 30
FRAMES = FPS * DURATION
RES_X, RES_Y = 640, 360

def mat(name, color, rough=0.7, metallic=0.0, emission=0.0):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.use_nodes = True
    bs = m.node_tree.nodes.get("Principled BSDF")
    if bs:
        bs.inputs["Base Color"].default_value = (*color, 1)
        bs.inputs["Roughness"].default_value = rough
        bs.inputs["Metallic"].default_value = metallic
        if emission:
            bs.inputs["Emission Color"].default_value = (*color, 1)
            bs.inputs["Emission Strength"].default_value = emission
    return m

M = {
    "forest": mat("Forest floor", (0.055,0.16,0.075)),
    "bamboo": mat("Bamboo green", (0.12,0.34,0.12)),
    "leaf": mat("Leaf green", (0.18,0.43,0.10)),
    "rock": mat("Slate rock", (0.19,0.22,0.23)),
    "water": mat("River blue", (0.025,0.24,0.34), rough=0.18, metallic=0.1),
    "gray": mat("Child gray outfit", (0.31,0.34,0.37)),
    "skin": mat("Warm skin", (0.78,0.48,0.31)),
    "black": mat("Panda black", (0.025,0.028,0.035)),
    "white": mat("Panda white", (0.91,0.89,0.81)),
    "eye": mat("Eye gloss", (0.01,0.01,0.01), rough=0.12),
    "red": mat("Helicopter red", (0.52,0.09,0.06), metallic=0.25),
    "metal": mat("Rotor metal", (0.18,0.20,0.22), metallic=0.6),
    "gold": mat("Magic seed glow", (1.0,0.45,0.045), emission=2.0),
    "foam": mat("Comic foam burst", (0.95,0.74,0.12), emission=0.25),
    "rope": mat("Rope", (0.32,0.18,0.07)),
}

def smooth(obj):
    if obj.type == "MESH":
        for p in obj.data.polygons: p.use_smooth = True
    return obj

def assign(obj, material):
    if material: obj.data.materials.append(material)
    return obj

def uv(name, loc, scale, material, seg=16, rings=10):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=rings, location=loc)
    o=bpy.context.object; o.name=name; o.scale=scale
    assign(o, material); smooth(o)
    return o

def cube(name, loc, scale, material, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o=bpy.context.object; o.name=name; o.dimensions=scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    assign(o, material)
    if bevel:
        mod=o.modifiers.new("Soft bevel", "BEVEL"); mod.width=bevel; mod.segments=2
    return o

def cyl(name, loc, radius, depth, material, vertices=12, rot=None):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc)
    o=bpy.context.object; o.name=name
    if rot: o.rotation_euler=rot
    assign(o, material); smooth(o)
    return o

def cone(name, loc, radius1, radius2, depth, material, rot=None):
    bpy.ops.mesh.primitive_cone_add(vertices=12, radius1=radius1, radius2=radius2, depth=depth, location=loc)
    o=bpy.context.object; o.name=name
    if rot: o.rotation_euler=rot
    assign(o, material); smooth(o)
    return o

def key_loc(obj, frame, loc):
    obj.location=loc; obj.keyframe_insert(data_path="location", frame=frame)

def key_rot(obj, frame, rot):
    obj.rotation_euler=rot; obj.keyframe_insert(data_path="rotation_euler", frame=frame)

def set_linear(obj):
    if obj.animation_data and obj.animation_data.action:
        for fc in obj.animation_data.action.fcurves:
            for kp in fc.keyframe_points:
                kp.interpolation="BEZIER"
                kp.handle_left_type="AUTO_CLAMPED"; kp.handle_right_type="AUTO_CLAMPED"

def track(obj, target):
    obj.rotation_euler=(Vector(target)-obj.location).to_track_quat("-Z","Y").to_euler()

def look_at_key(cam, frame, loc, target):
    cam.location=loc; track(cam,target)
    cam.keyframe_insert(data_path="location",frame=frame)
    cam.keyframe_insert(data_path="rotation_euler",frame=frame)

def make_camera(scene, name):
    data=bpy.data.cameras.new(name+" Lens")
    cam=bpy.data.objects.new(name,data); scene.collection.objects.link(cam)
    data.lens=42; data.dof.use_dof=False
    scene.camera=cam
    return cam

def create_child(prefix):
    # Proxy only. Replace with rigged reference-matched model in final production.
    root=bpy.data.objects.new(prefix+" Child root",None); bpy.context.scene.collection.objects.link(root)
    parts=[]
    parts.append(uv(prefix+" torso", (0,0,0.85),(0.34,0.27,0.43),M["gray"]))
    parts.append(uv(prefix+" head",(0.06,0,1.48),(0.38,0.34,0.36),M["skin"]))
    parts.append(uv(prefix+" hair",(0.03,0.02,1.73),(0.34,0.32,0.17),M["black"]))
    # Eyes face +Y, front camera approaches from y=-? Scene uses camera at negative Y,
    # so eyes are placed on the -Y side.
    parts.append(uv(prefix+" eye L",(-0.08,-0.31,1.51),(0.045,0.025,0.06),M["eye"],12,8))
    parts.append(uv(prefix+" eye R",(0.19,-0.31,1.51),(0.045,0.025,0.06),M["eye"],12,8))
    parts.append(uv(prefix+" arm L",(-0.31,-0.01,0.94),(0.13,0.14,0.29),M["gray"]))
    parts.append(uv(prefix+" arm R",(0.31,-0.01,0.94),(0.13,0.14,0.29),M["gray"]))
    parts.append(uv(prefix+" leg L",(-0.19,0.0,0.42),(0.15,0.17,0.27),M["gray"]))
    parts.append(uv(prefix+" leg R",(0.19,0.0,0.42),(0.15,0.17,0.27),M["gray"]))
    for o in parts:
        o.parent=root; o.matrix_parent_inverse=root.matrix_world.inverted()
    return root,parts

def create_panda(prefix):
    root=bpy.data.objects.new(prefix+" Panda root",None); bpy.context.scene.collection.objects.link(root)
    parts=[]
    parts.append(uv(prefix+" panda body",(0,0,0.78),(0.48,0.38,0.55),M["white"]))
    parts.append(uv(prefix+" panda head",(0.03,-0.02,1.47),(0.46,0.40,0.40),M["white"]))
    parts.append(uv(prefix+" ear L",(-0.31,0.0,1.79),(0.14,0.13,0.16),M["black"]))
    parts.append(uv(prefix+" ear R",(0.36,0.0,1.79),(0.14,0.13,0.16),M["black"]))
    parts.append(uv(prefix+" eye patch L",(-0.12,-0.365,1.51),(0.12,0.045,0.15),M["black"]))
    parts.append(uv(prefix+" eye patch R",(0.18,-0.365,1.51),(0.12,0.045,0.15),M["black"]))
    parts.append(uv(prefix+" eye L",(-0.12,-0.408,1.52),(0.035,0.02,0.04),M["eye"],12,8))
    parts.append(uv(prefix+" eye R",(0.18,-0.408,1.52),(0.035,0.02,0.04),M["eye"],12,8))
    for x in [-0.29,0.29]:
        parts.append(uv(prefix+" leg",(x,0.0,0.34),(0.18,0.2,0.28),M["black"]))
    parts.append(uv(prefix+" arm L",(-0.42,-0.01,0.91),(0.16,0.19,0.35),M["black"]))
    parts.append(uv(prefix+" arm R",(0.42,-0.01,0.91),(0.16,0.19,0.35),M["black"]))
    # Ice-cream cone as a prop parented to the panda root.
    prop=cone(prefix+" ice cream cone",(0.42,-0.28,1.28),0.10,0.035,0.28,M["gold"],rot=(pi,0,0))
    prop.parent=root; prop.matrix_parent_inverse=root.matrix_world.inverted(); parts.append(prop)
    for o in parts:
        if o.parent is None:
            o.parent=root; o.matrix_parent_inverse=root.matrix_world.inverted()
    return root,parts

def create_helicopter(prefix):
    root=bpy.data.objects.new(prefix+" Helicopter root",None); bpy.context.scene.collection.objects.link(root)
    body=uv(prefix+" fuselage",(0,0,0),(1.05,0.48,0.43),M["red"])
    nose=uv(prefix+" cockpit",(0.68,-0.03,-0.02),(0.42,0.42,0.32),M["water"])
    tail=cyl(prefix+" tail boom",(-1.15,0,0.10),0.11,1.7,M["red"],12,rot=(0,pi/2,0))
    mast=cyl(prefix+" rotor mast",(0,0,0.48),0.07,0.35,M["metal"])
    blade1=cube(prefix+" rotor blade 1",(0,0,0.70),(2.9,0.12,0.045),M["metal"])
    blade2=cube(prefix+" rotor blade 2",(0,0,0.71),(0.12,2.9,0.045),M["metal"])
    parts=[body,nose,tail,mast,blade1,blade2]
    for o in parts: o.parent=root; o.matrix_parent_inverse=root.matrix_world.inverted()
    return root,parts

def make_environment(scene, part):
    # Compact stage with route landmarks; same forest language across all clips.
    ground=cube(f"P{part:02d} Forest ground",(0,0,-0.45),(28,28,0.8),M["forest"])
    ground.name=f"P{part:02d} Forest ground"
    # River / ravine on right side for finale, stream in early parts.
    river=cube(f"P{part:02d} River",(7,1,-0.02),(5,25,0.16),M["water"])
    river.rotation_euler[2]=0.04
    # Bamboo stands at both sides, avoiding central action corridor.
    for i in range(34):
        x=((i*7)%17)-8.5
        y=((i*11)%22)-11
        if abs(x)<2.4 and abs(y)<3.0: x += 4.0 if x>=0 else -4.0
        h=3.5+((i*13)%10)*0.22
        stem=cyl(f"P{part:02d} Bamboo {i:02d}",(x,y,h/2-0.1),0.07,h,M["bamboo"],8)
        for z in [0.32,0.65]:
            cyl(f"P{part:02d} Bamboo node {i:02d}",(x,y,h*z),0.085,0.06,M["leaf"],8)
        uv(f"P{part:02d} Canopy {i:02d}",(x,y,h),(0.42,0.30,0.28),M["leaf"],12,8)
    # Rocks on the route and cliff shelf.
    for i in range(18):
        x=((i*5)%15)-7
        y=((i*9)%20)-10
        rock=uv(f"P{part:02d} Rock {i:02d}",(x,y,0.02),(0.45+(i%3)*0.18,0.42,0.25+(i%2)*0.15),M["rock"],12,8)
        rock.rotation_euler=(0.1*i,0.17*i,0.21*i)
    # Glowing seed pods, a repeatable magical set-piece.
    for i in range(12):
        x=-5.8+(i%4)*0.7; y=1.0+(i//4)*1.0; z=2.4+(i%3)*0.35
        uv(f"P{part:02d} Seed pod {i:02d}",(x,y,z),(0.19,0.18,0.27),M["gold"],12,8)
    # Distant ridge silhouette.
    for i in range(7):
        cone(f"P{part:02d} Ridge {i}",(10+i*1.3,8+i*0.3,1.1),1.5,0.2,2.4,M["rock"])
    # Lighting.
    ld=bpy.data.lights.new(f"P{part:02d} Sun","SUN"); lo=bpy.data.objects.new(f"P{part:02d} Sun",ld); scene.collection.objects.link(lo)
    lo.rotation_euler=(math.radians(28),math.radians(-22),math.radians(-30)); ld.energy=2.0
    area_data=bpy.data.lights.new(f"P{part:02d} Fill","AREA"); area=bpy.data.objects.new(f"P{part:02d} Fill",area_data); scene.collection.objects.link(area)
    area.location=(0,-8,10); area_data.energy=1500; area_data.shape="DISK"; area_data.size=8
    scene.world.color=(0.07,0.07,0.07)
    return ground

def add_action_props(part):
    # Nonlethal visual language: toy-like prop and magical bursts, never realistic weapons.
    for i in range(6):
        burst=uv(f"P{part:02d} Magic burst {i}",(-4.0+i*1.45,2.5,0.8),(0.12,0.12,0.12),M["foam"],10,6)
        burst.scale=(0.001,0.001,0.001)
        for f,s in [(150+i*12,0.001),(156+i*12,1.0),(168+i*12,0.001)]:
            burst.scale=(s,s,s); burst.keyframe_insert(data_path="scale",frame=f)

def setup_scene(scene, part):
    scene.frame_start=1; scene.frame_end=FRAMES; scene.render.fps=FPS
    scene.render.resolution_x=RES_X; scene.render.resolution_y=RES_Y; scene.render.resolution_percentage=100
    scene.render.engine="CYCLES" if False else "BLENDER_EEVEE_NEXT"
    scene.render.image_settings.file_format="FFMPEG"; scene.render.ffmpeg.format="MPEG4"; scene.render.ffmpeg.codec="H264"
    scene.view_settings.view_transform="Standard"
    scene.render.film_transparent=False
    make_environment(scene,part)
    child,cp=create_child(f"P{part:02d}")
    panda,pp=create_panda(f"P{part:02d}")
    heli,hp=create_helicopter(f"P{part:02d}")
    cam=make_camera(scene,f"P{part:02d} Camera")
    cam.data.lens=42
    # Part-specific stage marks. The action is deliberately a previs/blockout.
    child_path=[
      (-1.6,-5,0),( -1.2,-3.2,0),(-0.5,-1.0,0),(1.2,0.4,0),(2.2,1.5,0),
      (1.2,3.2,0),(0.0,4.5,0),(2.4,5.4,0),(4.4,6.2,0),(5.4,7.0,0)
    ]
    panda_path=[
      (1.4,-3.2,0),(2.3,-1.8,0),(3.2,0.2,0),(1.8,1.6,0),(3.8,2.7,0),
      (4.8,4.0,0),(3.4,5.0,0),(5.8,5.8,0),(7.0,6.8,0),(7.3,7.6,0)
    ]
    if part==1:
        heli_path=[(-4,-4,5),(-2,-2,4.7),(0,0,4.4),(1,0,3.8),(1,0,3.4),(1,0,3.4),(1,0,3.4),(1,0,3.4),(1,0,3.4),(1,0,3.4)]
    else:
        heli_path=[(-8,-8,9)]*10
    if part==9:
        panda_path=[(4.8,7.0,0),(5.1,7.1,0),(5.3,7.2,0),(5.5,7.3,0),(5.7,7.4,0),(5.9,7.5,0),(6.1,7.6,0),(6.3,7.7,0),(6.5,7.8,0),(6.6,7.9,0)]
    if part==10:
        panda_path=[(9,12,-4)]*10
        child_path=[(5.8,7.1,0)]*10
    for idx,sec in enumerate(range(0,31,3)):
        f=1+sec*FPS
        j=min(idx,len(child_path)-1)
        cl=child_path[j]; pl=panda_path[j]; hl=heli_path[j]
        key_loc(child,f,cl); key_loc(panda,f,pl); key_loc(heli,f,hl)
        # Character bounce/lean adds readable rough acting.
        key_rot(child,f,(0.02*sin(sec),0.03*cos(sec),0.08*sin(sec*0.8)))
        key_rot(panda,f,(0.04*cos(sec),0.02*sin(sec),-0.12+0.18*sin(sec*0.7)))
        key_rot(heli,f,(0.02*sin(sec),0.04*cos(sec),0.08*sin(sec)))
        # Camera alternates tracking, wide establishing and emotional close-up.
        if part==10:
            camloc=(5.8,-1.8,2.2); target=(5.8,7.1,1.25)
            if sec>=24: cam.data.lens=78
        elif sec<6:
            camloc=(0,-10,6); target=(0,0,0.8)
        elif sec<15:
            camloc=(3,-7,4.2); target=(2,1.5,0.8)
        elif sec<24:
            camloc=(4.8,-4.5,3.2); target=(3.8,4.0,0.9)
        else:
            camloc=(6,-2.5,2.8); target=(5,6,1.0)
        look_at_key(cam,f,camloc,target)
    for o in [child,panda,heli,cam]: set_linear(o)
    add_action_props(part)
    scene.camera=cam
    scene.render.filepath=os.path.join(OUT,f"clip_{part:02d}_")
    scene["clip_number"]=part
    scene["clip_duration_seconds"]=30
    scene["production_stage"]="rough previs / proxy animation"
    scene["handoff_note"]="For Seedance continuity, use actual rendered final frame as next clip start frame."
    # Timeline markers at every five-second shot boundary.
    for s in range(0,30,5):
        scene.timeline_markers.new(f"SHOT_{s//5+1:02d}_{s:02d}s",frame=1+s*FPS)

def clean_project():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for datablocks in (bpy.data.meshes,bpy.data.curves,bpy.data.cameras,bpy.data.lights):
        for block in list(datablocks):
            if block.users==0: datablocks.remove(block)

def main():
    clean_project()
    # Keep the default scene as clip 01, create nine additional scenes.
    scenes=[]
    scene=bpy.context.scene
    scene.name="CLIP_01_Approach"
    with bpy.context.temp_override(scene=scene, view_layer=scene.view_layers[0]):
        setup_scene(scene,1)
    scenes.append(scene)
    labels=[
      "02_Bamboo_Chase","03_Stream_Crossing","04_Rope_Bridge","05_Glowing_Grove",
      "06_Rolling_Stones","07_Ridge_Trail","08_Cliff_Shelf","09_Leap_To_River","10_Furious_End"
    ]
    for part,label in enumerate(labels,start=2):
        sc=bpy.data.scenes.new(f"CLIP_{part:02d}_{label}")
        with bpy.context.temp_override(scene=sc, view_layer=sc.view_layers[0]):
            setup_scene(sc,part)
        scenes.append(sc)
        # Save a Blender project containing all ten independently renderable clips.
    blend_path=os.path.join(OUT,"the_vanishing_panda_previs.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print("SAVED:",blend_path)
    print("SCENES:",len(scenes))
    for sc in scenes: print(sc.name,sc.frame_start,sc.frame_end,sc.render.fps)

if __name__=="__main__":
    main()
