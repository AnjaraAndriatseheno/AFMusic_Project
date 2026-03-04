from dotenv import load_dotenv
from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

import streamlit as st
from streamlit_mic_recorder import mic_recorder
from recognition import identifier_musique
from llm import generate_description

st.set_page_config(page_title="AFMusic", layout="centered")

st.markdown("## 🎵 AFMusic")
st.write("Dis ou chante quelques paroles d'une chanson")

audio = mic_recorder(start_prompt="🎤 Lancer l’écoute", stop_prompt="⏹ Stop")

if not audio:
    st.write("Clique sur le micro pour commencer")

if audio:

    # filtre audio trop court
    if len(audio["bytes"]) < 2000:
        st.warning("Aucun son détecté")
        st.stop()

    st.audio(audio["bytes"])

    with st.spinner("Analyse en cours..."):

        titre, artiste = identifier_musique(audio["bytes"])

        if titre:

            infos = generate_description(titre, artiste)

            st.markdown("### 🎵 Résultat")

            st.markdown(f"**{infos['title']}**")
            st.markdown(f"*{infos['artist']}*")

            st.markdown("### ARTIST")
            st.write(infos.get("artist_description"))

            st.markdown("### AUTRES CHANSONS")

            for song in infos.get("other_songs", []):
                st.write("🎵", song)

        else:
            st.error("Musique non reconnue")