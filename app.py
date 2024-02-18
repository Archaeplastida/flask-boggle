from boggle import Boggle
from flask import Flask, render_template, session, request, jsonify, redirect
from flask_debugtoolbar import DebugToolbarExtension
from time import time

#Boggle Game

boggle_game = Boggle()
app = Flask(__name__)
app.config["SECRET_KEY"] = "2005"
debug = DebugToolbarExtension(app)
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

def get_board():
    try:
        board = session["current_board"]
    except:
        board = boggle_game.make_board()
        session["current_board"] = board
    return board

def add_to_current_score(x=0):
    try:
        session["current_score"] = session["current_score"] + x
    except:
        session["current_score"] = 0
    return session["current_score"]

def add_correct_word(w):
    try:
        session["correctly_guessed_words"].append(w)
    except:
        session["correctly_guessed_words"] = [w]
    return session["correctly_guessed_words"]

@app.route("/", methods=["GET", "POST"])
def home(): #All you need to do now, is work on the restart button for the game page, so you don't have to keep going back to the home page to do another match of boggle, then you're all set.
    if request.method == 'POST':
        for x in ["correctly_guessed_words", "current_board", "current_score", "endTime"]:
            try:
                session.pop(x)
            except:pass
        return redirect("/game")
    return render_template("home.html")

@app.route("/game", methods=["GET", "POST"])
def game():
    if request.method == 'POST':
        try:
            if session["endTime"] != "Finished!":
                if "word" in request.json or "correctlyGuessedWord" in request.json:
                    word = ""
                    try:
                        word = request.json["word"]
                        score = add_to_current_score() #Right now, I'm making the logic to detect if a word has already been correctly guessed, by making a list and storing it on flask session. So, what I'm doing right now is trying to have app.py and script.js both have access to the list of correctly guessed words. First, I can use the js to display and tell the front end if a word has already been guessed correctly or not. Then I'd use the app.py python, to add more things into the list incase it sends a POST request via /games path. The python will also store the list in flask session. So, essentially, this is AJAX, since I'm not having the page refresh. Besides storing the values of the correctly guessed words, I'm also keeping track of score. If the guessed word is correct, the score will be added, based on the length of the word. Ex: If the word "Green" is on the board, and you guess it, then it will give you 5 points, since the length of the word is 5 letters/characters. But anyways, that's what I'm in the process of adding.
                        try:
                            session["correctly_guessed_words"]
                        except:
                            session["correctly_guessed_words"] = []
                            
                        return jsonify(check=boggle_game.check_valid_word(get_board(), word), score=score, correctly_guessed_words=session["correctly_guessed_words"])
                    except:
                        correctly_guessed_words = add_correct_word(request.json["correctlyGuessedWord"])
                        score = add_to_current_score(request.json["scoreAdded"])
                        return jsonify(check=boggle_game.check_valid_word(get_board(),request.json["correctlyGuessedWord"]), score=score, correctly_guessed_words=correctly_guessed_words)
                elif "endTime" in request.json:
                    try:
                        session["current_score"]
                    except:
                        session["current_score"] = 0

                    saved_high_score = session["high_score"]

                    if session["high_score"] < session["current_score"]:
                        session["high_score"] = session["current_score"] #What you need to do is implement the saving of a high score, then... you're all done. You'll be onto the CSS and the tests (CSS is much easier than the tests, but tests... gosh... are my weak point as I'm writing this.) ALSO THE TIMING SEEMS TO BE BROKEN FOR NOW, SO FIX THAT IMMEDIATELY BEFORE MOVING ON TO THE THINGS THAT I'VE JUST SAID.
                    try:
                        session["endTime"]
                        if request.json["endTime"] == "Finished!":
                            session["endTime"] = request.json["endTime"]
                            session["plays"] = session["plays"] + 1
                    except:
                        session["endTime"] = int(time()) + 60
                    return jsonify(endTime=session["endTime"], score=session["current_score"], high_score=saved_high_score)
            if "restart" in request.json:
                for x in ["correctly_guessed_words", "current_board", "current_score", "endTime"]:
                    session.pop(x)
                return jsonify(message="finished the restart")
        except:pass
            # try:
            #     if isinstance(request.json["timer"], int):
            #         session["time_left"] = request.json["timer"]
            #     else:
            #         raise
            # except:
            #     session["time_left"]
            # return jsonify(time_left=session["time_left"])
    try:session["correctly_guessed_words"]
    except:session["correctly_guessed_words"] = []
    # try:
    #     if session["time_left"] <= 0:
    #         session["time_left"] = "Finished" #You just need to work on the timer functionality a bit more, then you also have to work on the functionality of stopping the game once the timer is done, then you're all set.
    # except:
    #     try:
    #         session["time_left"] = request.json["timer"]
    #     except:
    #   
    #       session["time_left"] = 60

    try:
        session["plays"]
    except:
        session["plays"] = 0
    try:
        session["high_score"]
    except:
        session["high_score"] = 0
    time_left = "Finished!"
    try:session["endTime"]
    except:session["endTime"] = int(time()) + 60
    if isinstance(session["endTime"], int):
        if session["endTime"] - int(time()) <= 0:
            session["endTime"] = time_left
        else:
            time_left = session["endTime"] - int(time())
    return render_template("game.html", board=get_board(), score=add_to_current_score(), correctly_guessed_words=session["correctly_guessed_words"], time_left=time_left, high_score=session["high_score"], plays=session["plays"]) #Now, what I need to implement is to prevent to user from guessing the same correct answers that they've already guessed, so I need to implement that right now.