#!/usr/bin/env python3
"""
Script de téléchargement du modèle avec requests
"""

import os
import sys

try:
    import requests
    from tqdm import tqdm
except ImportError:
    print("Installation de requests et tqdm...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "tqdm"])
    import requests
    from tqdm import tqdm

def download_file_requests(url, save_path):
    """Télécharge un fichier avec requests et barre de progression."""
    print(f"Téléchargement depuis: {url}")
    print(f"Destination: {save_path}")
    print()
    
    # Créer le dossier si nécessaire
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    # Télécharger
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    total_size = int(response.headers.get('content-length', 0))
    
    with open(save_path, 'wb') as f, tqdm(
        desc="Téléchargement",
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                bar.update(len(chunk))
    
    print()
    print(f"✓ Téléchargement terminé!")
    print(f"  Fichier: {save_path}")
    print(f"  Taille: {os.path.getsize(save_path) / (1024*1024):.1f} MB")

if __name__ == "__main__":
    # Configuration
    MODEL_NAME = "exp_ObjectNav-RGB-ClipResNet50GRU-DDPPO__stage_02__steps_000415481616.pt"
    URL = f"https://pub-fbf23a0d54a0460882efdb338eb7282c.r2.dev/{MODEL_NAME}"
    SAVE_DIR = os.path.join(os.path.dirname(__file__), "pretrained_models")
    SAVE_PATH = os.path.join(SAVE_DIR, MODEL_NAME)
    
    print("=" * 60)
    print("  Téléchargement du Modèle ProcTHOR-RL CLIP-GRU")
    print("=" * 60)
    print()
    
    # Vérifier si le fichier existe déjà
    if os.path.exists(SAVE_PATH):
        size_mb = os.path.getsize(SAVE_PATH) / (1024*1024)
        print(f"✓ Le fichier existe déjà: {SAVE_PATH}")
        print(f"  Taille: {size_mb:.1f} MB")
        
        # Vérifier si la taille est correcte (environ 40 MB)
        if size_mb > 30:
            print()
            print("Le modèle semble déjà téléchargé correctement.")
            print("Téléchargement annulé.")
            exit(0)
        else:
            print("  ⚠ Taille incorrecte, re-téléchargement...")
    
    try:
        download_file_requests(URL, SAVE_PATH)
        print()
        print("=" * 60)
        print("✅ SUCCÈS!")
        print("=" * 60)
        print()
        print("Le modèle est prêt à être utilisé.")
        print("Vous pouvez maintenant lancer:")
        print("  python find_object.py")
        print("  ou")
        print("  python backend_server.py")
        print()
    except Exception as e:
        print()
        print("=" * 60)
        print("❌ ERREUR")
        print("=" * 60)
        print(f"Erreur lors du téléchargement: {e}")
        print()
        print("Veuillez télécharger manuellement depuis:")
        print(f"  {URL}")
        print(f"Et placer le fichier dans:")
        print(f"  {SAVE_DIR}")
        import traceback
        traceback.print_exc()
