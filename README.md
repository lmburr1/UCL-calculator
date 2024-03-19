This was a project to practice working with Python.

The goal is to produce a .csv that can then be turned into a heatmap with some conditional formatting in Excel/Sheets/etc. for most likely positions at the end of this years Champions League group stage. (FiveThirtyEight used to publish something similar.)

The adjacent football_clubs.txt is a list of this season's teams, labelled by group. The Elo ratings were pulled from https://footballdatabase.com/ on Sep. 1, 2023, the day after the draw. These ratings are not as serious as (e.g.) chess ratings, so the outcomes should not be taken particularly seriously. As I say, this was first and foremost meant to be a Python exercise.

I also want to note that I wrote this before knowing about Pandas or numpy, which would have made things much easier and the final 'product' much cleaner. I may revisit this after next year's draw with the benefit of more experience to make a better version.
