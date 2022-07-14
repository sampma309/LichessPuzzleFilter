# CS50x Final Project
# Michael Samp

from flask import Flask, render_template, request, redirect
import helpers

app = Flask(__name__)

# Homepage
@app.route("/")
def index():

    # Initial load
    return render_template('index.html')
        

# Page where puzzles are solved
@app.route("/puzzles")
def puzzles():

    # Get form data for pieces to include
    pieces = ""
    pieces += request.args.get('my_pawn', '')
    pieces += request.args.get('my_bishop', '')
    pieces += request.args.get('my_knight', '')
    pieces += request.args.get('my_rook', '')
    pieces += request.args.get('my_queen', '')
    pieces += request.args.get('op_pawn', '')
    pieces += request.args.get('op_bishop', '')
    pieces += request.args.get('op_knight', '')
    pieces += request.args.get('op_rook', '')
    pieces += request.args.get('op_queen', '')

    # Created sorted string to search for in DB
    pieces = ''.join(sorted(pieces))

    # Get form value for rating or use default value
    lower_rating = request.args.get('lower_rating')
    if lower_rating == '':
        lower_rating = 0
    upper_rating = request.args.get('upper_rating')
    if upper_rating == '':
        upper_rating == 5000

    # Get a random puzzle
    puzzle = helpers.find_puzzle(pieces, lower_rating, upper_rating)

    # Send to an error page if no puzzles are found
    if not puzzle:
        return redirect('/oops')

    # Render the puzzle page
    return render_template('puzzles.html', rating=puzzle[1], 
                                           moves=puzzle[0], 
                                           PuzzleId=puzzle[2], 
                                           URL=puzzle[3])

# Route if no puzzles are found
@app.route("/oops")
def oops():
    return render_template('oops.html')