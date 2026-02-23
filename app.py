import streamlit as st
from streamlit_mic_recorder import mic_recorder
from recognition import identifier_chantonnement  
from llm import generate_music_insights   


st.set_page_config(
    page_title="AFMusic",
    page_icon="🎧",
    layout="centered"
)


st.markdown("""
<style>
.title {
    text-align: center;
    font-size: 5rem;
    font-weight: 700;
    margin-bottom: 25px;
}

.card {
    background-color: #161b22;
    padding: 25px;
    border-radius: 14px;
    margin-top: 20px;
    box-shadow: 0 6px 25px rgba(0,0,0,0.35);
}
</style>
""", unsafe_allow_html=True)


st.markdown('<div class="title">🎵 AFMusic</div>', unsafe_allow_html=True)

st.write("Clique sur le bouton pour écouter et reconnaître la musique")


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
