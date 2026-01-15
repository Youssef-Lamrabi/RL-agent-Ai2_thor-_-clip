import platform
import os
import sys
from ai2thor.controller import Controller

print(f"OS: {platform.system()} {platform.release()}")
print(f"Python: {sys.version}")
print("Test AI2-THOR...")

try:
    # Essayer de forcer le téléchargement avec local_build=False si dispo ?
    c = Controller(scene="FloorPlan1", width=300, height=300, download_only=True)
    print("Téléchargement Succès!")
except Exception as e:
    print(f"Erreur Download: {e}")

try:
    c = Controller(scene="FloorPlan1", width=300, height=300)
    print("Controller Succès!")
    c.stop()
except Exception as e:
    print(f"Erreur Controller: {e}")
    # import traceback
    # traceback.print_exc()
