# RouteCraft

An interactive delivery-route algorithm lab with a Python HTTP API and a canvas visualisation.

## Run locally

Requires Python 3.12 or newer. No third-party packages or API keys.

```bash
python server.py
python -m unittest discover -v
```

Then open **http://127.0.0.1:8000**. Load the demo or click the map to add points. The first point is the depot. Optimise to display a closed route and the distance reduction.

## Design

Nearest neighbour builds a deterministic starting tour. 2-opt removes crossing or inefficient edge pairs by reversing route segments when the swap reduces Euclidean distance. The depot remains first and every stop appears exactly once. The solver returns to the depot when computing distance.

Nearest neighbour takes O(n²). A 2-opt pass is O(n²), with at most 100 passes. The input cap of 100 points bounds work for this local demo. This is a heuristic and does **not** guarantee the global optimum. Tests compare a small instance with exhaustive search and verify that larger seeded instances never worsen the initial tour.

The browser sends only point coordinates to the local `/solve` endpoint. Input size, coordinate shape and finite numeric values are validated. The UI discards an outdated response when the points change during a solve.

## Limits and next improvements

Coordinates are illustrative canvas units, not geographical distances. This does not account for roads, traffic, vehicle capacity or time windows. The standard-library server binds to loopback and is intended for local demonstration; no authentication, TLS or production deployment is included.

Add capacity constraints with multiple vehicles, compare solutions against a stronger solver, and present quality-versus-runtime measurements. An accessible keyboard interface and tabular stop editor would improve the canvas interaction.

## Provenance

Initial implementation created with AI assistance. Review, understand and extend it before presenting it as your own engineering work. See tests and design notes for supported behaviour; no production usage or performance claims are implied.
