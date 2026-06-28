# Proyecto final de asignaatura
# 🎮 Juego del Ahorcado (MVC)

Este repositorio contiene la arquitectura de software, diagramas lógicos e implementación del **Juego del Ahorcado** bajo la especificación del estándar de Lógica de Programación.

## 📊 1. Diagrama de Flujo Funcional

El comportamiento lógico del ciclo de juego (Game Loop) y sus compuertas condicionales de validación de entradas están estructurados de la siguiente forma:

```mermaid
flowchart TD
    Start([Inicio: Nueva Partida]) --> Init[Seleccionar Palabra y Seter Vidas en 6]
    Init --> Render[Mostrar Palabra Enmascarada e Intentos]
    Render --> Input[/Jugador ingresa una letra/]
    Input --> ValidCheck{¿Es carácter alfabético\n válido y nuevo?}
    ValidCheck -- No --> Term[Mostrar Advertencia] --> Render
    ValidCheck -- Sí --> MatchCheck{¿La letra pertenece\n a la palabra?}
    MatchCheck -- Sí --> UpdateWord[Revelar posiciones de la letra]
    UpdateWord --> WinCheck{¿Palabra completa?}
    WinCheck -- No --> Render
    WinCheck -- Sí --> Victory([Fin: Victoria])
    MatchCheck -- No --> SubLives[Restar 1 intento]
    SubLives --> LoseCheck{¿Intentos = 0?}
    LoseCheck -- No --> Render
    LoseCheck -- Sí --> Defeat([Fin: Derrota])
```

## 🏛️ 2. Diagrama de Arquitectura de Software

Estructura modular diseñada bajo el patrón de Separación de Responsabilidades para aislar los efectos secundarios de la terminal:

```mermaid
graph TD
    subgraph Presentacion [Capa de Presentación - Vista]
        Console[Interfaz de Consola CLI]
    end
    subgraph Logica [Capa de Lógica - Controlador]
        GameEngine[Motor Central / Game Loop]
        InputValidator[Validador de Entradas]
        StateEvaluator[Evaluador Win/Loss]
    end
    subgraph Datos [Capa de Datos - Modelo]
        WordRepository[Banco de Palabras]
        SessionState[Estado Dinámico de Partida]
    end

    Console <--> GameEngine
    GameEngine --> InputValidator
    GameEngine <--> SessionState
    SessionState --> WordRepository
    GameEngine --> StateEvaluator
```

## 🛠️ 3. Ejecución Local del Sistema

Para levantar la solución en un entorno limpio y controlado:

```bash
# Activar entorno virtual
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Correr programa
python main.py
```

---

## 🏃‍♂️ Instrucciones de Ejecución para el Des
