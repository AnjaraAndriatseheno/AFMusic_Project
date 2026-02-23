from dotenv import load_dotenv
from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

import streamlit as st
from streamlit_mic_recorder import mic_recorder
from recognition import identifier_chantonnement

st.title("🎵 AFMusic")

audio = mic_recorder(start_prompt="Lancer l’écoute", stop_prompt="Stop")

if audio:
    st.audio(audio["bytes"])

    titre, artiste = identifier_chantonnement(audio["bytes"])

    if titre:
        st.success("Musique reconnue ")
        st.subheader(f"{titre}")
        st.write(f"Artiste : {artiste}")
    else:
        st.error("Musique non reconnue.")