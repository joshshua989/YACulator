# 🏈 YACulator

**YACulator** is a data-driven wide-receiver performance projection engine. It simulates weekly and full-season WR vs defender matchups using granular snap, scheme, and efficiency data.

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

🧠 INTELLIGENCE ENHANCEMENT ROADMAP
1. 💡 Dynamic WR-DB Route Matching
Objective: Match WR route types (e.g. slant, go, post) vs DB weaknesses.

Enhancement Ideas:

Use route distributions per WR (from tracking or route data if available).

Match against defender vulnerabilities (e.g. allow high YAC on in-breaking routes).

Score matchups:
route_match_score = route_success * db_weakness[route_type]

✅ Use Big Data Bowl tracking or pre-tagged route charts.

2. 🧠 Smarter Defensive Scheme Modeling
Objective: Incorporate disguise, hybrid coverage, and scheme variance.

Enhancement Ideas:

Add man_zone_blend_score per defense instead of binary choice.

Pull 3rd-party scheme data (e.g. PFF, Sports Info Solutions) if available.

Penalize WRs with low win rates vs press in heavy press schemes.

3. 🧮 QB-WR Chemistry & QB Influence
Objective: Account for QB quality, targeting patterns, and consistency.

Enhancement Ideas:

Add qb_accuracy, aDOT, EPA/play, and target_share_to_WR.

WR fantasy points = fpts_per_target * targets, and targets depend on QB trust.

Create a qb_influence_score:

python
Copy
Edit
score = WR_target_share * QB_accuracy * EPA/play
4. 📈 Real-Time Adjustments (In-Season Smarts)
Objective: Learn from recent results.

Enhancement Ideas:

Add rolling averages (last 3 weeks):
e.g. WR vs man (last 3 games), DB recent targets allowed.

Add injury-adjusted usage spikes (e.g. WR2 becomes WR1).

Update matchups mid-season via API (or user CSV update).

5. 🎯 Game Script + Environment Modeling
Objective: Simulate how game context affects WR usage.

Enhancement Ideas:

Use Vegas odds or predicted score differentials.

WRs on trailing teams tend to see more volume.

Incorporate weather/dome/altitude:
Add env_boost = 1.05 for dome, -5% for snow/wind.

🚀 BONUS: Machine Learning Mode
Once your deterministic logic is maximized, add a lightweight ML layer:

Use LightGBM or XGBoost to learn from all your features (man rate, role penalties, recent form, QB stats, etc.).

Train on past seasons with fantasy point labels.

Use feature importance to guide future app improvements.

🔁 Summary of Next High-Impact Tasks:
Priority	Task	Benefit
🔥 High	Add QB influence (accuracy, target share, EPA)	Strong signal for WR projections
🔥 High	Simulate game scripts and pace	Boost realism of matchups
✅ Done	Soft alignment roles for DBs	Handles noisy data
⭐ Medium	Route matching vs DB vulnerabilities	Adds true football IQ
⭐ Medium	Rolling stat window (e.g. last 3 weeks)	Captures momentum/form
🚧 Optional	ML on top of deterministic logic	Boosts predictive power

Would you like to start with QB influence, game script modeling, or route vs DB vulnerability mapping? I can implement any of these in your current pipeline.

---

## ✅ License

This project is distributed under the **MIT License**.

---

## 📫 Author

Created by **Josh Ellen** –
GitHub: [@joshshua989](https://github.com/joshshua989)

---
