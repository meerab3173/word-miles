# ============================================
# WORD MILES - MAIN APP
# ============================================

import streamlit as st

from game_data import get_random_challenge, get_random_reaction, get_level
from game_logic import (
    find_shared_words,
    calculate_total_score,
    calculate_distance
)
from map import show_journey_map


# ============================================
# PAGE CONFIGURATION
# ============================================

st.set_page_config(
    page_title="Word Miles 💗",
    page_icon="💗",
    layout="centered"
)


# ============================================
# CUSTOM CSS
# ============================================

st.markdown(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&family=Quicksand:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Quicksand', sans-serif;
    }

    h1, h2, h3 {
        font-family: 'Fredoka', sans-serif !important;
        color: #7A2E42 !important;
    }

    .stApp {
        background: linear-gradient(180deg, #FFF9FB 0%, #FFEFF4 55%, #FFE9F1 100%);
    }

    /* ---------- Title & subtitle ---------- */

    .title {
        text-align: center;
        font-family: 'Fredoka', sans-serif;
        font-size: 52px;
        font-weight: 700;
        background: linear-gradient(135deg, #FF6F91, #E75480 55%, #C9184A);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 5px;
        animation: floatTitle 3s ease-in-out infinite;
    }

    @keyframes floatTitle {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-6px); }
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        font-weight: 600;
        color: #7A4A59;
        margin-bottom: 30px;
    }

    /* ---------- Cards ---------- */

    .big-card {
        background: linear-gradient(135deg, #FFF3F7 0%, #FFE4EC 100%);
        padding: 28px;
        border-radius: 24px;
        text-align: center;
        margin-bottom: 20px;
        border: 1px solid rgba(255, 182, 201, 0.6);
        box-shadow: 0 8px 24px rgba(231, 84, 128, 0.15);
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }

    .big-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 30px rgba(231, 84, 128, 0.22);
    }

    .stat-card {
        background: linear-gradient(160deg, #FFFFFF 0%, #FFF0F5 100%);
        padding: 18px 10px;
        border-radius: 18px;
        text-align: center;
        border: 1px solid #FFD1DF;
        box-shadow: 0 4px 14px rgba(231, 84, 128, 0.1);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .stat-card:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 20px rgba(231, 84, 128, 0.18);
    }

    .stat-icon {
        font-size: 22px;
        margin-bottom: 2px;
    }

    .stat-number {
        font-family: 'Fredoka', sans-serif;
        font-size: 30px;
        font-weight: 700;
        color: #E75480;
    }

    .stat-label {
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1px;
        color: #A15D70;
    }

    /* ---------- Letter tiles ---------- */

    .tile-row {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 10px;
        margin: 22px 0;
    }

    .tile {
        --rot: 0deg;
        width: 56px;
        height: 56px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(145deg, #FFFFFF, #FFE4EC);
        border: 2px solid #FFB6C9;
        border-radius: 14px;
        font-family: 'Fredoka', sans-serif;
        font-size: 26px;
        font-weight: 700;
        color: #E75480;
        box-shadow: 0 4px 0 #FFB6C9, 0 6px 12px rgba(231, 84, 128, 0.25);
        animation: tilePop 0.5s ease backwards;
    }

    @keyframes tilePop {
        0% { opacity: 0; transform: scale(0.4) rotate(var(--rot)); }
        70% { opacity: 1; transform: scale(1.12) rotate(var(--rot)); }
        100% { opacity: 1; transform: scale(1) rotate(var(--rot)); }
    }

    /* ---------- Shared words & results ---------- */

    .shared {
        background: linear-gradient(135deg, #FFF4E0, #FFE4EC);
        padding: 22px;
        border-radius: 20px;
        text-align: center;
        font-size: 22px;
        font-family: 'Fredoka', sans-serif;
        color: #E75480;
        border: 2px dashed #FFB6C9;
        animation: glow 2s ease-in-out infinite alternate;
    }

    @keyframes glow {
        from { box-shadow: 0 0 8px rgba(255, 182, 201, 0.35); }
        to   { box-shadow: 0 0 22px rgba(255, 182, 201, 0.85); }
    }

    .result-title {
        text-align: center;
        font-family: 'Fredoka', sans-serif;
        font-size: 40px;
        font-weight: 700;
        color: #E75480;
        animation: popIn 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
    }

    @keyframes popIn {
        0% { transform: scale(0.5); opacity: 0; }
        100% { transform: scale(1); opacity: 1; }
    }

    /* ---------- Buttons ---------- */

    div.stButton > button {
        background: linear-gradient(135deg, #FF8FAB 0%, #E75480 100%);
        color: white !important;
        font-family: 'Fredoka', sans-serif;
        font-weight: 600;
        font-size: 17px;
        border: none;
        border-radius: 50px;
        padding: 12px 20px;
        box-shadow: 0 4px 14px rgba(231, 84, 128, 0.35);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 6px 20px rgba(231, 84, 128, 0.45);
        color: white !important;
    }

    div.stButton > button:active {
        transform: translateY(0) scale(0.97);
    }

    /* ---------- Inputs ---------- */

    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 14px !important;
        border: 2px solid #FFD1DF !important;
        background-color: #FFFAFC !important;
        font-family: 'Quicksand', sans-serif !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #E75480 !important;
        box-shadow: 0 0 0 3px rgba(231, 84, 128, 0.15) !important;
    }

    /* ---------- Progress bar ---------- */

    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #FF8FAB, #E75480) !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================
# SESSION STATE
# ============================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "player1_name" not in st.session_state:
    st.session_state.player1_name = ""

if "player2_name" not in st.session_state:
    st.session_state.player2_name = ""

if "player1_city" not in st.session_state:
    st.session_state.player1_city = ""

if "player2_city" not in st.session_state:
    st.session_state.player2_city = ""

if "distance" not in st.session_state:
    st.session_state.distance = 0

if "xp" not in st.session_state:
    st.session_state.xp = 0

if "games_played" not in st.session_state:
    st.session_state.games_played = 0

if "shared_words_total" not in st.session_state:
    st.session_state.shared_words_total = 0

if "challenge" not in st.session_state:
    st.session_state.challenge = get_random_challenge()

if "player1_words" not in st.session_state:
    st.session_state.player1_words = []

if "player2_words" not in st.session_state:
    st.session_state.player2_words = []

if "player1_submitted" not in st.session_state:
    st.session_state.player1_submitted = False

if "player2_submitted" not in st.session_state:
    st.session_state.player2_submitted = False

if "result" not in st.session_state:
    st.session_state.result = None


# ============================================
# HOME PAGE
# ============================================

def home_page():

    st.markdown(
        '<div class="title">WORD MILES 💗</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">A friendship journey, one word at a time.</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="big-card">
            <h2>🌍 How far can your friendship travel?</h2>
            <p>
                You and your best friend receive the same letters,
                build words independently, and earn kilometers
                together.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 💗 Tell us about your friendship")

    player1_name = st.text_input(
        "Your name",
        value=st.session_state.player1_name,
        placeholder="e.g. Meerab"
    )

    player1_city = st.text_input(
        "Your city",
        value=st.session_state.player1_city,
        placeholder="e.g. Islamabad"
    )

    player2_name = st.text_input(
        "Your friend's name",
        value=st.session_state.player2_name,
        placeholder="e.g. Sarah"
    )

    player2_city = st.text_input(
        "Your friend's city",
        value=st.session_state.player2_city,
        placeholder="e.g. Karachi"
    )

    if st.button(
        "💗 Start Our Journey",
        use_container_width=True
    ):

        if (
            player1_name.strip()
            and player2_name.strip()
            and player1_city.strip()
            and player2_city.strip()
        ):

            st.session_state.player1_name = player1_name
            st.session_state.player2_name = player2_name

            st.session_state.player1_city = player1_city
            st.session_state.player2_city = player2_city

            st.session_state.distance = 0
            st.session_state.xp = 0
            st.session_state.games_played = 0
            st.session_state.shared_words_total = 0

            st.session_state.challenge = get_random_challenge()

            st.session_state.page = "dashboard"

            st.rerun()

        else:

            st.warning(
                "Please fill in all four fields before starting. 💗"
            )


# ============================================
# DASHBOARD
# ============================================

def dashboard():

    st.markdown(
        '<div class="title">WORD MILES 💗</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="subtitle">
            {st.session_state.player1_name}
            💗
            {st.session_state.player2_name}
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------
    # CITY INFORMATION
    # --------------------------------------------

    st.markdown(
        f"""
        <div class="big-card">
            <h2>
                📍 {st.session_state.player1_city}
                &nbsp; → &nbsp;
                {st.session_state.player2_city} 📍
            </h2>
            <p>
                Your friendship journey continues...
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------
    # STATISTICS
    # --------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-icon">🛣️</div>
                <div class="stat-number">
                    {st.session_state.distance}
                </div>
                <div class="stat-label">
                    KM TRAVELLED
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-icon">⭐</div>
                <div class="stat-number">
                    {st.session_state.xp}
                </div>
                <div class="stat-label">
                    XP
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-icon">🎮</div>
                <div class="stat-number">
                    {st.session_state.games_played}
                </div>
                <div class="stat-label">
                    GAMES
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    col4, col5 = st.columns(2)

    with col4:

        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-icon">💌</div>
                <div class="stat-number">
                    {st.session_state.shared_words_total}
                </div>
                <div class="stat-label">
                    SHARED WORDS
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col5:

        current_level = get_level(
            st.session_state.xp
        )

        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-icon">🏆</div>
                <div class="stat-number">
                    {current_level}
                </div>
                <div class="stat-label">
                    FRIENDSHIP LEVEL
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    # ============================================
    # JOURNEY MAP
    # ============================================

    st.markdown("## 🗺️ Our Journey")

    show_journey_map(
        st.session_state.distance
    )

    # ============================================
    # PLAY BUTTON
    # ============================================

    st.write("")

    if st.button(
        "🎮 Play Word Journey",
        use_container_width=True
    ):

        st.session_state.challenge = get_random_challenge()

        st.session_state.player1_words = []
        st.session_state.player2_words = []

        st.session_state.player1_submitted = False
        st.session_state.player2_submitted = False

        st.session_state.result = None

        st.session_state.page = "player1"

        st.rerun()

    # ============================================
    # RESET BUTTON
    # ============================================

    if st.button(
        "🔄 Reset Journey",
        use_container_width=True
    ):

        st.session_state.distance = 0
        st.session_state.xp = 0
        st.session_state.games_played = 0
        st.session_state.shared_words_total = 0

        st.session_state.page = "home"

        st.rerun()


# ============================================
# SHOW LETTERS
# ============================================

def show_letters():

    letters = st.session_state.challenge["letters"]

    tiles_html = ""

    for i, letter in enumerate(letters):

        rotation = -5 if i % 2 == 0 else 5
        delay = round(i * 0.07, 2)

        tiles_html += (
            f'<div class="tile" style="--rot:{rotation}deg; '
            f'animation-delay:{delay}s;">{letter}</div>'
        )

    st.markdown(
        f'<div class="tile-row">{tiles_html}</div>',
        unsafe_allow_html=True
    )


# ============================================
# PLAYER 1 PAGE
# ============================================

def player1_page():

    st.markdown(
        '<div class="title">YOUR TURN 💗</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="subtitle">
            {st.session_state.player1_name}
        </div>
        """,
        unsafe_allow_html=True
    )

    challenge = st.session_state.challenge

    st.markdown(
        f"""
        <div class="big-card">
            <h2>{challenge["theme"]}</h2>
            <p>{challenge["hint"]}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 🔤 Your letters")

    show_letters()

    st.info(
        "Enter one word per line. Try to think of as many "
        "words as you can!"
    )

    words_input = st.text_area(
        "Your words",
        placeholder="LOVE\nFRIEND\nSMILE\n...",
        height=180
    )

    if st.button(
        "🔒 Submit My Words",
        use_container_width=True
    ):

        words = words_input.split("\n")

        st.session_state.player1_words = words
        st.session_state.player1_submitted = True

        st.session_state.page = "player2"

        st.rerun()


# ============================================
# PLAYER 2 PAGE
# ============================================

def player2_page():

    st.markdown(
        '<div class="title">FRIEND\'S TURN 💗</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="subtitle">
            {st.session_state.player2_name}
        </div>
        """,
        unsafe_allow_html=True
    )

    challenge = st.session_state.challenge

    st.markdown(
        f"""
        <div class="big-card">
            <h2>{challenge["theme"]}</h2>
            <p>{challenge["hint"]}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 🔤 Same letters!")

    show_letters()

    st.info(
        "Don't look at your friend's answers! "
        "Enter your own words."
    )

    words_input = st.text_area(
        "Your words",
        placeholder="LOVE\nFRIEND\nSMILE\n...",
        height=180
    )

    if st.button(
        "🔒 Submit My Words",
        use_container_width=True
    ):

        words = words_input.split("\n")

        st.session_state.player2_words = words
        st.session_state.player2_submitted = True

        st.session_state.page = "results"

        st.rerun()


# ============================================
# RESULTS PAGE
# ============================================

def results_page():

    st.markdown(
        '<div class="result-title">REVEAL TIME! 💗</div>',
        unsafe_allow_html=True
    )

    player1_words = st.session_state.player1_words
    player2_words = st.session_state.player2_words

    # --------------------------------------------
    # FIND SHARED WORDS
    # --------------------------------------------

    shared_words = find_shared_words(
        player1_words,
        player2_words
    )

    # --------------------------------------------
    # CALCULATE SCORE
    # --------------------------------------------

    total_score, shared_words = calculate_total_score(
        player1_words,
        player2_words
    )

    earned_xp = total_score

    earned_km = calculate_distance(
        total_score
    )

    # --------------------------------------------
    # UPDATE GAME STATS
    # --------------------------------------------

    st.session_state.xp += earned_xp

    st.session_state.distance += earned_km

    st.session_state.games_played += 1

    st.session_state.shared_words_total += len(
        shared_words
    )

    # Prevent the result from being added repeatedly
    st.session_state.result = True

    # --------------------------------------------
    # PLAYER ANSWERS
    # --------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            f"### 💗 {st.session_state.player1_name}"
        )

        for word in player1_words:

            if word.strip():

                st.write(
                    f"• {word.strip().upper()}"
                )

    with col2:

        st.markdown(
            f"### 💗 {st.session_state.player2_name}"
        )

        for word in player2_words:

            if word.strip():

                st.write(
                    f"• {word.strip().upper()}"
                )

    # --------------------------------------------
    # SHARED WORDS
    # --------------------------------------------

    st.write("")

    if shared_words:

        shared_text = " • ".join(
            shared_words
        )

        st.markdown(
            f"""
            <div class="shared">
                💗 <b>YOU BOTH SAID:</b>
                <br><br>
                {shared_text}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.success(
            get_random_reaction()
        )

    else:

        st.warning(
            "No shared words this time... "
            "Maybe your friendship algorithms need an update 😂"
        )

    # --------------------------------------------
    # SCORE
    # --------------------------------------------

    st.write("")

    st.markdown(
        f"""
        <div class="big-card">
            <h2>🎉 Round Results</h2>

            <p>
                <b>Score:</b> {total_score} points
            </p>

            <p>
                <b>XP Earned:</b> +{earned_xp} XP
            </p>

            <p>
                <b>Distance Travelled:</b> +{earned_km} km
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------
    # FRIENDSHIP LEVEL
    # --------------------------------------------

    current_level = get_level(
        st.session_state.xp
    )

    st.markdown(
        f"""
        <div style="
            text-align:center;
            font-size:24px;
            color:#E75480;
            font-weight:bold;
        ">
            Current Level: {current_level}
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------
    # PROGRESS
    # --------------------------------------------

    journey_progress = min(
        st.session_state.distance / 1184,
        1.0
    )

    st.progress(
        journey_progress
    )

    st.markdown(
        f"""
        <div style="text-align:center;">
            🗺️
            {st.session_state.distance}
            / 1184 km travelled
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------
    # JOURNEY COMPLETE
    # --------------------------------------------

    if st.session_state.distance >= 1184:

        st.balloons()

        st.markdown(
            """
            <div class="big-card">
                <h1>🎉 YOU MADE IT! 🎉</h1>

                <p>
                    Islamabad → Karachi
                </p>

                <h2>
                    Distance couldn't stop you two. 💗
                </h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    # --------------------------------------------
    # BUTTONS
    # --------------------------------------------

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🎮 Play Again",
            use_container_width=True
        ):

            st.session_state.challenge = (
                get_random_challenge()
            )

            st.session_state.player1_words = []
            st.session_state.player2_words = []

            st.session_state.player1_submitted = False
            st.session_state.player2_submitted = False

            st.session_state.result = None

            st.session_state.page = "player1"

            st.rerun()

    with col2:

        if st.button(
            "🏠 Dashboard",
            use_container_width=True
        ):

            st.session_state.page = "dashboard"

            st.rerun()


# ============================================
# PAGE ROUTING
# ============================================

if st.session_state.page == "home":

    home_page()

elif st.session_state.page == "dashboard":

    dashboard()

elif st.session_state.page == "player1":

    player1_page()

elif st.session_state.page == "player2":

    player2_page()

elif st.session_state.page == "results":

    results_page()

