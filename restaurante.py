import tkinter as tk
from tkinter import messagebox, simpledialog
import time

# ---------------------------
# Datos del restaurante
# ---------------------------
RESTAURANTE = "🍕 Ristorante La Bella Italia 🍝"

menu = {
    "menu_del_dia": [
        {"nombre": "Espaguetis a la carbonara", "precio": 12, "sin_gluten": False},
        {"nombre": "Ensalada Caprese", "precio": 10, "sin_gluten": True},
        {"nombre": "Pollo al horno con hierbas", "precio": 14, "sin_gluten": True}
    ],
    "carta": [
        {"nombre": "Pizza Margherita", "precio": 9, "sin_gluten": False},
        {"nombre": "Lasaña de carne", "precio": 11, "sin_gluten": False},
        {"nombre": "Risotto de setas", "precio": 13, "sin_gluten": True}
    ],
    "brunch": [
        {"nombre": "Tostadas con aguacate", "precio": 8, "sin_gluten": True},
        {"nombre": "Croissant relleno", "precio": 5, "sin_gluten": False},
        {"nombre": "Smoothie de frutas", "precio": 4, "sin_gluten": True}
    ],
    "bebidas": [
        {"nombre": "Agua 💧", "precio": 2, "alcohol": False},
        {"nombre": "Refresco 🥤", "precio": 3, "alcohol": False},
        {"nombre": "Vino tinto 🍷", "precio": 6, "alcohol": True},
        {"nombre": "Cerveza 🍺", "precio": 5, "alcohol": True}
    ]
}

# Disponibilidad de mesas
mesas_disponibles = {
    "Mesa 1": {"capacidad": 2, "ocupada": False, "emoji": "🟩"},
    "Mesa 2": {"capacidad": 4, "ocupada": False, "emoji": "🟩"},
    "Mesa 3": {"capacidad": 2, "ocupada": False, "emoji": "🟩"},
    "Mesa 4": {"capacidad": 6, "ocupada": False, "emoji": "🟩"}
}

pedidos_finales = []

# ---------------------------
# Funciones de negocio
# ---------------------------
def asignar_mesa(nombre_mesa, personas):
    info = mesas_disponibles[nombre_mesa]
    if info["ocupada"]:
        return False, "La mesa ya está ocupada."
    if info["capacidad"] < personas:
        return False, "La mesa no tiene suficiente capacidad."
    mesas_disponibles[nombre_mesa]["ocupada"] = True
    return True, f"Se ha asignado {nombre_mesa}."

def calcular_total(pedido):
    total = sum(item['precio'] for item in pedido)
    return total

