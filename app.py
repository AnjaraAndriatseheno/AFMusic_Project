from dotenv import load_dotenv
from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

import streamlit as st
from streamlit_mic_recorder import mic_recorder
from recognition import identifier_chantonnement
from llm import generate_music_insights

st.set_page_config(page_title="AFMusic", page_icon="🎧", layout="centered")

st.title("🎵 AFMusic")
st.write("Clique sur le bouton pour reconnaître une musique")

audio = mic_recorder(start_prompt="Lancer l’écoute", stop_prompt="Stop")

if audio:
    st.audio(audio["bytes"])

    with st.spinner("Analyse en cours..."):

        titre, artiste = identifier_chantonnement(audio["bytes"])

        if titre:

            st.success("Musique reconnue 🎉")

            # Appel IA
            infos = generate_music_insights(titre, artiste)

            st.subheader(f"🎶 {infos['title']}")
            st.write(f"Artiste : {infos['artist']}")

            st.markdown("---")

            st.write("👤 **À propos de l’artiste**")
            st.write(infos.get("artist_description"))

            st.markdown("---")

            st.write("🎧 **À propos de la chanson**")
            st.write(infos.get("song_description"))

            st.markdown("---")

            st.write("🔥 **Autres titres populaires**")

            for song in infos.get("other_songs", []):
                st.write(f"- {song}")

        else:
            st.error("Musique non reconnue.")