import unittest
import os
import json
from modelo import AhorcadoModelo, normalizar_texto

class TestAhorcadoModelo(unittest.TestCase):
    def setUp(self):
        # Usamos un archivo JSON temporal para no alterar el del usuario
        self.archivo_temporal = "temp_palabras_test.json"
        # Inicializar el modelo con el archivo temporal
        self.modelo = AhorcadoModelo(ruta_archivo=self.archivo_temporal)

    def tearDown(self):
        # Limpiar el archivo temporal
        if os.path.exists(self.archivo_temporal):
            os.remove(self.archivo_temporal)

    def test_normalizar_texto(self):
        self.assertEqual(normalizar_texto("tecnología"), "TECNOLOGIA")
        self.assertEqual(normalizar_texto("informática"), "INFORMATICA")
        self.assertEqual(normalizar_texto("niño"), "NIÑO")
        self.assertEqual(normalizar_texto(" pingüino "), "PINGUINO")
        self.assertEqual(normalizar_texto("Cigüeña"), "CIGUEÑA")

    def test_inicializacion_modelo(self):
        self.assertIn("TECNOLOGIA", self.modelo.palabras_por_categoria)
        self.assertGreater(len(self.modelo.palabras_por_categoria["TECNOLOGIA"]), 0)

    def test_iniciar_partida(self):
        self.modelo.iniciar_partida("TECNOLOGIA")
        self.assertEqual(self.modelo.categoria_actual, "TECNOLOGIA")
        self.assertIn(self.modelo.palabra_secreta, self.modelo.palabras_por_categoria["TECNOLOGIA"])
        self.assertEqual(self.modelo.intentos_restantes, 6)
        self.assertEqual(len(self.modelo.letras_intentadas), 0)

    def test_registrar_intento_correcto_e_incorrecto(self):
        # Configurar manualmente la palabra para predecir los resultados
        self.modelo.palabra_secreta = "TEST"
        self.modelo.letras_unicas = set("TEST")
        self.modelo.letras_intentadas = set()
        self.modelo.intentos_restantes = 6

        # Intento correcto
        es_correcto = self.modelo.registrar_intento("T")
        self.assertTrue(es_correcto)
        self.assertIn("T", self.modelo.letras_intentadas)
        self.assertEqual(self.modelo.intentos_restantes, 6)

        # Intento incorrecto
        es_correcto = self.modelo.registrar_intento("Z")
        self.assertFalse(es_correcto)
        self.assertIn("Z", self.modelo.letras_intentadas)
        self.assertEqual(self.modelo.intentos_restantes, 5)

        # Intento repetido no debe cambiar intentos restantes
        es_correcto_repetido = self.modelo.registrar_intento("Z")
        self.assertFalse(es_correcto_repetido)
        self.assertEqual(self.modelo.intentos_restantes, 5)

    def test_ha_ganado_y_ha_perdido(self):
        self.modelo.palabra_secreta = "OK"
        self.modelo.letras_unicas = set("OK")
        self.modelo.letras_intentadas = set()
        self.modelo.intentos_restantes = 2

        self.assertFalse(self.modelo.ha_ganado())
        self.assertFalse(self.modelo.ha_perdido())

        # Registrar fallos
        self.modelo.registrar_intento("X")
        self.assertEqual(self.modelo.intentos_restantes, 1)
        self.assertFalse(self.modelo.ha_perdido())

        self.modelo.registrar_intento("Y")
        self.assertEqual(self.modelo.intentos_restantes, 0)
        self.assertTrue(self.modelo.ha_perdido())
        self.assertFalse(self.modelo.ha_ganado())

        # Resetear e intentar ganar
        self.modelo.intentos_restantes = 6
        self.modelo.letras_intentadas = set()
        self.modelo.registrar_intento("O")
        self.modelo.registrar_intento("K")
        self.assertTrue(self.modelo.ha_ganado())
        self.assertFalse(self.modelo.ha_perdido())

    def test_palabra_enmascarada(self):
        self.modelo.palabra_secreta = "CASA"
        self.modelo.letras_intentadas = set()
        self.assertEqual(self.modelo.palabra_enmascarada, "_ _ _ _")

        self.modelo.registrar_intento("A")
        self.assertEqual(self.modelo.palabra_enmascarada, "_ A _ A")

        self.modelo.registrar_intento("C")
        self.assertEqual(self.modelo.palabra_enmascarada, "C A _ A")

    def test_agregar_y_eliminar_palabra(self):
        categoria = "NUEVA_CATEGORIA"
        palabra = "PRUEBITA"

        # Agregar
        agregado = self.modelo.agregar_palabra(categoria, palabra)
        self.assertTrue(agregado)
        self.assertIn(palabra, self.modelo.palabras_por_categoria[categoria])

        # Verificar persistencia cargando un nuevo modelo desde el archivo
        otro_modelo = AhorcadoModelo(ruta_archivo=self.archivo_temporal)
        self.assertIn(palabra, otro_modelo.palabras_por_categoria[categoria])

        # Eliminar
        eliminado = self.modelo.eliminar_palabra(categoria, palabra)
        self.assertTrue(eliminado)
        self.assertNotIn(palabra, self.modelo.palabras_por_categoria[categoria])

if __name__ == "__main__":
    unittest.main()
