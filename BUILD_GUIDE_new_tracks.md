# Build guide: cloning this track into a new career

How to turn the Sports Analyst track into Music Analyst, Wildlife Scientist, or any other career. Budget half a day per track once you have done one.

## What a track is

Three ingredients, all in one folder:

1. `data.csv`, the dataset. Around 20 rows, a mix of text and number columns, last column numeric.
2. `scout.py`, the helper module. All the questions, hints, story, and scoring live here.
3. `challenge-0.ipynb` through `challenge-6.ipynb`, seven notebooks. Mostly framing text plus one-line calls into the helper.

Students only ever open the notebooks. The notebooks call the helper. The helper reads the data.

## Step 1: Pick the career and the decision

Every track is one professional making one decision with data. That decision is the spine of all seven challenges.

- Sports Analyst: which player should the team sign?
- Music Analyst: which artist should the label promote?
- Wildlife Scientist: which habitat should get protection funding?

Pick a decision a kid can care about, with a real trade-off (quality vs cost, impact vs budget).

## Step 2: Build the dataset

Rules that make everything downstream work:

- About 20 rows, one entity per row (player, artist, habitat)
- One name column (called whatever fits, but the helper's capstone searches it)
- Two or three "performance" number columns (points, streams, species count)
- One "cost" number column, and it must be the LAST column (Callysto convention, and the value-chart challenge plots performance against it)
- Make the data fictional but realistic. Fictional avoids licensing and update problems.
- Plant one bargain: a row with high performance and low cost, so the value chart has a discoverable answer. Sky Martin is the plant in the sports data.

## Step 3: Rewrite scout.py

Copy the file, then work top to bottom. Everything that mentions basketball is in plain sight, none of it is buried:

- The bot's name and emoji (Scout 🏀 becomes, say, Nova 🎵 or Ranger 🌲)
- `meet_the_team`, `first_look`: story text only
- `whos_on_the_roster`: the two multiple choice questions, options, and explanations
- `find_the_scorers`: which column gets sorted and the follow-up column students switch to
- `money_question`: the two filter conditions and the numbers in the story ("at least 18 points, under 20 million" becomes your career's version)
- `value_chart`: the two columns plotted and the corner explanation
- `your_call`: the three suggested investigation questions
- `the_pitch`: the GM line becomes the label boss line or the funding board line
- The `cheer()` compliments: re-theme them ("Nothing but net!" becomes "Platinum record!")

What you never touch: `_ask_mc`, `_ask_value`, `_award`, the answer-checking logic. That is the machinery that makes answers check by meaning instead of exact typing, and it is career-agnostic.

Answers are computed from the data, not hardcoded (`df.PointsPerGame.idxmax()` style), so most questions keep working when the data changes. Reread each question after the data swap to make sure the story around it still makes sense.

## Step 4: Re-theme the notebooks

The notebooks are thin. Change the story text in the markdown cells and the emoji, keep the structure and the one-line code calls identical. The function names in scout.py can stay the same even if the story changed; only the notebooks' words need to match the new career.

## Step 5: Test like a student

Run every notebook top to bottom and deliberately answer wrong first each time. Check that:

- Every wrong answer loops with a hint, never crashes
- Every computed answer matches what the data actually says
- The value chart has a visible bargain in the top left
- The capstone finds your entities by partial, case-insensitive name

## Step 6: Host it

The folder goes in a public GitHub repo. Callysto's hub can pull it with a git-pull link (that is how their own hackathons load), or it runs in JupyterLite. Either way: browser only, Chromebooks, no installs. Test `input()` behavior in JupyterLite specifically before an event; if prompts are flaky there, the contained fix is swapping `_ask_mc` to ipywidgets buttons inside scout.py, nothing else changes.

## Credits

Structure adapted from Callysto's hackathon mini-challenge templates (github.com/callysto/hackathon, CC-BY). Keep the attribution line in challenge-0 and challenge-6 in every new track.
