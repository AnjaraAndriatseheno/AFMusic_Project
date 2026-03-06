from dotenv import load_dotenv
from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

import streamlit as st
from streamlit_mic_recorder import mic_recorder
from recognition import identifier_chantonnement
from llm import generate_description

st.set_page_config(page_title="AFMusic", layout="centered")

st.title("AFMusic")
st.write("Dis ou prononce quelques paroles d'une chanson")

audio = mic_recorder(start_prompt="Lancer l’écoute", stop_prompt="⏹ Stop")

if not audio:
    st.info("Clique sur le micro pour commencer")

if audio:

    
    if len(audio["bytes"]) < 2000:
        st.warning("Aucun son détecté")
        st.stop()

    st.audio(audio["bytes"])

    with st.spinner("Analyse de la musique..."):

        titre, artiste = identifier_chantonnement(audio["bytes"])

        if titre:

            infos = generate_description(titre, artiste)

            st.markdown("---")

            st.subheader(" Résultat")

            st.markdown(f"### {infos['title']}")
            st.markdown(f"**Artiste :** {infos['artist']}")

            
            youtube_query = f"{infos['title']} {infos['artist']}".replace(" ", "+")
            youtube_url = f"https://www.youtube.com/results?search_query={youtube_query}"

            st.markdown(f"▶️ [Écouter la chanson sur YouTube]({youtube_url})")

          
            if infos.get("genre"):
                st.write(f" **Genre :** {infos['genre']}")

            if infos.get("year"):
                st.write(f"**Année :** {infos['year']}")

            st.markdown("---")

           
            st.markdown("###  À propos de la chanson")
            st.write(infos.get("song_description"))

            
            st.markdown("###  À propos de l'artiste")
            st.write(infos.get("artist_description"))

            st.markdown("---")

           
            st.markdown("###  Autres chansons de l'artiste")

            for song in infos.get("other_songs", []):
                st.write("", song)

        else:
            st.error("Musique non reconnue")