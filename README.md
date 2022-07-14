# CS50-Final-Project

The goal of this project is to take the publicly available database of Lichess puzzles (https://database.lichess.org/#puzzles) and filter it so you can work on puzzles involving a specific set of pieces. For example: if you wanted to work on rook and pawn endgames, the app will return only puzzles containing rooks and pawns.

Instructions for running locally:

1. Clone repository by typing: git clone https://www.github.com/sampma309/CS50-Final-Project
2. Activate virtual environment with: source venv/bin/activate
3. Run application with: flask run
4. Go to http://127.0.0.1:5000 in browser (note: 5000 is the default port, but Flask may use a different one)

Optionally, you can also change the complete set of puzzles. To do so:
1. Download the puzzle database from https://database.lichess.org/#puzzles and remove as many lines as you would like. Note: the complete database contains ~2.6 million puzzles, but I have included a database of only 150,000 puzzles by default.
2. Save the downloaded .csv file in the 'static/' directory as 'puzzles.csv'
3. Delete 'static/puzzles.db'
4. After activating the virtual environment, while in the top-level directory, run: python3 create_db.py (Note: depending on the size of your puzzle list, this might take a few minutes)


Credit for the embedded tactic generator goes to Arne Vogel and the rest of the contributors to listudy.org. Without that tool, I wouldn't have been able to do this at all.
