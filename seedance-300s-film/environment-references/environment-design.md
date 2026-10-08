# Environment Design Reference

## Purpose

Canonical environment specification for the complete 300-second Seedance 2.5 film.

The story takes place in one coherent, quiet residential neighborhood in Tehran, Iran. All ten 30-second videos are connected locations within this same physical neighborhood.

## Part-by-Part Environment Map

### Video 01 — Main Residential Street
Establish the quiet Tehran residential street, sidewalk, parked cars and residential building fronts. This is the geographic baseline for the film and the opening ice-cream area.

### Video 02 — Side Street
Continue directly from Video 01 into a connected side street. Preserve the same buildings, sidewalk materials, parked-car environment, sunlight and road geometry.

### Video 03 — Vehicle Route, Low Wall and Rooftop Staircase
Continue from the side street into the established parked-car route, low wall and the same residential rooftop staircase. The wall and staircase must belong to the same building system.

### Video 04 — Flat Rooftop
Continue directly from the staircase. Preserve the same rooftop: low parapets, water tanks, ventilation equipment, pipes, concrete surface and connected roof section.

### Video 05 — Street-Level Descent and Narrow Alley
Continue from the rooftop route down to the same street, then into a residential alley that progressively becomes narrower toward the dead end.

### Video 06 — Dead-End Alley
Use the exact alley geometry established in Video 05. Preserve the same walls, ground surface and dead-end wall. The wall section used for the comic collapse must be visibly lightweight and non-load-bearing.

### Video 07 — Same Alley Back to Street
Begin in the same dead-end area and move back through the same alley. Do not redesign the rubble, walls, gates or pavement. The route returns naturally to the established street.

### Video 08 — Open Residential Intersection
Use the same street route at the established open intersection. Preserve parked vehicles, building facades, sunlight and street materials.

### Video 09 — Intersection Toward Home
Remain in the same intersection and transition naturally toward the established home route. Reuse the same parked vehicle and surrounding geometry.

### Video 10 — Home/Building Entrance
End at the same residential entrance connected to Video 09. Preserve the same architectural style, materials, daylight and neighborhood identity.

## Global Environment Lock

Keep the entire film in the same quiet Tehran residential district during one sunny daytime period. Preserve sun direction, shadow direction, weather, architecture, street geometry, vehicle placement, rooftop layout, alley geometry, intersection and home entrance.

Use realistic Iranian residential architecture, asphalt streets, practical sidewalks, masonry or concrete walls, ordinary parked passenger cars, flat rooftops, rooftop utilities and believable building entrances.

Avoid crowds, tourist landmarks, commercial districts, highways, futuristic architecture, rural scenery, heavy traffic, random animals, sudden weather changes, sunset, night, seasonal changes, impossible roads or teleportation.

## Reference Conditioning

Use the canonical character references `sakhi.Refernce.jpg` and `panda-reference.png` together with the actual final frame of the immediately previous generated video whenever a previous video exists.

## Real-Frame Environment Handoff

Video 01 starts from the fixed environment specification. After each video is actually generated, extract its real final frame and use that exact frame as the opening continuity frame for the next video. Never invent future frames. The real previous frame controls immediate spatial continuity; this document controls the stable identity of the neighborhood.

## Final Standard

Every frame must look as though the camera is physically moving through one real, continuous, quiet Tehran residential neighborhood during the same sunny day. Continuity is more important than novelty.
