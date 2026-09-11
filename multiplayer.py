# ============================================
# WORD MILES - MULTIPLAYER ROOM STORE
#
# Rooms live in a single object shared by every
# visitor to this running app (st.cache_resource
# returns the same instance to all sessions), so
# two devices can read and write the same game
# state. A lock keeps concurrent submits safe.
# ============================================

import random
import string
import threading
import time

import streamlit as st

from game_data import get_random_challenge
from game_logic import calculate_total_score, calculate_distance


ROOM_CODE_CHARS = "".join(
    c for c in string.ascii_uppercase + string.digits
    if c not in "0O1I"
)

ROOM_CODE_LENGTH = 4

ROOM_MAX_AGE_SECONDS = 24 * 60 * 60


@st.cache_resource
def _get_store():

    return {
        "rooms": {},
        "lock": threading.Lock()
    }


def _new_room_code(rooms):

    while True:

        code = "".join(
            random.choice(ROOM_CODE_CHARS)
            for _ in range(ROOM_CODE_LENGTH)
        )

        if code not in rooms:
            return code


def _prune_old_rooms(rooms):

    cutoff = time.time() - ROOM_MAX_AGE_SECONDS

    stale = [
        code for code, room in rooms.items()
        if room["created_at"] < cutoff
    ]

    for code in stale:
        del rooms[code]


def create_room(player1_name, player1_city):
    """
    Creates a new room and returns its code.
    The creator becomes player1.
    """

    store = _get_store()

    with store["lock"]:

        _prune_old_rooms(store["rooms"])

        code = _new_room_code(store["rooms"])

        store["rooms"][code] = {
            "player1_name": player1_name,
            "player1_city": player1_city,
            "player2_name": "",
            "player2_city": "",
            "player2_joined": False,
            "distance": 0,
            "xp": 0,
            "games_played": 0,
            "shared_words_total": 0,
            "stage": "lobby",
            "challenge": None,
            "round_number": 0,
            "player1_words": [],
            "player2_words": [],
            "player1_submitted": False,
            "player2_submitted": False,
            "last_result": None,
            "created_at": time.time()
        }

    return code


def join_room(code, player2_name, player2_city):
    """
    Joins an existing room as player2.
    Returns (success, error_message).
    """

    store = _get_store()

    code = code.strip().upper()

    with store["lock"]:

        room = store["rooms"].get(code)

        if room is None:
            return False, "That room code doesn't exist. Double-check it with your friend! 💗"

        if room["player2_joined"]:
            return False, "That room already has two players in it."

        room["player2_name"] = player2_name
        room["player2_city"] = player2_city
        room["player2_joined"] = True

    return True, None


def get_room(code):

    if not code:
        return None

    store = _get_store()

    return store["rooms"].get(code.strip().upper())


def start_round(code):
    """
    Starts (or restarts) a round with a fresh challenge.
    """

    store = _get_store()

    with store["lock"]:

        room = store["rooms"].get(code)

        if room is None:
            return

        room["challenge"] = get_random_challenge()
        room["round_number"] = room.get("round_number", 0) + 1
        room["player1_words"] = []
        room["player2_words"] = []
        room["player1_submitted"] = False
        room["player2_submitted"] = False
        room["last_result"] = None
        room["stage"] = "playing"


def submit_words(code, role, words):
    """
    Records one player's words. If both players have
    now submitted, the round is scored immediately.
    """

    store = _get_store()

    with store["lock"]:

        room = store["rooms"].get(code)

        if room is None:
            return

        room[f"{role}_words"] = words
        room[f"{role}_submitted"] = True

        if (
            room["stage"] == "playing"
            and room["player1_submitted"]
            and room["player2_submitted"]
        ):
            _finalize_round(room)


def _finalize_round(room):

    total_score, shared_words = calculate_total_score(
        room["player1_words"],
        room["player2_words"]
    )

    earned_xp = total_score
    earned_km = calculate_distance(total_score)

    room["xp"] += earned_xp
    room["distance"] += earned_km
    room["games_played"] += 1
    room["shared_words_total"] += len(shared_words)

    room["last_result"] = {
        "shared_words": shared_words,
        "total_score": total_score,
        "earned_xp": earned_xp,
        "earned_km": earned_km
    }

    room["stage"] = "results"


def back_to_lobby(code):

    store = _get_store()

    with store["lock"]:

        room = store["rooms"].get(code)

        if room is None:
            return

        room["stage"] = "lobby"


def reset_journey(code):

    store = _get_store()

    with store["lock"]:

        room = store["rooms"].get(code)

        if room is None:
            return

        room["distance"] = 0
        room["xp"] = 0
        room["games_played"] = 0
        room["shared_words_total"] = 0
        room["stage"] = "lobby"
        room["challenge"] = None
