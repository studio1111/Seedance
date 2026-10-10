# Blender Previs — The Vanishing Panda

This folder generates a **rough 3D previs/blocking pass** for the 300-second film: ten independently renderable Blender scenes, each 30 seconds long, with proxy child/panda/helicopter geometry, forest landmarks, camera keyframes, action paths, and timeline markers every five seconds.

It is an animation-layout foundation, not a finished character animation. The proxy child and panda are simple primitive models; they do not yet match the reference images. Replace them with rigged, reference-matched models before final rendering.

## Build on a computer with Blender 4.x

From this folder, run:

```bash
blender -b -t 4 --python build_animatic.py
```

The project is saved to `output/the_vanishing_panda_previs.blend`.

To render low-resolution proxy clips (480×270, 6 fps, 30 seconds each):

```bash
blender -b -t 2 output/the_vanishing_panda_previs.blend --python render_previews.py
```

The ten preview videos are saved in `output/`.

## Build through GitHub Actions on a phone

1. Open the repository's **Actions** tab.
2. Choose **Blender Cinematic Previs**.
3. Tap **Run workflow** and confirm.
4. When the run finishes successfully, open its run page and download the artifact named `the-vanishing-panda-blender-previs`.
5. The artifact contains the `.blend` project and proxy MP4 clips.

The workflow is manual because rendering all ten scenes takes time and consumes CI resources. It stores artifacts for 30 days.

## Important continuity note

These Blender scenes are previs, not the final Seedance outputs. For the final Seedance workflow, render each clip, export its actual final frame, and use that exact frame as the next clip's first frame. The current Blender proxy does not automatically replace Seedance's real frame handoff.
