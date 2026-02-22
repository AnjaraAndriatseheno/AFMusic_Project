import streamlit as st
from streamlit_mic_recorder import mic_recorder
import os
from dotenv import load_dotenv

load_dotenv()

st.title("🎵 AFMusic - Test Micro")

st.write("Étape de validation : Enregistre-toi pour vérifier que le micro fonctionne.")

# Le bouton de ton collègue
audio = mic_recorder(
    start_prompt="Lancer l’écoute",
    stop_prompt="Stop",
    just_once=True
)

if audio:
    # 1. On affiche le lecteur audio pour vérifier le son
    st.audio(audio["bytes"])
    st.success("L'audio a été capturé avec succès !")

    # 2. On enregistre en fichier WAV pour l'étape suivante (Reconnaissance)
    with open("mon_chantonnement.wav", "wb") as f:
        f.write(audio["bytes"])
    
    st.write("Fichier 'mon_chantonnement.wav' créé avec succès.")
