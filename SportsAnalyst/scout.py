#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scout: helper for the MindFuel Digital Design Coding Challenge, Sports Analyst track.
v2: answers by clickable buttons (ipywidgets), so the full experience works with
NO login on the JupyterLite site as well as on Callysto Hub. Falls back to typed
input() automatically if widgets are unavailable.
Structure adapted from Callysto's hackathon templates (CC-BY). Original work by MindFuel.
"""

import random
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display

try:
    import ipywidgets as W
    HAS_W = True
except Exception:
    HAS_W = False

df = pd.read_csv("data.csv")

CHEERS = ["Nice work!", "That's exactly it!", "You'd make a great analyst!",
          "Right on the money!", "The coach is impressed!", "Nothing but net!",
          "You're a natural!", "Front office material right there!"]
SPARK = ["✨", "🌟", "🎉", "🏆", "🚀"]

def _fmt_cheer():
    return random.choice(SPARK) + " " + random.choice(CHEERS)

def scout(text):
    print("🏀 Scout: " + text)

_points = {"total": 0}
def _award(pts):
    _points["total"] += pts
    print(f"⭐ +{pts} points! Session total so far: {_points['total']}")

# ---------------------------------------------------------------- widget core
def _run_chain(steps):
    """steps: list of callables taking (advance) and rendering themselves."""
    if not steps:
        return
    def advance(i=[0]):
        i[0] += 1
        if i[0] < len(steps):
            steps[i[0]](advance)
    steps[0](advance)

def _mc_step(question, options, correct_index, why):
    """correct_index is 1-based."""
    def step(advance):
        if not HAS_W:
            while True:
                print("✅ " + question)
                for n, o in enumerate(options, 1):
                    print(f"   {n}. {o}")
                if input("Type the number of your answer: ").strip().rstrip(".") == str(correct_index):
                    print(_fmt_cheer()); scout(why); break
                print("❗️ Not that one. Look at the table above and try again!")
            advance()
            return
        out = W.Output()
        print("✅ " + question)
        btns = [W.Button(description=str(o)[:38], layout=W.Layout(width="auto", margin="2px"),
                         style={"button_color": "#e8e2f5"}) for o in options]
        box = W.VBox([W.HBox(btns), out])
        def make(n, b):
            def on(_):
                with out:
                    if n == correct_index:
                        for x in btns: x.disabled = True
                        b.style.button_color = "#a5d6a7"
                        print(_fmt_cheer()); scout(why)
                    else:
                        b.style.button_color = "#ef9a9a"
                        print("❗️ Not that one. Look again!")
                if n == correct_index:
                    advance()
            return on
        for n, b in enumerate(btns, 1):
            b.on_click(make(n, b))
        display(box)
    return step

def _value_step(prompt, correct, why, cast=str, placeholder="type your answer"):
    def check(ans):
        ans = str(ans).strip().strip('"').strip("'")
        try:
            if cast is float:
                return abs(float(ans) - float(correct)) < 0.051
            return ans.lower() == str(correct).lower()
        except ValueError:
            return False
    def step(advance):
        if not HAS_W:
            print("✅ " + prompt)
            while not check(input("Your answer: ")):
                print("❗️ Check the output above one more time. You've got this.")
            print(_fmt_cheer()); scout(why); advance()
            return
        out = W.Output()
        print("✅ " + prompt)
        txt = W.Text(placeholder=placeholder, layout=W.Layout(width="280px"))
        go = W.Button(description="Check ✔", style={"button_color": "#E8871E"})
        def on(_):
            with out:
                if check(txt.value):
                    txt.disabled = True; go.disabled = True
                    print(_fmt_cheer()); scout(why)
                else:
                    print("❗️ Not quite: " + repr(txt.value.strip()) + ". Check the output above and try again.")
            if txt.disabled:
                advance()
        go.on_click(on); txt.on_submit(lambda _ : on(None))
        display(W.VBox([W.HBox([txt, go]), out]))
    return step

def _award_step(pts):
    def step(advance):
        _award(pts); advance()
    return step

def _say_step(fn):
    def step(advance):
        fn(); advance()
    return step

# =================================================== CHALLENGES

def meet_the_team():
    def intro():
        scout("Hey! I'm Scout, the team's data assistant. Welcome to the front office!")
        scout("The general manager needs help deciding which player to sign, and YOU are the analyst on the case.")
        scout("Here's our scouting database. Real data, the way analysts actually see it:")
        display(df)
        scout("Every row is a player. Every column is a fact about them. That's all a dataset is!")
    _run_chain([_say_step(intro), _award_step(1)])

def first_look():
    def go():
        scout("Let's try plotting everything at once, just to see what happens.")
        df.plot(); plt.show()
        scout("Messy, right? A pile of lines with no story. By the end of these challenges "
              "you'll make charts that actually answer questions. That's the whole job.")
    _run_chain([_say_step(go), _award_step(1)])

def whos_on_the_roster():
    def intro():
        scout("First skill: reading the table. No code needed, just sharp eyes.")
        display(df.head(6))
    _run_chain([
        _say_step(intro),
        _mc_step("The .head() command shows the FIRST few rows. Which player is in the very first row?",
                 [df.iloc[3].Player, df.iloc[0].Player, df.iloc[5].Player, df.iloc[2].Player], 2,
                 "head() shows the top of the data. Analysts peek at the top first to learn what the columns mean."),
        _mc_step("Which column tells you how many points a player scores in a typical game?",
                 ["Games", "SalaryMillions", "PointsPerGame", "Player"], 3,
                 "PointsPerGame is what a player DELIVERS. Salary is what they COST. Analysts always separate the two."),
        _award_step(3),
    ])

def find_the_scorers():
    top_name = df.loc[df.PointsPerGame.idxmax(), "Player"].split()[0]
    def intro():
        scout("The GM texted: 'Who are our best scorers?' Let's sort the table.")
        display(df.sort_values("PointsPerGame", ascending=False).head(5))
    def outro():
        scout("Now look at the code cell below this one. It sorts by PointsPerGame. "
              "Change the column name to ReboundsPerGame and run it again. Same trick, new question!")
    _run_chain([
        _say_step(intro),
        _value_step("Which player has the HIGHEST points per game? (first name)", top_name,
                    "Sorting turns a pile of numbers into a ranking. One line, instant answer.",
                    placeholder="first name"),
        _say_step(outro),
        _award_step(3),
    ])

def sort_by(column):
    if column not in df.columns:
        print("❗️ '" + str(column) + "' isn't a column. Options: " + str(list(df.columns)))
        return
    display(df.sort_values(column, ascending=False).head(5))
    scout(f"Top 5 by {column}. Same tool, different question.")

def money_question():
    result = df[(df.PointsPerGame >= 18) & (df.SalaryMillions < 20)]
    best = result.loc[result.PointsPerGame.idxmax(), "Player"].split()[0]
    def intro():
        scout("The real assignment: the team has 20 million to spend, and the GM wants a scorer. "
              "At least 18 points per game, salary UNDER 20 million.")
        scout("I filtered the database with two conditions at once:")
        display(result)
    _run_chain([
        _say_step(intro),
        _value_step("How many players fit BOTH conditions? (type the number)", str(len(result)),
                    "Filtering with conditions is the number one daily skill of real analysts, everywhere.",
                    placeholder="a number"),
        _value_step("Which of those players scores the most? (first name)", best,
                    "Narrow the field, then rank what's left. That's the professional move.",
                    placeholder="first name"),
        _award_step(5),
    ])

def value_chart():
    def intro():
        scout("Numbers convince analysts. Charts convince COACHES. Let's make one.")
        plt.figure(figsize=(9, 5))
        plt.scatter(df.SalaryMillions, df.PointsPerGame)
        for _, row in df.iterrows():
            plt.annotate(row.Player.split()[0], (row.SalaryMillions, row.PointsPerGame), fontsize=8)
        plt.xlabel("Salary (millions)"); plt.ylabel("Points per game")
        plt.title("What does scoring cost?"); plt.show()
        scout("Players in the TOP LEFT score a lot but cost little. That corner is where smart teams shop.")
    _run_chain([
        _say_step(intro),
        _mc_step("A player in the top-left corner of this chart is:",
                 ["Expensive and low scoring", "A bargain: high scoring, low cost", "Injured", "The most famous"], 2,
                 "That corner is called value. Moneyball is a whole movie about finding it."),
        _award_step(5),
    ])

def your_call():
    def go():
        scout("You've got the skills. Time for YOUR analysis. Below this cell is working code "
              "for sorting, filtering, and charting. Copy it, change columns and numbers, and "
              "investigate a question YOU think the GM should care about.")
        scout("Ideas: Who is the best passer per salary dollar? Do centers rebound more than forwards? "
              "Who plays the most games?")
        scout("There is no single right answer. Real analysts choose their own question. That's the job.")
    _run_chain([_say_step(go), _award_step(7)])

def the_pitch():
    def intro():
        scout("Final challenge, demo day. The GM walks in: 'One sentence. Who do we sign, and why?'")
    if not HAS_W:
        intro()
        while True:
            name = input("Which player do you recommend? ").strip()
            m = df[df.Player.str.contains(name, case=False, na=False)] if name else df.iloc[0:0]
            if len(m) == 1:
                p = m.iloc[0]
                scout(f"{p.Player}: {p.PointsPerGame} pts, {p.ReboundsPerGame} reb, {p.AssistsPerGame} ast, "
                      f"{p.Games} games, ${p.SalaryMillions}M.")
                reason = input("Now the why. What does the data say? ").strip()
                if len(reason) >= 15:
                    print(_fmt_cheer())
                    scout("THAT is a data-backed recommendation. This skill is the daily job of sports analysts, "
                          "business analysts, and data scientists everywhere.")
                    _award(10); return
                print("❗️ Give the GM at least a sentence of evidence.")
            else:
                print("❗️ Can't find that player. Check the spelling in the table above.")
    intro()
    out = W.Output()
    pick = W.Dropdown(options=list(df.Player), description="Sign:")
    reason = W.Textarea(placeholder="The why: what does the data say? (at least one real sentence)",
                        layout=W.Layout(width="420px", height="70px"))
    go = W.Button(description="Pitch it to the GM 🎤", style={"button_color": "#E8871E"})
    done = {"ok": False}
    def on(_):
        with out:
            if done["ok"]:
                return
            p = df[df.Player == pick.value].iloc[0]
            if len(reason.value.strip()) < 15:
                print("❗️ The GM needs at least a sentence of evidence. Which numbers back your pick?")
                return
            done["ok"] = True
            pick.disabled = True; reason.disabled = True; go.disabled = True
            scout(f"{p.Player}: {p.PointsPerGame} pts, {p.ReboundsPerGame} reb, {p.AssistsPerGame} ast, "
                  f"{p.Games} games, ${p.SalaryMillions}M.")
            print(_fmt_cheer())
            scout("THAT is a data-backed recommendation. You found evidence, weighed cost against results, "
                  "and made a call out loud. Sports analyst, business analyst, data scientist: "
                  "this is the skill they're all paid for.")
            _award(10)
    go.on_click(on)
    display(W.VBox([pick, reason, go, out]))

def scoreboard():
    scout(f"Your point total: {_points['total']}")
    scout("1-3 point challenges built your skills. 5s made you an analyst. "
          "7s and 10s made you the one the GM listens to.")
