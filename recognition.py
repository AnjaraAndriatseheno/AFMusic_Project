import requests
import os
from dotenv import load_dotenv

load_dotenv()

def identifier_chantonnement(audio_bytes):
    """
    Envoie les données audio à l'API AudD pour identifier le chantonnement.
    """
    url = os.getenv("ACR_URL")
    api_token = os.getenv("AUDD_API_KEY")
    
    # On prépare le fichier audio (les octets provenant du micro)
    files = {'file': audio_bytes}
    data = {'api_token': api_token}
    
    try:
        # Appel à l'API spécialisée Humming/chantonnement
        response = requests.post(url, data=data, files=files)
        resultat = response.json()
        
        if resultat.get('status') == 'success' and resultat.get('result'):
            # On récupère le meilleur résultat (le premier de la liste)
            musique = resultat['result']['list'][0]
            return musique['title'], musique['artist']
            
    except Exception as e:
        print(f"Erreur technique reconnaissance : {e}")
        
    # Si rien n'est trouvé ou s'il y a une erreur
    return None, None