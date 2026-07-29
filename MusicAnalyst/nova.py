#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nova: helper module for the MindFuel Digital Design Coding Challenge,
Music Analyst track.

Architecture adapted from the Callysto hackathon mini-challenge templates
(github.com/callysto/hackathon, Creative Commons Attribution license).
Rebuilt by MindFuel: answers are checked by meaning, not exact string
matching, so students are never wrong because of a space or a quote mark.
"""

import random
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display

df = pd.read_csv("data.csv")

# ---------------------------------------------------------------- voices

def nova(text):
    print("\033[1;37;40m 🎵 Nova: \033[1;0m" + text)

def task(text):
    print("\033[1;36m✅ " + text + "\033[1;0m")

def cheer():
    lines = [
        "Platinum record!", "That's a hit!", "Chart topper!", "You've got the ear!",
        "The label boss is impressed!", "Straight to number one!", "Encore! Encore!",
        "A&R material right there!",
    ]
    print("\033[1;35m" + random.choice(["✨ ", "🌟 ", "🎉 ", "🎤 ", "🚀 "]) + random.choice(lines) + "\033[1;0m")

def hint(text):
    print("\033[1;31m❗️ " + text + "\033[1;0m")

# ------------------------------------------------------- answer checking

def _ask_mc(question, options, correct_index, why):
    print()
    task(question)
    for n, opt in enumerate(options, start=1):
        print(f"   {n}. {opt}")
    while True:
        ans = input("Type the number of your answer: ").strip().rstrip(".")
        if ans == str(correct_index):
            cheer()
            nova(why)
            return True
        hint("Not that one. Look at the table above and try again!")

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
            nova(why)
            return True
        hint("Check the output above one more time. You've got this.")

# ------------------------------------------------------------ points bar

_points = {"total": 0}

def _award(pts):
    _points["total"] += pts
    print(f"\033[1;33m +{pts} points! Session total so far: {_points['total']} \033[1;0m")

# =================================================== CHALLENGE FUNCTIONS

def meet_the_label():
    """Challenge 0, worth 1 point."""
    name = input(" 🎵 Nova: Hey! I'm Nova, the label's data assistant. What's your name? ").strip() or "Rookie"
    nova(f"Welcome to the A&R department, {name}! The label has budget to "
         "promote exactly one artist next quarter, and you're the analyst "
         "who decides who gets the push.")
    nova("Here's our artist database. This is real data the way music "
         "industry analysts actually see it:")
    display(df)
    nova("Every row is an artist. Every column is a fact about them. "
         "That's all a dataset is!")
    _award(1)

def first_listen():
    """Challenge 0b, worth 1 point."""
    nova("Let's plot everything at once, just to see what happens.")
    df.plot()
    plt.show()
    nova("Noisy, right? Like every song playing at the same time. By the end "
         "of these challenges you'll make charts that actually answer "
         "questions. That's the whole job of a music analyst.")
    _award(1)

def read_the_charts():
    """Challenge 1, worth 3 points. Table reading, multiple choice."""
    nova("First skill: reading the table. No code needed, just sharp eyes.")
    display(df.head(6))
    _ask_mc(
        "The .head() command shows the FIRST few rows. Which artist is in the very first row?",
        ["Luna Vale", "Nova Reyes", "Cipher", "DJ Meridian"],
        2,
        "head() shows the top of the data. Analysts peek at the top first to learn what the columns mean.",
    )
    _ask_mc(
        "Look at the column names. Which column tells you how big an artist's audience is right now?",
        ["Songs", "PromoCostMillions", "MonthlyListenersMillions", "Artist"],
        3,
        "MonthlyListeners is audience. PromoCost is what the push costs. Analysts always separate what an artist DRAWS from what an artist COSTS.",
    )
    _award(3)

def find_the_headliners():
    """Challenge 2, worth 3 points. Sorting + change-a-value."""
    nova("The label boss texted: 'Who has the biggest audience right now?' Let's sort the table.")
    top = df.sort_values("MonthlyListenersMillions", ascending=False)
    display(top.head(5))
    _ask_value(
        "Which artist has the MOST monthly listeners? (type their stage name's first word)",
        df.loc[df.MonthlyListenersMillions.idxmax(), "Artist"].split()[0],
        "Sorting turns a pile of numbers into a ranking. One line of code, instant answer.",
    )
    nova("Now look at the code cell below this one. It sorts by "
         "MonthlyListenersMillions. Change the column name to "
         "StreamsPerSongMillions and run it again to find whose songs hit "
         "hardest per release. Same trick, different question!")
    _award(3)

def sort_by(column):
    """Student-modifiable sorter."""
    if column not in df.columns:
        hint(f"'{column}' isn't a column. Options: {list(df.columns)}")
        return
    out = df.sort_values(column, ascending=False).head(5)
    display(out)
    nova(f"Top 5 by {column}. See how the same tool answers a new question?")

def the_budget_meeting():
    """Challenge 3, worth 5 points. Filtering with two conditions."""
    nova("Here's the real assignment. The promo budget is 7 million. The boss "
         "wants reach: at least 12 million monthly listeners, promo cost UNDER 7 million.")
    result = df[(df.MonthlyListenersMillions >= 12) & (df.PromoCostMillions < 7)]
    nova("I filtered the database with two conditions at once:")
    display(result)
    _ask_value(
        "How many artists fit BOTH conditions? (type the number)",
        str(len(result)),
        "Filtering with conditions is the number one daily skill of real analysts, in music, in business, everywhere.",
    )
    _ask_value(
        "Which of those artists has the most monthly listeners? (first word of their name)",
        result.loc[result.MonthlyListenersMillions.idxmax(), "Artist"].split()[0],
        "You just did what a real A&R analyst does before a signing: narrow the field, then rank what's left.",
    )
    _award(5)

def value_chart():
    """Challenge 4, worth 5 points."""
    nova("Numbers convince analysts. Charts convince the BOSS. Let's make one.")
    plt.figure(figsize=(9, 5))
    plt.scatter(df.PromoCostMillions, df.MonthlyListenersMillions)
    for _, row in df.iterrows():
        plt.annotate(row.Artist.split()[0], (row.PromoCostMillions, row.MonthlyListenersMillions), fontsize=7)
    plt.xlabel("Promo cost (millions)")
    plt.ylabel("Monthly listeners (millions)")
    plt.title("What does an audience cost?")
    plt.show()
    nova("Artists in the TOP LEFT draw huge audiences but cost little to "
         "promote. That corner is where smart labels shop.")
    _ask_mc(
        "An artist in the top-left corner of this chart is:",
        ["Expensive with a small audience", "A bargain: big audience, low promo cost", "Retired", "The most famous"],
        2,
        "That corner is called value. Every label hunts for the artist about to blow up before the price does.",
    )
    _award(5)

def your_call():
    """Challenge 5, capstone part 1, worth 7 points."""
    nova("You've got the skills. Time for YOUR analysis. Below this cell "
         "you'll find working code for sorting, filtering, and charting. "
         "Copy any of it, change columns and numbers, and investigate "
         "a question YOU think the label should care about.")
    nova("Ideas if you want one: Who delivers the most streams per promo "
         "dollar? Do Major label artists really cost more than Indie ones? "
         "Which genre draws the biggest audiences?")
    nova("There is no single right answer here. Real analysts choose their "
         "own question. That's the job.")
    _award(7)

def the_pitch():
    """Challenge 6, capstone part 2, worth 10 points."""
    nova("Final challenge. The label boss walks in and says: 'One sentence. "
         "Who gets the promo budget, and why?'")
    name = input("Which artist do you recommend? ").strip()
    matches = df[df.Artist.str.contains(name, case=False, na=False)] if name else df.iloc[0:0]
    if len(matches) == 1:
        a = matches.iloc[0]
        nova(f"{a.Artist}: {a.MonthlyListenersMillions}M listeners, "
             f"{a.StreamsPerSongMillions}M streams per song, "
             f"{a.SocialFollowersMillions}M followers, promo cost ${a.PromoCostMillions}M.")
        reason = input("Now the why. What does the data say? ").strip()
        if len(reason) >= 15:
            cheer()
            nova("THAT is a data-backed recommendation. You found evidence, "
                 "weighed cost against reach, and made a call. Music analyst, "
                 "business analyst, data scientist: this is the skill "
                 "they're all paid for.")
            _award(10)
        else:
            hint("Give the boss at least a sentence of evidence. Which numbers back your pick?")
            the_pitch()
    else:
        hint(f"I can't find '{name}' in the database. Check the spelling in the table above.")
        the_pitch()

def scoreboard():
    nova(f"Your point total: {_points['total']}")
    nova("1-3 point challenges built your skills. 5s made you an analyst. "
         "7s and 10s made you the one the label listens to.")
