import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_description(title, artist):

    prompt = f"""
    Tu es un expert en musique et en culture musicale.

    Fournis uniquement des informations réelles et connues sur cette chanson et cet artiste.

    Informations connues :

    Titre : {title}
    Artiste : {artist}

    Instructions importantes :

    - N'invente aucune information.
    - Si tu n'es pas sûr d'une information, laisse le champ vide ("").
    - La description de la chanson doit contenir 3 à 4 phrases.
    - La description de l'artiste doit contenir 4 à 5 phrases.
    - Les descriptions doivent être informatives, factuelles et claires.
    - other_songs doit contenir exactement 3 chansons populaires du même artiste.
    - Ne répète jamais la chanson "{title}" dans other_songs.
    - Réponds uniquement avec un objet JSON valide.
    - N'ajoute aucun texte avant ou après le JSON.

    Format de réponse attendu :

    {{
    "title": "{title}",
    "artist": "{artist}",
    "song_description": "",
    "artist_description": "",
    "genre": "",
    "year": "",
    "other_songs": ["", "", ""]
    }}
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}]
    )

    content = response.choices[0].message.content

    try:
        json_match = re.search(r"\{.*\}", content, re.DOTALL)
        data = json.loads(json_match.group())

    except:
        data = {
            "artist_description": "",
            "other_songs": []
        }

    return {
        "title": title,
        "artist": artist,
        **data
    }   