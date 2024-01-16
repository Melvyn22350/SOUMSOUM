import xmlrpc.client
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import io
import base64

class StockUpdaterGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Mise à jour du stock")
        self.set_icon()  # Ajoutez cette ligne pour définir l'icône
        self.create_widgets()
        self.tree.bind("<ButtonRelease-1>", self.show_selected_article_image)
        self.center_window()  # Centrer la fenêtre lors de l'initialisation

    def set_icon(self):
        # Charger l'icône avec Pillow
        icon = Image.open("/home/user/Téléchargements/SOUMSOUM.png")
        # Convertir l'icône en format Tkinter
        icon_tk = ImageTk.PhotoImage(icon)
        # Définir l'icône de la fenêtre
        self.master.iconphoto(True, icon_tk)

    def create_widgets(self):
        # Tableau pour afficher les informations sur les articles
        self.tree = ttk.Treeview(self.master, columns=("Nom", "Référence", "Prix", "Quantité en stock"))
        self.tree.heading("#0", text="ID")
        self.tree.heading("Nom", text="Nom de l'article")
        self.tree.heading("Référence", text="Référence")
        self.tree.heading("Prix", text="Prix")
        self.tree.heading("Quantité en stock", text="Quantité en stock")
        self.tree.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W)

        # Connexion à Odoo
        url = "http://localhost:8069"
        db = "SOUMSOUMv2"
        username = "melvyndupas01@gmail.com"
        password = "123456789"

        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

        # Récupérer les informations sur les articles depuis Odoo
        articles = models.execute_kw(db, uid, password, 'product.template', 'search_read', [], {'fields': ['id', 'name', 'default_code', 'list_price', 'qty_available']})

        # Remplir le tableau avec les informations récupérées
        for article in articles:
            self.tree.insert("", tk.END, text=article['id'], values=(article['name'], article['default_code'], "${:.2f}".format(article['list_price']), article['qty_available']))

        self.label_ref = ttk.Label(self.master, text="Référence de l'article:")
        self.label_ref.grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)

        self.entry_ref = ttk.Entry(self.master)
        self.entry_ref.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

        self.label_quantity = ttk.Label(self.master, text="Nouvelle quantité:")
        self.label_quantity.grid(row=2, column=0, padx=10, pady=10, sticky=tk.E)

        self.entry_quantity = ttk.Entry(self.master)
        self.entry_quantity.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

        self.button_update = ttk.Button(self.master, text="Mettre à jour le stock", command=self.update_stock)
        self.button_update.grid(row=3, column=0, columnspan=2, pady=20)

        # Ajout d'un widget pour afficher l'image
        self.image_label = tk.Label(self.master, text="Aucune image sélectionnée")
        self.image_label.grid(row=0, column=2, rowspan=4, padx=10, pady=10)

    def update_stock(self):
        article_default_code = self.entry_ref.get()
        new_quantity = max(0, int(self.entry_quantity.get()))

        # Connexion à Odoo
        url = "http://localhost:8069"
        db = "SOUMSOUMv2"
        username = "melvyndupas01@gmail.com"
        password = "123456789"

        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

        # Recherche de l'ID de l'article par la référence interne
        article_id = models.execute_kw(db, uid, password, 'product.template', 'search', [[('default_code', '=', article_default_code)]])
        
        if article_id:
            # Rechercher les entrées du modèle stock.quant associées à l'article
            stock_entries = models.execute_kw(db, uid, password, 'stock.quant', 'search_read', [
                [('product_id', '=', article_id[0])]
            ])

            if stock_entries:
                # Mettre à jour la quantité en remplaçant par la nouvelle quantité
                new_stock_quantity = new_quantity

                # Mettre à jour la stock.quant associée à l'article
                models.execute_kw(db, uid, password, 'stock.quant', 'write', [stock_entries[0]['id'], {'quantity': new_stock_quantity}])
                print("Quantité en stock mise à jour avec succès.")

                # Réinitialiser la fenêtre après la mise à jour
                self.master.destroy()
                root = tk.Tk()
                app = StockUpdaterGUI(root)
                root.mainloop()
            else:
                print("Aucune entrée stock.quant trouvée pour l'article.")
        else:
            print("Article non trouvé.")

    def show_selected_article_image(self, event):
        # Obtenir l'ID de l'article sélectionné
        selected_item_id = self.tree.item(self.tree.selection())['text']

        # Connexion à Odoo
        url = "http://localhost:8069"
        db = "SOUMSOUMv2"
        username = "melvyndupas01@gmail.com"
        password = "123456789"

        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

        # Récupérer l'image associée à l'article
        article_image = models.execute_kw(db, uid, password, 'product.template', 'read', [int(selected_item_id)], {'fields': ['image_1920']})

        if article_image and 'image_1920' in article_image[0]:
            # Afficher l'image dans la fenêtre
            image_data = article_image[0]['image_1920']
            image = Image.open(io.BytesIO(base64.b64decode(image_data)))
            image.thumbnail((500, 500))  # Ajuster la taille de l'image
            tk_image = ImageTk.PhotoImage(image)

            # Mettre à jour le widget Label avec la nouvelle image
            self.image_label.configure(image=tk_image, text="")
            self.image_label.image = tk_image
        else:
            # Aucune image trouvée, afficher un message
            self.image_label.configure(image=None, text="Aucune image disponible")

    def center_window(self):
        # Centrer la fenêtre sur l'écran
        self.master.update_idletasks()
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x_position = (screen_width - self.master.winfo_reqwidth()) // 2
        y_position = (screen_height - self.master.winfo_reqheight()) // 2
        self.master.geometry("+{}+{}".format(x_position, y_position))

def main():
    root = tk.Tk()
    app = StockUpdaterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

