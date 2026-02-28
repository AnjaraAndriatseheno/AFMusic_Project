from groq import Groq
import os
import json

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_music_insights(title, artist):
    """
    Génère des informations enrichies sur une musique via Groq
    """

    prompt = f"""
    Tu es un assistant spécialisé en musique.

    Pour la chanson "{title}" de {artist}, fournis des informations fiables.

    IMPORTANT :
    - N'invente aucune information.
    - Si tu n'es pas sûr, indique "Information non disponible".
    - Les autres chansons doivent être des titres réels connus de l'artiste de la chanson reconnu.

    Réponds STRICTEMENT en JSON avec :

    artist_description
    song_description
    other_songs (liste de 3 titres maximum)
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    content = response.choices[0].message.content

    try:
        data = json.loads(content)
    except Exception:
        data = {
            "artist_description": content,
            "song_description": "",
            "other_songs": []
        }

    return {
        "title": title,
        "artist": artist,
        **data
    }