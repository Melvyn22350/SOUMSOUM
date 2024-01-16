import xmlrpc.client
import tkinter as tk
from tkinter import ttk
import sys
import subprocess
import base64
from PIL import Image, ImageTk, ImageOps
import io


class OdooAPI:
    def __init__(self, url, db, username, password):
        self.url = url
        self.db = db
        self.username = username
        self.password = password
        self.common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        self.uid = self.authenticate()
        self.models = None
        self.root = None  # Garder une référence à la fenêtre principale

    def authenticate(self):
        try:
            uid = self.common.authenticate(self.db, self.username, self.password, {})
            return uid
        except Exception as e:
            print(f"Erreur d'authentification : {e}")
            return None

    def get_order_ids(self):
        try:
            order_ids = self.models.execute_kw(
                self.db, self.uid, self.password,
                'mrp.production', 'search',
                [[['state', 'in', ['confirmed', 'progress']]]]
            )
            return order_ids
        except Exception as e:
            print(f"Erreur lors de la récupération des numéros d'ordre de fabrication : {e}")
            return []

    def get_order_info(self, order_id):
        try:
            order_info = self.models.execute_kw(
                self.db, self.uid, self.password,
                'mrp.production', 'search_read',
                [[['id', '=', order_id]]],
                {'fields': ['name', 'product_id', 'date_planned_start', 'product_qty', 'qty_producing']}
            )
            return order_info
        except Exception as e:
            print(f"Erreur lors de la récupération de l'ordre de fabrication : {e}")
            return []

    def update_quantity_produced(self, order_id, new_quantity_produced, tree):
        try:
            order_id = int(order_id)
            new_quantity_produced = float(new_quantity_produced)

            if new_quantity_produced >= 0:
                order_info = self.get_order_info(order_id)
                if order_info:
                    order_info = order_info[0]
                    product_ref = order_info.get('product_id', '')
                    date_planned = order_info.get('date_planned_start', '')

                    # Mettre à jour la quantité produite dans Odoo
                    self.models.execute_kw(
                        self.db, self.uid, self.password,
                        'mrp.production', 'write',
                        [[order_id], {'qty_producing': new_quantity_produced}]
                    )
                    print(f"Quantité produite de l'OF {order_id} mise à jour avec succès : {new_quantity_produced}")

                    # Mettre à jour la quantité produite dans le tableau
                    product_qty = order_info.get('product_qty', '')
                    tree.item(order_id, values=(order_id, product_ref, date_planned, new_quantity_produced, product_qty))
                else:
                    print(f"Aucune information trouvée pour l'ordre de fabrication avec l'ID {order_id}")
            else:
                print("Veuillez entrer une quantité produite positive.")
        except ValueError:
            print("Veuillez entrer un nombre valide pour la quantité produite.")
        except Exception as e:
            print(f"Erreur lors de la mise à jour de la quantité produite : {e}")

    def display_article_image(self, event, article_id):
        try:
            # Récupérer l'image associée à l'article
            article_image = self.models.execute_kw(
                self.db, self.uid, self.password,
                'product.template', 'read',
                [int(article_id)],
                {'fields': ['image_1920']}
            )

            if article_image and 'image_1920' in article_image[0]:
                # Afficher l'image dans une nouvelle fenêtre
                image_data = article_image[0]['image_1920']
                image = Image.open(io.BytesIO(base64.b64decode(image_data)))
                image.thumbnail((500, 500))  # Ajuster la taille de l'image

                # Inverser les couleurs de l'image (optionnel)
                inverted_image = ImageOps.invert(image)

                tk_image = ImageTk.PhotoImage(inverted_image)

                # Créer une fenêtre pour afficher l'image
                image_window = tk.Toplevel()
                image_window.title("Image de l'article")

                # Ajouter un Label pour afficher l'image
                image_label = tk.Label(image_window, image=tk_image)
                image_label.image = tk_image
                image_label.pack()

                # Lancer la boucle principale de la fenêtre
                image_window.mainloop()
            else:
                # Aucune image trouvée, afficher un message
                print("Aucune image disponible pour cet article.")
        except Exception as e:
            print(f"Erreur lors de la récupération de l'image : {e}")

    def display_and_modify_orders(self):
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(self.url))
        uid = common.authenticate(self.db, self.username, self.password, {})

        if uid is not None:
            self.models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url))

            root = tk.Tk()
            root.title("Informations et Modification des Ordres de Fabrication - Odoo")

            # Changer la couleur de fond à une couleur sombre
            root.configure(bg='#333333')

            tree = ttk.Treeview(root, columns=("Ordre ID", "Réference Produit", "Date prévue", "Quantité Produite", "Stock Produit"), show="headings")
            tree.heading("Ordre ID", text="Ordre ID", anchor="center", command=lambda: self.sort_treeview(tree, "Ordre ID"))
            tree.heading("Réference Produit", text="Réference Produit", anchor="center", command=lambda: self.sort_treeview(tree, "Réference Produit"))
            tree.heading("Date prévue", text="Date prévue", anchor="center", command=lambda: self.sort_treeview(tree, "Date prévue"))
            tree.heading("Quantité Produite", text="Quantité Produite", anchor="center", command=lambda: self.sort_treeview(tree, "Quantité Produite"))
            tree.heading("Stock Produit", text="Stock Produit", anchor="center", command=lambda: self.sort_treeview(tree, "Stock Produit"))

            order_ids = self.get_order_ids()
            for order_id in order_ids:
                order_info = self.get_order_info(order_id)
                if order_info:
                    order_info = order_info[0]
                    product_ref = order_info.get('product_id', '')
                    date_planned = order_info.get('date_planned_start', '')
                    qty_producing = order_info.get('qty_producing', '')
                    product_qty = order_info.get('product_qty', '')

                    # Ajouter la ligne avec le gestionnaire d'événements
                    tree.insert("", "end", iid=order_id, values=(order_id, product_ref, date_planned, qty_producing, product_qty))
                    
                    # Lier la fonction display_article_image à l'événement de clic
                    tree.tag_bind(order_id, "<Button-1>", lambda event, id=product_ref: self.display_article_image(event, id))

            tree.pack(pady=10)

            id_label = tk.Label(root, text="Rentrez l'ID de l'ordre de fabrication afin de modifier la quantité produite :", fg="white", font=("Helvetica", 12, "bold"), highlightthickness=0, background='#333333')
            id_label.pack(pady=10)

            id_entry = tk.Entry(root)
            id_entry.pack(pady=10)

            quantity_produced_label = tk.Label(root, text="Quantité produite actuelle :", fg="white", font=("Helvetica", 12, "bold"), highlightthickness=0, background='#333333')
            quantity_produced_label.pack(pady=10)

            quantity_produced_entry = tk.Entry(root)
            quantity_produced_entry.pack(pady=10)

            def open_update_interface():
                order_id = id_entry.get()
                new_quantity_produced = quantity_produced_entry.get()
                self.update_quantity_produced(order_id, new_quantity_produced, tree)

            update_button = tk.Button(root, text="Mettre à jour la quantité produite", command=open_update_interface, fg="black", font=("Helvetica", 12, "bold"), highlightbackground='#333333')
            update_button.pack(pady=40)

            # Ajoute un bouton pour actualiser la fenêtre en la fermant
            restart_button = tk.Button(root, text="Actualiser la page", command=self.restart_program, fg="black", font=("Helvetica", 12, "bold"), highlightbackground='#333333')
            restart_button.pack(side="left", pady=75)

            # Ajoute un bouton pour quitter le programme
            quit_button = tk.Button(root, text="Déconnexion", command=lambda: self.quit_program(root), fg="black", font=("Helvetica", 12, "bold"), highlightbackground='#333333')
            quit_button.pack(side="right", pady=75)

            # Fonction pour centrer la fenêtre après avoir créé tous les éléments graphiques
            def center_window():
                root.update_idletasks()
                screen_width = root.winfo_screenwidth()
                screen_height = root.winfo_screenheight()
                x_position = (screen_width - root.winfo_reqwidth()) // 2
                y_position = (screen_height - root.winfo_reqheight()) // 2
                root.geometry("+{}+{}".format(x_position, y_position))

            center_window()

            # Ajout d'une gestion de fermeture de fenêtre
            root.protocol("WM_DELETE_WINDOW", lambda: self.close_program(root))

            self.set_icon(root)

            self.root = root  # Enregistrez la référence à la fenêtre principale

            root.mainloop()
        else:
            print("Échec de l'authentification.")


