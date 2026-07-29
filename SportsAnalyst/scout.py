#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scout: the helper module for the MindFuel Digital Design Coding Challenge,
Sports Analyst track.

Architecture adapted from the Callysto hackathon mini-challenge templates
(github.com/callysto/hackathon, Creative Commons Attribution license).
Rebuilt by MindFuel: answers are checked by meaning, not by exact string
matching, so students are never wrong because of a space or a quote mark.

Students never need to write code from scratch. Low-floor questions are
multiple choice or run-the-cell. High-ceiling questions accept any correct
code because we evaluate the result, not the typing.
"""

import random
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display

df = pd.read_csv("data.csv")

# ---------------------------------------------------------------- voices

def scout(text):
    print("\033[1;37;40m 🏀 Scout: \033[1;0m" + text)

def task(text):
    print("\033[1;36m✅ " + text + "\033[1;0m")

def cheer():
    lines = [
        "Nice work!", "That's exactly it!", "You'd make a great analyst!",
        "Right on the money!", "The coach is impressed!", "Nothing but net!",
        "You're a natural!", "Front office material right there!",
    ]
    print("\033[1;35m" + random.choice(["✨ ", "🌟 ", "🎉 ", "🏆 ", "🚀 "]) + random.choice(lines) + "\033[1;0m")

def hint(text):
    print("\033[1;31m❗️ " + text + "\033[1;0m")

# ------------------------------------------------------- answer checking
# Multiple choice: student types a number. No syntax to get wrong.

def _ask_mc(question, options, correct_index, why):
    print()
    task(question)
    for n, opt in enumerate(options, start=1):
        print(f"   {n}. {opt}")
    while True:
        ans = input("Type the number of your answer: ").strip().rstrip(".")
        if ans == str(correct_index):
            cheer()
            scout(why)
            return True
        hint("Not that one. Look at the table above and try again!")

# Value questions: any formatting of the right value counts.

def _ask_value(question, correct, why, cast=str):
    print()
    task(question)
    while True:
        ans = input("Your answer: ").strip().strip('"').strip("'")
        try:
            if cast is float:
                ok = abs(float(ans) - float(correct)) < 0.051
            else:
                ok = ans.lower() == str(correct).lower()
        except ValueError:
            ok = False
        if ok:
            cheer()
            scout(why)
            return True
        hint("Check the output above one more time. You've got this.")

# ------------------------------------------------------------ points bar

_points = {"total": 0}

def _award(pts):
    _points["total"] += pts
    print(f"\033[1;33m +{pts} points! Session total so far: {_points['total']} \033[1;0m")

# =================================================== CHALLENGE FUNCTIONS

def meet_the_team():
    """Challenge 0, worth 1 point. Run the cell, meet the data."""
    name = input(" 🏀 Scout: Hey! I'm Scout, the team's data assistant. What's your name? ").strip() or "Rookie"
    scout(f"Great to have you on staff, {name}! The general manager needs help "
          "deciding which player to sign, and you're the analyst on the case.")
    scout("Here's our scouting database. This table is real data the way "
          "analysts actually see it:")
    display(df)
    scout("Every row is a player. Every column is a fact about them. "
          "That's all a dataset is!")
    _award(1)

def first_look():
    """Challenge 0b, worth 1 point. First chart, zero typing."""
    scout("Let's try plotting everything at once, just to see what happens.")
    df.plot()
    plt.show()
    scout("Messy, right? A pile of lines with no story. By the end of these "
          "challenges you'll make charts that actually answer questions. "
          "That's the whole job of a sports analyst.")
    _award(1)

def whos_on_the_roster():
    """Challenge 1, worth 3 points. Reading the table. Multiple choice."""
    scout("First skill: reading the table. No code needed, just sharp eyes.")
    display(df.head(6))
    _ask_mc(
        "The .head() command shows the FIRST few rows. Which player is in the very first row?",
        ["Sam Okafor", "Alex Rivera", "Jamie Cole", "Taylor Brooks"],
        2,
        "head() shows the top of the data. Analysts peek at the top first to learn what the columns mean.",
    )
    _ask_mc(
        "Look at the column names. Which column tells you how many points a player scores in a typical game?",
        ["Games", "SalaryMillions", "PointsPerGame", "Player"],
        3,
        "PointsPerGame is scoring. Salary is what they cost. Analysts always separate what a player DOES from what a player COSTS.",
    )
    _award(3)

def find_the_scorers():
    """Challenge 2, worth 3 points. Sorting. Change one value and rerun."""
    scout("The GM texted: 'Who are our best scorers?' Let's sort the table.")
    top = df.sort_values("PointsPerGame", ascending=False)
    display(top.head(5))
    _ask_value(
        "Which player has the HIGHEST points per game? (type their first name)",
        df.loc[df.PointsPerGame.idxmax(), "Player"].split()[0],
        "Sorting turns a pile of numbers into a ranking. One line of code, instant answer.",
    )
    scout("Now look at the code cell below this one. It sorts by PointsPerGame. "
          "Change the column name to ReboundsPerGame and run it again to find "
          "the best rebounder. Same trick, different question!")
    _award(3)

def sort_by(column):
    """Student-modifiable sorter used after find_the_scorers."""
    if column not in df.columns:
        hint(f"'{column}' isn't a column. Options: {list(df.columns)}")
        return
    out = df.sort_values(column, ascending=False).head(5)
    display(out)
    scout(f"Top 5 by {column}. See how the same tool answers a new question?")

def money_question():
    """Challenge 3, worth 5 points. Filtering. The analyst's real job."""
    scout("Here's the real assignment. The team has 20 million to spend. "
          "The GM wants a scorer: at least 18 points per game, salary UNDER 20 million.")
    result = df[(df.PointsPerGame >= 18) & (df.SalaryMillions < 20)]
    scout("I filtered the database with two conditions at once:")
    display(result)
    _ask_value(
        "How many players fit BOTH conditions? (type the number)",
        str(len(result)),
        "Filtering with conditions is the number one daily skill of real analysts, in sports, in business, everywhere.",
    )
    _ask_value(
        "Which of those players scores the most? (first name)",
        result.loc[result.PointsPerGame.idxmax(), "Player"].split()[0],
        "You just did what a pro scout does before a signing: narrow the field, then rank what's left.",
    )
    _award(5)

