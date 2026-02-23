from groq import Groq
import os
import json

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_music_insights(title, artist):

    prompt = f"""
    Donne les informations suivantes pour la chanson "{title}" de {artist}.
    Réponds uniquement en JSON avec les clés :

    artist_description
    song_description
    other_songs (liste de 3 titres)
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