# Feature 1: Dimensions → Map

Turn basic room measurements into a simple, dimension-accurate digital layout.

**Status:** Current focus — build this first.  
**Depends on:** Nothing (foundation feature)

---

## Goal

A homeowner enters room dimensions, doors, and windows. The platform generates a simple digital map they can view in 2D and 3D — accurate to the centimeter, editable, and completable in under 10 minutes.

---

## User stories

### Must have (MVP)

| ID | As a… | I want to… | So that… |
|----|-------|------------|----------|
| F1-01 | homeowner | enter a room's width, length, and height | I have an accurate starting shell |
| F1-02 | homeowner | see a 2D top-down floor plan | I can understand the layout at a glance |
| F1-03 | homeowner | see dimension labels on walls | I trust the map matches my measurements |
| F1-04 | homeowner | edit a wall length and see the plan update | I can fix mistakes without starting over |
| F1-05 | homeowner | add a door to a wall with width and swing | I know where passages are |
| F1-06 | homeowner | add a window to a wall with width and height | openings are represented accurately |
| F1-07 | homeowner | name a room (e.g. "Living Room") | I can identify spaces in a multi-room home |
| F1-08 | homeowner | add multiple rooms | I can map my whole home |
| F1-09 | homeowner | switch between 2D and 3D views | I can visualize height and openings |
| F1-10 | homeowner | pan and zoom the canvas | I can navigate larger layouts |

### Should have (v1.1)

| ID | As a… | I want to… | So that… |
|----|-------|------------|----------|
| F1-11 | homeowner | connect adjacent rooms | my layout reflects real floor plan topology |
| F1-12 | homeowner | choose cm or inches | I can use familiar units |
| F1-13 | homeowner | upload a floor plan image to trace over | I don't have to measure everything from scratch |

### Won't have (this feature)

- Furniture or objects (Feature 2)
- Fit/clearance checks (Feature 3)
- Textures, colors, materials
- Photorealistic rendering
- Professional CAD export
- AI recommendations (Feature 5)

---

## User flow

```
1. Create home
   └─> Name (optional)

2. Add first room
   └─> Enter: name, width, length, height
   └─> See: rectangle on 2D plan + 3D shell

3. Edit dimensions
   └─> Click wall or dimension label
   └─> Type new value
   └─> Plan updates live

4. Add openings
   └─> Select wall
   └─> Place door: width, swing direction (left/right, inward/outward)
   └─> Place window: width, sill height, height

5. Add more rooms
   └─> Repeat steps 2–4
   └─> Position relative to existing rooms (v1.1: shared walls)

6. Review
   └─> Switch 2D ↔ 3D
   └─> Pan / zoom
   └─> Confirm all dimensions look correct
```

---

## Data model

### Home

```typescript
interface Home {
  id: string
  name: string
  units: 'cm' | 'in'
  rooms: Room[]
  createdAt: string
  updatedAt: string
}
```

### Room

A room is a rectangular space. Complex shapes (L-shaped rooms) are out of scope for MVP — use multiple rectangular rooms instead.

```typescript
interface Room {
  id: string
  name: string           // e.g. "Living Room", "Kitchen"
  width: number          // X axis (cm)
  length: number         // Y axis (cm)
  height: number         // Z axis (cm)
  position: { x: number; y: number }  // origin on floor plan
  rotation: number       // degrees, default 0
  walls: Wall[]
  openings: Opening[]
}
```

### Wall

For MVP, walls are derived from room dimensions (4 walls per rectangle). Explicit wall editing comes in v1.1.

```typescript
interface Wall {
  id: string
  roomId: string
  start: { x: number; y: number }
  end: { x: number; y: number }
  // length derived from start/end
}
```

### Opening (door or window)

```typescript
type OpeningType = 'door' | 'window'

interface Opening {
  id: string
  roomId: string
  wallId: string
  type: OpeningType
  offset: number         // distance from wall start (cm)
  width: number
  height: number         // windows only; doors use room height or standard
  sillHeight?: number    // windows only — distance from floor
  swing?: 'left-in' | 'left-out' | 'right-in' | 'right-out'  // doors only
}
```

---

## Views

### 2D floor plan (primary editing view)

- Top-down orthographic view
- Room outline as rectangle with labeled dimensions
- Doors shown as gap + swing arc
- Windows shown as gap on wall
- Grid optional (10 cm or 1 ft intervals)
- Click wall → edit length
- Click opening → edit width/position

### 3D shell view (visualization)

- Extruded walls from floor plan
- Floor and ceiling planes
- Door openings as cutouts; windows as transparent cutouts
- Orbit camera (rotate, pan, zoom)
- Dimension labels on hover or toggle
- No furniture, textures, or lighting effects beyond basic shading

---

## UI components (MVP)

| Component | Purpose |
|-----------|---------|
| Room form | Name + W × L × H inputs |
| Floor plan canvas | 2D interactive plan |
| 3D viewport | Simple shell renderer |
| View toggle | Switch 2D / 3D |
| Dimension label | Inline editable measurement |
| Opening tool | Add/edit door or window on selected wall |
| Room list | Sidebar of all rooms; click to focus |
| Toolbar | Add room, add opening, pan, zoom |

---

## MVP slices (build in order)

| Step | Deliverable | Validates |
|------|-------------|-----------|
| **1.1** | Single room from W × L × H → rectangle on 2D canvas | F1-01, F1-02, F1-03 |
| **1.2** | Click-to-edit dimensions; labels update live | F1-04 |
| **1.3** | Add door on wall (width + swing) | F1-05 |
| **1.4** | Add window on wall (width + sill + height) | F1-06 |
| **1.5** | Multiple named rooms in sidebar | F1-07, F1-08 |
| **1.6** | Basic 3D extruded shell + 2D/3D toggle | F1-09 |
| **1.7** | Pan, zoom, fit-to-view | F1-10 |

---

## Acceptance criteria

Feature 1 is done when:

- [ ] User can create a room by entering width, length, height
- [ ] 2D plan shows room with dimension labels on every wall
- [ ] Editing a dimension updates the plan immediately
- [ ] User can add at least one door and one window per room
- [ ] User can create 3+ named rooms
- [ ] 3D view shows extruded walls with door/window cutouts
- [ ] User can switch between 2D and 3D
- [ ] User can pan and zoom in both views
- [ ] All measurements display in chosen units (cm default)
- [ ] No furniture, textures, or fit-check logic present

---

## Design constraints

1. **Rectangular rooms only** in MVP — L-shaped rooms = multiple connected rectangles (v1.1)
2. **Centimeters default** — inch support in v1.1
3. **No freehand drawing** — all input is numeric
4. **Labels always visible** in 2D; toggle in 3D
5. **Minimal visual styling** — light walls, clear lines, readable type
6. **Fast** — room creation to visible plan in under 3 seconds

---

## Technical notes (non-binding)

Suggested stack for implementation (decide when building):

- **Web app:** React + TypeScript
- **2D canvas:** SVG or Canvas API
- **3D:** Three.js with extruded shapes from floor plan data
- **State:** Room data as JSON; local storage for MVP persistence
- **No backend required** for MVP slices 1.1–1.7

---

## Open questions

- [ ] How should adjacent rooms share walls in v1.1?
- [ ] Floor plan upload: trace mode vs auto-detect?
- [ ] Default door width (80 cm?) and window sill height (90 cm?) by region?
- [ ] Mobile support in MVP or desktop-first?

Record decisions here as they are made.
