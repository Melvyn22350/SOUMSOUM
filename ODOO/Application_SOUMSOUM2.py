import xmlrpc.client
import tkinter as tk

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

    def get_manufacturing_orders(self):
        if self.uid is not None:
            try:
                orders = self.models.execute_kw(self.db, self.uid, self.password,
                                                'mrp.production', 'search_read',
                                                [[['name', 'like', 'PA']]],
                                                {'fields': ['name', 'product_id', 'date_planned_start', 'product_qty']})

                return orders
            except Exception as e:
                print(f"Erreur lors de la récupération des ordres de fabrication : {e}")
                return []
        else:
            print("Échec d'authentification. Vérifiez vos informations d'identification.")
            return []

def update_quantity(self, order_id, new_quantity):
        try:
            order_id = int(order_id)
            new_quantity = float(new_quantity)

            if new_quantity >= 0:
                self.models.execute_kw(self.db, self.uid, self.password,
                                        'mrp.production', 'write',
                                        [[order_id], {'product_qty': new_quantity}])
                print(f"Quantité de l'OF {order_id} mise à jour avec succès : {new_quantity}")
            else:
                print("La quantité doit être un nombre positif.")
        except ValueError:
            print("Veuillez entrer un nombre valide pour la quantité.")
        except Exception as e:
            print(f"Erreur lors de la mise à jour de la quantité : {e}")

def open_orders_page(orders_info, odoo_api):
    root = tk.Tk()
    root.title("Ordres de Fabrication")
    root.geometry("1000x800")

    label = tk.Label(root, text="Informations sur les ordres de fabrication :")
    label.pack(pady=20)

    def update_quantity(order_id, entry):
        new_quantity = entry.get()
        try:
            new_quantity = float(new_quantity)
            if new_quantity >= 0:
                odoo_api.update_quantity(order_id, new_quantity)
                # Mise à jour de l'interface graphique avec la nouvelle quantité
                entry.delete(0, tk.END)
                entry.insert(0, str(new_quantity))
            else:
                print("La quantité doit être un nombre positif.")
        except ValueError:
            print("Veuillez entrer un nombre valide pour la quantité.")

    if orders_info:
        for order_info in orders_info:
            order_label = tk.Label(root, text=f"OF: {order_info['name']} | "
                                             f"No de l'article: {order_info['product_id']} | "
                                             f"Date de fabrication: {order_info['date_planned_start']} | "
                                             f"Quantité à produire: {order_info['product_qty']}")
            order_label.pack()

            entry_label = tk.Label(root, text="Nouvelle quantité :")
            entry_label.pack()

            entry = tk.Entry(root)
            entry.pack()
            entry.insert(0, str(order_info['product_qty']))  # Pré-remplir le champ avec la quantité actuelle

            update_button = tk.Button(root, text="Mettre à jour la quantité",
                                      command=lambda order_id=order_info['name'], entry=entry: update_quantity(order_id, entry))
            update_button.pack()

            separator = tk.Frame(root, height=2, bd=1, relief=tk.SUNKEN)
            separator.pack(fill=tk.X, padx=5, pady=5)

    else:
        no_order_label = tk.Label(root, text="Aucun ordre de fabrication commençant par 'PA' trouvé.")
        no_order_label.pack()

    root.mainloop()

def get_orders_info(odoo_api):
    try:
        orders = odoo_api.models.execute_kw(odoo_api.db, odoo_api.uid, odoo_api.password,
                                            'mrp.production', 'search_read',
                                            [[['name', 'like', 'PA']]],
                                            {'fields': ['name', 'product_id', 'date_planned_start', 'product_qty']})

        orders_info = []

        if orders:
            for order in orders:
                orders_info.append({
                    'name': order['name'],
                    'product_id': order.get('product_id', 'N/A'),
                    'date_planned_start': order['date_planned_start'],
                    'product_qty': order['product_qty'],
                })

        return orders_info
    except Exception as e:
        print(f"Erreur lors de la récupération des informations des ordres de fabrication : {e}")
        return []

def Connect():
    url = "http://localhost:8069"
    db = "demo"
    username = "melvyn.dupas@gmail.com"
    password = "123456789"

    odoo_api = OdooAPI(url, db, username, password)

    if odoo_api.uid is not None:
        odoo_api.models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(odoo_api.url))
        return odoo_api
    else:
        print("Échec de l'authentification.")
        return None

if __name__ == "__main__":
    odoo_api = Connect()

    if odoo_api is not None:
        orders_info = get_orders_info(odoo_api)
        open_orders_page(orders_info, odoo_api)
    else:
        print("Échec de la connexion à Odoo.")
