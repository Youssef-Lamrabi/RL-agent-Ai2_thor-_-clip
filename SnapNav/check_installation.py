#!/usr/bin/env python3
"""
Script de Vérification de l'Installation
Vérifie que toutes les dépendances sont installées correctement
"""

import sys

def check_installation():
    print("=" * 60)
    print("  Vérification de l'Installation - RL AI2-THOR")
    print("=" * 60)
    print()
    
    errors = []
    warnings = []
    
    # Check Python version
    print("1. Python Version:")
    print(f"   ✓ Python {sys.version.split()[0]}")
    print()
    
    # Check PyTorch
    print("2. PyTorch:")
    try:
        import torch
        print(f"   ✓ torch {torch.__version__}")
        print(f"   ✓ CUDA disponible: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"   ✓ CUDA version: {torch.version.cuda}")
        else:
            warnings.append("CUDA non disponible - le modèle utilisera le CPU (plus lent)")
    except ImportError as e:
        errors.append(f"PyTorch non installé: {e}")
        print(f"   ✗ PyTorch: ERREUR")
    print()
    
    # Check CLIP
    print("3. CLIP:")
    try:
        import clip
        print(f"   ✓ CLIP installé")
        # Test loading
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model, preprocess = clip.load("RN50", device=device)
        print(f"   ✓ CLIP RN50 chargé sur {device}")
    except ImportError as e:
        errors.append(f"CLIP non installé: {e}")
        print(f"   ✗ CLIP: ERREUR")
    except Exception as e:
        warnings.append(f"CLIP installé mais erreur au chargement: {e}")
        print(f"   ⚠ CLIP: Installé mais erreur au chargement")
    print()
    
    # Check AI2-THOR
    print("4. AI2-THOR:")
    try:
        import ai2thor
        from ai2thor.controller import Controller
        print(f"   ✓ ai2thor {ai2thor.__version__}")
    except ImportError as e:
        errors.append(f"AI2-THOR non installé: {e}")
        print(f"   ✗ AI2-THOR: ERREUR")
    print()
    
    # Check FastAPI
    print("5. FastAPI:")
    try:
        import fastapi
        import uvicorn
        print(f"   ✓ FastAPI installé")
        print(f"   ✓ uvicorn installé")
    except ImportError as e:
        errors.append(f"FastAPI/uvicorn non installé: {e}")
        print(f"   ✗ FastAPI: ERREUR")
    print()
    
    # Check other dependencies
    print("6. Autres dépendances:")
    deps = {
        "numpy": "numpy",
        "PIL": "Pillow",
        "tqdm": "tqdm",
        "websockets": "websockets",
    }
    
    for module, name in deps.items():
        try:
            __import__(module)
            print(f"   ✓ {name}")
        except ImportError:
            errors.append(f"{name} non installé")
            print(f"   ✗ {name}: MANQUANT")
    print()
    
    # Check pretrained model
    print("7. Modèle pré-entraîné:")
    import os
    model_dir = os.path.join(os.path.dirname(__file__), "pretrained_models")
    model_names = [
        "finetuned_floorplan1.pt",
        "exp_ObjectNav-RGB-ClipResNet50GRU-DDPPO__stage_02__steps_000415481616.pt",
    ]
    
    model_found = False
    for name in model_names:
        path = os.path.join(model_dir, name)
        if os.path.exists(path):
            size_mb = os.path.getsize(path) / (1024 * 1024)
            print(f"   ✓ {name} ({size_mb:.1f} MB)")
            model_found = True
            break
    
    if not model_found:
        errors.append("Aucun modèle pré-entraîné trouvé dans pretrained_models/")
        print(f"   ✗ AUCUN MODÈLE TROUVÉ")
        print(f"   → Télécharger depuis: https://github.com/allenai/procthor-rl")
    print()
    
    # Summary
    print("=" * 60)
    print("  RÉSUMÉ")
    print("=" * 60)
    print()
    
    if errors:
        print("❌ ERREURS CRITIQUES:")
        for error in errors:
            print(f"   • {error}")
        print()
    
    if warnings:
        print("⚠️  AVERTISSEMENTS:")
        for warning in warnings:
            print(f"   • {warning}")
        print()
    
    if not errors and not warnings:
        print("✅ TOUT EST INSTALLÉ CORRECTEMENT!")
        print()
        print("Prochaines étapes:")
        print("  1. Télécharger le modèle pré-entraîné (si pas déjà fait)")
        print("  2. Lancer: python find_object.py")
        print("  3. Ou lancer le serveur: python backend_server.py")
    elif not errors:
        print("✅ Installation fonctionnelle avec quelques avertissements")
        print()
        print("Le projet devrait fonctionner, mais vérifiez les avertissements ci-dessus.")
    else:
        print("❌ Installation incomplète")
        print()
        print("Installez les dépendances manquantes:")
        print("  pip install -r requirements.txt")
    
    print()
    print("=" * 60)
    
    return len(errors) == 0

if __name__ == "__main__":
    success = check_installation()
    sys.exit(0 if success else 1)
