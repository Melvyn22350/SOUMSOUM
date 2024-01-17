import xmlrpc.client
import tkinter as tk
import platform
import os
import sys
import subprocess
import base64
import io
import datetime
import ctypes
from ctypes import wintypes
from tkinter import ttk
from io import BytesIO
from PIL import Image, ImageTk, ImageOps


#====================================================================
#============= Application de Production ============================
#====================================================================


# Obtenir le nom du système d'exploitation
os_name = platform.system()
 
# Vérifier le système d'exploitation
if os_name == "Windows":
    print("Le systeme d'exploitation est Windows.")
elif os_name == "Linux":
    print("Le systeme d'exploitation est Linux.")
else:
    print(f"Le systeme d'exploitation est {os_name}.")
 
# Obtenir le chemin complet du script
chemin_script = os.path.abspath(os.path.realpath(__file__))
print(chemin_script)

# Obtenir le chemin du répertoire parent
repertoire_parent = os.path.dirname(chemin_script)
print(repertoire_parent)
 
class OdooAPI:
    def __init__(self, url, db, username, password):
        self.url = url
        self.db = db
        self.username = username
        self.password = password
        self.common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        self.uid = self.authenticate()
        self.models = None
        self.root = None
        self.status_column = "Statut de la Commande"
 
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
                {'fields': ['name', 'product_id', 'date_planned_start', 'product_qty', 'qty_producing', 'state']}
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
                    order_status = order_info.get('state', '')
 
                    # Mettre à jour la quantité produite dans Odoo
                    self.models.execute_kw(
                        self.db, self.uid, self.password,
                        'mrp.production', 'write',
                        [[order_id], {'qty_producing': new_quantity_produced}]
                    )
                    print(f"Quantité produite de l'OF {order_id} mise à jour avec succès : {new_quantity_produced}")
 
                    # Mettre à jour la quantité produite dans le tableau
                    product_qty = order_info.get('product_qty', '')
                    tree.item(order_id, values=(order_id, product_ref, date_planned, new_quantity_produced, product_qty, order_status))
                else:
                    print(f"Aucune information trouvée pour l'ordre de fabrication avec l'ID {order_id}")
            else:
                print("Veuillez entrer une quantité produite positive.")
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
            self.configure_root(root)
 
            tree = self.create_treeview(root)
            self.display_treeview(tree)
 
            id_label, id_entry, quantity_produced_label, quantity_produced_entry, style = self.create_user_interface(root, tree)
            self.create_buttons(root, tree, id_entry, quantity_produced_entry, style)
            
            root.protocol("WM_DELETE_WINDOW", lambda: self.close_program(root))
            self.set_icon(root)
            self.root = root
            self.center_window(root)
 
            root.mainloop()
        else:
            print("Échec de l'authentification.")
 
    def configure_root(self, root):
        root.title("Informations et Modification des Ordres de Fabrication - Odoo")
        root.configure(bg='#3498db')
 
    def create_treeview(self, root):
        tree = ttk.Treeview(root, columns=("Ordre ID", "Réference Produit", "Date prévue", "Quantité Produite", "Stock Produit", self.status_column), show="headings")
        self.configure_treeview(tree)
        return tree
 
    def configure_treeview(self, tree):
        tree.heading("Ordre ID", text="Ordre ID", anchor="center", command=lambda: self.sort_treeview(tree, "Ordre ID"))
        tree.heading("Réference Produit", text="Réference Produit", anchor="center", command=lambda: self.sort_treeview(tree, "Réference Produit"))
        tree.heading("Date prévue", text="Date prévue", anchor="center", command=lambda: self.sort_treeview(tree, "Date prévue"))
        tree.heading("Quantité Produite", text="Quantité Produite", anchor="center", command=lambda: self.sort_treeview(tree, "Quantité Produite"))
        tree.heading("Stock Produit", text="Stock Produit", anchor="center", command=lambda: self.sort_treeview(tree, "Stock Produit"))
        tree.heading(self.status_column, text=self.status_column, anchor="center", command=lambda: self.sort_treeview(tree, self.status_column))
 
        for col in ("Ordre ID", "Réference Produit", "Date prévue", "Quantité Produite", "Stock Produit", self.status_column):
            tree.column(col, anchor="center")
 
    def display_treeview(self, tree):
        order_ids = self.get_order_ids()
        for order_id in order_ids:
            order_info = self.get_order_info(order_id)
            if order_info:
                order_info = order_info[0]
                product_ref = order_info.get('product_id', '')
                date_planned = order_info.get('date_planned_start', '')
                qty_producing = order_info.get('qty_producing', '')
                product_qty = order_info.get('product_qty', '')
                order_status = order_info.get('state', '')
 
                today = datetime.datetime.today().strftime('%Y-%m-%d')
                date_style = 'green' if date_planned >= today else 'red'
 
                tree.insert("", "end", iid=order_id, values=(order_id, product_ref, date_planned, qty_producing, product_qty, order_status), tags=(date_style,))
 
        tree.tag_configure('red', foreground='red')
        tree.tag_configure('green', foreground='green')
 
        tree.pack(padx=10, pady=10)
 
    def create_user_interface(self, root, tree):
        id_label = tk.Label(root, text="ID de l'ordre de fabrication :", fg="white", font=("Helvetica", 12, "bold"), highlightthickness=0, bg='#3498db')
        id_label.pack(pady=10)
 
        id_entry = tk.Entry(root)
        id_entry.pack(pady=10)
 
        quantity_produced_label = tk.Label(root, text="Quantité produite actuelle :", fg="white", font=("Helvetica", 12, "bold"),
        highlightthickness=0, background='#3498db')
        quantity_produced_label.pack(pady=10)
 
        quantity_produced_entry = tk.Entry(root)
        quantity_produced_entry.pack(pady=10)
 
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 12, "bold"))
        
        style.map("Red.TButton",
                foreground=[('pressed', 'white'), ('active', 'white')],
                background=[('pressed', 'red'), ('active', 'red')])
 
        style.map("Green.TButton",
                foreground=[('pressed', 'white'), ('active', 'white')],
                background=[('pressed', 'green'), ('active', 'green')])
 
        return id_label, id_entry, quantity_produced_label, quantity_produced_entry, style
 
    def create_buttons(self, root, tree, id_entry, quantity_produced_entry, style):
        update_button = ttk.Button(root, text="Mettre à jour la quantité produite", command=lambda: self.update_quantity_produced(id_entry.get(), quantity_produced_entry.get(), tree), style="Green.TButton", cursor="hand2")
        update_button.pack(pady=60)
 
        restart_button = ttk.Button(root, text="Actualiser la page", command=self.restart_program, style="Green.TButton", cursor="hand2")
        restart_button.pack(side="left", padx=30, pady=30)
 
        quit_button = ttk.Button(root, text="Déconnexion", command=lambda: self.quit_program(root), style="Red.TButton", cursor="hand2")
        quit_button.pack(side="right", padx=30, pady=30)
 
    def center_window(self, root):
        root.update_idletasks()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_position = (screen_width - root.winfo_reqwidth()) // 2
        y_position = (screen_height - root.winfo_reqheight()) // 2
        root.geometry("+{}+{}".format(x_position, y_position))
 
    
