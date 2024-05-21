Hola este es un avance de lo de software, es basicamente el prototipo.

1.- comida.py se supone es el CRUD del inventario de la cafeteria pero por el momento solo inserta
2.- main.py es la pantalla donde se supone que el que cobra hace los pedidos y genera el ticket, tiene una parte donde salen los productos de la base de datos, los selecciona y les agrega una cantidad, tmb el nombre del cliente 
    despues genera el ticket y se imprime pero en pantalla, la orden se sube a la base de datos a su coleccion correspondiente
3.- ticketer.py es el que accede a los datos de pedidos y genera el ticket
4.- pantalla.py es la pantalla que se supone que ven los clientes donde aparecen los pedidos en espera y los que estan listos, se actualiza cada 5 segundo por si cambia un pedido de en espera a listo
5.- cocina.py es la pantalla que se tiene en cocina donde ven los pedidos por hacer y que pueden actualizar a listo
6.- dbconfi es el archivo donde esta la configuracion para acceder a la base de datos, actualmente esta ligada a mi base de datos en la nube de mongoatlas, pero si quieren pueden cambiarlo a local como ya saben hacerlo

si ven esta hecho tkinter por facilidad de desarrollo, pero siempre podemos adaptarlo a web o ponerlo mas bonito con customtkinter u otra cosa que les parezca
