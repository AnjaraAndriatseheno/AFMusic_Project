from dotenv import load_dotenv
from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

import streamlit as st
from streamlit_mic_recorder import mic_recorder
from recognition import identifier_chantonnement
from llm import generate_description

st.set_page_config(page_title="AFMusic",layout="centered" )

st.markdown("""
<style>

.stApp {
    background: radial-gradient(circle at 50% 30%, #0b0f2a, #050716 70%);
    color: white;
    font-family: 'Roboto', sans-serif;
}

/* Header */
.app-title {
    font-size: 28px;
    font-weight: 600;
    margin-bottom: 40px;
}

/* Listen button */
.listen-btn {
    width: 180px;
    height: 180px;
    border-radius: 50%;
    background: linear-gradient(135deg, #5b6cff, #c84dff);
    display: flex;
    align-items: center;
    justify-content: center;
    margin: auto;
    box-shadow: 0 0 60px rgba(124, 77, 255, 0.5);
    font-size: 40px;
}

/* Result card */
.result-card {
    background: rgba(255,255,255,0.05);
    padding: 30px;
    border-radius: 20px;
    margin-top: 40px;
    backdrop-filter: blur(20px);
    box-shadow: 0 0 40px rgba(0,0,0,0.4);
}

/* Section titles */
.section-title {
    font-size: 14px;
    letter-spacing: 1px;
    color: #9aa4ff;
    margin-top: 25px;
    margin-bottom: 10px;
}

.song-title {
    font-size: 32px;
    font-weight: 700;
}

.artist-name {
    font-size: 20px;
    color: #c7c9ff;
}

</style>
""", unsafe_allow_html=True)



st.markdown('<div class="app-title">AFMusic</div>', unsafe_allow_html=True)
st.write("Clique sur le bouton pour reconnaître une musique")

audio = mic_recorder(start_prompt="Lancer l’écoute", stop_prompt="Stop")


if not audio:
    st.markdown(
        '<div class="listen-btn">🎧</div>',
        unsafe_allow_html=True
    )


if audio:
    st.audio(audio["bytes"])

    with st.spinner("Analyse en cours..."):

        titre, artiste = identifier_chantonnement(audio["bytes"])

        if titre:

            infos = generate_description(titre, artiste)

            st.markdown('<div class="result-card">', unsafe_allow_html=True)

            st.markdown(f'<div class="song-title">{infos["title"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="artist-name">{infos["artist"]}</div>', unsafe_allow_html=True)

            st.markdown('<div class="section-title">ARTIST</div>', unsafe_allow_html=True)
            st.write(infos.get("artist_description"))

            st.markdown('<div class="section-title">ABOUT THIS SONG</div>', unsafe_allow_html=True)
            st.write(infos.get("song_description"))

            st.markdown('<div class="section-title">MORE FROM THIS ARTIST</div>', unsafe_allow_html=True)

            for song in infos.get("other_songs", []):
                st.markdown(f"{song}")

            st.markdown('</div>', unsafe_allow_html=True)

        else:
            st.error("Musique non reconnue.")