#=====================================================================
#=====================================================================
    def set_icon(self, root):
        # Charger l'icône avec Pillow
        icon = tk.PhotoImage(file="/home/user/Documents/SOUMSOUM/Image/SOUMSOUM_icon.png")
        # Définir l'icône de la fenêtre
        root.tk.call('wm', 'iconphoto', root._w, icon)
#=====================================================================
#=====================================================================
        

    def close_program(self, root):
        if root:
            root.destroy()

    def restart_program(self):
        # Ne redémarre le programme que s'il existe une fenêtre principale
        if self.root:
            self.close_program(self.root)
            self.display_and_modify_orders()  # Actualiser la page

    def quit_program(self, root):
        # Ajoutez le code pour quitter le programme ici
        print("Programme fermé.")
        # Redirigez vers la page de connexion (vous devez implémenter cette fonction)
        self.redirect_to_login(root)


#=====================================================================
#=====================================================================
    def redirect_to_login(self, root):
        print("Redirection vers la page de connexion.")
        root.destroy()
        subprocess.Popen([sys.executable, '/home/user/Documents/SOUMSOUM/Programme/Page_de_connection.py'])
#=====================================================================
#=====================================================================
        

    def sort_treeview(self, tree, column):
        items = [(tree.set(k, column), k) for k in tree.get_children('')]
        items.sort()
        for index, (val, k) in enumerate(items):
            tree.move(k, '', index)
        tree.heading(column, command=lambda: self.sort_treeview(tree, column))


#=====================================================================
#=====================================================================
if __name__ == "__main__":
    odoo_api = OdooAPI('http://localhost:8069', 'SOUMSOUM', 'melvyndupas01@gmail.com', '123456789')
    odoo_api.display_and_modify_orders()
#=====================================================================
#=====================================================================