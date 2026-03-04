import requests
import os
import time
import hmac
import hashlib
import base64
from dotenv import load_dotenv

load_dotenv()

def identifier_chantonnement(audio_bytes):

    host = os.getenv("ACR_HOST")
    access_key = os.getenv("ACR_ACCESS_KEY")
    access_secret = os.getenv("ACR_ACCESS_SECRET")

    http_method = "POST"
    http_uri = "/v1/identify"
    data_type = "audio"
    signature_version = "1"

    timestamp = str(int(time.time()))

    # Création de la signature pour ACRCloud
    string_to_sign = "\n".join([
        http_method,
        http_uri,
        access_key,
        data_type,
        signature_version,
        timestamp
    ])

    sign = base64.b64encode(
        hmac.new(
            access_secret.encode("utf-8"),
            string_to_sign.encode("utf-8"),
            hashlib.sha1
        ).digest()
    ).decode("utf-8")

    url = f"https://{host}{http_uri}"

    files = {
        "sample": audio_bytes
    }

    data = {
        "access_key": access_key,
        "data_type": data_type,
        "signature_version": signature_version,
        "signature": sign,
        "timestamp": timestamp
    }

    try:
        response = requests.post(url, files=files, data=data)
        result = response.json()

        if result["status"]["msg"] == "Success":
            music = result["metadata"]["music"][0]

            title = music["title"]
            artist = music["artists"][0]["name"]

            return title, artist

    except Exception as e:
        print("Erreur reconnaissance :", e)

    return None, None