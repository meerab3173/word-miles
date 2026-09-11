# ============================================
# WORD MILES - JOURNEY MAP
# ============================================

import streamlit as st
import plotly.graph_objects as go


# Islamabad and Karachi coordinates
ISLAMABAD = {
    "name": "Islamabad",
    "lat": 33.6844,
    "lon": 73.0479
}

KARACHI = {
    "name": "Karachi",
    "lat": 24.8607,
    "lon": 67.0011
}

# Approximate road distance
TOTAL_DISTANCE = 1184


def get_position(progress_km):
    """
    Calculates the position of the heart along
    the Islamabad-Karachi journey.
    """

    # Keep progress between 0 and total distance
    progress_km = max(0, min(progress_km, TOTAL_DISTANCE))

    percentage = progress_km / TOTAL_DISTANCE

    # Calculate latitude and longitude
    lat = (
        ISLAMABAD["lat"]
        + (KARACHI["lat"] - ISLAMABAD["lat"]) * percentage
    )

    lon = (
        ISLAMABAD["lon"]
        + (KARACHI["lon"] - ISLAMABAD["lon"]) * percentage
    )

    return lat, lon


def show_journey_map(progress_km):
    """
    Displays the Islamabad-Karachi journey map.
    """

    current_lat, current_lon = get_position(progress_km)

    fig = go.Figure()

    # --------------------------------------------
    # Travel route
    # --------------------------------------------

    fig.add_trace(
        go.Scattergeo(
            lat=[
                ISLAMABAD["lat"],
                KARACHI["lat"]
            ],
            lon=[
                ISLAMABAD["lon"],
                KARACHI["lon"]
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
            ISLAMABAD["lat"]
            + (KARACHI["lat"] - ISLAMABAD["lat"]) * percentage
        )

        lon = (
            ISLAMABAD["lon"]
            + (KARACHI["lon"] - ISLAMABAD["lon"]) * percentage
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
    # Islamabad
    # --------------------------------------------

    fig.add_trace(
        go.Scattergeo(
            lat=[ISLAMABAD["lat"]],
            lon=[ISLAMABAD["lon"]],
            mode="markers+text",
            marker=dict(
                size=14,
                color="#C9184A"
            ),
            text=["📍 Islamabad"],
            textposition="top center",
            name="Islamabad"
        )
    )

    # --------------------------------------------
    # Karachi
    # --------------------------------------------

    fig.add_trace(
        go.Scattergeo(
            lat=[KARACHI["lat"]],
            lon=[KARACHI["lon"]],
            mode="markers+text",
            marker=dict(
                size=14,
                color="#C9184A"
            ),
            text=["📍 Karachi"],
            textposition="bottom center",
            name="Karachi"
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

    # --------------------------------------------
    # Journey information
    # --------------------------------------------

    remaining = TOTAL_DISTANCE - progress_km
    percentage = (progress_km / TOTAL_DISTANCE) * 100

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