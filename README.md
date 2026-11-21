# Home Planner

The simplest home planning platform for everyday homeowners — not architects or interior designers.

Help people answer practical questions before they buy furniture or appliances: *Will this fit? Is there enough walking space? Can the door still open?*

## Quick start

```bash
git clone <repository-url>
cd home-planner
pip install -r requirements.txt
streamlit run app.py
```

Open the URL shown in the terminal (default: http://localhost:8501).

## Local AI assistant setup

The optional AI Space Assistant uses Ollama locally. No OpenAI account, API
key, or cloud billing is required.

### Install Ollama on macOS

1. Download and install Ollama from [ollama.com/download](https://ollama.com/download).
2. Open the Ollama application once so its local server starts.
3. In a terminal, download the default model:

	```bash
	ollama pull llama3.2
	```

	If you opened the Ollama application, its server is already running. Only
	run `ollama serve` if this check fails:

	```bash
	curl http://127.0.0.1:11434/api/tags
	```

4. In another terminal, start Home Planner:

	```bash
	streamlit run app.py
	```

The assistant connects to `http://127.0.0.1:11434`. To use another model or
server, set `OLLAMA_MODEL` or `OLLAMA_URL` before starting Streamlit.

## Project structure

```
home-planner/
├── app.py                  # Streamlit entry point
├── requirements.txt
├── docs/                   # Product and feature specs
├── home_planner/           # Application package
│   ├── constants.py        # Shared defaults
│   ├── models.py           # Domain models (Home, Room, Furniture)
│   ├── units.py            # Unit conversion (internal storage: cm)
│   ├── services/           # Business logic
│   ├── rendering/          # Floor plan visualization
│   └── ui/                 # Streamlit UI components
└── tests/
```

## Features (current)

- Create rooms with name, width, length, and height
- Generate a dimension-accurate 2D floor plan
- Add furniture blocks and check whether they fit
- Support display units: cm, m, inch, feet

## Documentation

| Doc | Purpose |
|-----|---------|
| [AGENTS.md](./AGENTS.md) | AI agent onboarding |
| [docs/PROJECT_OVERVIEW.md](./docs/PROJECT_OVERVIEW.md) | Current features, roadmap, user flow, architecture, milestones, and validation |
| [docs/PRODUCT.md](./docs/PRODUCT.md) | Vision, philosophy, target users |
| [docs/FEATURES.md](./docs/FEATURES.md) | Feature breakdown and build order |
| [docs/features/01-dimensions-to-map.md](./docs/features/01-dimensions-to-map.md) | Feature 1 spec |
| [docs/GLOSSARY.md](./docs/GLOSSARY.md) | Shared terminology |

## Build order

```
1. Dimensions → Map          ← current
2. Basic Interior
3. Fit & Clearance Checks
4. Shopping Planner
5. AI Space Assistant
6. Room Organization
```

## Testing

```bash
python -m unittest discover -s tests -v
```

## Core principle

**Simple over professional.** Every feature reduces complexity instead of adding it. Dimensions matter; aesthetics do not.
