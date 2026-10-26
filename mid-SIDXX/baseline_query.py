# Baseline Query
# unoptimized INNER JOIN between results and races, checks that the tables are correctly linked, and times the query
import sqlite3
import shutil
import time
import statistics

ORIGINAL_DB = "ECE401 Project Database.db"
BASELINE_DB = "baseline.db"
RUNS = 100

# copy so we don't edit OG
shutil.copy(ORIGINAL_DB, BASELINE_DB)
con = sqlite3.connect(BASELINE_DB)

# load script created an index on results.raceId so remove so no extra indexes in baseline
con.execute("DROP INDEX IF EXISTS idx_results_raceId")
con.commit()

# 1) table linking
results_rows = con.execute("SELECT COUNT(*) FROM results").fetchone()[0]
joined_rows = con.execute("""
    SELECT COUNT(*)
    FROM results r
    INNER JOIN races ra ON r.raceId = ra.raceId
""").fetchone()[0]

print("Rows in results:      ", results_rows)
print("Rows after INNER JOIN:", joined_rows)
if results_rows == joined_rows:
    print("Every result matches a race, so the join drops nothing it shouldn't.")
else:
    print("WARNING:", results_rows - joined_rows, "results have no matching race.")
print()

# 2) baseline query
# pole position = grid 1. Grid 0 (pit lane / no grid slot) is left out by the filter
# a retirement (position is NULL) still pole start but not win
# COUNT(DISTINCT raceId) counts each race once since  some 1950s races have two drivers sharing the same car and both are listed at grid 1
BASELINE_QUERY = """
    SELECT (ra.year / 10) * 10 AS decade,
           COUNT(DISTINCT r.raceId) AS pole_starts,
           COUNT(DISTINCT CASE WHEN r.position = 1 THEN r.raceId END) AS pole_wins
    FROM results r
    INNER JOIN races ra ON r.raceId = ra.raceId
    WHERE r.grid = 1
    GROUP BY decade
    ORDER BY decade
"""

rows = con.execute(BASELINE_QUERY).fetchall()

print("Decade  Pole starts  Pole wins  Win %")
total_starts = 0
total_wins = 0
for decade, starts, wins in rows:
    print(f"{decade}s  {starts:>11}  {wins:>9}  {100 * wins / starts:5.1f}")
    total_starts += starts
    total_wins += wins
print(f"Total  {total_starts:>12}  {total_wins:>9}  {100 * total_wins / total_starts:5.1f}")
print()

# 3) print query 
print("Query plan:")
for row in con.execute("EXPLAIN QUERY PLAN " + BASELINE_QUERY):
    print("  ", row[3])
print()

# 4) time the query 
times = []
for i in range(RUNS):
    start = time.perf_counter()
    con.execute(BASELINE_QUERY).fetchall()
    end = time.perf_counter()
    times.append((end - start) * 1000)  # time in milliseconds

print(f"Baseline timing over {RUNS} runs:")
print(f"   median: {statistics.median(times):.3f} ms")
print(f"   mean:   {statistics.mean(times):.3f} ms")
print(f"   min:    {min(times):.3f} ms")
print(f"   max:    {max(times):.3f} ms")

con.close()
