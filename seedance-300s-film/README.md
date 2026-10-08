# Seedance 2.5 — 300 Second Continuous Film

10 videos x 30 seconds = exactly 300 seconds.

## Master Prompt

The complete unified production instructions are in `MASTER_PROMPT.md` and `MASTER_PROMPT.txt`. Both contain the global continuity rules and the full definition of all ten 30-second parts. `MASTER_PROMPT.txt` is the plain-text version for direct copy/paste into a video-generation workflow.

## Reference Assets

`sakhi.Refernce.jpg` = canonical child identity reference.
`panda-reference.png` = canonical panda identity reference.

Character locks are documented in:
- `child-reference/REFERENCE_INFO.md`
- `panda-reference/REFERENCE_INFO.md`

The environment is documented in:
- `environment-references/environment-design.md`

## Generation Order

Generate exactly in order: **01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09 → 10**.

## Real-Frame Continuity

Video 01 starts from the fixed character and environment references. After each video is actually generated, extract its **real final frame** and use that exact frame as the opening reference for the next video. Never invent future start or end frames in advance.

Keep `sakhi.Refernce.jpg` active as the child identity reference and `panda-reference.png` active as the panda identity reference in every generation.

## Final Runtime

**10 × 30 seconds = exactly 300 seconds.**

The goal is one continuous photorealistic cinematic comedy-action film, not ten unrelated clips.
