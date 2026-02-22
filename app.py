import streamlit as st
from streamlit_mic_recorder import mic_recorder


st.set_page_config(
    page_title="AFMusic",
    page_icon="🎧",
    layout="centered"
)


st.markdown("""
<style>
.title {
    text-align: center;
    font-size: 3rem;
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


audio = mic_recorder(
    start_prompt="Lancer l’écoute",
    stop_prompt="Stop",
    just_once=True,
    use_container_width=True
)


if audio:

    st.audio(audio["bytes"])

    st.info("Analyse du son en cours...")

    # 👉 ICI TU METS TON APPEL ACRCloud
    # Exemple données simulées
    title = "Blinding Lights"
    artist = "The Weeknd"
    description = "Titre pop synthwave sorti en 2019."
    similar_tracks = ["Save Your Tears", "In Your Eyes"]

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader(f"🎶 {title}")
    st.write(f"**Artiste :** {artist}")
    st.write(description)

    st.markdown("### Autres titres du même artiste")
    for track in similar_tracks:
        st.write(f"• {track}")

    st.markdown('</div>', unsafe_allow_html=True)
