# CS50x Final Project
# Michael Samp

from flask import Flask, render_template, request
import base64
import helpers

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        pawn = request.form.get('pawn', '')
        bishop = request.form.get('bishop', '')
        knight = request.form.get('knight', '')
        rook = request.form.get('rook', '')
        queen = request.form.get('queen', '')

        pieces = pawn + bishop + knight + rook + queen

        puzzle = helpers.find_puzzle(pieces)
        
        encoded_url = helpers.encode_puzzle(puzzle)
        
        base_url = "https://listudy.org/en/iframe/custom-tactic#"
        
        puzzle_url = base_url + encoded_url
            
        return render_template('index.html', puzzle_url=encoded_url, pieces=pieces)
    
    if request.method == "GET":

        return render_template('index.html', puzzle_url='')

