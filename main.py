import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as tkFileDialog, scrolledtext as tkScrolledText
import os
from PIL import Image, ImageTk
# Importando funciones adicionales de los módulos
from hypertext.parser import run_html_tests
from cplusplus.parser import run_cpp_tests
from javascript.parser import run_js_tests
from pascal.parser import run_pascal_tests
from python.main import run_python_tests
from tsql.parser import run_sql_tests

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Code Identifier")
        self.configure(bg='#85c1e9')

        self.main_frame = tk.Frame(self, bg='#85c1e9')
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.right_frame = tk.Frame(self.main_frame, bg='#85c1e9')
        self.right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.title_label = tk.Label(
            self.right_frame,
            text="Code Identifier",
            font=("Helvetica", 20, "bold"),
            bg='#85c1e9',
            fg='white'
        )
        self.title_label.pack(pady=(10, 10))

        self.load_logo()  # Asegúrate de tener este método definido

        # Frame de botones "pintado"
        botones_frame = tk.Frame(
            self.right_frame,
            bg='#85c1e9',     # Mismo color de fondo
        )
        botones_frame.pack(pady=(10, 20))

        self.boton_analizar = ttk.Button(
            botones_frame,
            text="Seleccionar archivo",
            command=self.seleccionar_archivo_y_analizar,
            style='TButton'
        )
        self.boton_analizar.pack(side="left", padx=5, pady=10, )

        self.boton_adivinar = ttk.Button(
            botones_frame,
            text="Analizar texto",
            command=self.abrir_nueva_ventana,
            style='TButton'
        )
        self.boton_adivinar.pack(side="left", padx=5, pady=10)

        # Estilo para los botones (opcional)
        style = ttk.Style()
        style.configure('TButton', font=('Segoe UI', 10), padding=6)

        self.minsize(500, 300)
        self.eval('tk::PlaceWindow %s center' % self.winfo_toplevel())

    def load_logo(self):
        logo_path = os.path.join(os.path.dirname(__file__), 'icono.png')
        img = Image.open(logo_path)
        img = img.resize((175, 125), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        self.logo_label = tk.Label(self.right_frame, image=photo, bg='#85c1e9')
        self.logo_label.image = photo
        self.logo_label.pack(pady=(20, 20))

    def seleccionar_archivo_y_analizar(self):
        filepath = tkFileDialog.askopenfilename(
            title="Seleccionar archivo",
            filetypes=(("Todos los archivos", "*.*"),),
            parent=self
        )
        if filepath:
            extension = os.path.splitext(filepath)[1].lower()
            with open(filepath, 'r', encoding='utf-8') as file:
                file_content = file.read()
            lenguaje, resultado = self.identificar_lenguaje_por_extension(extension, file_content)
            self.mostrar_resultados(lenguaje, resultado)

    def abrir_nueva_ventana(self):
        new_window = tk.Toplevel(self)
        new_window.title("Analizar texto")
        new_window.configure(bg='#03A062')
        new_window.geometry("600x400")

        container = tk.Frame(new_window, bg='#03A062')
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        text_area = tk.Text(container, wrap=tk.WORD, font=('Courier New', 12), background='#03A062', foreground='black', borderwidth=2, relief="solid")
        text_area.grid(row=0, column=0, sticky="nsew")

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        button_frame = tk.Frame(container, bg='#03A062')
        button_frame.grid(row=1, column=0, sticky="ew")

        analyze_button = ttk.Button(button_frame, text="Analizar", command=lambda: self.analizar_texto(text_area.get("1.0", tk.END)), style='TButton')
        analyze_button.pack(side=tk.RIGHT, padx=10, pady=10)

        clear_button = ttk.Button(button_frame, text="Limpiar pantalla", command=lambda: text_area.delete('1.0', tk.END), style='TButton')
        clear_button.pack(side=tk.RIGHT, padx=10, pady=10)

    def identificar_lenguaje_por_extension(self, extension, content):
        switcher = {
            '.sql': ('SQL', run_sql_tests),
            '.cpp': ('C++', run_cpp_tests),
            '.html': ('HTML', run_html_tests),
            '.htm': ('HTML', run_html_tests),
            '.js': ('JavaScript', run_js_tests),
            '.pas': ('Pascal', run_pascal_tests),
            '.py': ('Python', run_python_tests)
        }
        try:
            if extension in switcher:
                lenguaje, funcion = switcher[extension]
                resultado = funcion(content)
            else:
                lenguaje = 'Lenguaje desconocido'
                resultado = 'No se pudo identificar el lenguaje.'
        except Exception as e:
            lenguaje = 'Error'
            resultado = f"Error durante el análisis: {e}"
        return lenguaje, resultado

    def identificar_lenguaje_por_contenido(self, content):
        # Esta función intenta identificar el lenguaje basado en el contenido del texto
        if "SELECT" in content and "FROM" in content:
            return "SQL", run_sql_tests
        elif "#include" in content or "int main" in content or "void main" in content:
            return "C++", run_cpp_tests
        elif "<html>" in content or "<body>" in content:
            return "HTML", run_html_tests
        elif "function" in content or "var " in content:
            return "JavaScript", run_js_tests
        elif "BEGIN" in content or "END" in content:
            return "Pascal", run_pascal_tests
        elif "def " in content or "import " in content or "print(" in content:
            return "Python", run_python_tests
        else:
            return "Lenguaje desconocido", lambda x: "No se pudo identificar el lenguaje."

    def analizar_texto(self, content):
        lenguaje, funcion = self.identificar_lenguaje_por_contenido(content)
        resultado = funcion(content)
        self.mostrar_resultados(lenguaje, resultado)

    def mostrar_resultados(self, lenguaje, resultado):
        result_window = tk.Toplevel(self)
        result_window.title(f"Resultados de Análisis - {lenguaje}")
        result_window.configure(bg='#03A062')
        result_window.geometry("700x400")

        text_area = tkScrolledText.ScrolledText(result_window, wrap=tk.WORD, font=('Courier New', 12), background='#03A062', foreground='black')
        text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        text_area.insert(tk.END, resultado)
        text_area.config(state='disabled')

if __name__ == '__main__':
    app = Application()
    app.mainloop()