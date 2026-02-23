from acrcloud.recognizer import ACRCloudRecognizer
import os

config = {
    "host": os.getenv("ACR_HOST"),
    "access_key": os.getenv("ACR_ACCESS_KEY"),
    "access_secret": os.getenv("ACR_ACCESS_SECRET"),
    "timeout": 10
}

recognizer = ACRCloudRecognizer(config)

def identifier_chantonnement(audio_bytes):
    try:
        result = recognizer.recognize_by_filebuffer(audio_bytes, 0)
        import json
        data = json.loads(result)

        if data["status"]["msg"] == "Success":
            music = data["metadata"]["music"][0]
            return music["title"], music["artists"][0]["name"]

    except Exception as e:
        print("Erreur ACRCloud:", e)

    return None, None