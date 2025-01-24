import tkinter as tk
from tkinter import PhotoImage
from yeelight import Bulb, BulbException

# Adresse IP des lampes
lampes = {
    "Salon": "192.168.1.2",
    "Chambre": "192.168.1.15",
    "Chambre David": "192.168.1.16",
    "Bureau": "192.168.1.17",
    "Cuisine": "192.168.1.8",
    "SDB": "192.168.1.6",
    "Bureau David": "192.168.1.10"
}

# Fonction pour changer l'état de la lampe
def toggle_lampe(nom, ip):
    try:
        bulb = Bulb(ip)
        if bulb.get_properties()["power"] == "on":
            bulb.turn_off()
            boutons[nom].config(image=bulb_off_icons[nom], bg="grey", activebackground="grey")
        else:
            bulb.turn_on()
            boutons[nom].config(image=bulb_on_icons[nom], bg="gold", activebackground="gold")
    except BulbException as e:
        print(f"Erreur avec {nom}: {e}")

# Fonction pour animer le bouton
def animate_button(bouton, couleur_initiale):
    bouton.config(bg="blue")  # Change la couleur à bleu temporairement
    root.after(100, lambda: bouton.config(bg=couleur_initiale))  # Reviens à la couleur initiale après 100ms

# Fonction appelée lors du clic sur le bouton
def on_button_click(nom, ip):
    toggle_lampe(nom, ip)
    animate_button(boutons[nom], boutons[nom].cget("bg"))

# Créer la fenêtre principale
root = tk.Tk()
root.title("Contrôle des lampes Yeelight")

# Masquer le pointeur de la souris
root.config(cursor="none")

# Mettre la fenêtre en plein écran
root.attributes('-fullscreen', True)

# Configurer la taille de la fenêtre pour un écran de 320x480 pixels
root.geometry("320x480")

# Dictionnaire pour stocker les boutons
boutons = {}
bulb_on_icons = {}
bulb_off_icons = {}

# Définir les dimensions et le style des boutons
button_font = ('Helvetica', 10, 'bold')  # Taille de la police ajustée pour s'adapter à l'écran

# Charger les icônes
for nom in lampes.keys():
    bulb_on_icons[nom] = PhotoImage(file="bulb_on.png")
    bulb_off_icons[nom] = PhotoImage(file="bulb_off.png")

# Créer un bouton pour chaque lampe et les organiser dans une grille
row = 0
col = 0
for nom, ip in lampes.items():
    bouton = tk.Button(root, text=nom, font=button_font, bg="grey", activebackground="grey", compound="top",
                       image=bulb_off_icons[nom], command=lambda n=nom, i=ip: on_button_click(n, i))
    bouton.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
    boutons[nom] = bouton
    
    col += 1
    if col > 1:  # Ajuster le nombre de colonnes selon votre préférence
        col = 0
        row += 1

# Configurer le poids des lignes et des colonnes pour qu'ils s'adaptent à la fenêtre
for i in range(row + 1):
    root.grid_rowconfigure(i, weight=1)
for j in range(2):  # Nombre de colonnes
    root.grid_columnconfigure(j, weight=1)

# Fonction pour mettre à jour l'état des boutons
def update_buttons():
    for nom, ip in lampes.items():
        try:
            bulb = Bulb(ip)
            if bulb.get_properties()["power"] == "on":
                boutons[nom].config(image=bulb_on_icons[nom], bg="gold", activebackground="gold")
            else:
                boutons[nom].config(image=bulb_off_icons[nom], bg="grey", activebackground="grey")
        except BulbException:
            boutons[nom].config(image=bulb_off_icons[nom], bg="grey", activebackground="grey")
    root.after(5000, update_buttons)  # Mettre à jour toutes les 5 secondes

update_buttons()

# Lancer la boucle principale
root.mainloop()