# Glossary

Shared terms used across the project.

| Term | Definition |
|------|------------|
| **Bare shell** | Empty house with walls, doors, and windows only — no furniture |
| **Block** | A simple rectangular 3D object defined by width, depth, height |
| **Clearance** | Empty space required around an object for use or movement |
| **Circulation** | Paths people walk through a home; "walking space" in user-facing copy |
| **Dimension-first** | Design principle: accurate measurements matter more than appearance |
| **Door opening** | A gap in a wall with width and swing direction |
| **Floor plan** | Top-down 2D view of room layout |
| **Map** | The digital layout generated from user measurements |
| **Opening** | Generic term for doors and windows placed on walls |
| **Preset** | A common furniture size users can select instead of entering dimensions manually |
| **Room** | A named space with width, length, height, and optional doors/windows |
| **Shell** | The 3D extrusion of walls, floor, and ceiling — no furniture |
| **Wall** | A segment between two points with a defined length |

## User-facing vs internal

| User-facing | Internal / code |
|-------------|-----------------|
| walking space | circulation path |
| does it fit? | spatial constraint check |
| room size | room dimensions (W × L × H) |
| door | door opening with swing |

Prefer user-facing language in UI; use internal terms in code comments and docs when precision helps.
