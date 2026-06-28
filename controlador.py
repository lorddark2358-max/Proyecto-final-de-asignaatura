import tkinter as tk
from typing import Dict, List
from modelo import AhorcadoModelo, normalizar_texto
from vista import AhorcadoVistaGUI

class AhorcadoControladorGUI:
    """Capa de Lógica (Controlador): Conecta el Modelo y la Vista en base a eventos de usuario."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.modelo = AhorcadoModelo()
        self.vista = AhorcadoVistaGUI(root)

        # Configurar enlace de eventos y acciones
        self.configurar_eventos()

        # Iniciar partida inicial
        self.actualizar_combobox_categorias()
        self.iniciar_nueva_partida()

    def configurar_eventos(self):
        """Conecta los clics de botones y el teclado físico con los métodos del controlador."""
        # Botones de control superior
        self.vista.btn_nueva_partida.configure(command=self.iniciar_nueva_partida)
        self.vista.btn_gestor.configure(command=self.abrir_gestor_palabras)

        # Teclado Virtual: configurar clics en las teclas
        def crear_manejador_tecla(letra_virtual):
            return lambda: self.procesar_intento_letra(letra_virtual)

        for letra, btn in self.vista.botones_teclado.items():
            btn.configure(command=crear_manejador_tecla(letra))

        # Teclado Físico: asociar eventos de teclado de la ventana principal
        self.root.bind("<Key>", self.procesar_teclado_fisico)

    def actualizar_combobox_categorias(self):
        """Actualiza la lista de categorías en la barra de control superior."""
        categorias = sorted(list(self.modelo.palabras_por_categoria.keys()))
        self.vista.combo_categoria.configure(values=["TODAS"] + categorias)
        self.vista.combo_categoria.current(0) # "TODAS" seleccionada por defecto

    def iniciar_nueva_partida(self):
        """Prepara e inicia una nueva partida de juego."""
        # Obtener categoría seleccionada
        cat_seleccionada = self.vista.combo_categoria.get()
        if cat_seleccionada == "TODAS" or not cat_seleccionada:
            cat_actual = None
        else:
            cat_actual = cat_seleccionada

        # Iniciar el estado en el Modelo
        self.modelo.iniciar_partida(cat_actual)

        # Actualizar la Vista
        self.vista.resetear_teclado()
        self.vista.dibujar_base_horca()
        
        # Si la categoría elegida fue aleatoria (debido a "TODAS"), actualizar el combo temporalmente sin disparar evento
        if cat_seleccionada == "TODAS":
            self.vista.combo_categoria.set(f"TODAS ({self.modelo.categoria_actual})")

        self.vista.actualizar_palabra(self.modelo.palabra_enmascarada)
        self.vista.actualizar_letras_incorrectas([])
        self.vista.actualizar_estadisticas(self.modelo.racha_victorias, self.modelo.puntuacion_total)
        self.vista.mostrar_notificacion("Nueva partida iniciada. ¡Selecciona una letra!")

    def procesar_intento_letra(self, letra: str):
        """Lógica de evaluación cuando el usuario intenta una letra (virtual o física)."""
        # Si el juego ya ha terminado, ignorar
        if self.modelo.ha_ganado() or self.modelo.ha_perdido():
            return

        letra_normalizada = normalizar_texto(letra)
        if not letra_normalizada or len(letra_normalizada) != 1:
            return

        # Comprobar si ya se había intentado
        if letra_normalizada in self.modelo.letras_intentadas:
            self.vista.mostrar_notificacion(f"La letra '{letra_normalizada}' ya fue intentada.", es_error=True)
            return

        # Registrar en el modelo
        es_acierto = self.modelo.registrar_intento(letra_normalizada)

        # Actualizar la tecla en la Vista
        self.vista.deshabilitar_tecla(letra_normalizada, es_acierto)

        # Actualizar estado de la palabra y fallos
        self.vista.actualizar_palabra(self.modelo.palabra_enmascarada)
        
        # Calcular letras incorrectas (todas las intentadas que no están en la palabra)
        letras_incorrectas = [l for l in self.modelo.letras_intentadas if l not in self.modelo.letras_unicas]
        self.vista.actualizar_letras_incorrectas(letras_incorrectas)

        # Dibujar la parte correspondiente
        errores = len(letras_incorrectas)
        self.vista.actualizar_dibujo_ahorcado(errores)

        # Actualizar estadísticas en tiempo real
        self.vista.actualizar_estadisticas(self.modelo.racha_victorias, self.modelo.puntuacion_total)

        # Comprobar fin de partida
        if self.modelo.ha_ganado():
            self.modelo.finalizar_partida(exito=True)
            self.vista.actualizar_estadisticas(self.modelo.racha_victorias, self.modelo.puntuacion_total)
            self.vista.actualizar_dibujo_ahorcado(errores, ha_ganado=True)
            self.vista.mostrar_resultado_final(ganado=True, palabra_secreta=self.modelo.palabra_secreta)
        
        elif self.modelo.ha_perdido():
            self.modelo.finalizar_partida(exito=False)
            self.vista.actualizar_estadisticas(self.modelo.racha_victorias, self.modelo.puntuacion_total)
            self.vista.actualizar_dibujo_ahorcado(6, ha_perdido=True)
            self.vista.mostrar_resultado_final(ganado=False, palabra_secreta=self.modelo.palabra_secreta)
            
        else:
            if es_acierto:
                self.vista.mostrar_notificacion(f"¡Bien hecho! La letra '{letra_normalizada}' es correcta.")
            else:
                self.vista.mostrar_notificacion(f"Lo siento, la letra '{letra_normalizada}' no está en la palabra.", es_error=True)

    def procesar_teclado_fisico(self, event):
        """Captura pulsaciones del teclado real del usuario."""
        letra = event.char.upper()
        
        # Validar si es una letra del abecedario español
        abecedario = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
        if letra in abecedario and letra != "":
            # Obtener el estado del botón en el teclado virtual
            btn = self.vista.botones_teclado.get(letra)
            if btn and btn["state"] == tk.NORMAL:
                self.procesar_intento_letra(letra)

    def abrir_gestor_palabras(self):
        """Abre la ventana modal del gestor de palabras y enlaza sus callbacks."""
        
        def callback_agregar(cat: str, pal: str) -> bool:
            exito = self.modelo.agregar_palabra(cat, pal)
            if exito:
                # Si se agregó correctamente, actualizar el controlador por si se agregó una nueva categoría
                self.actualizar_combobox_categorias()
            return exito

        def callback_eliminar(cat: str, pal: str) -> bool:
            exito = self.modelo.eliminar_palabra(cat, pal)
            if exito:
                self.actualizar_combobox_categorias()
            return exito

        # Pasar una copia del diccionario actual de palabras al gestor
        palabras_copia = {cat: list(pals) for cat, pals in self.modelo.palabras_por_categoria.items()}
        self.vista.abrir_gestor_palabras(palabras_copia, callback_agregar, callback_eliminar)
