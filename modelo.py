import json
import os
import random

def normalizar_texto(texto: str) -> str:
    """Normaliza el texto eliminando tildes y convirtiendo a mayúsculas, conservando la Ñ."""
    texto = texto.strip().upper()
    reemplazos = {
        'Á': 'A',
        'É': 'E',
        'Í': 'I',
        'Ó': 'O',
        'Ú': 'U',
        'Ü': 'U'
    }
    for con_tilde, sin_tilde in reemplazos.items():
        texto = texto.replace(con_tilde, sin_tilde)
    return texto

class AhorcadoModelo:
    """Capa de Datos (Modelo): Administra el banco de palabras y el estado de la partida."""

    DEFAULT_PALABRAS = {
        "TECNOLOGIA": [
            "TECNOLOGIA", "INFORMATICA", "VARIABLE", "AUTOMATIZACION", 
            "PROGRAMACION", "ALGORITMO", "BASEDATOS", "SOFTWARE", 
            "INTERNET", "COMPILADOR"
        ],
        "CIENCIA": [
            "GRAVEDAD", "QUIMICA", "BIOLOGIA", "ATOMO", "EVOLUCION", 
            "MATEMATICAS", "FISICA", "ASTRONOMIA", "GALAXIA", "NEURONA"
        ],
        "GEOGRAFIA": [
            "PATAGONIA", "CORDILLERA", "OCEANO", "ECUADOR", "VOLCAN", 
            "CONTINENTE", "PENINSULA", "DESIERTO", "ATLANTICO", "AMAZONAS"
        ],
        "ARTE": [
            "PINTURA", "ESCULTURA", "LITERATURA", "MUSICA", "TEATRO", 
            "CINE", "ARQUITECTURA", "POESIA", "SINFONIA", "OPERA"
        ],
        "DEPORTES": [
            "BALONCESTO", "ATLETISMO", "NATACION", "CICLISMO", "TENIS", 
            "MARATON", "GIMNASIA", "FUTBOL", "SENDERISMO", "AJEDREZ"
        ]
    }

    def __init__(self, ruta_archivo: str = "palabras.json"):
        self.ruta_archivo = ruta_archivo
        self.palabras_por_categoria = {}
        self.cargar_palabras()

        # Variables de estado del juego
        self.categoria_actual = ""
        self.palabra_secreta = ""
        self.letras_unicas = set()
        self.letras_intentadas = set()
        self.intentos_restantes = 6
        
        # Estadísticas persistentes en memoria de la sesión
        self.racha_victorias = 0
        self.puntuacion_total = 0

    def cargar_palabras(self):
        """Carga el diccionario de palabras desde un archivo JSON o usa los valores por defecto."""
        if os.path.exists(self.ruta_archivo):
            try:
                with open(self.ruta_archivo, "r", encoding="utf-8") as f:
                    datos = json.load(f)
                    # Normalizar todas las palabras cargadas
                    self.palabras_por_categoria = {
                        cat.upper(): [normalizar_texto(pal) for pal in pals if pal.strip()]
                        for cat, pals in datos.items()
                    }
                return
            except (json.JSONDecodeError, IOError):
                pass
        
        # Si falla o no existe, usar las por defecto y guardar
        self.palabras_por_categoria = {
            cat: [normalizar_texto(pal) for pal in pals]
            for cat, pals in self.DEFAULT_PALABRAS.items()
        }
        self.guardar_palabras()

    def guardar_palabras(self):
        """Guarda la base de datos de palabras en un archivo JSON."""
        try:
            with open(self.ruta_archivo, "w", encoding="utf-8") as f:
                json.dump(self.palabras_por_categoria, f, indent=2, ensure_ascii=False)
            return True
        except IOError:
            return False

    def iniciar_partida(self, categoria: str = None):
        """Inicializa una nueva partida seleccionando una palabra secreta de una categoría."""
        if not self.palabras_por_categoria:
            self.cargar_palabras()

        # Si no se especifica o no existe la categoría, seleccionar una aleatoria con palabras
        categorias_validas = [cat for cat, pals in self.palabras_por_categoria.items() if pals]
        if not categorias_validas:
            # Fallback de emergencia si todas las categorías están vacías
            self.palabras_por_categoria = {
                cat: [normalizar_texto(pal) for pal in pals]
                for cat, pals in self.DEFAULT_PALABRAS.items()
            }
            self.guardar_palabras()
            categorias_validas = list(self.palabras_por_categoria.keys())

        if categoria not in categorias_validas:
            categoria = random.choice(categorias_validas)

        self.categoria_actual = categoria
        palabras_disponibles = self.palabras_por_categoria[categoria]
        self.palabra_secreta = random.choice(palabras_disponibles)
        
        self.letras_unicas = set(self.palabra_secreta)
        self.letras_intentadas = set()
        self.intentos_restantes = 6

    def registrar_intento(self, letra: str) -> bool:
        """Registra el intento de una letra y evalúa si fue correcto. Retorna True si acierta."""
        letra_normalizada = normalizar_texto(letra)
        if len(letra_normalizada) != 1 or not letra_normalizada.isalpha():
            return False

        if letra_normalizada in self.letras_intentadas:
            return False  # Letra ya intentada anteriormente

        self.letras_intentadas.add(letra_normalizada)
        if letra_normalizada in self.letras_unicas:
            # Sumar puntos por letra acertada
            self.puntuacion_total += 10
            return True
        
        self.intentos_restantes -= 1
        # Restar un pequeño puntaje por error (sin bajar de cero)
        self.puntuacion_total = max(0, self.puntuacion_total - 5)
        return False

    @property
    def palabra_enmascarada(self) -> str:
        """Retorna la palabra secreta con guiones bajos para las letras no descubiertas."""
        return " ".join(
            [letra if letra in self.letras_intentadas else "_" for letra in self.palabra_secreta]
        )

    def ha_ganado(self) -> bool:
        """Comprueba si el jugador ha descubierto todas las letras."""
        ganado = self.letras_unicas.issubset(self.letras_intentadas)
        if ganado and len(self.letras_intentadas) > 0:
            # Si acaba de ganar y la partida no estaba terminada, se procesa en el controlador
            pass
        return ganado

    def ha_perdido(self) -> bool:
        """Comprueba si el jugador se ha quedado sin intentos."""
        return self.intentos_restantes <= 0

    def finalizar_partida(self, exito: bool):
        """Actualiza rachas y puntaje final de la partida."""
        if exito:
            self.racha_victorias += 1
            self.puntuacion_total += 50  # Bonus de victoria
        else:
            self.racha_victorias = 0

    def agregar_palabra(self, categoria: str, palabra: str) -> bool:
        """Agrega una palabra a una categoría específica, normalizándola previamente."""
        categoria_formateada = normalizar_texto(categoria)
        palabra_formateada = normalizar_texto(palabra)

        # Validaciones
        if not categoria_formateada or not palabra_formateada:
            return False
        if not palabra_formateada.isalpha():
            return False

        if categoria_formateada not in self.palabras_por_categoria:
            self.palabras_por_categoria[categoria_formateada] = []

        if palabra_formateada not in self.palabras_por_categoria[categoria_formateada]:
            self.palabras_por_categoria[categoria_formateada].append(palabra_formateada)
            return self.guardar_palabras()
        return False

    def eliminar_palabra(self, categoria: str, palabra: str) -> bool:
        """Elimina una palabra de una categoría."""
        categoria_formateada = normalizar_texto(categoria)
        palabra_formateada = normalizar_texto(palabra)

        if categoria_formateada in self.palabras_por_categoria:
            lista_palabras = self.palabras_por_categoria[categoria_formateada]
            if palabra_formateada in lista_palabras:
                lista_palabras.remove(palabra_formateada)
                # Si la categoría queda vacía, podemos mantenerla o no. La mantendremos.
                return self.guardar_palabras()
        return False
