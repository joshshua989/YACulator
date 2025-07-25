# 🏈 YACulator

**YACulator** is a data-driven wide-receiver FFP projection engine using matchup-based simulation. It simulates weekly and full-season WR vs defender matchups using advanced snap, scheme, and efficiency data.

---

## 🚀 Features

- Flexible execution:
  - 📅 Simulate the **full 2025 season**
  - 🔍 Run **single-week test projections**
- Uses **multi-year blended stats** (2022–2024) with configurable decay weights
- Intelligent matchup logic:
  - Slot / Wide vs slot / wide / LB / Safety alignment
  - Weighted man/zone scheme blending
- Adjusts projections based on defender quality (e.g. catch rate, separation, passer rating)
- Designed for weekly updates using live 2025 data via Cron or task scheduling

---

## 📂 Project Structure

````
YACulator/
├── config.py                  # Configuration: file paths, weights, version control
├── matchup\_simulator.py      # Core logic: matchups and fantasy point adjustments
├── sim\_engine.py             # Runner: weekly and full-season projection loops
├── main.py                   # CLI interface using --mode and --week flags
├── stat\_loader.py            # Standard loader for CSV input files
├── data\_loader.py            # (Optional) Multi-year blending, nflverse ingestion
├── quality\_control.py        # Validates data consistency across datasets
├── multi\_year\_blend.py       # Implements weighted blending of recent years
├── exports/
│   ├── season\_projection\_output.csv   # Full season projection output
│   └── test\_week\_projection.csv       # Single week projection output
├── data/
│   ├── NFL\_SCHEDULE\_2025.csv
│   ├── ADVANCED\_WR\_STATS\_2024.csv
│   ├── CB\_ALIGNMENT.csv
│   ├── DEF\_COVERAGE\_TAGS.csv
│   ├── roster\_2025.csv
│   └── roster\_2024.csv (optional fallback)
└── README.md
````

---

## 📥 Required Input Files

Below are the CSVs required for the engine to run, as well as their key column headers:

| File                           | Purpose                               | Key Columns                                                |
|--------------------------------|----------------------------------------|------------------------------------------------------------|
| `NFL_SCHEDULE_2025.csv`        | Defines weekly matchups                | `week`, `team`, `opponent`                                 |
| `ADVANCED_WR_STATS_2024.csv`   | WR route / alignment / efficiency stats| `Player`, `Team`, `SlotSnapRate`, `SnapShare`, `RoutesVsMan`, `RoutesVsZone`, `FantasyPointsPerTargetVsMan`, `FantasyPointsPerTargetVsZone` |
| `CB_ALIGNMENT.csv`             | Defender coverage alignment & quality | `PlayerYear`, `Team`, `Position`, `Catch Rate Allowed`, `Target Separation`, `Fantasy Points Allowed Per Target` |
| `DEF_COVERAGE_TAGS.csv`        | Team man/zone usage per week          | `team`, `week`, `man_coverage_rate`, `zone_coverage_rate`  |
| `roster_2025.csv`              | Team rosters and player IDs (2025)    | `team`, `position`, `depth_chart_position`, `full_name`, `gsis_id` |
| `roster_2024.csv` *(optional)* | Fallback roster if 2025 file missing   | Same columns as above                                     |

✅ A template pack (with sample rows) is available: `YACulator_CSV_Templates.zip`

---

## ⚙️ How to Run

You run the engine from the command line using these flags:

```bash
# Test a specific week (e.g., Week 3)
python main.py --mode test --week 3

# Simulate full 2025 season
python main.py --mode season

# Optionally specify custom output file
python main.py --mode test --week 3 --output my_week3_output.csv
````

* In **test mode**, it runs a projection for the specified week and saves to `test_week_projection.csv` by default.
* In **season mode**, it processes all weeks and saves to `season_projection_output.csv`.

---

## 🛠 Configurable Settings (`config.py`)

All constants are centralized in `config.py`:

* Data file names
* Role weights (slot, wide, safety, LB)
* Multi‑year blend decay (`WEIGHT_2024`, etc.)
* Output filenames
* Quality control toggles

Easily adjust behavior without changing script logic.

---

## 🧱 Roadmap

1. **QB Influence** – add QB accuracy, aDOT, EPA/play impact
2. **Route‑matching** – model WR route types (slants, posts, etc.) vs defender vulnerabilities
3. **Environmental factors** – weather, dome, altitude, pace
4. **Live weekly ingestion** – pull updated 2025 stats via `nflverse` or R integration
5. **Dashboard integration** – Excel or JSON export for visualization

---

## ✅ License

This project is distributed under the **MIT License**.

---

## 📫 Author

Created by **Josh Ellen** –
GitHub: [@joshshua989](https://github.com/joshshua989)

---
