from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle
from time import time

test_boggle = Boggle()

class FlaskTests(TestCase):
    def test_home_page(self):
        with app.test_client() as client:
            res = client.get("/")
            html = res.get_data(as_text=True)
            
            self.assertEqual(res.status_code, 200)
            self.assertIn("<h1>BOGGLE!</h1>", html)

    def test_redirection_from_home_page(self):
        with app.test_client() as client:
            res = client.post("/")

            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, "http://localhost/game")
            #Testing data-wipe of given sessions in the list below, whenever you get redirected to the game page. The purpose it provides: Ensures that the users always get a new game when they get redirected to the game page.
            for x in ["correctly_guessed_words", "current_board", "current_score", "endTime"]:
                self.assertEqual(session.get(x), None)

    def test_game(self):
        with app.test_client() as client:
            res = client.get("/game")

            self.assertEqual(res.status_code, 200) #What I need to implement right here is the rest of the tests for the game view function. Remember, there's a lot of things that you need to test for game, especially the sessions, to check if they're storing the values correctly.
            for x in ["correctly_guessed_words", "current_board", "current_score", "endTime"]:
                self.assertNotEqual(session.get(x), None) #This is to check if the values were actually created and are NOT equal to None.

            session["current_board"] = [['I', 'C', 'W', 'G', 'M'], ['X', 'M', 'W', 'O', 'W'], ['R', 'I', 'D', 'K', 'G'], ['B', 'I', 'N', 'Q', 'J'], ['X', 'E', 'S', 'U', 'U']]
            timeDif = session.get("endTime") - int(time())
            self.assertIn(timeDif, [59,60])

            self.assertEqual(test_boggle.check_valid_word(board=session["current_board"], word="in"), "ok")
            self.assertEqual(test_boggle.check_valid_word(board=session["current_board"], word="bind"), "ok")
            self.assertEqual(test_boggle.check_valid_word(board=session["current_board"], word="bin"), "ok")
            self.assertEqual(test_boggle.check_valid_word(board=session["current_board"], word="purple"), "not-on-board")
            self.assertEqual(test_boggle.check_valid_word(board=session["current_board"], word="green"), "not-on-board")
            self.assertEqual(test_boggle.check_valid_word(board=session["current_board"], word="real"), "not-on-board")
            self.assertEqual(test_boggle.check_valid_word(board=session["current_board"], word="jfdib"), "not-word")
            self.assertEqual(test_boggle.check_valid_word(board=session["current_board"], word="godsib"), "not-word")
            self.assertEqual(test_boggle.check_valid_word(board=session["current_board"], word="sioubid"), "not-word")