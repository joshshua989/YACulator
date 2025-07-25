# 🏈 YACulator

**YACulator** is a data-driven WR Projection Engine using matchup-based simulation.

## Features

- 🧠 Simulates WR production using DB alignment, coverage tendencies, slot vs wide usage
- 🔄 Uses multi-year blended stats (2022–2024)
- 🧮 Supports full 2025 NFL season simulation
- ✅ Coverage scheme logic via external tags
- 📊 Exports ready-to-visualize Excel and dashboard output

## Folder Structure

YACulator/
├── config.py
├── matchup_simulator.py
├── sim_engine.py
├── data_loader.py
├── quality_control.py
├── main.py
├── exports/
│ ├── season_projection_output.csv
│ └── test_week_projection.csv
├── data/
│ └── [Your CSV Files]


## How to Run

```bash
# Run test week projection
python main.py --mode test

# Run full season simulation
python main.py --mode season
```


Required Data Files
NFL_SCHEDULE_2025.csv

ADVANCED_WR_STATS_2024.csv

CB_ALIGNMENT.csv

DEF_COVERAGE_TAGS.csv

roster_2025.csv

roster_2024.csv (optional fallback)

See the /data folder or download the template pack.


---

#### 5. **Commit + Push to GitHub**
```bash
git add .
git commit -m "Initial commit with YACulator Checkpoint 1"
git push origin main
```
