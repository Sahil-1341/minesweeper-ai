# Minesweeper AI

A lightweight Python implementation of the classic Minesweeper game plus an AI/experiment runner. Use this repo to study Minesweeper-solving strategies, run automated experiments, and collect results.


![Home Page](assets/results/Minesweeper%20home%20page%20snapshot.png) 
![win page](assets/results/Manual%20game%20win%20snapshot.png)
![lost page](assets/results/Manual%20game%20lost%20snapshot.png) 
![ai page](assets/results/win%20using%20AI%20move%20snapshot.png)

[requirements.txt](requirements.txt) • [assets/](assets/) • [runner.py](runner.py) • [minesweeper.py](minesweeper.py)

## Table of contents

- [What this project does](#what-this-project-does)
- [Why this project is useful](#why-this-project-is-useful)
- [Key features](#key-features)
- [Getting started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Install](#install)
  - [Run the game (interactive)](#run-the-game-interactive)
  - [Run experiments / AI runner](#run-experiments--ai-runner)
- [Assets and results](#assets-and-results)
- [Project structure](#project-structure)
- [How to get help](#how-to-get-help)
- [Maintainers and contributing](#maintainers-and-contributing)
- [License](#license)

## What this project does

This repository contains:
- A Minesweeper game engine (board generation, reveal and flag logic, neighbor counting).
- A runner script to execute AI agents over many trials for statistical evaluation.
- A small set of assets (fonts/images) and a directory for storing experiment results.

Intended audience: developers and researchers wanting a compact codebase to prototype Minesweeper solvers and benchmark strategies.

## Why this project is useful

- Provides a ready-to-run environment to test rule-based and algorithmic Minesweeper solvers.
- Lets you run many simulated games to collect win-rate and performance metrics.
- Easy to extend: add new agents or modify board generation and collection logic.

## Key features

- Pure-Python game logic.
- Experiment runner to automate repeated games and collect results.
- Lightweight dependency list in [requirements.txt](requirements.txt).
- Assets folder for images/fonts and a results directory for experiment outputs.

## Getting started

### Prerequisites

- Python 3.8+ recommended
- pip

### Install

Clone and install:

```bash
git clone https://github.com/Sahil-1341/minesweeper-ai.git
cd minesweeper-ai

# optional: create and activate a virtual environment
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

### Run the game (interactive)

If the repository includes an interactive mode, start it with:

```bash
python minesweeper.py
```

If the script exposes CLI options, check available flags:

```bash
python minesweeper.py --help
```

Adapt options based on the flags shown.

### Run experiments / AI runner

The runner automates playing multiple games and collecting metrics. Basic usage:

```bash
python runner.py
```

To inspect available options and any configurable output path, run:

```bash
python runner.py --help
```

Typical runner options you might expect (check actual flags with --help):
- --trials N           — number of games to run
- --rows R --cols C    — board dimensions
- --mines M            — mine count
- --agent NAME         — choose an AI/solver implementation
- --output PATH        — where to save results (CSV/JSON/plots)

The runner may save experiment summaries and per-trial data to the repository's results directory (see below).

## Assets and results

This repository includes an assets folder containing fonts, images and a results directory:

- assets/fonts/ — fonts used by any UI or for generating images.
- assets/images/ — icons and image assets used by the game and README:
  - assets/images/flag.png
  - assets/images/mine.png
- assets/results/ — output from experiment runs (CSV, JSON, PNG plots, etc).

How results are used:
- The runner writes aggregated statistics (win rate, average time, etc.) and per-trial logs into `assets/results/` by default if that folder exists, or to another configured output path.
- Files in `assets/results/` are intended to be lightweight export artifacts for later analysis (spreadsheet, plotting, or ML training).

When you run experiments:
- Check `assets/results/` after an experiment to find timestamped result files.
- If you want results in a different folder, either pass an `--output` flag to `runner.py` (if available) or update the runner configuration.

## Project structure

At the repository root you will find:

- assets/
  - fonts/
  - images/
    - flag.png
    - mine.png
  - results/         ← experiment outputs (CSV/JSON/plots)
- minesweeper.py     ← game logic and (possible) interactive entry point
- runner.py          ← experiment harness / AI runner
- requirements.txt   ← Python dependencies
- README.md

## How to get help

- Open an issue on the repository: https://github.com/Sahil-1341/minesweeper-ai/issues
- If the repo contains a `CONTRIBUTING.md` or `docs/`, consult those first:
  - [CONTRIBUTING.md](CONTRIBUTING.md) (if present)
  - [assets/](assets/) for sample assets used by the project

## Maintainers and contributing

Maintainer
- Sahil — [Sahil-1341](https://github.com/Sahil-1341)

Contributing
- Fork the repository and create a branch for your changes.
- Open a pull request describing your change and why it helps the project.
- Small, focused PRs that include tests or example runs are appreciated.

For full contribution guidelines, add or consult `CONTRIBUTING.md`.

## License

See the repository `LICENSE` file for license terms.
