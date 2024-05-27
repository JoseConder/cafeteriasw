import tkinter as tk
from dbconfig import *
import customtkinter as ctk


def actualizar_cola_espera():
    pedidos_espera = pedidos_collection.find({"estado": "En espera"})
    listbox_espera.delete(0, tk.END)
    for pedido in pedidos_espera:
        ticket_info = f"Ticket {pedido['numero_pedido']} - {pedido['nombre']} "
        listbox_espera.insert(tk.END, ticket_info)
    
    pedidos_listos = pedidos_collection.find({"estado": "Listo"})
    listbox_listos.delete(0, tk.END)
    for pedido in pedidos_listos:
        ticket_info = f"Ticket {pedido['numero_pedido']} - {pedido['nombre']} "
        listbox_listos.insert(tk.END, ticket_info)
    
    root.after(5000, actualizar_cola_espera)  # 

ctk.set_appearance_mode("System")  # O puedes usar "Dark" para modo oscuro
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.title("Cola de espera")

frame_principal = ctk.CTkFrame(root)
frame_principal.pack(pady=20, padx=20, fill="both", expand=True)


label_titulo_pe = ctk.CTkLabel(frame_principal, text="Pedidos en Espera:", font=ctk.CTkFont(size=20, weight="bold"))
label_titulo_pe.pack(pady=10)

# Crear un CTkFrame para el Listbox para aplicar estilo coherente
listbox_frame_pe = ctk.CTkFrame(frame_principal, corner_radius=10)
listbox_frame_pe.pack(pady=10, fill="both", expand=True)

# Configurar los colores manualmente
bg_color = "#2b2b2b"  # color de fondo similar a "Dark" mode
fg_color = "#ffffff"  # color de texto similar a "Light" mode

listbox_espera = tk.Listbox(listbox_frame_pe, width=50, height=20, font=("Arial", 14), bg=bg_color, fg=fg_color)
listbox_espera.pack(pady=10, padx=10, fill="both", expand=True)

# tk.Label(root, text="Pedidos en Espera:").pack(pady=10)
# listbox_espera = tk.Listbox(root, width=50, height=10)
# listbox_espera.pack()

label_titulo_pl = ctk.CTkLabel(frame_principal, text="Pedidos Listos:", font=ctk.CTkFont(size=20, weight="bold"))
label_titulo_pl.pack(pady=10)

# Crear un CTkFrame para el Listbox para aplicar estilo coherente
listbox_frame_pl = ctk.CTkFrame(frame_principal, corner_radius=10)
listbox_frame_pl.pack(pady=10, fill="both", expand=True)

# Configurar los colores manualmente
bg_color = "#2b2b2b" 
fg_color = "#ffffff"  

listbox_listos = tk.Listbox(listbox_frame_pl, width=50, height=20, font=("Arial", 14), bg=bg_color, fg=fg_color)
listbox_listos.pack(pady=10, padx=10, fill="both", expand=True)

# tk.Label(root, text="Pedidos Listos:").pack(pady=10)
# listbox_listos = tk.Listbox(root, width=50, height=10)
# listbox_listos.pack()

actualizar_cola_espera()

root.mainloop()

