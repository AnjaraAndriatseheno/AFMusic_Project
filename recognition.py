import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def identifier_musique(audio_bytes):

    transcription = client.audio.transcriptions.create(
        file=("audio.wav", audio_bytes),
        model="whisper-large-v3"
    )

    texte = transcription.text.strip()

    # DEBUG pour la démo
    print("Texte détecté :", texte)

    # ❗ ignorer silence ou bruit
    if len(texte) < 5:
        return None, None

    prompt = f"""
    Un utilisateur prononce des paroles ou le titre d'une chanson.

    Texte entendu :
    {texte}

    Identifie la chanson seulement si tu es sûr.

    Si tu n'es pas sûr réponds :

    {{"title": null, "artist": null}}

    Sinon réponds uniquement en JSON :

    {{
      "title": "",
      "artist": ""
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

        if not data["title"]:
            return None, None

        return data["title"], data["artist"]

    except:
        return None, None