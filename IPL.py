# IPL DATA ANALYSIS
# -----------------
# Basic IPL data analysis and visualization


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================
# 1. FUNCTIONS
# ============================================================

np.random.seed(42)


def random_colors(no_of_colors):
    colors = []

    for i in range(no_of_colors):
        color = "#" + "".join(
            np.random.choice(list("0123456789ABCDEF"))
            for j in range(6)
        )
        colors.append(color)

    return colors


# ============================================================
# 2. LOAD DATA
# ============================================================

match = pd.read_csv("matches.csv")
delivery = pd.read_csv("deliveries.csv")

print("Matches Shape:", match.shape)
print("Deliveries Shape:", delivery.shape)

print("\nMatches Data:")
print(match.head())

print("\nDeliveries Data:")
print(delivery.head())


# ============================================================
# 3. DATA CLEANING
# ============================================================

team_name_mapping = {
    "Rising Pune Supergiants": "Rising Pune Supergiant",
    "Royal Challengers Bangalore": "Royal Challengers Bengaluru"
}

for column in ["team1", "team2", "toss_winner", "winner"]:
    match[column] = match[column].replace(team_name_mapping)

for column in ["batting_team", "bowling_team"]:
    delivery[column] = delivery[column].replace(team_name_mapping)

match["city"] = match["city"].fillna("Unknown")
match["method"] = match["method"].fillna("Non D/L")


# ============================================================
# 4. TEAM SUCCESS RATE
# ============================================================

matches_played = pd.concat(
    [match["team1"], match["team2"]]
).value_counts()

matches_won = match["winner"].value_counts()

success_rate = (
    matches_won / matches_played * 100
).sort_values(ascending=False)

plt.figure(figsize=(12, 7))

plt.barh(
    success_rate.index,
    success_rate.values,
    color=random_colors(len(success_rate))
)

plt.gca().invert_yaxis()

plt.title("Team Success Rate")
plt.xlabel("Success Rate (%)")
plt.ylabel("Teams")

plt.tight_layout()
plt.show()


# ============================================================
# 5. IPL TITLES WON BY TEAMS
# ============================================================

title_won = (
    match.groupby("season")[["season", "winner"]]
    .tail(1)["winner"]
    .value_counts()
    .sort_values(ascending=False)
)

plt.figure(figsize=(12, 7))

plt.bar(
    title_won.index,
    title_won.values,
    color=random_colors(len(title_won))
)

plt.title("IPL Titles Won by Teams")
plt.xlabel("Teams")
plt.ylabel("Number of Titles")

plt.xticks(rotation=35, ha="right")

plt.tight_layout()
plt.show()


# ============================================================
# 6. TOP 10 RUN SCORERS
# ============================================================

