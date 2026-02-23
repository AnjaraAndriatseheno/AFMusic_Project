import streamlit as st
from streamlit_mic_recorder import mic_recorder
from recognition import identifier_chantonnement  # Import du Back-end reconnaissance
from llm import generate_music_insights         # Import du Back-end IA

# --- DESIGN (Front-end) ---
st.set_page_config(page_title="AFMusic", page_icon="🎧")
st.markdown('<div class="title">🎵 AFMusic</div>', unsafe_allow_html=True) # Utilise le CSS de ton collègue

audio = mic_recorder(start_prompt="Lancer l’écoute", stop_prompt="Stop")

if audio:
    # On reste dans l'interface : on affiche ce qu'on fait
    st.audio(audio["bytes"])
    
    with st.spinner("Analyse en cours..."):
        # ON APPELLE LE BACK-END ICI
        titre, artiste = identifier_chantonnement(audio["bytes"])
        
        if titre:
            # ON APPELLE LE DEUXIÈME BACK-END (IA)
            infos_ia = generate_music_insights(titre, artiste)
            
            # AFFICHAGE FRONT-END (Dans la card du collègue)
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader(f"🎶 {titre}")
            st.write(f"**Artiste :** {artiste}")
            st.info(infos_ia.get('song_description'))
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("Musique non reconnue.") 