import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import pandas as pd


class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion des Notes des Étudiants")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f4f7")

        # Appliquer un style moderne
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 12), padding=5)
        self.style.configure("TLabel", font=("Arial", 12), background="#f0f4f7")
        self.style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
        self.style.configure("Treeview", font=("Arial", 10), rowheight=30)

        # Liste des étudiants
        self.etudiants = []

        # Création de l'interface
        self.creer_interface()

    def creer_interface(self):
        # Menu
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        fichier_menu = tk.Menu(menu_bar, tearoff=0)
        fichier_menu.add_command(label="Générer un rapport", command=self.generer_rapport)
        fichier_menu.add_separator()
        fichier_menu.add_command(label="Quitter", command=self.root.quit)
        menu_bar.add_cascade(label="Fichier", menu=fichier_menu)

        # Section des entrées
        cadre_haut = tk.Frame(self.root, bg="#f0f4f7", bd=1, relief="solid")
        cadre_haut.pack(pady=20, padx=20, fill="x")

        ttk.Label(cadre_haut, text="Nom de l'étudiant:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entree_nom = ttk.Entry(cadre_haut, width=30)
        self.entree_nom.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(cadre_haut, text="Note:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entree_note = ttk.Entry(cadre_haut, width=30)
        self.entree_note.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(cadre_haut, text="Date d'inscription (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.entree_date = ttk.Entry(cadre_haut, width=30)
        self.entree_date.grid(row=2, column=1, padx=10, pady=10)

        ttk.Button(cadre_haut, text="Ajouter Étudiant", command=self.ajouter_etudiant).grid(row=3, column=1, pady=10)

        # Section de la liste des étudiants
        colonnes = ("Nom", "Note", "Date d'inscription")
        cadre_table = tk.Frame(self.root, bg="#ffffff", bd=1, relief="solid")
        cadre_table.pack(pady=20, padx=20, fill="both", expand=True)

        self.liste_etudiants = ttk.Treeview(cadre_table, columns=colonnes, show="headings")
        for col in colonnes:
            self.liste_etudiants.heading(col, text=col, anchor="center")
            self.liste_etudiants.column(col, anchor="center")
        self.liste_etudiants.pack(fill="both", expand=True)

        # Boutons de tri
        cadre_boutons = tk.Frame(self.root, bg="#f0f4f7")
        cadre_boutons.pack(pady=20, fill="x")

        ttk.Button(cadre_boutons, text="Trier par nom (Mergesort)", command=lambda: self.trier_etudiants('nom', 'mergesort')).pack(side="left", padx=10)
        ttk.Button(cadre_boutons, text="Trier par note (Quicksort)", command=lambda: self.trier_etudiants('note', 'quicksort')).pack(side="left", padx=10)
        ttk.Button(cadre_boutons, text="Trier par date (Mergesort)", command=lambda: self.trier_etudiants('date', 'mergesort')).pack(side="left", padx=10)

        ttk.Button(cadre_boutons, text="Générer un rapport", command=self.generer_rapport).pack(side="right", padx=10)

    def ajouter_etudiant(self):
        nom = self.entree_nom.get()
        note = self.entree_note.get()
        date_inscription = self.entree_date.get()

        if nom and note and date_inscription:
            try:
                note = float(note)
                date_obj = datetime.strptime(date_inscription, '%Y-%m-%d')
                self.etudiants.append({"nom": nom, "note": note, "date": date_obj})
                messagebox.showinfo("Succès", "Étudiant ajouté avec succès.")
                self.actualiser_liste()
            except ValueError:
                messagebox.showerror("Erreur", "Veuillez entrer une date valide (YYYY-MM-DD) et une note valide.")
        else:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")

        self.entree_nom.delete(0, tk.END)
        self.entree_note.delete(0, tk.END)
        self.entree_date.delete(0, tk.END)

    def trier_etudiants(self, critere, methode='mergesort'):
        if methode == 'mergesort':
            self.mergesort(self.etudiants, critere)
        elif methode == 'quicksort':
            self.quicksort(self.etudiants, critere)
        self.actualiser_liste()

    def mergesort(self, array, key):
        if len(array) > 1:
            mid = len(array) // 2
            L = array[:mid]
            R = array[mid:]

            self.mergesort(L, key)
            self.mergesort(R, key)

            i = j = k = 0
            while i < len(L) and j < len(R):
                if L[i][key] < R[j][key]:
                    array[k] = L[i]
                    i += 1
                else:
                    array[k] = R[j]
                    j += 1
                k += 1

            while i < len(L):
                array[k] = L[i]
                i += 1
                k += 1

            while j < len(R):
                array[k] = R[j]
                j += 1
                k += 1

    def quicksort(self, array, key, low=0, high=None):
        if high is None:
            high = len(array) - 1

        def partition(arr, low, high, key):
            pivot = arr[high][key]
            i = low - 1
            for j in range(low, high):
                if arr[j][key] <= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            return i + 1

        if low < high:
            pi = partition(array, low, high, key)
            self.quicksort(array, key, low, pi - 1)
            self.quicksort(array, key, pi + 1, high)

    def actualiser_liste(self):
        self.liste_etudiants.delete(*self.liste_etudiants.get_children())
        for etudiant in self.etudiants:
            self.liste_etudiants.insert("", "end", values=(etudiant["nom"], etudiant["note"], etudiant["date"].strftime('%Y-%m-%d')))

    def generer_rapport(self):
        if not self.etudiants:
            messagebox.showerror("Erreur", "Aucun étudiant dans le système.")
            return

        total_notes = sum(e["note"] for e in self.etudiants)
        moyenne = total_notes / len(self.etudiants)
        meilleur_etudiant = max(self.etudiants, key=lambda x: x["note"])
        pire_etudiant = min(self.etudiants, key=lambda x: x["note"])

        rapport = f"""
        Rapport des Performances des Étudiants
        =====================================
        Nombre total d'étudiants : {len(self.etudiants)}
        Note moyenne : {moyenne:.2f}
        Meilleur étudiant : {meilleur_etudiant["nom"]} (Note: {meilleur_etudiant["note"]})
        Pire étudiant : {pire_etudiant["nom"]} (Note: {pire_etudiant["note"]})

        Liste des étudiants triée par notes :
        """
        for etudiant in sorted(self.etudiants, key=lambda x: x["note"], reverse=True):
            rapport += f"\n{etudiant['nom']} - Note: {etudiant['note']}"

        # Afficher le rapport dans une boîte de dialogue
        messagebox.showinfo("Rapport", rapport)
        
        fichier = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")],
        title="Enregistrer le rapport sous"
        )
        if fichier:
            try:
                with open(fichier, "w", encoding="utf-8") as f:
                    f.write(rapport)
                messagebox.showinfo("Succès", f"Rapport enregistré avec succès dans {fichier}.")
            except Exception as e:
                messagebox.showerror("Erreur", f"Une erreur s'est produite lors de l'enregistrement : {e}")


# Lancer l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
