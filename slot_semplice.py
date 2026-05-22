import tkinter as tk
import random
from PIL import Image, ImageTk
import os

CARTELLA_IMG = os.path.join(os.path.dirname(__file__), "immagini")
DIMENSIONE   = (150, 150)  

NOMI_SIMBOLI = ["sette", "bar", "stella", "diamante", "trifoglio", "cuore"]

BG       = "#1a1a2e"
BG2      = "#16213e"
GOLD     = "#f5a623"        
VERDE    = "#4CAF50"
ROSSO    = "#e74c3c"
BIANCO   = "#ffffff"
RULLO_BG = "#0f3460"

crediti = 10

COLORI_PLACEHOLDER = {
    "sette":     ("#e74c3c", "7"),
    "bar":       ("#f5a623", "BAR"),
    "stella":    ("#f1c40f", "★"),
    "diamante":  ("#3498db", "♦"),
    "trifoglio": ("#2ecc71", "♣"),
    "cuore":     ("#e91e63", "♥"),
}

def carica_immagini():
    imgs = {}
    os.makedirs(CARTELLA_IMG, exist_ok=True)
    for nome in NOMI_SIMBOLI:
        percorso = os.path.join(CARTELLA_IMG, f"{nome}.png")
        if os.path.exists(percorso):
            img = Image.open(percorso).resize(DIMENSIONE, Image.LANCZOS)
        else:
            colore, testo = COLORI_PLACEHOLDER[nome]
            img = Image.new("RGB", DIMENSIONE, colore)
            from PIL import ImageDraw, ImageFont
            draw = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
            except Exception:
                font = ImageFont.load_default()
            bbox = draw.textbbox((0, 0), testo, font=font)
            x = (DIMENSIONE[0] - (bbox[2] - bbox[0])) // 2
            y = (DIMENSIONE[1] - (bbox[3] - bbox[1])) // 2
            draw.text((x, y), testo, fill="white", font=font)
        imgs[nome] = ImageTk.PhotoImage(img)
    return imgs

def gira():
    global crediti

    if crediti <= 0:
        risultato.config(text="Hai esaurito i crediti!", fg=ROSSO)
        return

    crediti -= 1
    aggiorna_crediti()

    s1 = random.choice(NOMI_SIMBOLI)
    s2 = random.choice(NOMI_SIMBOLI)
    s3 = random.choice(NOMI_SIMBOLI)

    rullo1.config(image=immagini[s1])
    rullo2.config(image=immagini[s2])
    rullo3.config(image=immagini[s3])

    if s1 == s2 == s3:
        crediti += 10
        risultato.config(text="HAI VINTO! +10 crediti", fg=GOLD)
    elif s1 == s2 or s2 == s3 or s1 == s3:
        crediti += 3
        risultato.config(text="Quasi! +3 crediti", fg=VERDE)
    else:
        risultato.config(text="Ritenta...", fg=ROSSO)

    aggiorna_crediti()

def aggiorna_crediti():
    label_crediti.config(text=f"Crediti: {crediti}")

finestra = tk.Tk()
finestra.title("Slot Machine")
finestra.configure(bg=BG)
finestra.attributes("-fullscreen", True)
finestra.bind("<Escape>", lambda e: finestra.attributes("-fullscreen", False))

immagini = carica_immagini()

tk.Label(finestra, text="SLOT MACHINE", font=("Arial", 48, "bold"),
         bg=BG, fg=GOLD).pack(pady=60)

frame_rulli = tk.Frame(finestra, bg=BG2, bd=4, relief="ridge")
frame_rulli.pack(pady=20)

stile_rullo = dict(bg=RULLO_BG, relief="sunken", bd=6,
                   width=DIMENSIONE[0], height=DIMENSIONE[1])

rullo1 = tk.Label(frame_rulli, image=immagini["sette"], **stile_rullo)
rullo1.grid(row=0, column=0, padx=15, pady=15)

rullo2 = tk.Label(frame_rulli, image=immagini["sette"], **stile_rullo)
rullo2.grid(row=0, column=1, padx=15, pady=15)

rullo3 = tk.Label(frame_rulli, image=immagini["sette"], **stile_rullo)
rullo3.grid(row=0, column=2, padx=15, pady=15)

risultato = tk.Label(finestra, text="Premi Gira per iniziare!",
                     font=("Arial", 22), bg=BG, fg=BIANCO)
risultato.pack(pady=20)

label_crediti = tk.Label(finestra, text=f"Crediti: {crediti}",
                          font=("Arial", 26, "bold"), bg=BG, fg=GOLD)
label_crediti.pack(pady=10)

tk.Button(finestra, text="GIRA!", font=("Arial", 24, "bold"),
          command=gira, bg=VERDE, fg=BIANCO,
          padx=30, pady=15, relief="flat", cursor="hand2").pack(pady=30)

tk.Label(finestra, text="ESC per uscire dal fullscreen",
         font=("Arial", 10), bg=BG, fg="#555577").pack(side="bottom", pady=10)

finestra.mainloop()
