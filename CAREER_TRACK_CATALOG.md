# Digital Design Coding Challenge — career track catalog

Fifteen STEM career tracks, all built, all tested, all passing the same design sentence: easy for beginners with no coding experience to have fun, understand, and learn something they keep for life.

Every track is the same proven engine: seven notebooks, a friendly bot, points from 1 to 10, answers checked by meaning instead of exact typing, and a final pitch where the student makes a real professional's decision backed by data. A student who finishes any track has loaded a database, read it, ranked it, filtered it under a budget, charted it, investigated their own question, and defended a recommendation. That workflow IS the career.

## The tracks

| # | Track | The student is a... | The decision they make | Folder |
|---|-------|--------------------|-----------------------|--------|
| 1 | Sports Analyst | basketball front-office analyst | which player the team signs | Coding_Challenge_SportsAnalyst |
| 2 | Music Analyst | record label data analyst | which artist gets the promo budget | Coding_Challenge_MusicAnalyst |
| 3 | Codebreaker | cybersecurity agent | crack the Cipher Ring's messages | Coding_Challenge_Codebreaker |
| 4 | Wildlife Biologist | parks conservation scientist | which habitat gets protection funding | Coding_Challenge_Tracks/WildlifeBiologist |
| 5 | Epidemiologist | public health analyst | which district gets the flu clinic first | Coding_Challenge_Tracks/Epidemiologist |
| 6 | Meteorologist | weather service analyst | which town gets the new radar | Coding_Challenge_Tracks/Meteorologist |
| 7 | Mars Mission Planner | space agency planner | where the rover lands | Coding_Challenge_Tracks/MarsMissionPlanner |
| 8 | Game Studio Analyst | game studio analyst | which game gets a sequel | Coding_Challenge_Tracks/GameStudioAnalyst |
| 9 | Urban Planner | city hall planner | which neighbourhood gets the new park | Coding_Challenge_Tracks/UrbanPlanner |
| 10 | Marine Biologist | ocean institute researcher | which reef gets restored | Coding_Challenge_Tracks/MarineBiologist |
| 11 | Energy Engineer | power utility engineer | where the solar farm gets built | Coding_Challenge_Tracks/EnergyEngineer |
| 12 | Food Scientist | food lab product developer | which snack recipe goes to production | Coding_Challenge_Tracks/FoodScientist |
| 13 | Astronomer | observatory researcher | which exoplanet gets telescope time | Coding_Challenge_Tracks/Astronomer |
| 14 | EMS Planner | emergency services analyst | where the new ambulance is stationed | Coding_Challenge_Tracks/EMSPlanner |
| 15 | Agriculture Scientist | crop research scientist | which wheat variety farmers plant | Coding_Challenge_Tracks/AgriScientist |

Tracks 1 and 2 are the hand-crafted originals with fully custom stories. Track 3 is a different mechanic entirely (cipher cracking instead of data analysis) for kids who want a second visit to feel new. Tracks 4 to 15 are generated from the tested engine, each with its own fictional dataset, its own bot (Ranger the owl, Iris, Gale, Orbit, Pixel, Metro, Coral, Volt, Basil, Nova, Sprint, Terra), its own investigation prompts, and its own career ladder on the final page.

## Why this is original

The seven-notebook shape comes from Callysto's openly licensed template (credited in every track). Everything inside is MindFuel's: original fictional datasets built so the answers are discoverable, original stories, original characters, and an original answer-checking engine that accepts any correct answer regardless of typing, spelling, or capitalization, which Callysto's version does not do. That last part is the piece built specifically for students who have never coded and may struggle with spelling.

## Event formats this supports

One event, students pick their career: 15 doors into the same skills, so friends can sit together and work different jobs. Or themed events: a health sciences day runs Epidemiologist + EMS Planner + Food Scientist; a space day runs Mars Mission Planner + Astronomer; an environment day runs Wildlife + Marine + Energy + Urban Planner.

## Making more

`generate_tracks.py` (in the session outputs) stamps a new track from a one-paragraph config: career, decision, column names, 20 fictional entity names, three investigation ideas. Add a config, run it, run the test. Veterinarian, pilot, geologist, water quality engineer, and sports medicine are natural next candidates.
