import xmlrpc.client
import tkinter as tk
from tkinter import ttk

class OdooAPI:
    def __init__(self, url, db, username, password):
        self.url = url
        self.db = db
        self.username = username
        self.password = password
        self.common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        self.uid = self.authenticate()
        self.models = None

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
        except ValueError:
            print("Veuillez entrer un nombre valide pour la quantité produite.")
        except Exception as e:
            print(f"Erreur lors de la mise à jour de la quantité produite : {e}")

    def display_and_modify_orders(self):
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(self.url))
        uid = common.authenticate(self.db, self.username, self.password, {})

        if uid is not None:
            self.models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url))

            root = tk.Tk()
            root.title("Informations et Modification des Ordres de Fabrication - Odoo")
            self.set_icon(root)  # Ajoutez cette ligne pour définir l'icône

            tree = ttk.Treeview(root, columns=("Order ID", "Product Ref", "Date Planned", "Qty Producing", "Product Qty"), show="headings")
            tree.heading("Order ID", text="Order ID")
            tree.heading("Product Ref", text="Product Ref")
            tree.heading("Date Planned", text="Date Planned")
            tree.heading("Qty Producing", text="Qty Producing")
            tree.heading("Product Qty", text="Product Qty")  # Nouvelle colonne

            order_ids = self.get_order_ids()
            for order_id in order_ids:
                order_info = self.get_order_info(order_id)
                if order_info:
                    order_info = order_info[0]
                    product_ref = order_info.get('product_id', '')
                    date_planned = order_info.get('date_planned_start', '')
                    qty_producing = order_info.get('qty_producing', '')
                    product_qty = order_info.get('product_qty', '')  # Nouvelle variable pour la quantité du produit
                    tree.insert("", "end", iid=order_id, values=(order_id, product_ref, date_planned, qty_producing, product_qty))

            tree.pack(pady=10)

            id_label = tk.Label(root, text="Rentrez l'ID de l'ordre de fabrication afin de modifier la quantité produite :")
            id_label.pack(pady=10)

            id_entry = tk.Entry(root)
            id_entry.pack(pady=10)

            quantity_produced_label = tk.Label(root, text="Quantité produite actuelle :")
            quantity_produced_label.pack(pady=10)

            quantity_produced_entry = tk.Entry(root)
            quantity_produced_entry.pack(pady=10)

            def open_update_interface():
                order_id = id_entry.get()
                new_quantity_produced = quantity_produced_entry.get()
                self.update_quantity_produced(order_id, new_quantity_produced, tree)

            update_button = tk.Button(root, text="Mettre à jour la quantité produite", command=open_update_interface)
            update_button.pack(pady=10)

            # Fonction pour centrer la fenêtre après avoir créé tous les éléments graphiques
            def center_window():
                root.update_idletasks()
                screen_width = root.winfo_screenwidth()
                screen_height = root.winfo_screenheight()
                x_position = (screen_width - root.winfo_reqwidth()) // 2
                y_position = (screen_height - root.winfo_reqheight()) // 2
                root.geometry("+{}+{}".format(x_position, y_position))

            center_window()

            root.mainloop()
        else:
            print("Échec de l'authentification.")

    def set_icon(self, root):
        # Charger l'icône avec Pillow
        icon = tk.PhotoImage(file="/home/user/Téléchargements/SOUMSOUM.png")
        # Définir l'icône de la fenêtre
        root.tk.call('wm', 'iconphoto', root._w, icon)

if __name__ == "__main__":
    # Remplacez 'your_password' par votre mot de passe Odoo
    odoo_api = OdooAPI('http://localhost:8069', 'SOUMSOUMv2', 'melvyndupas01@gmail.com', '123456789')
    odoo_api.display_and_modify_orders()
