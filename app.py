# ============================================
# WORD MILES - MAIN APP
# ============================================

import streamlit as st
from streamlit_autorefresh import st_autorefresh

from game_data import get_random_reaction, get_level
from map import show_journey_map
from multiplayer import (
    create_room,
    join_room,
    get_room,
    start_round,
    submit_words,
    back_to_lobby,
    reset_journey
)


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

    /* ---------- Room code ---------- */

    .room-code {
        text-align: center;
        font-family: 'Fredoka', sans-serif;
        font-size: 44px;
        font-weight: 700;
        letter-spacing: 12px;
        color: #E75480;
        background: linear-gradient(145deg, #FFFFFF, #FFE4EC);
        border: 3px dashed #FFB6C9;
        border-radius: 20px;
        padding: 18px 10px;
        margin: 20px 0;
        animation: glow 2s ease-in-out infinite alternate;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================
# SESSION STATE
#
# Only identity lives here (which room this
# device is in, and whether it's player1 or
# player2). The actual game state lives in the
# shared room store in multiplayer.py so both
# devices see the same thing.
# ============================================

if "room_code" not in st.session_state:
    st.session_state.room_code = None

if "my_role" not in st.session_state:
    st.session_state.my_role = None

# Restore identity after a page refresh using the URL,
# so reloading the tab doesn't kick a player out.
if st.session_state.room_code is None:

    qp_room = st.query_params.get("room")
    qp_role = st.query_params.get("role")

    if (
        qp_room
        and qp_role in ("player1", "player2")
        and get_room(qp_room) is not None
    ):

        st.session_state.room_code = qp_room.strip().upper()
        st.session_state.my_role = qp_role


def _remember_in_url(code, role):

    st.query_params["room"] = code
    st.query_params["role"] = role


def _leave_room():

    st.session_state.room_code = None
    st.session_state.my_role = None
    st.query_params.clear()


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
                Create a room, send the code to your best friend, and
                play together from two different devices — anywhere
                in the world. You'll each get the same letters, build
                words independently, and earn kilometers together.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    tab_create, tab_join = st.tabs(
        ["✨ Create a Room", "🔑 Join a Room"]
    )

    # --------------------------------------------
    # CREATE ROOM
    # --------------------------------------------

    with tab_create:

        st.markdown("#### Start a new journey")

        create_name = st.text_input(
            "Your name",
            placeholder="e.g. Meerab",
            key="create_name"
        )

        create_city = st.text_input(
            "Your city",
            placeholder="e.g. Islamabad",
            key="create_city"
        )

        if st.button(
            "💗 Create Room",
            use_container_width=True,
            key="create_room_btn"
        ):

            if create_name.strip() and create_city.strip():

                code = create_room(
                    create_name.strip(),
                    create_city.strip()
                )

                st.session_state.room_code = code
                st.session_state.my_role = "player1"

                _remember_in_url(code, "player1")

                st.rerun()

            else:

                st.warning(
                    "Please enter your name and city. 💗"
                )

    # --------------------------------------------
    # JOIN ROOM
    # --------------------------------------------

    with tab_join:

        st.markdown("#### Join your friend's journey")

        join_code = st.text_input(
            "Room code",
            placeholder="e.g. AB3D",
            key="join_code"
        ).strip().upper()

        join_name = st.text_input(
            "Your name",
            placeholder="e.g. Sarah",
            key="join_name"
        )

        join_city = st.text_input(
            "Your city",
            placeholder="e.g. Karachi",
            key="join_city"
        )

        if st.button(
            "🔑 Join Room",
            use_container_width=True,
            key="join_room_btn"
        ):

            if join_code and join_name.strip() and join_city.strip():

                success, error = join_room(
                    join_code,
                    join_name.strip(),
                    join_city.strip()
                )

                if success:

                    st.session_state.room_code = join_code
                    st.session_state.my_role = "player2"

                    _remember_in_url(join_code, "player2")

                    st.rerun()

                else:

                    st.warning(error)

            else:

                st.warning(
                    "Please fill in the room code, your name, "
                    "and your city. 💗"
                )


# ============================================
# LOBBY (shared room "waiting room" + dashboard)
# ============================================

def lobby_page(room):

    code = st.session_state.room_code

    st.markdown(
        '<div class="title">WORD MILES 💗</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------
    # WAITING FOR FRIEND TO JOIN
    # --------------------------------------------

    if not room["player2_joined"]:

        st.markdown(
            '<div class="subtitle">Waiting for your friend to join...</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="big-card">
                <h2>📨 Share this code with your friend</h2>
                <p>
                    They can open this same app on their own device
                    and enter this code under "Join a Room".
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="room-code">{code}</div>',
            unsafe_allow_html=True
        )

        st.info(
            "This page updates automatically the moment they join. 💗"
        )

        if st.button(
            "🚪 Leave Room",
            use_container_width=True
        ):

            _leave_room()

            st.rerun()

        st_autorefresh(interval=2500, key="lobby_wait_refresh")

        return

    # --------------------------------------------
    # BOTH PLAYERS JOINED
    # --------------------------------------------

    st.markdown(
        f"""
        <div class="subtitle">
            {room["player1_name"]}
            💗
            {room["player2_name"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="big-card">
            <h2>
                📍 {room["player1_city"]}
                &nbsp; → &nbsp;
                {room["player2_city"]} 📍
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
                    {room["distance"]}
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
                    {room["xp"]}
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
                    {room["games_played"]}
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
                    {room["shared_words_total"]}
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
            room["xp"]
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
        room["distance"]
    )

    # ============================================
    # PLAY BUTTON
    # ============================================

    st.write("")

    if st.button(
        "🎮 Play Word Journey",
        use_container_width=True
    ):

        start_round(code)

        st.rerun()

    # ============================================
    # RESET / LEAVE BUTTONS
    # ============================================

    if st.button(
        "🔄 Reset Journey",
        use_container_width=True
    ):

        reset_journey(code)

        st.rerun()

    if st.button(
        "🚪 Leave Room",
        use_container_width=True
    ):

        _leave_room()

        st.rerun()

    st_autorefresh(interval=4000, key="lobby_sync_refresh")


# ============================================
# SHOW LETTERS
# ============================================

def show_letters(challenge):

    letters = challenge["letters"]

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
# PLAY PAGE (both players play simultaneously,
# each from their own device)
# ============================================

def play_page(room):

    code = st.session_state.room_code
    my_role = st.session_state.my_role
    other_role = "player2" if my_role == "player1" else "player1"

    my_name = room[f"{my_role}_name"]
    other_name = room[f"{other_role}_name"]

    challenge = room["challenge"]

    st.markdown(
        '<div class="title">YOUR TURN 💗</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="subtitle">{my_name}</div>',
        unsafe_allow_html=True
    )

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

    show_letters(challenge)

    already_submitted = room[f"{my_role}_submitted"]

    if already_submitted:

        st.markdown(
            f"""
            <div class="big-card">
                <h2>✅ Words locked in!</h2>
                <p>Waiting for {other_name} to submit their words...</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st_autorefresh(interval=2000, key="play_wait_refresh")

    else:

        st.info(
            "Don't peek at your friend's answers! Enter one word "
            "per line, try to think of as many as you can."
        )

        words_input = st.text_area(
            "Your words",
            placeholder="LOVE\nFRIEND\nSMILE\n...",
            height=180,
            key=f"words_{code}_{my_role}_{room['round_number']}"
        )

        if st.button(
            "🔒 Submit My Words",
            use_container_width=True
        ):

            words = words_input.split("\n")

            submit_words(code, my_role, words)

            st.rerun()


# ============================================
# RESULTS PAGE
# ============================================

def results_page(room):

    code = st.session_state.room_code

    st.markdown(
        '<div class="result-title">REVEAL TIME! 💗</div>',
        unsafe_allow_html=True
    )

    result = room["last_result"]

    if result is None:

        st.info("Scoring your round...")

        st_autorefresh(interval=1500, key="results_wait_refresh")

        return

    player1_words = room["player1_words"]
    player2_words = room["player2_words"]

    # --------------------------------------------
    # PLAYER ANSWERS
    # --------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            f"### 💗 {room['player1_name']}"
        )

        for word in player1_words:

            if word.strip():

                st.write(
                    f"• {word.strip().upper()}"
                )

    with col2:

        st.markdown(
            f"### 💗 {room['player2_name']}"
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

    shared_words = result["shared_words"]

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
                <b>Score:</b> {result["total_score"]} points
            </p>
            <p>
                <b>XP Earned:</b> +{result["earned_xp"]} XP
            </p>
            <p>
                <b>Distance Travelled:</b> +{result["earned_km"]} km
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------
    # FRIENDSHIP LEVEL
    # --------------------------------------------

    current_level = get_level(
        room["xp"]
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
        room["distance"] / 1184,
        1.0
    )

    st.progress(
        journey_progress
    )

    st.markdown(
        f"""
        <div style="text-align:center;">
            🗺️
            {room["distance"]}
            / 1184 km travelled
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------
    # JOURNEY COMPLETE
    # --------------------------------------------

    if room["distance"] >= 1184:

        st.balloons()

        st.markdown(
            f"""
            <div class="big-card">
                <h1>🎉 YOU MADE IT! 🎉</h1>
                <p>
                    {room["player1_city"]} → {room["player2_city"]}
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

            start_round(code)

            st.rerun()

    with col2:

        if st.button(
            "🏠 Lobby",
            use_container_width=True
        ):

            back_to_lobby(code)

            st.rerun()

    st_autorefresh(interval=3000, key="results_sync_refresh")


# ============================================
# PAGE ROUTING
# ============================================

if st.session_state.room_code is None:

    home_page()

else:

    current_room = get_room(st.session_state.room_code)

    if current_room is None:

        st.markdown(
            '<div class="title">WORD MILES 💗</div>',
            unsafe_allow_html=True
        )

        st.warning(
            "This room no longer exists — the app may have "
            "restarted. Please create or join a new one. 💗"
        )

        if st.button(
            "🏠 Back to Home",
            use_container_width=True
        ):

            _leave_room()

            st.rerun()

    elif current_room["stage"] == "playing":

        play_page(current_room)

    elif current_room["stage"] == "results":

        results_page(current_room)

    else:

        lobby_page(current_room)

