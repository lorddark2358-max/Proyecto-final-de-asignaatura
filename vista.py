import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List, Callable

# Definición de la paleta de colores del tema "Midnight Dark"
BG_MAIN = "#181825"       # Fondo de la aplicación
BG_CARD = "#1e1e2e"       # Fondo de paneles y tarjetas
FG_TEXT = "#cdd6f4"       # Texto claro principal
FG_MUTED = "#a6adc8"      # Texto secundario/atenuado
COLOR_ACCENT = "#89b4fa"  # Azul lavanda para elementos destacados
COLOR_SUCCESS = "#a6e3a1" # Verde pastel para aciertos/victoria
COLOR_ERROR = "#f38ba8"   # Rojo pastel para errores/derrota
COLOR_KEY_BG = "#313244"  # Fondo de botones del teclado
COLOR_KEY_HOVER = "#45475a"# Color de hover del teclado
COLOR_KEY_TEXT = "#cdd6f4" # Texto del teclado

class AhorcadoVistaGUI:
    """Capa de Presentación (Vista): Interfaz gráfica de usuario implementada en Tkinter."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Ahorcado Cognitivo - Proyecto Integrador")
        self.root.geometry("900x650")
        self.root.minsize(800, 580)
        self.root.configure(bg=BG_MAIN)

        # Configurar estilos generales para ttk
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Personalizar elementos ttk con colores oscuros
        self.style.configure(".", background=BG_MAIN, foreground=FG_TEXT)
        self.style.configure("TLabel", background=BG_CARD, foreground=FG_TEXT, font=("Segoe UI", 11))
        self.style.configure("Header.TLabel", background=BG_MAIN, foreground=COLOR_ACCENT, font=("Segoe UI", 24, "bold"))
        self.style.configure("Sub.TLabel", background=BG_MAIN, foreground=FG_MUTED, font=("Segoe UI", 11, "italic"))
        self.style.configure("Stat.TLabel", background=BG_CARD, foreground=COLOR_ACCENT, font=("Segoe UI", 12, "bold"))
        self.style.configure("Word.TLabel", background=BG_CARD, foreground=FG_TEXT, font=("Consolas", 28, "bold"))
        
        self.style.configure("TButton", 
                             background=COLOR_ACCENT, 
                             foreground=BG_MAIN, 
                             borderwidth=0, 
                             focusthickness=0, 
                             font=("Segoe UI", 10, "bold"))
        self.style.map("TButton",
                       background=[("active", COLOR_SUCCESS), ("disabled", "#585b70")],
                       foreground=[("disabled", "#a6adc8")])
        
        self.style.configure("Secondary.TButton", 
                             background=COLOR_KEY_BG, 
                             foreground=FG_TEXT, 
                             font=("Segoe UI", 10, "bold"))
        self.style.map("Secondary.TButton",
                       background=[("active", COLOR_KEY_HOVER)])

        self.style.configure("TCombobox", 
                             background=BG_CARD, 
                             foreground=FG_TEXT, 
                             fieldbackground=BG_CARD, 
                             bordercolor=COLOR_KEY_BG,
                             arrowcolor=COLOR_ACCENT)

        # Diccionario para almacenar los botones del teclado virtual
        self.botones_teclado: Dict[str, tk.Button] = {}

        # Construir estructura de la GUI
        self.inicializar_componentes()

    def inicializar_componentes(self):
        """Crea y organiza los contenedores principales y widgets."""
        # --- HEADER PANEL (Superior) ---
        header_frame = tk.Frame(self.root, bg=BG_MAIN, pady=15, padx=20)
        header_frame.pack(fill=tk.X)
        
        titulo = ttk.Label(header_frame, text="AHORCADO COGNITIVO", style="Header.TLabel")
        titulo.pack(side=tk.LEFT, anchor=tk.W)
        
        subtitulo = ttk.Label(header_frame, text="Sistema de Estimulación & MVC", style="Sub.TLabel")
        subtitulo.pack(side=tk.LEFT, anchor=tk.S, padx=15, pady=5)

        # --- MAIN PANEL (Central) ---
        main_frame = tk.Frame(self.root, bg=BG_MAIN, padx=20, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.columnconfigure(0, weight=4) # Columna del Canvas
        main_frame.columnconfigure(1, weight=5) # Columna de la Palabra y teclado

        # Panel Izquierdo: Dibujo del Ahorcado
        canvas_container = tk.LabelFrame(
            main_frame, text=" Estado Visual del Ahorcado ", 
            bg=BG_CARD, fg=COLOR_ACCENT, font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT, bd=0
        )
        canvas_container.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=10)
        # Añadir un borde visual simulado con un frame interno de color diferente
        canvas_container.configure(highlightbackground=COLOR_KEY_BG, highlightthickness=1)

        self.canvas = tk.Canvas(canvas_container, bg=BG_CARD, width=280, height=320, bd=0, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        self.dibujar_base_horca()

        # Panel Derecho: Palabra, Estadísticas y Teclado
        right_container = tk.Frame(main_frame, bg=BG_MAIN)
        right_container.grid(row=0, column=1, sticky="nsew", pady=10)
        right_container.rowconfigure(0, weight=1) # Ficha de estadísticas y selector
        right_container.rowconfigure(1, weight=2) # Panel de visualización de la palabra
        right_container.rowconfigure(2, weight=3) # Teclado

        # Fila 0 de la derecha: Estadísticas y Selector de Categoría
        stats_frame = tk.LabelFrame(
            right_container, text=" Panel de Control & Estadísticas ",
            bg=BG_CARD, fg=COLOR_ACCENT, font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT, bd=0, highlightbackground=COLOR_KEY_BG, highlightthickness=1
        )
        stats_frame.pack(fill=tk.X, pady=(0, 10))

        # Controles
        control_subframe = tk.Frame(stats_frame, bg=BG_CARD, pady=10, padx=15)
        control_subframe.pack(fill=tk.X)

        tk.Label(control_subframe, text="Categoría:", bg=BG_CARD, fg=FG_MUTED, font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", padx=5)
        self.combo_categoria = ttk.Combobox(control_subframe, state="readonly", width=15)
        self.combo_categoria.grid(row=0, column=1, padx=5, sticky="w")

        self.btn_nueva_partida = ttk.Button(control_subframe, text="Nuevo Juego")
        self.btn_nueva_partida.grid(row=0, column=2, padx=10)

        self.btn_gestor = ttk.Button(control_subframe, text="Gestor Palabras", style="Secondary.TButton")
        self.btn_gestor.grid(row=0, column=3, padx=5)

        # Stats Labels
        stats_subframe = tk.Frame(stats_frame, bg=BG_CARD, pady=5, padx=15)
        stats_subframe.pack(fill=tk.X)
        
        self.lbl_racha = ttk.Label(stats_subframe, text="Racha: 0 🔥", style="Stat.TLabel")
        self.lbl_racha.pack(side=tk.LEFT, padx=10)

        self.lbl_puntuacion = ttk.Label(stats_subframe, text="Puntaje: 0 🏆", style="Stat.TLabel")
        self.lbl_puntuacion.pack(side=tk.LEFT, padx=30)

        # Fila 1 de la derecha: Visualización de la Palabra enmascarada e incorrectas
        word_frame = tk.LabelFrame(
            right_container, text=" Palabra Secreta ",
            bg=BG_CARD, fg=COLOR_ACCENT, font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT, bd=0, highlightbackground=COLOR_KEY_BG, highlightthickness=1
        )
        word_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.lbl_palabra = ttk.Label(word_frame, text="_ _ _ _ _", style="Word.TLabel", anchor="center")
        self.lbl_palabra.pack(fill=tk.BOTH, expand=True, pady=15)

        # Aviso del sistema e historial de fallos
        self.lbl_notificacion = tk.Label(word_frame, text="¡Buena suerte! Selecciona una letra.", bg=BG_CARD, fg=FG_MUTED, font=("Segoe UI", 11, "italic"))
        self.lbl_notificacion.pack(fill=tk.X, side=tk.BOTTOM, pady=5)

        self.lbl_fallos = tk.Label(word_frame, text="Errores: Ninguno", bg=BG_CARD, fg=COLOR_ERROR, font=("Segoe UI", 10, "bold"))
        self.lbl_fallos.pack(fill=tk.X, side=tk.BOTTOM)

        # Fila 2 de la derecha: Teclado Virtual QWERTY
        self.keyboard_frame = tk.LabelFrame(
            right_container, text=" Teclado Virtual ",
            bg=BG_CARD, fg=COLOR_ACCENT, font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT, bd=0, highlightbackground=COLOR_KEY_BG, highlightthickness=1
        )
        self.keyboard_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        self.crear_teclado_virtual()

    def dibujar_base_horca(self):
        """Limpia el canvas y dibuja la estructura de madera de la horca."""
        self.canvas.delete("all")
        
        # Base de madera
        self.canvas.create_line(30, 290, 150, 290, width=6, fill="#45475a", capstyle=tk.ROUND, tags="gallows")
        # Poste vertical principal
        self.canvas.create_line(80, 290, 80, 50, width=6, fill="#45475a", capstyle=tk.ROUND, tags="gallows")
        # Viga horizontal superior
        self.canvas.create_line(80, 50, 200, 50, width=6, fill="#45475a", capstyle=tk.ROUND, tags="gallows")
        # Soporte diagonal
        self.canvas.create_line(80, 100, 130, 50, width=4, fill="#45475a", capstyle=tk.ROUND, tags="gallows")
        # La cuerda
        self.canvas.create_line(200, 50, 200, 95, width=3, fill="#f9e2af", capstyle=tk.ROUND, tags="gallows")

    def actualizar_dibujo_ahorcado(self, errores: int, ha_ganado: bool = False, ha_perdido: bool = False):
        """Redibuja de forma limpia los segmentos correspondientes al número de errores cometido."""
        # Limpiar partes del ahorcado pero mantener la estructura
        self.canvas.delete("hangman")
        
        # Color del ahorcado según el estado (normal, victoria, derrota)
        color_cuerpo = COLOR_SUCCESS if ha_ganado else (COLOR_ERROR if ha_perdido else FG_TEXT)
        color_detalles = COLOR_ERROR if ha_perdido else BG_CARD

        # Definición geométrica de las partes del cuerpo
        # 1. Cabeza
        if errores >= 1:
            self.canvas.create_oval(175, 95, 225, 145, width=4, outline=color_cuerpo, fill=BG_CARD, tags="hangman")
            
            # Dibujar rostros en la cabeza
            if ha_ganado:
                # Ojos felices ^ ^
                self.canvas.create_line(188, 115, 193, 110, width=2, fill=color_cuerpo, tags="hangman")
                self.canvas.create_line(193, 110, 198, 115, width=2, fill=color_cuerpo, tags="hangman")
                self.canvas.create_line(202, 115, 207, 110, width=2, fill=color_cuerpo, tags="hangman")
                self.canvas.create_line(207, 110, 212, 115, width=2, fill=color_cuerpo, tags="hangman")
                # Sonrisa
                self.canvas.create_arc(188, 112, 212, 134, start=180, extent=180, width=2, outline=color_cuerpo, style=tk.ARC, tags="hangman")
            elif ha_perdido:
                # Ojos X X
                self.canvas.create_line(187, 110, 195, 118, width=2.5, fill=color_detalles, tags="hangman")
                self.canvas.create_line(195, 110, 187, 118, width=2.5, fill=color_detalles, tags="hangman")
                self.canvas.create_line(205, 110, 213, 118, width=2.5, fill=color_detalles, tags="hangman")
                self.canvas.create_line(213, 110, 205, 118, width=2.5, fill=color_detalles, tags="hangman")
                # Boca triste
                self.canvas.create_arc(188, 125, 212, 137, start=0, extent=180, width=2.5, outline=color_detalles, style=tk.ARC, tags="hangman")
            else:
                # Ojos normales
                self.canvas.create_oval(190, 112, 193, 115, fill=color_cuerpo, outline=color_cuerpo, tags="hangman")
                self.canvas.create_oval(207, 112, 210, 115, fill=color_cuerpo, outline=color_cuerpo, tags="hangman")
                # Boca neutra
                self.canvas.create_line(192, 130, 208, 130, width=2, fill=color_cuerpo, tags="hangman")

        # 2. Tronco/Cuerpo
        if errores >= 2:
            self.canvas.create_line(200, 145, 200, 220, width=4, fill=color_cuerpo, capstyle=tk.ROUND, tags="hangman")
        
        # 3. Brazo izquierdo
        if errores >= 3:
            self.canvas.create_line(200, 165, 165, 195, width=4, fill=color_cuerpo, capstyle=tk.ROUND, tags="hangman")
        
        # 4. Brazo derecho
        if errores >= 4:
            self.canvas.create_line(200, 165, 235, 195, width=4, fill=color_cuerpo, capstyle=tk.ROUND, tags="hangman")
        
        # 5. Pierna izquierda
        if errores >= 5:
            self.canvas.create_line(200, 220, 170, 275, width=4, fill=color_cuerpo, capstyle=tk.ROUND, tags="hangman")
        
        # 6. Pierna derecha
        if errores >= 6:
            self.canvas.create_line(200, 220, 230, 275, width=4, fill=color_cuerpo, capstyle=tk.ROUND, tags="hangman")

    def crear_teclado_virtual(self):
        """Genera una distribución QWERTY táctil para el teclado de letras."""
        # Limpiar teclado existente si lo hubiera
        for widget in self.keyboard_frame.winfo_children():
            widget.destroy()
        self.botones_teclado.clear()

        # Filas de QWERTY adaptadas para incluir la Ñ
        filas = [
            ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L", "Ñ"],
            ["Z", "X", "C", "V", "B", "N", "M"]
        ]

        # Contenedor del teclado para centrado
        kb_inner = tk.Frame(self.keyboard_frame, bg=BG_CARD)
        kb_inner.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        for r_idx, fila in enumerate(filas):
            row_frame = tk.Frame(kb_inner, bg=BG_CARD)
            row_frame.pack(pady=3)
            
            for letra in fila:
                # Usamos tk.Button clásico para poder controlar perfectamente los colores
                # de fondo sin las restricciones de tema rígidas de ttk en ciertos Sistemas Operativos.
                btn = tk.Button(
                    row_frame, text=letra, width=4, height=1,
                    bg=COLOR_KEY_BG, fg=COLOR_KEY_TEXT,
                    activebackground=COLOR_KEY_HOVER, activeforeground=COLOR_KEY_TEXT,
                    font=("Segoe UI", 11, "bold"), bd=0, relief=tk.FLAT,
                    cursor="hand2"
                )
                btn.pack(side=tk.LEFT, padx=3)
                
                # Efecto hover visual
                btn.bind("<Enter>", lambda e, b=btn: self._on_button_hover(b, True))
                btn.bind("<Leave>", lambda e, b=btn: self._on_button_hover(b, False))
                
                self.botones_teclado[letra] = btn

    def _on_button_hover(self, button: tk.Button, hover: bool):
        """Maneja el cambio de color al pasar el cursor sobre los botones activos del teclado."""
        if button["state"] == tk.NORMAL:
            button.configure(bg=COLOR_KEY_HOVER if hover else COLOR_KEY_BG)

    def deshabilitar_tecla(self, letra: str, es_acierto: bool):
        """Colorea y deshabilita una tecla del teclado virtual."""
        btn = self.botones_teclado.get(letra)
        if btn:
            color_fondo = COLOR_SUCCESS if es_acierto else COLOR_ERROR
            btn.configure(
                bg=color_fondo, 
                fg=BG_MAIN, 
                state=tk.DISABLED,
                disabledforeground=BG_MAIN
            )

    def resetear_teclado(self):
        """Vuelve todos los botones del teclado a su estado activo original."""
        for letra, btn in self.botones_teclado.items():
            btn.configure(
                bg=COLOR_KEY_BG, 
                fg=COLOR_KEY_TEXT, 
                state=tk.NORMAL
            )

    def actualizar_palabra(self, palabra_enmascarada: str):
        """Actualiza el texto enmascarado en la pantalla."""
        self.lbl_palabra.configure(text=palabra_enmascarada)

    def actualizar_estadisticas(self, racha: int, puntuacion: int):
        """Actualiza las etiquetas de racha y puntuación."""
        self.lbl_racha.configure(text=f"Racha: {racha} 🔥")
        self.lbl_puntuacion.configure(text=f"Puntaje: {puntuacion} 🏆")

    def actualizar_letras_incorrectas(self, fallos: List[str]):
        """Actualiza la lista visual de letras incorrectas."""
        if not fallos:
            self.lbl_fallos.configure(text="Errores: Ninguno", fg=COLOR_SUCCESS)
        else:
            self.lbl_fallos.configure(
                text=f"Errores ({len(fallos)}/6):  {', '.join(sorted(fallos))}",
                fg=COLOR_ERROR
            )

    def mostrar_notificacion(self, mensaje: str, es_error: bool = False):
        """Muestra un mensaje informativo en la parte inferior."""
        color = COLOR_ERROR if es_error else COLOR_ACCENT
        self.lbl_notificacion.configure(text=mensaje, fg=color)

    def mostrar_resultado_final(self, ganado: bool, palabra_secreta: str):
        """Deshabilita el teclado y notifica el cierre del juego."""
        # Deshabilitar todas las teclas restantes
        for btn in self.botones_teclado.values():
            if btn["state"] == tk.NORMAL:
                btn.configure(state=tk.DISABLED, bg="#585b70", fg="#a6adc8")
        
        if ganado:
            self.mostrar_notificacion("🎉 ¡PROCESO EXITOSO! Has resuelto la palabra.", es_error=False)
            messagebox.showinfo("¡Felicidades!", f"🎉 ¡Victoria!\n\nHas descifrado la palabra: {palabra_secreta}\n¡Tu racha sigue activa!")
        else:
            self.mostrar_notificacion(f"💀 DERROTA. La palabra correcta era: {palabra_secreta}", es_error=True)
            messagebox.showerror("Fin del Juego", f"💀 Has sido colgado.\n\nLa palabra correcta era: {palabra_secreta}\nTu racha ha vuelto a 0.")

    def abrir_gestor_palabras(self, 
                              palabras_por_cat: Dict[str, List[str]], 
                              callback_agregar: Callable[[str, str], bool], 
                              callback_eliminar: Callable[[str, str], bool]):
        """Abre un diálogo modal para la gestión del banco de palabras."""
        gestor_win = tk.Toplevel(self.root)
        gestor_win.title("Gestor de Diccionario - Ahorcado")
        gestor_win.geometry("550x450")
        gestor_win.transient(self.root)
        gestor_win.grab_set()
        gestor_win.configure(bg=BG_CARD)

        # Diseño interno de la ventana modal
        gestor_win.rowconfigure(0, weight=1)
        gestor_win.columnconfigure(0, weight=4) # Lista de palabras
        gestor_win.columnconfigure(1, weight=5) # Formulario agregar

        # Panel Izquierdo: Lista de palabras de la categoría seleccionada
        list_frame = tk.Frame(gestor_win, bg=BG_CARD, padx=10, pady=10)
        list_frame.grid(row=0, column=0, sticky="nsew")
        list_frame.rowconfigure(2, weight=1)

        tk.Label(list_frame, text="Categoría:", bg=BG_CARD, fg=FG_TEXT, font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w", pady=(0,5))
        
        combo_cat_gestor = ttk.Combobox(list_frame, state="readonly", values=list(palabras_por_cat.keys()))
        combo_cat_gestor.grid(row=1, column=0, sticky="ew", pady=(0,10))
        if list(palabras_por_cat.keys()):
            combo_cat_gestor.current(0)

        # Listbox para las palabras
        listbox_frame = tk.Frame(list_frame, bg=BG_CARD)
        listbox_frame.grid(row=2, column=0, sticky="nsew")
        listbox_frame.rowconfigure(0, weight=1)
        listbox_frame.columnconfigure(0, weight=1)

        scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
        scrollbar.grid(row=0, column=1, sticky="ns")

        listbox_words = tk.Listbox(
            listbox_frame, bg=BG_MAIN, fg=FG_TEXT, 
            selectbackground=COLOR_ACCENT, selectforeground=BG_MAIN,
            highlightcolor=COLOR_KEY_BG, bd=0, 
            font=("Consolas", 11), yscrollcommand=scrollbar.set
        )
        listbox_words.grid(row=0, column=0, sticky="nsew")
        scrollbar.config(command=listbox_words.yview)

        btn_eliminar = ttk.Button(list_frame, text="Eliminar Selección", style="Secondary.TButton")
        btn_eliminar.grid(row=3, column=0, sticky="ew", pady=(10,0))

        # Panel Derecho: Formulario Agregar
        form_frame = tk.Frame(gestor_win, bg=BG_CARD, padx=15, pady=10, highlightbackground=COLOR_KEY_BG, highlightthickness=1)
        form_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        tk.Label(form_frame, text="AÑADIR PALABRA", bg=BG_CARD, fg=COLOR_ACCENT, font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0,15))

        tk.Label(form_frame, text="Nueva Palabra:", bg=BG_CARD, fg=FG_TEXT).pack(anchor="w", pady=5)
        entry_palabra = tk.Entry(
            form_frame, bg=BG_MAIN, fg=FG_TEXT, insertbackground=FG_TEXT,
            relief=tk.FLAT, font=("Segoe UI", 11), bd=5
        )
        entry_palabra.pack(fill=tk.X, pady=(0,15))

        tk.Label(form_frame, text="Categoría de Destino:", bg=BG_CARD, fg=FG_TEXT).pack(anchor="w", pady=5)
        combo_cat_destino = ttk.Combobox(form_frame, state="readonly", values=list(palabras_por_cat.keys()))
        combo_cat_destino.pack(fill=tk.X, pady=(0,20))
        if list(palabras_por_cat.keys()):
            combo_cat_destino.current(0)

        btn_agregar = ttk.Button(form_frame, text="Agregar Palabra")
        btn_agregar.pack(fill=tk.X)

        # Lógica de carga del Listbox según la categoría seleccionada
        def actualizar_listbox(e=None):
            listbox_words.delete(0, tk.END)
            cat_seleccionada = combo_cat_gestor.get()
            if cat_seleccionada in palabras_por_cat:
                for palabra in sorted(palabras_por_cat[cat_seleccionada]):
                    listbox_words.insert(tk.END, palabra)

        combo_cat_gestor.bind("<<ComboboxSelected>>", actualizar_listbox)
        actualizar_listbox() # Ejecución inicial

        # Callbacks de botones
        def on_agregar():
            pal = entry_palabra.get().strip()
            cat = combo_cat_destino.get()
            
            if not pal:
                messagebox.showwarning("Campo Vacío", "Por favor, escriba una palabra.")
                return
            if not pal.isalpha():
                messagebox.showwarning("Entrada Inválida", "La palabra debe contener únicamente letras.")
                return

            if callback_agregar(cat, pal):
                messagebox.showinfo("Éxito", f"Se agregó '{pal.upper()}' a {cat}.")
                entry_palabra.delete(0, tk.END)
                
                # Actualizar el diccionario local
                if cat not in palabras_por_cat:
                    palabras_por_cat[cat] = []
                palabras_por_cat[cat].append(pal.upper())
                
                # Refrescar listbox si es necesario
                if combo_cat_gestor.get() == cat:
                    actualizar_listbox()
            else:
                messagebox.showerror("Error", f"No se pudo añadir. Verifique si la palabra ya existe.")

        def on_eliminar():
            seleccion = listbox_words.curselection()
            if not seleccion:
                messagebox.showwarning("Sin Selección", "Por favor, seleccione una palabra de la lista.")
                return
            
            pal = listbox_words.get(seleccion[0])
            cat = combo_cat_gestor.get()
            
            if messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de eliminar '{pal}' de la categoría '{cat}'?"):
                if callback_eliminar(cat, pal):
                    messagebox.showinfo("Éxito", f"Palabra '{pal}' eliminada con éxito.")
                    
                    # Actualizar diccionario local
                    if cat in palabras_por_cat and pal in palabras_por_cat[cat]:
                        palabras_por_cat[cat].remove(pal)
                    
                    actualizar_listbox()
                else:
                    messagebox.showerror("Error", "No se pudo eliminar la palabra.")

        btn_agregar.configure(command=on_agregar)
        btn_eliminar.configure(command=on_eliminar)
