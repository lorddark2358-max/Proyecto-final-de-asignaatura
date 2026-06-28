import tkinter as tk
from controlador import AhorcadoControladorGUI

def main():
    # Inicialización de la ventana principal de Tkinter
    root = tk.Tk()
    
    # Instanciación del controlador que orquesta la aplicación
    app = AhorcadoControladorGUI(root)
    
    # Centrado dinámico de la ventana en pantalla para una experiencia de usuario fluida
    root.update_idletasks()
    anchura = root.winfo_width()
    altura = root.winfo_height()
    pos_x = (root.winfo_screenwidth() // 2) - (anchura // 2)
    pos_y = (root.winfo_screenheight() // 2) - (altura // 2)
    root.geometry(f"{anchura}x{altura}+{pos_x}+{pos_y}")
    
    # Bucle principal de ejecución de eventos
    root.mainloop()

if __name__ == "__main__":
    main()