#====================================================================
#====================================================================
    def set_icon(self, root):
        url = "http://172.31.11.79:8069"
        db = "SOUMSOUM"
        username = "melvyndupas01@gmail.com"
        password = "123456789"
#====================================================================
#====================================================================
        
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        
        if uid:
            models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
            company_data = models.execute_kw(db, uid, password,
                                            'res.company', 'read',
                                            [1], {'fields': ['logo']})
            if company_data and company_data[0].get('logo'):
                logo_data = company_data[0]['logo']
                try:
                    decoded_logo_data = base64.b64decode(logo_data)
                    logo_image = Image.open(BytesIO(decoded_logo_data))
                    logo_tk = ImageTk.PhotoImage(logo_image)
 
                    root.iconphoto(True, logo_tk)
                except Exception as e:
                    print(f"Erreur lors du traitement du logo : {e}")
            else:
                print("Logo non trouvé pour la société.")
        else:
            print("Échec de l'authentification. Veuillez vérifier vos identifiants.")

 
 
    def on_treeview_click(self, event, order_id, id_entry):
        id_entry.delete(0, tk.END)
        id_entry.insert(0, order_id)
 
    def close_program(self, root):
        if root:
            root.destroy()
 
    def restart_program(self):
        if self.root:
            self.close_program(self.root)
            self.display_and_modify_orders()
 
    def quit_program(self, root):
        print("Programme fermé.")
        self.redirect_to_login(root)
 
    def redirect_to_login(self, master):
        print("Redirection vers page de connexion.")
        self.master = master
        self.master.destroy()  # Fermez la fenêtre actuelle
        if os_name == "Windows":
            subprocess.Popen([sys.executable, f'{repertoire_parent}//Page_De_Connexion.py'])
        else:      
            subprocess.Popen([sys.executable, f'{repertoire_parent}//Page_De_Connexion.py'])

 
    def sort_treeview(self, tree, column):
        items = [(tree.set(k, column), k) for k in tree.get_children('')]
        items.sort()
        for index, (val, k) in enumerate(items):
            tree.move(k, '', index)
        tree.heading(column, command=lambda: self.sort_treeview(tree, column))
 
#====================================================================
#====================================================================
if __name__ == "__main__":
    odoo_api = OdooAPI('http://172.31.11.79:8069', 'SOUMSOUM', 'melvyndupas01@gmail.com', '123456789')
    odoo_api.display_and_modify_orders()
#====================================================================
#====================================================================
