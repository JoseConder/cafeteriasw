import tkinter as tk
from dbconfig import *

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

root = tk.Tk()
root.title("Cola de Espera")

tk.Label(root, text="Pedidos en Espera:").pack(pady=10)
listbox_espera = tk.Listbox(root, width=50, height=10)
listbox_espera.pack()

tk.Label(root, text="Pedidos Listos:").pack(pady=10)
listbox_listos = tk.Listbox(root, width=50, height=10)
listbox_listos.pack()

actualizar_cola_espera()

root.mainloop()
