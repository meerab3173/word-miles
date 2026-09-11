# ============================================
# WORD MILES - GAME LOGIC
# ============================================


def clean_words(words):
    """
    Cleans the words entered by a player.
    """

    cleaned = []

    for word in words:

        word = word.strip().upper()

        if word != "" and word not in cleaned:
            cleaned.append(word)

    return cleaned


def find_shared_words(player1_words, player2_words):
    """
    Finds words that both players entered.
    """

    player1_words = clean_words(player1_words)
    player2_words = clean_words(player2_words)

    shared = []

    for word in player1_words:

        if word in player2_words:
            shared.append(word)

    return shared


def calculate_score(words):
    """
    Gives a player 10 points for every word.
    """

    words = clean_words(words)

    return len(words) * 10


def calculate_shared_bonus(shared_words):
    """
    Gives 20 bonus points for every shared word.
    """

    return len(shared_words) * 20


def calculate_total_score(player1_words, player2_words):
    """
    Calculates the total score earned by both players.
    """

    shared_words = find_shared_words(
        player1_words,
        player2_words
    )

    player1_score = calculate_score(player1_words)
    player2_score = calculate_score(player2_words)

    shared_bonus = calculate_shared_bonus(shared_words)

    total_score = (
        player1_score
        + player2_score
        + shared_bonus
    )

    return total_score, shared_words


def calculate_distance(total_score):
    """
    Converts game points into virtual kilometres.

    Every 10 points = 1 km.
    """

    kilometers = total_score // 10

    return kilometers