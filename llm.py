from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_music_insights(title, artist):
    """
    Génère des informations enrichies sur une musique et son artiste.
    """

    prompt = f"""
    Donne les informations suivantes pour la chanson "{title}" de {artist}.
    Réponds uniquement en JSON avec les clés suivantes :

    artist_description : courte description de l'artiste
    song_description : description de la chanson
    other_songs : liste de 3 autres chansons connues de l'artiste
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    content = response.choices[0].message.content

    # Convertir la réponse JSON en dict Python
    try:
        data = json.loads(content)
    except:
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
