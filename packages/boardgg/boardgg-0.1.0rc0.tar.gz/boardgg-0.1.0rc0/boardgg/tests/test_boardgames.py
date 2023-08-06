from unittest import TestCase
from unittest.mock import patch

import pytest

from boardgg.v1.entities import BoardGame
from boardgg.tests.mocks.boardgames import (
    search_boardgame,
    retrieve_boardgame,
    boardgame_not_found,
)


class TestBoardGames(TestCase):
    @patch("requests.get", side_effect=search_boardgame)
    def test_search_boardgame(self, search_call):
        board_game = BoardGame()
        results = board_game.search("7 Wonders Duel")
        assert search_call.called
        assert len(results) == 8

    @patch(
        "requests.get",
        side_effect=[
            search_boardgame(),
            retrieve_boardgame(),
        ],
    )
    def test_search_then_retrieve_boardgame(self, search_call):
        board_game = BoardGame()
        results = board_game.search("7 Wonders Duel")
        assert len(results) == 8

        game = board_game.retrieve(results[0].get("objectid"))
        assert game.get("objectid") == results[0].get("objectid")

        assert search_call.called
        assert search_call.call_count == 2

    @patch("requests.get", side_effect=boardgame_not_found)
    def test_boardgame_not_found(self, search_call):
        board_game = BoardGame()

        with pytest.raises(Exception) as e:
            game = board_game.retrieve("noesiten")

        assert search_call.called
