from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


    # TODO -- write tests for every view function / feature!

class TestBoggle(TestCase):
    def setUp(self):
        self.boggle_game = Boggle()
        self.board = self.boggle_game.make_board()
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.word = 'testword'
        self.b = Boggle()

    def test_show_board(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['board'] = self.board
            response = c.get('/board')
            self.assertEqual(response.status_code, 200)
            self.assertIn('board', session)
            self.assertEqual(session['board'], self.board)

    def test_check_word(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['board'] = self.board
            response = c.get(f'/check-word?word={self.word}')
            self.assertEqual(response.status_code, 200)
            result = response.get_json()['result']
            self.assertIsNotNone(result)

    def test_update_score(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['nplays'] = 1
                sess['highscore'] = 5
            response = c.post('/post-score', json={'score': 10})
            self.assertEqual(response.status_code, 200)
            result = response.get_json()
            self.assertEqual(result, {'broken_record': True})
            self.assertEqual(session['nplays'], 2)
            self.assertEqual(session['highscore'], 10)

    def test_check_valid_word(self):
        board = [
            ['a', 'b', 'a', 'd', 'e'],
            ['f', 'a', 'c', 'd', 'g'],
            ['k', 'l', 'm', 'n', 'o'],
            ['p', 'q', 'r', 's', 't'],
            ['u', 'v', 'w', 'x', 'y'],
        ]
        self.assertEqual(self.b.check_valid_word(board, "dog"), "not-on-board")
        self.assertEqual(self.b.check_valid_word(board, "cra"), "not-word")
        self.assertEqual(self.b.check_valid_word(board, "abc"), "ok")