#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ranger: helper for the MindFuel Digital Design Coding Challenge, Wildlife Biologist track.
Architecture adapted from the Callysto hackathon mini-challenge templates
(github.com/callysto/hackathon, CC-BY). Original content by MindFuel:
answers are checked by meaning, not exact typing.
"""
import random
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display

df = pd.read_csv("data.csv")
T = {'bot': 'Ranger', 'emoji': '🦉', 'org': 'the national parks service', 'boss': 'park director', 'entity': 'habitat', 'entities': 'habitats', 'decision': "Which habitat gets this year's protection funding?", 'name_col': 'Habitat', 'p1': 'SpeciesCount', 'p2': 'EndangeredSpecies', 'count_col': 'SurveysDone', 'cost': 'ProtectionCostMillions', 'p1_meaning': 'how much a habitat delivers (SpeciesCount)', 'p1_thresh': 156, 'cost_thresh': 9.8, 'filter_story': 'The park director needs SpeciesCount of at least 156, with ProtectionCostMillions under 9.8.', 'idea1': 'Which region has the most endangered species overall?', 'idea2': 'Do wetlands hold more species than forests?', 'idea3': 'Which habitat protects the most species per dollar?', 'cheers': ['The forest thanks you!', 'Field-notes worthy!', 'A true conservationist!', 'The director is impressed!', 'Species saved!']}

def bot(text):
    print("\033[1;37;40m " + T["emoji"] + " " + T["bot"] + ": \033[1;0m" + text)

def task(text):
    print("\033[1;36m✅ " + text + "\033[1;0m")

def cheer():
    print("\033[1;35m" + random.choice(["✨ ","🌟 ","🎉 ","🏆 ","🚀 "]) + random.choice(T["cheers"]) + "\033[1;0m")

def hint(text):
    print("\033[1;31m❗️ " + text + "\033[1;0m")

def _ask_mc(question, options, correct_index, why):
    print(); task(question)
    for n, opt in enumerate(options, start=1):
        print("   " + str(n) + ". " + str(opt))
    while True:
        ans = input("Type the number of your answer: ").strip().rstrip(".")
        if ans == str(correct_index):
            cheer(); bot(why); return True
        hint("Not that one. Look at the table above and try again!")

def _ask_value(question, correct, why, cast=str):
    print(); task(question)
    while True:
        ans = input("Your answer: ").strip().strip('"').strip("'")
        try:
            ok = abs(float(ans) - float(correct)) < 0.051 if cast is float else ans.lower() == str(correct).lower()
        except ValueError:
            ok = False
        if ok:
            cheer(); bot(why); return True
        hint("Check the output above one more time. You've got this.")

_points = {"total": 0}
def _award(pts):
    _points["total"] += pts
    print("\033[1;33m +" + str(pts) + " points! Session total so far: " + str(_points["total"]) + " \033[1;0m")

NAME = T["name_col"]; P1 = T["p1"]; COST = T["cost"]

def meet():
    who = input(" " + T["emoji"] + " " + T["bot"] + ": Hi! I'm " + T["bot"] + ", the data assistant at " + T["org"] + ". What's your name? ").strip() or "Rookie"
    bot("Welcome aboard, " + who + "! The " + T["boss"] + " has one big question: " + T["decision"])
    bot("You're the analyst who answers it. Here's our database:")
    display(df)
    bot("Every row is a " + T["entity"] + ". Every column is a fact. That's all a dataset is!")
    _award(1)

def first_look():
    bot("Let's plot everything at once, just to see.")
    df.plot(); plt.show()
    bot("Messy, right? By the end of these challenges your charts will actually answer questions. That's the job.")
    _award(1)

def read_the_table():
    bot("First skill: reading the table. Sharp eyes, no code.")
    display(df.head(6))
    opts = [df.iloc[3][NAME], df.iloc[0][NAME], df.iloc[5][NAME], df.iloc[2][NAME]]
    _ask_mc("The .head() command shows the FIRST few rows. Which " + T["entity"] + " is in the very first row?",
            opts, 2, "head() shows the top of the data. Analysts peek at the top first to learn the columns.")
    _ask_mc("Which column tells you about " + T["p1_meaning"] + "?",
            [T["count_col"], COST, P1, NAME], 3,
            P1 + " is what a " + T["entity"] + " DELIVERS. " + COST + " is what it COSTS. Analysts always separate the two.")
    _award(3)

def find_the_leaders():
    bot("The " + T["boss"] + " asked: which " + T["entities"] + " lead on " + P1 + "? Sorting answers ranking questions instantly.")
    display(df.sort_values(P1, ascending=False).head(5))
    _ask_value("Which " + T["entity"] + " is highest on " + P1 + "? (type the first word of its name)",
               str(df.loc[df[P1].idxmax(), NAME]).split()[0],
               "Sorting turns a pile of numbers into a ranking. One line, instant answer.")
    bot("The cell below sorts by " + P1 + ". Change the column name to " + T["p2"] + " and rerun it. Same tool, new question!")
    _award(3)

def sort_by(column):
    if column not in df.columns:
        hint(str(column) + " isn't a column. Options: " + str(list(df.columns))); return
    display(df.sort_values(column, ascending=False).head(5))
    bot("Top 5 by " + str(column) + ". Same tool, different question.")

def the_big_filter():
    bot("The real assignment. " + T["filter_story"])
    result = df[(df[P1] >= T["p1_thresh"]) & (df[COST] < T["cost_thresh"])]
    bot("I filtered with two conditions at once:")
    display(result)
    _ask_value("How many " + T["entities"] + " fit BOTH conditions? (type the number)", str(len(result)),
               "Filtering with conditions is the number one daily skill of real analysts, everywhere.")
    _ask_value("Which of those is highest on " + P1 + "? (first word of its name)",
               str(result.loc[result[P1].idxmax(), NAME]).split()[0],
               "Narrow the field, then rank what's left. That's the professional move.")
    _award(5)

def value_chart():
    bot("Numbers convince analysts. Charts convince the " + T["boss"] + ". Let's make one.")
    plt.figure(figsize=(9,5))
    plt.scatter(df[COST], df[P1])
    for _, row in df.iterrows():
        plt.annotate(str(row[NAME]).split()[0], (row[COST], row[P1]), fontsize=7)
    plt.xlabel(COST); plt.ylabel(P1); plt.title("What does " + P1 + " cost?")
    plt.show()
    bot("Top LEFT of this chart: strong results, low cost. That corner is where smart decisions live.")
    _ask_mc("A " + T["entity"] + " in the top-left corner of this chart is:",
            ["Expensive with weak results", "A bargain: strong results, low cost", "Missing data", "The most famous"],
            2, "That corner is called value. Every professional field hunts for it.")
    _award(5)

def your_call():
    bot("You've got the skills. Now YOU choose the question. Working code for sorting, filtering, and charting sits below. Copy it, change columns and numbers, chase what you're curious about.")
    bot("Ideas if you want one: " + T["idea1"] + " " + T["idea2"] + " " + T["idea3"])
    bot("There is no single right answer. Real analysts pick their own question. That's the job.")
    _award(7)

def the_pitch():
    bot("Final challenge. The " + T["boss"] + " walks in: 'One sentence. " + T["decision"] + " And why?'")
    pick = input("Which " + T["entity"] + " do you recommend? ").strip()
    matches = df[df[NAME].astype(str).str.contains(pick, case=False, na=False)] if pick else df.iloc[0:0]
    if len(matches) == 1:
        row = matches.iloc[0]
        bot("; ".join(str(c) + ": " + str(row[c]) for c in df.columns))
        reason = input("Now the why. What does the data say? ").strip()
        if len(reason) >= 15:
            cheer()
            bot("THAT is a data-backed recommendation. Evidence, cost against results, a clear call. " +
                "That skill is the daily job in every career on the final page.")
            _award(10)
        else:
            hint("Give at least a sentence of evidence. Which numbers back your pick?")
            the_pitch()
    else:
        hint("I can't find that exact " + T["entity"] + ". Check the spelling in the table above (or type a longer part of the name).")
        the_pitch()

def scoreboard():
    bot("Your point total: " + str(_points["total"]))
    bot("1-3 point challenges built your skills. 5s made you an analyst. 7s and 10s made you the one the " + T["boss"] + " listens to.")
