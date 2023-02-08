from boggle import Boggle
from flask import Flask, render_template, session, jsonify, request
from flask_debugtoolbar import DebugToolbarExtension

boggle_game = Boggle()

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"

debug = DebugToolbarExtension(app)


@app.route("/")
def show_board():
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get('highscore', 0)
    nplays = session.get('nplays', 0)
    context = {'board': board, 'highscore': highscore, 'nplays': nplays }
    
    return render_template('home.html', **context)

@app.route('/check-word')
def check_word():
    word = request.args['word']
    board = session['board']
    response = boggle_game.check_valid_word(board, word)
    print(response)
    return jsonify({'result': response})

@app.route('/post-score', methods=["POST"])
def update_score():
    last_score = request.json['score']
    highscore = session.get('highscore', 0)
    nplays = session.get('nplays', 0)
    session['nplays'] = nplays +1
    session['highscore'] = max(last_score, highscore)
        
    return jsonify(broken_record = True if last_score > highscore else False)