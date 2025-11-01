import os
import time
import subprocess

SCREEN_NAME = "SimpleBackUp"

def start():
    # läuft schon?
    res = subprocess.run(["screen", "-ls"], capture_output=True, text=True)
    if SCREEN_NAME.lower() in res.stdout.lower():
        print("[WARN] läuft schon.")
        return
    # screen startet unseren daemon
    # wichtig: wir rufen unser eigenes CLI mit "run" o.ä. auf – siehe __main__.py
    os.system(f"screen -dmS {SCREEN_NAME} bash -c 'SimpleBackUp run'")
    print("[OK] gestartet in screen.")

def stop():
    res = subprocess.run(["screen", "-ls"], capture_output=True, text=True)
    if SCREEN_NAME.lower() not in res.stdout.lower():
        print("[WARN] kein screen gefunden.")
        return
    os.system(f"screen -S {SCREEN_NAME} -X quit")
    print("[OK] screen beendet.")

def restart():
    stop()
    time.sleep(1)
    start()