# ---------------------------
# GUI con Tkinter
# ---------------------------
class RestauranteApp:
    def __init__(self, root):
        self.root = root
        self.root.title(RESTAURANTE)
        self.root.geometry("900x700")
        self.root.configure(bg="#FFF5E1")  # Fondo crema
        self.personas = 0
        self.cliente_actual = 0
        self.pedidos = []
        self.crear_pantalla_inicio()

    # ---------------------------
    # Pantalla de inicio
    # ---------------------------
    def crear_pantalla_inicio(self):
        self.limpiar_pantalla()
        tk.Label(self.root, text=RESTAURANTE, font=("Helvetica", 28, "bold"), bg="#FFF5E1").pack(pady=30)
        tk.Label(self.root, text="¡Bienvenido al mejor restaurante italiano!", font=("Helvetica", 18), bg="#FFF5E1").pack(pady=10)
        tk.Label(self.root, text="¿Cuántas personas serán?", font=("Helvetica", 16), bg="#FFF5E1").pack(pady=5)
        self.entrada_personas = tk.Entry(self.root, font=("Helvetica", 16), justify="center")
        self.entrada_personas.pack(pady=5)
        tk.Button(self.root, text="Siguiente ➡️", font=("Helvetica", 16, "bold"), bg="#FF5733", fg="white",
                  command=self.guardar_personas).pack(pady=20)

    def guardar_personas(self):
        try:
            valor = int(self.entrada_personas.get())
            if valor <= 0:
                raise ValueError
            self.personas = valor
            self.cliente_actual = 0
            self.pedidos = []
            self.crear_pantalla_mesas()
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número válido de personas.")

    # ---------------------------
    # Selección de mesa
    # ---------------------------
    def crear_pantalla_mesas(self):
        self.limpiar_pantalla()
        tk.Label(self.root, text="Seleccione su mesa disponible", font=("Helvetica", 20, "bold"), bg="#FFF5E1").pack(pady=10)

        frame = tk.Frame(self.root, bg="#FFF5E1")
        frame.pack(pady=20)
        mesas_validas = [nombre for nombre, info in mesas_disponibles.items() if not info["ocupada"] and info["capacidad"] >= self.personas]
        if not mesas_validas:
            tk.Label(self.root, text="No hay mesas disponibles para este número de personas.", font=("Helvetica", 16), fg="red", bg="#FFF5E1").pack(pady=20)
            tk.Button(self.root, text="⬅️ Volver", font=("Helvetica", 14), command=self.crear_pantalla_inicio).pack(pady=10)
            return

        for nombre in mesas_validas:
            info = mesas_disponibles[nombre]
            tk.Button(frame, text=f"{info['emoji']} {nombre}\nCapacidad: {info['capacidad']}", font=("Helvetica", 16, "bold"),
                      bg="green", fg="white", width=20, height=3,
                      command=lambda n=nombre: self.seleccionar_mesa(n)).pack(pady=5)

        tk.Button(self.root, text="⬅️ Atrás", font=("Helvetica", 14), command=self.crear_pantalla_inicio).pack(pady=20)

    def seleccionar_mesa(self, nombre_mesa):
        exito, msg = asignar_mesa(nombre_mesa, self.personas)
        if exito:
            self.mesa_asignada = nombre_mesa
            self.crear_pantalla_cliente()
        else:
            messagebox.showerror("Error", msg)

    # ---------------------------
    # Selección de menú y bebida por cliente
    # ---------------------------
    def crear_pantalla_cliente(self):
        if self.cliente_actual >= self.personas:
            self.crear_pantalla_pago()
            return

        self.limpiar_pantalla()
        tk.Label(self.root, text=f"Cliente {self.cliente_actual + 1}: elija su menú y bebida 🍽️🍹",
                 font=("Helvetica", 18, "bold"), bg="#FFF5E1").pack(pady=10)

        # Tipo de menú
        frame_menu = tk.Frame(self.root, bg="#FFF5E1")
        frame_menu.pack(pady=10)
        tk.Label(frame_menu, text="Tipo de menú:", font=("Helvetica", 16), bg="#FFF5E1").pack()
        self.tipo_menu_var = tk.StringVar()
        self.tipo_menu_var.set("menu_del_dia")
        opciones = [("Menú del día 🍝", "menu_del_dia"),
                    ("Carta 🍕", "carta"),
                    ("Brunch 🥪", "brunch"),
                    ("Sorpresa 🎁", "menu_del_dia")]
        for text, value in opciones:
            tk.Radiobutton(frame_menu, text=text, variable=self.tipo_menu_var, value=value,
                           font=("Helvetica", 14), bg="#FFF5E1").pack(anchor="w")

        # Plato
        tk.Label(frame_menu, text="Plato:", font=("Helvetica", 16), bg="#FFF5E1").pack(pady=5)
        self.plato_var = tk.StringVar()
        self.plato_var.set(menu[self.tipo_menu_var.get()][0]["nombre"])
        self.plato_menu = tk.OptionMenu(frame_menu, self.plato_var, *[p["nombre"] for p in menu[self.tipo_menu_var.get()]])
        self.plato_menu.config(font=("Helvetica", 14))
        self.plato_menu.pack()

        # Bebida
        tk.Label(frame_menu, text="Bebida:", font=("Helvetica", 16), bg="#FFF5E1").pack(pady=5)
        self.bebida_var = tk.StringVar()
        self.bebida_var.set(menu["bebidas"][0]["nombre"])
        self.bebida_menu = tk.OptionMenu(frame_menu, self.bebida_var, *[b["nombre"] for b in menu["bebidas"]])
        self.bebida_menu.config(font=("Helvetica", 14))
        self.bebida_menu.pack(pady=5)

        # Actualizar platos según tipo de menú
        self.tipo_menu_var.trace("w", self.actualizar_platos)

        # Botones
        frame_botones = tk.Frame(self.root, bg="#FFF5E1")
        frame_botones.pack(pady=20)
        tk.Button(frame_botones, text="⬅️ Atrás", font=("Helvetica", 14), command=self.cliente_atras).pack(side="left", padx=10)
        tk.Button(frame_botones, text="Siguiente ➡️", font=("Helvetica", 14, "bold"), bg="#FF5733", fg="white",
                  command=self.guardar_pedido_cliente).pack(side="right", padx=10)

    def actualizar_platos(self, *args):
        menu_seleccionado = self.tipo_menu_var.get()
        self.plato_var.set(menu[menu_seleccionado][0]["nombre"])
        menu_opciones = menu[menu_seleccionado]
        self.plato_menu['menu'].delete(0, 'end')
        for plato in menu_opciones:
            self.plato_menu['menu'].add_command(label=plato["nombre"], command=tk._setit(self.plato_var, plato["nombre"]))

    def cliente_atras(self):
        if self.cliente_actual == 0:
            self.crear_pantalla_mesas()
        else:
            self.cliente_actual -= 1
            self.pedidos.pop()
            self.crear_pantalla_cliente()

    def guardar_pedido_cliente(self):
        tipo_menu = self.tipo_menu_var.get()
        plato_seleccionado = next((p for p in menu[tipo_menu] if p["nombre"] == self.plato_var.get()), None)
        bebida_seleccionada = next((b for b in menu["bebidas"] if b["nombre"] == self.bebida_var.get()), None)

        # Edad para alcohol
        if bebida_seleccionada["alcohol"]:
            edad = simpledialog.askinteger("Edad", "Ingrese su edad para la bebida alcohólica:")
            if edad < 18:
                messagebox.showinfo("Aviso", "Menor de edad: se le asigna Agua 💧.")
                bebida_seleccionada = menu["bebidas"][0]

        self.pedidos.append([plato_seleccionado, bebida_seleccionada])
        self.cliente_actual += 1
        self.crear_pantalla_cliente()

    # ---------------------------
    # Pantalla de pago y propina
    # ---------------------------
    def crear_pantalla_pago(self):
        self.limpiar_pantalla()
        tk.Label(self.root, text="Resumen de pedidos y pago 💳", font=("Helvetica", 18, "bold"), bg="#FFF5E1").pack(pady=10)
        total_por_cliente = [calcular_total(p) for p in self.pedidos]
        for i, total in enumerate(total_por_cliente):
            tk.Label(self.root, text=f"Cliente {i+1}: {total}€", font=("Helvetica", 16), bg="#FFF5E1").pack()

        tk.Label(self.root, text="¿Desea pagar en conjunto o por separado?", font=("Helvetica", 16), bg="#FFF5E1").pack(pady=10)
        self.pago_var = tk.StringVar()
        self.pago_var.set("conjunto")
        tk.Radiobutton(self.root, text="Conjunto", variable=self.pago_var, value="conjunto", font=("Helvetica", 14), bg="#FFF5E1").pack()
        tk.Radiobutton(self.root, text="Separado", variable=self.pago_var, value="separado", font=("Helvetica", 14), bg="#FFF5E1").pack()

        tk.Button(self.root, text="Finalizar pago ✅", font=("Helvetica", 14, "bold"), bg="#28B463", fg="white",
                  command=self.finalizar_pago).pack(pady=20)
        tk.Button(self.root, text="⬅️ Atrás", font=("Helvetica", 14), command=self.cliente_atras).pack()

    def finalizar_pago(self):
        if self.pago_var.get() == "separado":
            for i, p in enumerate(self.pedidos):
                total = calcular_total(p)
                messagebox.showinfo("Cobro", f"Cliente {i+1} debe pagar: {total}€")
        else:
            total = sum([calcular_total(p) for p in self.pedidos])
            messagebox.showinfo("Cobro", f"Pago en conjunto: {total}€")

        propina = simpledialog.askfloat("Propina", "Ingrese propina (0 si no desea dejar):")
        if propina and propina > 0:
            messagebox.showinfo("Gracias", f"¡Gracias por su propina de {propina}€!")

        self.crear_pantalla_resumen()

    # ---------------------------
    # Pantalla final y mapa
    # ---------------------------
    def crear_pantalla_resumen(self):
        self.limpiar_pantalla()
        tk.Label(self.root, text="¡Gracias por visitar nuestro restaurante! 🎉", font=("Helvetica", 18, "bold"), bg="#FFF5E1").pack(pady=20)
        tiempo_espera = 10 + 5 * self.personas
        tk.Label(self.root, text=f"Tiempo aproximado de comida: {tiempo_espera} minutos ⏱️", font=("Helvetica", 16), bg="#FFF5E1").pack(pady=10)
        tk.Label(self.root, text=f"Su mesa: {self.mesa_asignada} 🪑", font=("Helvetica", 16), bg="#FFF5E1").pack(pady=10)

        # Mapa del restaurante con camino a la mesa
        mapa = "🍳 Cocina   🚻 Baños   🍹 Barra   🌿 Terraza\n\n"
        for nombre, info in mesas_disponibles.items():
            if info["ocupada"]:
                emoji = "🔴"  # ocupado
            else:
                emoji = "🟩"  # libre
            if nombre == self.mesa_asignada:
                emoji = "➡️"  # camino hacia la mesa
            mapa += f"{nombre}: {emoji}\n"
        tk.Label(self.root, text=mapa, font=("Helvetica", 14), bg="#FFF5E1", justify="left").pack(pady=20)

        tk.Button(self.root, text="Volver al inicio 🔄", font=("Helvetica", 16, "bold"), bg="#FF5733", fg="white",
                  command=self.crear_pantalla_inicio).pack(pady=20)

    # ---------------------------
    # Limpiar pantalla
    # ---------------------------
    def limpiar_pantalla(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# ---------------------------
# Ejecutar aplicación
# ---------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = RestauranteApp(root)
    root.mainloop()
