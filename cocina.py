import tkinter as tk
import customtkinter as ctk
from dbconfig import *
from bson import ObjectId
import threading


def actualizar_cola_espera():
    pedidos = pedidos_collection.find({"estado": "En espera"})
    listbox_espera.delete(0, tk.END)
    for pedido in pedidos:
        ticket_info = f"Ticket {pedido['numero_pedido']} - {pedido['nombre']}\n"
        for producto in pedido['productos']:
            producto_info = productos_collection.find_one({"_id": producto['producto_id']})
            if producto_info:
                descripcion_producto = f"    {producto_info['nombre']} (x{producto['cantidad']}) - ${producto['precio']}\n"
                descripcion_producto += f"    Descripción: {producto_info['descripcion']}\n"
                ticket_info += descripcion_producto
        listbox_espera.insert(tk.END, ticket_info)
    root.after(5000, actualizar_cola_espera)  # Actualizar cada 5 segundos

def marcar_como_listo():
    selected_index = listbox_espera.curselection()
    if not selected_index:
        return
    selected_ticket_info = listbox_espera.get(selected_index)
    selected_ticket_id1 = selected_ticket_info.split()[1]
    selected_ticket_id2 = selected_ticket_info.split()[3]
    pedidos_collection.update_one({"numero_pedido": int(selected_ticket_id1), "nombre": selected_ticket_id2, "estado": "En espera"}, {"$set": {"estado": "Listo"}})
    #pedidos_collection.update_one({"_id": ObjectId(selected_ticket_id)}, {"$set": {"estado": "Listo"}})
    actualizar_cola_espera()

ctk.set_appearance_mode("System")  # O puedes usar "Dark" para modo oscuro
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.title("Control Cocina")

frame_principal = ctk.CTkFrame(root)
frame_principal.pack(pady=20, padx=20, fill="both", expand=True)

label_titulo = ctk.CTkLabel(frame_principal, text="Pedidos en Espera:", font=ctk.CTkFont(size=20, weight="bold"))
label_titulo.pack(pady=10)

# Crear un CTkFrame para el Listbox para aplicar estilo coherente
listbox_frame = ctk.CTkFrame(frame_principal, corner_radius=10)
listbox_frame.pack(pady=10, fill="both", expand=True)

# Configurar los colores manualmente
bg_color = "#2b2b2b"  # color de fondo similar a "Dark" mode
fg_color = "#ffffff"  # color de texto similar a "Light" mode

listbox_espera = tk.Listbox(listbox_frame, width=80, height=20, font=("Arial", 14), bg=bg_color, fg=fg_color)
listbox_espera.pack(pady=10, padx=10, fill="both", expand=True)

boton_marcar_listo = ctk.CTkButton(frame_principal, font=("Arial",15),text="Marcar como Listo", command=marcar_como_listo, corner_radius=10, width=200, height=40)
boton_marcar_listo.pack(pady=20)

actualizar_cola_espera()

root.mainloop()

