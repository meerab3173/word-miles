# ============================================
# WORD MILES - JOURNEY MAP
# ============================================

import streamlit as st
import plotly.graph_objects as go


def get_position(progress_km, start, end, total_distance_km):
    """
    Calculates the current position along the journey
    between the two players' cities.
    """

    total_distance_km = max(total_distance_km, 1)

    progress_km = max(0, min(progress_km, total_distance_km))

    percentage = progress_km / total_distance_km

    lat = start["lat"] + (end["lat"] - start["lat"]) * percentage
    lon = start["lon"] + (end["lon"] - start["lon"]) * percentage

    return lat, lon


def show_journey_map(progress_km, total_distance_km, start=None, end=None):
    """
    Displays the friendship journey map between the two
    players' cities. Falls back to a simple distance readout
    if either city couldn't be found on the map.
    """

    if start is None or end is None:

        st.info(
            "Couldn't find one of your cities on the map, but "
            "your journey still counts! 💗"
        )

        _show_progress_text(progress_km, total_distance_km)

        return

    current_lat, current_lon = get_position(
        progress_km, start, end, total_distance_km
    )

    fig = go.Figure()

    # --------------------------------------------
    # Travel route
    # --------------------------------------------

    fig.add_trace(
        go.Scattergeo(
            lat=[
                start["lat"],
                end["lat"]
            ],
            lon=[
                start["lon"],
                end["lon"]
            ],
            mode="lines",
            line=dict(
                width=4,
                color="#E75480",
                dash="dot"
            ),
            name="Journey"
        )
    )

    # --------------------------------------------
    # Checkpoints
    # --------------------------------------------

    checkpoint_percentages = [
        0.20,
        0.40,
        0.60,
        0.80
    ]

    checkpoint_lats = []
    checkpoint_lons = []

    for percentage in checkpoint_percentages:

        lat = (
            start["lat"]
            + (end["lat"] - start["lat"]) * percentage
        )

        lon = (
            start["lon"]
            + (end["lon"] - start["lon"]) * percentage
        )

        checkpoint_lats.append(lat)
        checkpoint_lons.append(lon)

    fig.add_trace(
        go.Scattergeo(
            lat=checkpoint_lats,
            lon=checkpoint_lons,
            mode="markers",
            marker=dict(
                size=9,
                color="#FFB6C9",
                line=dict(width=1, color="#E75480")
            ),
            name="Checkpoints"
        )
    )

    # --------------------------------------------
    # Start city
    # --------------------------------------------

    fig.add_trace(
        go.Scattergeo(
            lat=[start["lat"]],
            lon=[start["lon"]],
            mode="markers+text",
            marker=dict(
                size=14,
                color="#C9184A"
            ),
            text=[f'📍 {start["name"]}'],
            textposition="top center",
            name=start["name"]
        )
    )

    # --------------------------------------------
    # End city
    # --------------------------------------------

    fig.add_trace(
        go.Scattergeo(
            lat=[end["lat"]],
            lon=[end["lon"]],
            mode="markers+text",
            marker=dict(
                size=14,
                color="#C9184A"
            ),
            text=[f'📍 {end["name"]}'],
            textposition="bottom center",
            name=end["name"]
        )
    )

    # --------------------------------------------
    # Current position
    # --------------------------------------------

    fig.add_trace(
        go.Scattergeo(
            lat=[current_lat],
            lon=[current_lon],
            mode="markers+text",
            marker=dict(
                size=18,
                color="#FF1493"
            ),
            text=["💗"],
            textposition="top center",
            name="Your Journey"
        )
    )

    # --------------------------------------------
    # Map settings
    # --------------------------------------------

    fig.update_geos(
        scope="world",
        projection_type="natural earth",
        showcountries=True,
        countrycolor="#FFD1DF",
        showland=True,
        landcolor="#FFF6F9",
        showocean=True,
        oceancolor="#EAF6FB",
        showlakes=False,
        showframe=False
    )

    fig.update_layout(
        height=500,
        margin=dict(
            l=0,
            r=0,
            t=20,
            b=0
        ),
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    _show_progress_text(progress_km, total_distance_km)


def _show_progress_text(progress_km, total_distance_km):

    remaining = max(total_distance_km - progress_km, 0)
    percentage = (progress_km / total_distance_km) * 100

    st.markdown(
        f"""
        <div style="
            text-align:center;
            padding:10px;
            font-size:18px;
        ">
            💗 <b>{progress_km} km</b> travelled
            &nbsp;&nbsp;•&nbsp;&nbsp;
            <b>{remaining} km</b> remaining
            <br>
            <small>{percentage:.1f}% of the journey completed</small>
        </div>
        """,
        unsafe_allow_html=True
    )