top_10_runs = (
    delivery.groupby("batter")["batsman_runs"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .sort_values()
)

plt.figure(figsize=(11, 7))

plt.barh(
    top_10_runs.index,
    top_10_runs.values,
    color=random_colors(len(top_10_runs))
)

plt.title("Top 10 Run Scorers in IPL")
plt.xlabel("Total Runs")
plt.ylabel("Batter")

plt.tight_layout()
plt.show()


# ============================================================
# 7. TOP 10 BATTING PERFORMANCES IN A MATCH
# ============================================================

# Calculate runs scored by each batter in each match
batting_innings = (
    delivery.groupby(["match_id", "batter"])["batsman_runs"]
    .sum()
    .reset_index(name="Innings Runs")
)

top_batsmen_scores = (
    batting_innings
    .sort_values("Innings Runs", ascending=False)
    .head(10)
)

# Calculate balls faced by each batter in each match
batsman_ball_faced = (
    delivery.groupby(["match_id", "batter"])["batsman_runs"]
    .count()
    .reset_index(name="Balls Faced")
)

# Combine runs and balls faced
batsmen_performance = pd.merge(
    top_batsmen_scores,
    batsman_ball_faced,
    on=["match_id", "batter"],
    how="inner"
)

# Calculate strike rate
batsmen_performance["Strike Rate for Match"] = (
    batsmen_performance["Innings Runs"] * 100
    / batsmen_performance["Balls Faced"]
)

plt.figure(figsize=(12, 8))

sns.scatterplot(
    data=batsmen_performance,
    x="Strike Rate for Match",
    y="Innings Runs",
    hue="batter",
    s=150,
    palette=random_colors(
        batsmen_performance["batter"].nunique()
    )
)

plt.title("Top 10 Batting Performances in an IPL Match")
plt.xlabel("Strike Rate")
plt.ylabel("Runs in a Match / Innings")

plt.legend(
    title="Batter",
    bbox_to_anchor=(1.02, 1),
    loc="upper left"
)

plt.tight_layout()
plt.show()


# ============================================================
# 8. TOP 10 BOWLERS BY WICKETS
# ============================================================

# Run outs are not credited to the bowler
bowling_wickets = delivery[
    delivery["dismissal_kind"] != "run out"
]

top_bowlers = (
    bowling_wickets
    .groupby("bowler")["dismissal_kind"]
    .count()
    .reset_index(name="Wickets")
    .sort_values("Wickets", ascending=False)
    .head(10)
    .sort_values("Wickets")
)

plt.figure(figsize=(11, 7))

plt.barh(
    top_bowlers["bowler"],
    top_bowlers["Wickets"],
    color=random_colors(len(top_bowlers))
)

plt.title("Top 10 Bowlers in IPL")
plt.xlabel("Wickets Taken")
plt.ylabel("Bowler")

plt.tight_layout()
plt.show()


# ============================================================
# 9. TOP 10 BOWLING PERFORMANCES IN A MATCH
# ============================================================

# Calculate wickets taken by each bowler in each match
match_bowling_top = (
    delivery[delivery["dismissal_kind"] != "run out"]
    .groupby(["match_id", "bowler"])["dismissal_kind"]
    .count()
    .reset_index(name="Wickets")
)

# Calculate runs conceded by each bowler in each match
match_bowler_runs = (
    delivery.groupby(["match_id", "bowler"])["total_runs"]
    .sum()
    .reset_index(name="Runs Conceded")
)

# Combine wickets and runs conceded
match_bowler_performance = pd.merge(
    match_bowling_top,
    match_bowler_runs,
    on=["match_id", "bowler"],
    how="inner"
)

# Select the best 10 bowling performances
top_10_bowling = (
    match_bowler_performance
    .sort_values(
        ["Wickets", "Runs Conceded"],
        ascending=[False, True]
    )
    .head(10)
)

plt.figure(figsize=(12, 8))

sns.scatterplot(
    data=top_10_bowling,
    x="Runs Conceded",
    y="Wickets",
    hue="bowler",
    s=170,
    palette=random_colors(
        top_10_bowling["bowler"].nunique()
    )
)

plt.title("Top 10 Bowling Performances in an IPL Match")
plt.xlabel("Runs Conceded")
plt.ylabel("Wickets Taken")

plt.yticks(range(4, 8))

plt.legend(
    title="Bowler",
    bbox_to_anchor=(1.02, 1),
    loc="upper left"
)

plt.tight_layout()
plt.show()


# ============================================================
# 10. TOP 10 CITIES BY MATCHES PLAYED
# ============================================================

top_city = (
    match["city"]
    .value_counts()
    .head(10)
    .sort_values()
)

plt.figure(figsize=(9, 9))

plt.pie(
    top_city.values,
    labels=top_city.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Top 10 Cities by Number of IPL Matches")

plt.tight_layout()
plt.show()


# ============================================================
# 11. ALL DISMISSAL TYPES
# ============================================================

dismissals = (
    delivery["dismissal_kind"]
    .dropna()
    .value_counts()
    .sort_values()
)

plt.figure(figsize=(11, 7))

plt.barh(
    dismissals.index,
    dismissals.values,
    color=random_colors(len(dismissals))
)

# Log scale makes rare dismissal types easier to see
plt.xscale("log")

plt.title("Dismissal Types in IPL")
plt.xlabel("Number of Dismissals (Log Scale)")
plt.ylabel("Dismissal Type")

plt.tight_layout()
plt.show()


# ============================================================
# 12. TOP 10 FIELDERS
# ============================================================

top_fielders = (
    delivery["fielder"]
    .dropna()
    .value_counts()
    .head(10)
    .sort_values()
)

plt.figure(figsize=(10, 7))

plt.barh(
    top_fielders.index,
    top_fielders.values,
    color=random_colors(len(top_fielders))
)

plt.title("Top 10 Fielders by Dismissals")
plt.xlabel("Dismissals")
plt.ylabel("Fielder")

plt.tight_layout()
plt.show()


# ============================================================
# 13. OVER-BY-OVER ANALYSIS
# ============================================================

over_summary = (
    delivery.groupby("over")[
        ["total_runs", "is_wicket", "extra_runs", "batsman_runs"]
    ]
    .sum()
)

plt.figure(figsize=(14, 9))


# Total Runs
plt.subplot(2, 2, 1)

plt.plot(
    over_summary.index,
    over_summary["total_runs"],
    marker="o"
)

plt.title("Total Runs")
plt.xlabel("Over")
plt.ylabel("Runs")


# Wickets
plt.subplot(2, 2, 2)

plt.plot(
    over_summary.index,
    over_summary["is_wicket"],
    marker="o"
)

plt.title("Wickets")
plt.xlabel("Over")
plt.ylabel("Wickets")


# Extra Runs
plt.subplot(2, 2, 3)

plt.plot(
    over_summary.index,
    over_summary["extra_runs"],
    marker="o"
)

plt.title("Extra Runs")
plt.xlabel("Over")
plt.ylabel("Runs")


# Batsman Runs
plt.subplot(2, 2, 4)

plt.plot(
    over_summary.index,
    over_summary["batsman_runs"],
    marker="o"
)

plt.title("Batsman Runs")
plt.xlabel("Over")
plt.ylabel("Runs")


plt.suptitle("Over-by-Over Analysis")

plt.tight_layout()
plt.show()
