# CS50x Final Project
# Michael Samp

from flask import Flask, render_template, request
import base64
import helpers

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        pieces = ""
        pieces += request.form.get('my_pawn', '')
        pieces += request.form.get('my_bishop', '')
        pieces += request.form.get('my_knight', '')
        pieces += request.form.get('my_rook', '')
        pieces += request.form.get('my_queen', '')
        pieces += request.form.get('op_pawn', '')
        pieces += request.form.get('op_bishop', '')
        pieces += request.form.get('op_knight', '')
        pieces += request.form.get('op_rook', '')
        pieces += request.form.get('op_queen', '')

        lower_rating = int(request.form.get('lower_rating', 0))
        upper_rating = int(request.form.get('upper_rating', 5000))

        pieces = ''.join(sorted(pieces))

        puzzle = helpers.find_puzzle(pieces, lower_rating, upper_rating)
        
        encoded_url = helpers.encode_puzzle(puzzle[0])
        
        base_url = "https://listudy.org/en/iframe/custom-tactic#"
            
        return render_template('index.html', puzzle_url=encoded_url, pieces=pieces, rating=puzzle[0][2], PuzzleId=puzzle[0][3], moves=puzzle[0][1])
    
    if request.method == "GET":

        return render_template('index.html', puzzle_url='')