def value_chart():
    """Challenge 4, worth 5 points. First real chart."""
    scout("Numbers convince analysts. Charts convince COACHES. Let's make one.")
    plt.figure(figsize=(9, 5))
    plt.scatter(df.SalaryMillions, df.PointsPerGame)
    for _, row in df.iterrows():
        plt.annotate(row.Player.split()[0], (row.SalaryMillions, row.PointsPerGame), fontsize=7)
    plt.xlabel("Salary (millions)")
    plt.ylabel("Points per game")
    plt.title("What does scoring cost?")
    plt.show()
    scout("Players in the TOP LEFT score a lot but cost little. That corner "
          "is where smart teams shop.")
    _ask_mc(
        "A player in the top-left corner of this chart is:",
        ["Expensive and low scoring", "A bargain: high scoring, low cost", "Injured", "The most famous"],
        2,
        "That corner is called value. Moneyball is a whole movie about finding it.",
    )
    _award(5)

def your_call():
    """Challenge 5, capstone part 1, worth 7 points. Open exploration."""
    scout("You've got the skills. Time for YOUR analysis. Below this cell "
          "you'll find working code for sorting, filtering, and charting. "
          "Copy any of it, change columns and numbers, and investigate "
          "a question YOU think the GM should care about.")
    scout("Ideas if you want one: Who is the best passer per salary dollar? "
          "Do centers rebound more than forwards? Who plays the most games?")
    scout("There is no single right answer here. Real analysts choose their "
          "own question. That's the job.")
    _award(7)

def the_pitch():
    """Challenge 6, capstone part 2, worth 10 points. The recommendation."""
    scout("Final challenge. The GM walks in and says: 'One sentence. "
          "Who do we sign, and why?'")
    name = input("Which player do you recommend? ").strip()
    matches = df[df.Player.str.contains(name, case=False, na=False)] if name else df.iloc[0:0]
    if len(matches) == 1:
        p = matches.iloc[0]
        scout(f"{p.Player}: {p.PointsPerGame} pts, {p.ReboundsPerGame} reb, "
              f"{p.AssistsPerGame} ast, {p.Games} games, ${p.SalaryMillions}M.")
        reason = input("Now the why. What does the data say? ").strip()
        if len(reason) >= 15:
            cheer()
            scout("THAT is a data-backed recommendation. You found evidence, "
                  "weighed cost against production, and made a call. "
                  "Sports analyst, business analyst, data scientist: "
                  "this is the skill they're all paid for.")
            _award(10)
        else:
            hint("Give the GM at least a sentence of evidence. Which numbers back your pick?")
            the_pitch()
    else:
        hint(f"I can't find '{name}' in the database. Check the spelling in the table above.")
        the_pitch()

def scoreboard():
    scout(f"Your point total: {_points['total']}")
    scout("1-3 point challenges built your skills. 5s made you an analyst. "
          "7s and 10s made you the one the GM listens to.")
