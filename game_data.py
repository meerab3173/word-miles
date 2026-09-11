# ============================================
# WORD MILES - GAME DATA
# ============================================

import random


# Word challenges
CHALLENGES = [
    {
        "letters": ["F", "R", "I", "E", "N", "D", "S"],
        "theme": "Friendship",
        "hint": "Words connected to friendship"
    },

    {
        "letters": ["L", "O", "V", "E", "R", "S"],
        "theme": "Love & Friendship",
        "hint": "Words that remind you of people you love"
    },

    {
        "letters": ["H", "A", "P", "P", "Y", "D", "A", "Y"],
        "theme": "Happy",
        "hint": "Words that make you feel good"
    },

    {
        "letters": ["S", "U", "M", "M", "E", "R"],
        "theme": "Summer",
        "hint": "Things associated with summer"
    },

    {
        "letters": ["C", "O", "F", "F", "E", "E"],
        "theme": "Coffee",
        "hint": "Words related to coffee and cozy days"
    },

    {
        "letters": ["P", "A", "R", "T", "Y"],
        "theme": "Party",
        "hint": "Things you might find at a party"
    },

    {
        "letters": ["T", "R", "A", "V", "E", "L"],
        "theme": "Travel",
        "hint": "Words related to travelling"
    },

    {
        "letters": ["S", "M", "I", "L", "E"],
        "theme": "Smile",
        "hint": "Things that make you smile"
    },

    {
        "letters": ["D", "R", "E", "A", "M"],
        "theme": "Dreams",
        "hint": "Words related to dreams and goals"
    }
]


# Funny reactions after each round
REACTIONS = [
    "Okay... you two might actually share one brain. 🧠💗",
    "The telepathy is getting suspicious. 👀",
    "Bestie behavior detected. 💅",
    "You two really think alike! 💗",
    "Distance can't stop the friendship! 🌍💗",
    "That was actually adorable. 🥹",
    "Okay, this friendship is elite. 👑",
    "The friendship algorithm approves. 🤝💗"
]


# Friendship levels
LEVELS = [
    (0, "Just Friends 🌸"),
    (100, "Besties 💗"),
    (250, "Close AF 🎀"),
    (500, "Same Brain 🧠"),
    (1000, "Telepathic ✨"),
    (2000, "Unfortunately Attached 💀💗")
]


def get_random_challenge():
    """
    Returns a random word challenge.
    """

    return random.choice(CHALLENGES)


def get_random_reaction():
    """
    Returns a random funny reaction.
    """

    return random.choice(REACTIONS)


def get_level(xp):
    """
    Determines the friendship level based on XP.
    """

    current_level = LEVELS[0][1]

    for required_xp, level_name in LEVELS:

        if xp >= required_xp:
            current_level = level_name

    return current_level