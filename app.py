# CS50x Final Project
# Michael Samp

from flask import Flask, render_template, request, redirect
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

        lower_rating = request.form.get('lower_rating')
        if lower_rating == '':
            lower_rating = 0
        upper_rating = request.form.get('upper_rating')
        if upper_rating == '':
            upper_rating == 5000

        pieces = ''.join(sorted(pieces))

        puzzle = helpers.find_puzzle(pieces, lower_rating, upper_rating)
            
        return redirect("/puzzles")
    
    if request.method == "GET":

        return render_template('index.html', puzzle_url='')

@app.route("/puzzles")
def puzzles():
     

    return render_template('puzzles.html')
