import xmlrpc.client
import tkinter as tk
import io
import base64
import sys
import subprocess

class StockUpdaterGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Mise à jour du stock")
        self.set_icon()
        self.create_widgets()
        self.tree.bind("<ButtonRelease-1>", self.show_selected_article_image)
        self.center_window()

    def set_icon(self):
        # Charger l'icône avec Pillow
        icon = Image.open("/home/user/Documents/SOUMSOUM/Image/SOUMSOUM_icon.png")
        # Convertir l'icône en format Tkinter
        icon_tk = ImageTk.PhotoImage(icon)
        # Définir l'icône de la fenêtre
        self.master.iconphoto(True, icon_tk)
#=====================================================================
#=====================================================================
        

    def create_widgets(self):
        self.tree = ttk.Treeview(self.master, columns=("Nom", "Référence", "Prix", "Quantité en stock"))
        self.tree.heading("#0", text="ID")
        self.tree.heading("Nom", text="Nom de l'article", anchor=tk.CENTER)
        self.tree.heading("Référence", text="Référence", anchor=tk.CENTER)
        self.tree.heading("Prix", text="Prix", anchor=tk.CENTER)
        self.tree.heading("Quantité en stock", text="Quantité en stock", anchor=tk.CENTER)
        self.tree.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W)

        # Centrer le texte dans chaque colonne
        for col in ("Nom", "Référence", "Prix", "Quantité en stock"):
            self.tree.column(col, anchor=tk.CENTER)

        url = "http://172.31.11.79:8069"
        db = "SOUMSOUM"
        username = "melvyndupas01@gmail.com"
        password = "123456789"

        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

        articles = models.execute_kw(db, uid, password, 'product.template', 'search_read', [], {'fields': ['id', 'name', 'default_code', 'list_price', 'qty_available']})

        for article in articles:
            self.tree.insert("", tk.END, text=article['id'], values=(article['name'], article['default_code'], "${:.2f}".format(article['list_price']), article['qty_available']))

        self.label_ref = ttk.Label(self.master, text="Référence de l'article:", font=("Helvetica", 10, "bold"), foreground="white", background="#3498db")
        self.label_ref.grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)

        self.entry_ref = ttk.Entry(self.master)
        self.entry_ref.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

        self.label_quantity = ttk.Label(self.master, text="Nouvelle quantité:", font=("Helvetica", 10, "bold"), foreground="white", background="#3498db")
        self.label_quantity.grid(row=2, column=0, padx=10, pady=10, sticky=tk.E)

        self.entry_quantity = ttk.Entry(self.master)
        self.entry_quantity.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

        # Créer un style pour les boutons
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 12, "bold"))

        # Définir le style pour le bouton de déconnexion avec la couleur rouge
        style.map("Red.TButton",
                  foreground=[('pressed', 'white'), ('active', 'white')],
                  background=[('pressed', 'red'), ('active', 'red')])

        # Définir le style pour le bouton de mise à jour avec la couleur verte
        style.map("Green.TButton",
                  foreground=[('pressed', 'white'), ('active', 'white')],
                  background=[('pressed', 'green'), ('active', 'green')])

        self.button_update = ttk.Button(self.master, text="Mettre à jour le stock", command=self.update_stock, style="Green.TButton", cursor="hand2")
        self.button_update.grid(row=3, column=0, columnspan=2, pady=20)

        quit_button = ttk.Button(self.master, text="Déconnexion", command=self.quit_program, style="Red.TButton", cursor="hand2")
        quit_button.grid(row=4, column=0, columnspan=2, pady=20)

        # Initialiser le texte de l'étiquette de l'image
        self.selected_reference_text = StringVar(value="Sélectionner une référence")
        self.image_label = tk.Label(self.master, textvariable=self.selected_reference_text)
        self.image_label.grid(row=0, column=2, rowspan=4, padx=10, pady=10)

    def update_stock(self):
        article_default_code = self.entry_ref.get()
        new_quantity = max(0, int(self.entry_quantity.get()))

        url = "http://172.31.11.79:8069"
        db = "SOUMSOUM"
        username = "melvyndupas01@gmail.com"
        password = "123456789"

        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

        article_id = models.execute_kw(db, uid, password, 'product.template', 'search', [[('default_code', '=', article_default_code)]])
        
        if article_id:
            stock_entries = models.execute_kw(db, uid, password, 'stock.quant', 'search_read', [
                [('product_id', '=', article_id[0])]
            ])

            if stock_entries:
                new_stock_quantity = new_quantity

                models.execute_kw(db, uid, password, 'stock.quant', 'write', [stock_entries[0]['id'], {'quantity': new_stock_quantity}])
                print("Quantite en stock mise à jour avec succes.")

                self.master.destroy()
                root = tk.Tk()
                app = StockUpdaterGUI(root)
                app.configure_bg_color('#3498db')  # Ajouter cette ligne pour restaurer la couleur de fond
                root.mainloop()
            else:
                print("Aucune entree stock.quant trouvee pour l'article.")
        else:
            print("Article non trouve.")

    def show_selected_article_image(self, event):
        selected_item_id = self.tree.item(self.tree.selection())['text']
        selected_item_ref = self.tree.item(self.tree.selection())['values'][1]

        self.entry_ref.delete(0, tk.END)  # Effacer le contenu actuel
        self.entry_ref.insert(0, selected_item_ref)  # Insérer la référence sélectionnée

        url = "http://172.31.11.79:8069"
        db = "SOUMSOUM"
        username = "melvyndupas01@gmail.com"
        password = "123456789"

        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

        article_image = models.execute_kw(db, uid, password, 'product.template', 'read', [int(selected_item_id)], {'fields': ['image_1920']})

        if article_image and 'image_1920' in article_image[0]:
            image_data = article_image[0]['image_1920']
            image = Image.open(io.BytesIO(base64.b64decode(image_data)))
            image.thumbnail((500, 500))
            tk_image = ImageTk.PhotoImage(image)

            self.selected_reference_text.set("")  # Réinitialiser le texte
            self.image_label.configure(image=tk_image)
            self.image_label.image = tk_image
        else:
            self.selected_reference_text.set("Sélectionner une référence")
            self.image_label.configure(image=None)

    def center_window(self):
        self.master.update_idletasks()
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x_position = (screen_width - self.master.winfo_reqwidth()) // 2
        y_position = (screen_height - self.master.winfo_reqheight()) // 2
        self.master.geometry("+{}+{}".format(x_position, y_position))

    def configure_bg_color(self, color):
        self.master.configure(bg=color)

    def quit_program(self):
        # Ajoutez le code pour quitter le programme ici
        print("Programme fermé.")
        # Redirigez vers le programme Page_de_connection_V2.py
        self.redirect_to_login()

    def redirect_to_login(self):
        print("Redirection vers page de connexion.")
        self.master.destroy()  # Fermez la fenêtre actuelle
        subprocess.Popen([sys.executable, '/home/user/Documents/SOURCE/SOUMSOUM/SOUMSOUM Version 4/Page_de_connection.py'])
#=====================================================================
#=====================================================================


def main():
    root = tk.Tk()
    app = StockUpdaterGUI(root)
    # Changer la couleur de fond en bleu
    app.configure_bg_color('#3498db')
    root.mainloop()

if __name__ == "__main__":
    main()
