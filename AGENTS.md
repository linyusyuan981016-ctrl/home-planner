# Agent onboarding

Read this before making changes to the Home Planner codebase.

## What this project is

A dimension-first home planning tool for everyday homeowners. The current MVP (Feature 1) turns room measurements into a 2D floor plan and supports basic furniture placement with fit checks.

## Where to look

| Area | Location |
|------|----------|
| Streamlit entry | `app.py` |
| UI components | `home_planner/ui/` |
| Domain models | `home_planner/models.py` |
| Business logic | `home_planner/services/` |
| Floor plan rendering | `home_planner/rendering/` |
| Unit conversion | `home_planner/units.py` (internal storage is always cm) |
| Tests | `tests/` |
| Product docs | `docs/` |

## Conventions

- Keep UI code in `home_planner/ui/`; keep logic in `services/`.
- Store all dimensions in **centimeters** internally; convert only at UI boundaries.
- Prefer small, focused modules over monolithic scripts.
- Do not add commented-out code or duplicate entry points.
- Match existing naming and module layout when extending features.

## Running locally

```bash
pip install -r requirements.txt
streamlit run app.py
python -m unittest discover -s tests -v
```

## Feature roadmap

See [docs/FEATURES.md](./docs/FEATURES.md). Feature 1 is the current focus.
