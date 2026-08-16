# Features

Six features, built in order. Each depends on the ones before it.

---

## Feature 1: Dimensions → Map

**Status:** Current focus

Turn basic measurements into a simple, dimension-accurate digital layout.

**Inputs:** room W × L × H, doors, windows  
**Outputs:** 2D floor plan, simple 3D shell, dimension labels  
**Spec:** [features/01-dimensions-to-map.md](./features/01-dimensions-to-map.md)

---

## Feature 2: Basic Interior

Add simple rectangular furniture blocks to the map.

**Inputs:** W × D × H per object, or preset sizes  
**Outputs:** draggable blocks, dimension labels, room overview  
**Depends on:** Feature 1

### Capabilities

- Create object from dimensions (no furniture library required)
- Preset sizes (e.g. 3-seat sofa: 180 / 210 / 240 cm)
- Drag, rotate, duplicate, delete
- Combine rectangles for L-shapes
- No textures, colors, or detailed models

---

## Feature 3: Fit & Clearance Checks

Answer "does it fit?" and "can I still move around?"

**Depends on:** Features 1, 2

### Checks

- Object fits within room bounds
- Remaining clearance (e.g. "only 5 cm left")
- Door / cabinet swing clearance
- Walkway width vs recommended minimum
- Overlap detection between objects

### Outputs

- Pass / warn / fail per check
- Short explanation for each issue

### Recommended clearances (examples)

- Walking space beside a bed
- Clearance to open a refrigerator
- Space behind dining chairs
- Clearance for wardrobe doors
- Kitchen working aisle width

---

## Feature 4: Shopping Planner

Test products before buying.

**Depends on:** Features 1–3

### Flow

1. Enter product dimensions (or pick preset)
2. See whether and where it fits
3. See remaining space and circulation impact
4. Save candidate items

### Answers

- Will this fit?
- Where can it go?
- How much space is left?
- Does it block doors or walkways?

---

## Feature 5: AI Space Assistant

Practical layout suggestions, not interior design.

**Depends on:** Features 1–3 (rules engine); enhanced with Feature 4 data

### Capabilities

- Recommend circulation paths (regional standards)
- Suggest layouts by household size and needs
- Flag blocked movement, wasted space, crowded rooms
- Propose rearrangements
- Explain reasoning behind every recommendation

### Examples

- Improve walking paths
- Increase storage efficiency
- Rearrange for better space utilization
- Identify wasted space
- Detect furniture blocking movement

---

## Feature 6: Room Organization

Manage multi-room homes.

**Depends on:** Feature 1; grows with Features 2–5

### Capabilities

- Organize by room / zone (Living Room, Kitchen, Master Bedroom, etc.)
- Switch between rooms
- Whole-home overview
- Per-room fit status and warnings

---

## Build order summary

```
1. Dimensions → Map
2. Basic Interior
3. Fit & Clearance Checks
4. Shopping Planner
5. AI Space Assistant
6. Room Organization
```
