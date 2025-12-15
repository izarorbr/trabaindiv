import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Librería PIL para manejar imágenes

# -----------------------------
# Datos de los animales
# -----------------------------
animales = {
    "León": {"tipo": "Mamífero", "horario": "10:00-18:00", "alimentación": "Carnívoro", 
             "curiosidades": "Rey de la selva, vive en manadas", "imagen": "imagenes/leon.png"},
    "Elefante": {"tipo": "Mamífero", "horario": "09:00-17:00", "alimentación": "Herbívoro", 
                 "curiosidades": "Mamífero más grande terrestre", "imagen": "imagenes/elefante.png"},
    "Pingüino": {"tipo": "Ave", "horario": "11:00-16:00", "alimentación": "Pescador", 
                 "curiosidades": "Ave que no vuela, nada muy bien", "imagen": "imagenes/pinguino.png"},
    "Tigre": {"tipo": "Mamífero", "horario": "10:00-18:00", "alimentación": "Carnívoro", 
              "curiosidades": "Felino ágil y fuerte, rayas distintivas", "imagen": "imagenes/tigre.png"},
    "Jirafa": {"tipo": "Mamífero", "horario": "09:00-17:00", "alimentación": "Herbívoro", 
               "curiosidades": "Cuello largo para alcanzar hojas altas", "imagen": "imagenes/jirafa.png"},
    "Cocodrilo": {"tipo": "Reptil", "horario": "10:00-18:00", "alimentación": "Carnívoro", 
                   "curiosidades": "Depredador de ríos y lagunas", "imagen": "imagenes/cocodrilo.png"},
    "Loro": {"tipo": "Ave", "horario": "10:00-17:00", "alimentación": "Frutas y semillas", 
             "curiosidades": "Ave colorida que imita sonidos", "imagen": "imagenes/loro.png"},
    # ... Añadir más animales
}

# Shows del zoo
shows = {
    "Show de aves": "12:00 y 15:00",
    "Alimentación de leones": "13:00",
    "Baile de pingüinos": "14:30"
}

# Rutas recomendadas (simples)
rutas_recomendadas = {
    "Ruta 1": ["León", "Tigre", "Elefante", "Jirafa"],
    "Ruta 2": ["Jirafa", "Pingüino", "Loro", "León"],
    "Ruta 3": ["Elefante", "Jirafa", "Tigre", "Cocodrilo"]
}

# -----------------------------
# Funciones del programa
# -----------------------------
def mostrar_info_animal():
    animal = lista_animales.get(tk.ACTIVE)
    if animal:
        info = animales[animal]
        # Mostrar ventana con imagen y datos
        ventana_info = tk.Toplevel()
        ventana_info.title(animal)
        ventana_info.geometry("350x400")
        ventana_info.configure(bg="#f0f0f0")
        
        img = Image.open(info["imagen"])
        img = img.resize((150, 150), Image.ANTIALIAS)
        img_tk = ImageTk.PhotoImage(img)
        label_img = tk.Label(ventana_info, image=img_tk)
        label_img.image = img_tk
        label_img.pack(pady=10)

        texto = f"Tipo: {info['tipo']}\nHorario: {info['horario']}\nAlimentación: {info['alimentación']}\nCuriosidades: {info['curiosidades']}"
        label_texto = tk.Label(ventana_info, text=texto, bg="#f0f0f0", font=("Arial", 12))
        label_texto.pack(pady=10)

def generar_ruta_personalizada():
    seleccion = lista_animales.curselection()
    if not seleccion:
        messagebox.showwarning("Atención", "Debes seleccionar al menos un animal")
        return
    seleccion_animales = [lista_animales.get(i) for i in seleccion]
    
    mejor_ruta = None
    max_animales = 0
    for nombre_ruta, animales_ruta in rutas_recomendadas.items():
        conteo = sum(a in animales_ruta for a in seleccion_animales)
        if conteo > max_animales:
            max_animales = conteo
            mejor_ruta = nombre_ruta
    
    ruta_text = f"Te recomendamos la {mejor_ruta} que incluye: {', '.join(rutas_recomendadas[mejor_ruta])}"
    messagebox.showinfo("Ruta recomendada", ruta_text)

