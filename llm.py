import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_description(title, artist):

    prompt = f"""
    Tu es un expert en musique.

    Donne uniquement des informations réelles et connues sur cet artiste.

    Titre de la chanson : {title}
    Artiste : {artist}

    Instructions :
    - N'invente aucune information.
    - Si tu n'es pas sûr, laisse le champ vide.
    - Donne une description du son en 2 phrases max.
    - Donne exactement 3 chansons populaires du même artiste.
    - Ne répète pas "{title}".

    Réponds uniquement en JSON :

    {{
      "song_description":"",  
      "artist_description": "",
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