def mostrar_shows():
    texto = "\n".join([f"{show}: {hora}" for show, hora in shows.items()])
    messagebox.showinfo("Shows del zoo", texto)

def guardar_plan_visita():
    seleccion = lista_animales.curselection()
    seleccion_animales = [lista_animales.get(i) for i in seleccion]
    with open("plan_visita.txt", "w") as f:
        for animal in seleccion_animales:
            f.write(animal + "\n")
    messagebox.showinfo("Guardado", "Tu plan de visita ha sido guardado en 'plan_visita.txt'")

# -----------------------------
# Interfaz gráfica
# -----------------------------
ventana = tk.Tk()
ventana.title("Zoo Explorer Deluxe")
ventana.geometry("800x600")
ventana.configure(bg="#e6f2ff")

titulo = tk.Label(ventana, text="Bienvenido a Zoo Explorer Deluxe", font=("Arial", 18, "bold"), bg="#e6f2ff")
titulo.pack(pady=10)

frame_principal = tk.Frame(ventana, bg="#e6f2ff")
frame_principal.pack(pady=10, fill="both", expand=True)

# Panel izquierdo: lista de animales
frame_izq = tk.Frame(frame_principal, bg="#cce6ff", padx=10, pady=10)
frame_izq.pack(side="left", fill="y")

label_animales = tk.Label(frame_izq, text="Selecciona animales:", bg="#cce6ff", font=("Arial", 14))
label_animales.pack(pady=5)

lista_animales = tk.Listbox(frame_izq, selectmode=tk.MULTIPLE, width=25, height=20, font=("Arial", 12))
for animal in animales:
    lista_animales.insert(tk.END, animal)
lista_animales.pack(pady=5)

btn_info = tk.Button(frame_izq, text="Ver información", command=mostrar_info_animal, bg="#3399ff", fg="white", font=("Arial", 12))
btn_info.pack(pady=5, fill="x")

btn_ruta = tk.Button(frame_izq, text="Generar ruta", command=generar_ruta_personalizada, bg="#33cc33", fg="white", font=("Arial", 12))
btn_ruta.pack(pady=5, fill="x")

btn_shows = tk.Button(frame_izq, text="Ver shows", command=mostrar_shows, bg="#ff9933", fg="white", font=("Arial", 12))
btn_shows.pack(pady=5, fill="x")

btn_guardar = tk.Button(frame_izq, text="Guardar plan", command=guardar_plan_visita, bg="#cc33ff", fg="white", font=("Arial", 12))
btn_guardar.pack(pady=5, fill="x")

# Panel derecho: mapa del zoo (puede ser una imagen de fondo)
frame_der = tk.Frame(frame_principal, bg="#ffffff", padx=10, pady=10)
frame_der.pack(side="right", fill="both", expand=True)

label_mapa = tk.Label(frame_der, text="Mapa del Zoo (zonas y animales)", font=("Arial", 16), bg="#ffffff")
label_mapa.pack(pady=10)

# Aquí se pueden añadir figuras 2D, botones o imágenes representando zonas
canvas = tk.Canvas(frame_der, width=400, height=400, bg="#e6f2ff")
canvas.pack()

# Ejemplo de figuras 2D (zonas del zoo)
canvas.create_rectangle(50, 50, 150, 150, fill="orange", outline="black", width=2)
canvas.create_text(100, 100, text="Zona Mamíferos", font=("Arial", 12, "bold"))

canvas.create_rectangle(200, 50, 350, 150, fill="lightgreen", outline="black", width=2)
canvas.create_text(275, 100, text="Zona Reptiles", font=("Arial", 12, "bold"))

canvas.create_rectangle(50, 200, 150, 350, fill="lightblue", outline="black", width=2)
canvas.create_text(100, 275, text="Zona Aves", font=("Arial", 12, "bold"))

canvas.create_rectangle(200, 200, 350, 350, fill="pink", outline="black", width=2)
canvas.create_text(275, 275, text="Zona Exhibiciones", font=("Arial", 12, "bold"))

ventana.mainloop()
