"""
    vista
"""
import tkinter as tk
from tkinter import font

# Importaciones de tus controladores (asegúrate de que las rutas sean correctas)
from src.controlador.login_controller import LoginController
from src.controlador.register_controller import RegisterUserController
from src.controlador.main_view_controller import MainViewController
from src.controlador.task_controller import TaskController


class RootView:
    """
    Clase Raíz mejorada con un tema centralizado para una apariencia moderna y consistente.
    """
    # --- TEMA DE LA APLICACIÓN ---
    COLOR_BACKGROUND = '#FDFEFE'  # Un blanco casi puro, muy limpio
    COLOR_FRAME = '#F2F3F4'  # Un gris muy claro para los marcos
    COLOR_PRIMARY = '#0A79DF'  # Azul principal para botones y elementos interactivos
    COLOR_SUCCESS = '#28B463'  # Verde para acciones exitosas
    COLOR_DANGER = '#E74C3C'  # Rojo para alertas o botones de estado "incompleto"
    COLOR_TEXT_LIGHT = '#FEFEFE'  # Texto blanco para fondos oscuros
    COLOR_TEXT_DARK = '#212529'  # Texto oscuro para fondos claros

    FONT_TITLE = ("Helvetica", 22, "bold")
    FONT_BODY = ("Helvetica", 12)
    FONT_BUTTON = ("Helvetica", 11, "bold")
    FONT_LABEL = ("Helvetica", 12, "bold")
    # -----------------------------

    componentes = {}

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("700x550")
        self.root.config(bg=self.COLOR_BACKGROUND)
        self.root.title('TO-DO LIST | By Gemini')
        self.center_window()

    def center_window(self):
        """Centra la ventana en la pantalla."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def __comprobate_existe(self, name):
        """Comprueba si un componente ya existe y lo destruye."""
        if componente := self.componentes.get(name):
            componente.destroy()

    def create_button(self, container, name: str, funcion, text: str = '',
                      bg=COLOR_PRIMARY, fg=COLOR_TEXT_LIGHT, pack_info=None):
        """Crea un botón con el estilo moderno."""
        self.__comprobate_existe(name)
        if pack_info is None:
            pack_info = {'pady': 10, 'ipadx': 20, 'ipady': 5, 'fill': 'x'}

        bt = tk.Button(container, text=text, command=funcion, bg=bg, fg=fg,
                       font=self.FONT_BUTTON, relief='flat', borderwidth=0,
                       activebackground=self.COLOR_SUCCESS, activeforeground=self.COLOR_TEXT_LIGHT,
                       cursor="hand2")
        bt.pack(**pack_info)
        self.componentes[name] = bt

    def create_input(self, container, name, secret=False, pack_info=None):
        """Crea un campo de entrada con estilo."""
        self.__comprobate_existe(name)
        if pack_info is None:
            pack_info = {'pady': 5, 'ipady': 4, 'fill': 'x'}

        inp = tk.Entry(container, show='•' if secret else '', font=self.FONT_BODY,
                       bg=self.COLOR_BACKGROUND, fg=self.COLOR_TEXT_DARK,
                       relief='solid', borderwidth=1)
        inp.pack(**pack_info)
        self.componentes[name] = inp

    def create_label(self, container, name, text: str = '', fg: str = COLOR_TEXT_DARK,
                     font_style=None, pack_info=None):
        """Crea una etiqueta con estilo."""
        if font_style is None:
            font_style = self.FONT_BODY
        if pack_info is None:
            pack_info = {'pady': 2}
        self.__comprobate_existe(name)

        lbl = tk.Label(container, text=text, fg=fg, bg=container.cget('bg'), font=font_style)
        lbl.pack(**pack_info)
        self.componentes[name] = lbl

    def btn_cambiar_secret_input(self, name_input: str, name_button: str):
        """Alterna la visibilidad de la contraseña en un input."""
        simbolo = '' if self.componentes[name_input].cget('show') else '•'
        self.componentes[name_input].config(show=simbolo)

        texto_boton = 'Ocultar' if simbolo == '' else 'Mostrar'
        self.componentes[name_button].config(text=texto_boton)

    def limpiar_componentes(self):
        """Destruye todos los widgets hijos del root para limpiar la ventana."""
        for widget in self.root.winfo_children():
            widget.destroy()
        self.componentes.clear()

    def main(self):
        self.root.mainloop()

    def cerrar_ventana(self):
        self.root.destroy()


class LoginInView:
    def __init__(self, root: RootView):
        self.root = root
        self.create_login()
        # self.root.main() # No es necesario llamarlo aquí, se llama al final

    @staticmethod
    def independent_login():
        root = RootView()
        login_view = LoginInView(root)
        root.main()  # Se llama aquí para iniciar la aplicación
        return login_view

    def create_login(self):
        """Crea la interfaz de inicio de sesión centrada y con estilo."""
        self.root.limpiar_componentes()
        main_frame = tk.Frame(self.root.root, bg=self.root.COLOR_FRAME, padx=40, pady=40)
        main_frame.pack(expand=True)

        self.root.create_label(main_frame, name='lblLoginTitle', text='Inicio de Sesión',
                               font_style=self.root.FONT_TITLE, pack_info={'pady': (0, 20)})

        self.root.create_label(main_frame, name='lblAliasLogin', text='Alias de Usuario',
                               font_style=self.root.FONT_LABEL, pack_info={'pady': (10, 0), 'anchor': 'w'})
        self.root.create_input(main_frame, name='alias')

        self.root.create_label(main_frame, name='lblPasswordLogin', text='Contraseña',
                               font_style=self.root.FONT_LABEL, pack_info={'pady': (10, 0), 'anchor': 'w'})
        self.root.create_input(main_frame, name='password', secret=True)

        self.root.create_button(main_frame, name='btnOcultarPassLogin', text='Mostrar',
                                funcion=self.btn_mostrar_contrasena, bg='#6C757D',
                                pack_info={'pady': 5, 'ipadx': 10, 'ipady': 2, 'anchor': 'e'})

        self.root.create_button(main_frame, name='btnLogin', funcion=self.btn_login, text='Ingresar')

        self.root.create_label(main_frame, name='lblGoToRegister', text='¿No tienes una cuenta?')
        self.root.create_button(main_frame, name='btnRegistrase', funcion=self.go_to_register,
                                text='Regístrate Aquí', bg=self.root.COLOR_SUCCESS)

    def go_to_register(self):
        RegisterUserView(root=self.root)

    def btn_mostrar_contrasena(self):
        self.root.btn_cambiar_secret_input(name_input='password', name_button='btnOcultarPassLogin')

    def btn_login(self):
        alias = self.root.componentes.get('alias').get()
        password = self.root.componentes.get('password').get()
        is_login, response = LoginController.login(alias, password)

        if is_login:
            MainView(self.root)
            return

        # Etiqueta de error
        container = self.root.componentes.get('btnLogin').master
        self.root.create_label(container, name='login_error', text=response,
                               fg=self.root.COLOR_DANGER, font_style=(self.root.FONT_BODY[0], 10, "italic"))


class RegisterUserView:
    def __init__(self, root: RootView):
        self.root = root
        self.create_register_interface()

    def create_register_interface(self):
        """Crea la interfaz de registro con un formulario bien alineado."""
        self.root.limpiar_componentes()
        main_frame = tk.Frame(self.root.root, bg=self.root.COLOR_FRAME, padx=40, pady=40)
        main_frame.pack(expand=True)

        self.root.create_label(main_frame, name='lblRegisterTitle', text='Crear Cuenta',
                               font_style=self.root.FONT_TITLE, pack_info={'pady': (0, 20)})

        # Usamos grid para alinear etiquetas y entradas
        form_frame = tk.Frame(main_frame, bg=main_frame.cget('bg'))
        form_frame.pack()

        labels_texts = ['Nombres:', 'Apellidos:', 'Alias:', 'Contraseña:', 'Confirmar Contraseña:']
        inputs_names = ['inpNombreRegistro', 'inpApellidoRegistro', 'inpAliasRegistro',
                        'inpContraseñaRegistro', 'inpConfirmarContraseñaRegistro']

        for i, text in enumerate(labels_texts):
            lbl = tk.Label(form_frame, text=text, font=self.root.FONT_LABEL, bg=form_frame.cget('bg'),
                           fg=self.root.COLOR_TEXT_DARK)
            lbl.grid(row=i, column=0, sticky='w', pady=5, padx=5)

            is_secret = 'Contraseña' in text
            inp = tk.Entry(form_frame, show='•' if is_secret else '', font=self.root.FONT_BODY,
                           bg=self.root.COLOR_BACKGROUND, fg=self.root.COLOR_TEXT_DARK, relief='solid', borderwidth=1)
            inp.grid(row=i, column=1, sticky='ew', pady=5, padx=5, ipady=4)
            self.root.componentes[inputs_names[i]] = inp

        self.root.create_button(main_frame, name='btnRegistrarUsuario', text='Registrarse',
                                funcion=self.btn_registrar_usuario, bg=self.root.COLOR_SUCCESS)
        self.root.create_button(main_frame, name='btnRegresarLogin', text='Volver al Inicio',
                                funcion=self.go_to_login, bg='#6C757D')

    def btn_registrar_usuario(self):
        nombres = self.root.componentes.get('inpNombreRegistro').get()
        apellidos = self.root.componentes.get('inpApellidoRegistro').get()
        alias = self.root.componentes.get('inpAliasRegistro').get()
        password = self.root.componentes.get('inpContraseñaRegistro').get()
        confirm_password = self.root.componentes.get('inpConfirmarContraseñaRegistro').get()

        is_user_save, response = RegisterUserController.register_user(
            nombres=nombres, apellidos=apellidos, alias=alias,
            password=password, confirm_password=confirm_password)

        container = self.root.componentes.get('btnRegistrarUsuario').master
        color = self.root.COLOR_SUCCESS if is_user_save else self.root.COLOR_DANGER

        self.root.create_label(container, name='lblRegistroSuccess', text=response, fg=color)

        if is_user_save:
            self.root.componentes.get('btnRegistrarUsuario').config(state='disabled')
            self.root.create_button(container, name='btnAceptarRegistro', text='Aceptar',
                                    funcion=self.go_to_login, bg=self.root.COLOR_PRIMARY)

    def go_to_login(self):
        LoginInView(self.root)


class MainView:
    tareas: list = []

    def __init__(self, root: RootView):
        self.root = root
        self.create_main_interface()

    def create_main_interface(self):
        """Crea la interfaz principal con cabecera y lista de tareas."""
        self.root.limpiar_componentes()

        # --- Cabecera ---
        header_frame = tk.Frame(self.root.root, bg=self.root.COLOR_FRAME, padx=20, pady=10)
        header_frame.pack(fill='x')

        self.root.create_button(header_frame, name='btnCrearTarea', text='✚ Nueva Tarea',
                                funcion=self.go_to_create_tarea, bg=self.root.COLOR_PRIMARY,
                                pack_info={'side': 'left', 'padx': 10})
        self.root.create_button(header_frame, name='btnLogOut', text='Cerrar Sesión',
                                funcion=self.go_to_login, bg=self.root.COLOR_DANGER,
                                pack_info={'side': 'right', 'padx': 10})

        # --- Contenedor de Tareas ---
        self.tasks_container = tk.Frame(self.root.root, bg=self.root.COLOR_BACKGROUND, padx=20, pady=20)
        self.tasks_container.pack(fill='both', expand=True)

        self.root.create_label(self.tasks_container, name='lblTasksTitle', text='Tareas para Hoy',
                               font_style=self.root.FONT_TITLE, pack_info={'pady': (0, 20)})
        self.create_tasks_view()

    def create_tasks_view(self):
        """Obtiene y muestra las tareas en la interfaz."""
        for widget in self.tasks_container.winfo_children():
            if 'Task' in widget.winfo_name() or 'NoTasks' in widget.winfo_name():
                widget.destroy()

        is_task_recover, response = MainViewController.recover_task_today_with_format()

        if not is_task_recover:
            self.root.create_label(self.tasks_container, name='lblNoTasksError', text=response,
                                   fg=self.root.COLOR_DANGER)
            return

        self.tareas = response
        if not self.tareas:
            self.root.create_label(self.tasks_container, name='lblAreNoTasks',
                                   text='🎉 ¡Felicidades! No hay tareas pendientes para hoy.',
                                   fg='#6C757D', font_style=("Helvetica", 14, "italic"))
            return

        task_header = tk.Frame(self.tasks_container, bg=self.tasks_container.cget('bg'))
        task_header.pack(fill='x', pady=(0, 10))
        headers = ['Nombre', 'Fecha', 'Prioridad', 'Acciones']
        for i, h in enumerate(headers):
            tk.Label(task_header, text=h, font=self.root.FONT_LABEL, bg=task_header.cget('bg')).pack(side='left',
                                                                                                     expand=True)

        for i, tarea in enumerate(self.tareas):
            self.insert_task_view(tarea, i)

    def insert_task_view(self, tarea: dict, index: int):
        """Inserta una única fila de tarea con un diseño moderno."""
        task_id = tarea.get('id')

        task_frame = tk.Frame(self.tasks_container, name=f'frameTask{task_id}',
                              bg=self.root.COLOR_FRAME, relief='solid', borderwidth=1, padx=10, pady=10)
        task_frame.pack(fill='x', pady=5)

        info_text = f"{tarea.get('nombre')}"
        info_fecha = f"{tarea.get('fecha')}"
        info_prioridad = f"Prioridad: {tarea.get('prioridad')}"

        tk.Label(task_frame, text=info_text, font=self.root.FONT_BODY, bg=task_frame.cget('bg')).pack(side='left',
                                                                                                      expand=True,
                                                                                                      anchor='w')
        tk.Label(task_frame, text=info_fecha, font=self.root.FONT_BODY, bg=task_frame.cget('bg')).pack(side='left',
                                                                                                       expand=True)
        tk.Label(task_frame, text=info_prioridad, font=self.root.FONT_BODY, bg=task_frame.cget('bg')).pack(side='left',
                                                                                                           expand=True)

        actions_frame = tk.Frame(task_frame, bg=task_frame.cget('bg'))
        actions_frame.pack(side='left', expand=True)

        realizado = tarea.get('realizado')
        check_bg = self.root.COLOR_SUCCESS if realizado else self.root.COLOR_DANGER
        check_text = '✔' if realizado else '✖'

        # --- CAMBIO IMPORTANTE AQUÍ ---
        # La lambda ahora solo pasa el id y el índice, no el estado 'realizado'
        btn_check = tk.Button(actions_frame, name=f'btnCheckTask{task_id}', text=check_text,
                              bg=check_bg, fg=self.root.COLOR_TEXT_LIGHT, font=self.root.FONT_BUTTON,
                              relief='flat', cursor="hand2",
                              command=lambda id=task_id, idx=index: self.btn_check_task(id, idx))
        btn_check.pack(side='left', padx=5)
        self.root.componentes[f'btnCheckTask{task_id}'] = btn_check

        btn_edit = tk.Button(actions_frame, name=f'btnEditTask{task_id}', text='Editar',
                             bg='#6C757D', fg=self.root.COLOR_TEXT_LIGHT, font=self.root.FONT_BUTTON,
                             relief='flat', cursor="hand2",
                             command=lambda id=task_id, idx=index: self.btn_edit_task(id, idx))
        btn_edit.pack(side='left', padx=5)
        self.root.componentes[f'btnEditTask{task_id}'] = btn_edit

    # --- CAMBIO IMPORTANTE AQUÍ ---
    # La función ahora busca el estado actual antes de cambiarlo
    def btn_check_task(self, id_tarea, indice):
        # 1. Obtener el estado actual de la tarea desde nuestra lista de datos
        estado_actual = self.tareas[indice]['realizado']

        # 2. Calcular el nuevo estado
        nuevo_estado = not estado_actual

        # 3. Llamar al controlador para actualizar el backend
        is_change_task, response = TaskController.event_update_task_session_manager(id_tarea, realizado=nuevo_estado)

        if not is_change_task:
            # Si hay un error en el backend, no hacemos cambios en la UI
            return

        # 4. Actualizar el estado en la lista local y la apariencia del botón
        self.tareas[indice]['realizado'] = nuevo_estado
        btn_check = self.root.componentes.get(f'btnCheckTask{id_tarea}')
        if btn_check:
            new_bg = self.root.COLOR_SUCCESS if nuevo_estado else self.root.COLOR_DANGER
            new_text = '✔' if nuevo_estado else '✖'
            btn_check.config(bg=new_bg, text=new_text)

    def btn_edit_task(self, id_task, indice):
        print(f"Funcionalidad de editar tarea ID: {id_task} aún no implementada en la vista.")
        pass

    def go_to_create_tarea(self):
        RegisterTareaUserView(self.root)

    def go_to_login(self):
        MainViewController.log_out()
        LoginInView(self.root)


class RegisterTareaUserView:
    def __init__(self, root: RootView):
        self.root = root
        self.create_fomulate_tarea()

    def create_fomulate_tarea(self):
        """Crea la interfaz para registrar una nueva tarea."""
        self.root.limpiar_componentes()
        main_frame = tk.Frame(self.root.root, bg=self.root.COLOR_FRAME, padx=40, pady=40)
        main_frame.pack(expand=True)

        self.root.create_label(main_frame, name='lblCreateTaskTitle', text='Registrar Nueva Tarea',
                               font_style=self.root.FONT_TITLE, pack_info={'pady': (0, 20)})

        # Formulario con grid
        form_frame = tk.Frame(main_frame, bg=main_frame.cget('bg'))
        form_frame.pack()

        labels_texts = ['Nombre de la Tarea:', 'Fecha (dd-mm-aaaa):', 'Prioridad (1-5):', 'Detalle:']
        inputs_names = ['inpNombreCreateTareaUser', 'inpFechaProgramadaCreateTareaUser', 'inpPrioridadCreateTarea', 'inpDetalleCreateTarea']

        for i, text in enumerate(labels_texts):
            lbl = tk.Label(form_frame, text=text, font=self.root.FONT_LABEL, bg=form_frame.cget('bg'),
                           fg=self.root.COLOR_TEXT_DARK)
            lbl.grid(row=i, column=0, sticky='w', pady=5, padx=5)

            inp = tk.Entry(form_frame, font=self.root.FONT_BODY, bg=self.root.COLOR_BACKGROUND,
                           fg=self.root.COLOR_TEXT_DARK, relief='solid', borderwidth=1)
            inp.grid(row=i, column=1, sticky='ew', pady=5, padx=5, ipady=4)
            self.root.componentes[inputs_names[i]] = inp

        self.root.create_button(main_frame, name='btnRegistrarTareaCreateTarea', text='Guardar Tarea',
                                funcion=self.btn_registrar_tarea, bg=self.root.COLOR_SUCCESS)
        self.root.create_button(main_frame, name='btnVolverCreateTareaUser', text='Volver',
                                funcion=self.btn_volver, bg='#6C757D')

    def btn_registrar_tarea(self):
        nombre = self.root.componentes.get('inpNombreCreateTareaUser').get()
        fecha = self.root.componentes.get('inpFechaProgramadaCreateTareaUser').get()
        prioridad = self.root.componentes.get('inpPrioridadCreateTarea').get()
        detalle = self.root.componentes.get('inpDetalleCreateTarea').get()
        is_registered_task, response = TaskController.event_register_task_user(
            nombre=nombre, fecha=fecha, prioridad=prioridad, detalle= detalle)

        container = self.root.componentes.get('btnRegistrarTareaCreateTarea').master
        color = self.root.COLOR_SUCCESS if is_registered_task else self.root.COLOR_DANGER

        if is_registered_task:
            self.root.componentes.get('btnRegistrarTareaCreateTarea').config(state='disabled')
            self.root.create_label(container, 'lblTareaAnadida', text=response, fg=color)
            self.root.create_button(container, 'btnAceptarRegistroCreateTarea', text='Aceptar',
                                    funcion=self.btn_aceptar_crear_tarea)
        else:
            self.root.create_label(container, 'lblErrorCreateTarea', text=response, fg=color)

    def btn_volver(self):
        MainView(self.root)

    def btn_aceptar_crear_tarea(self):
        MainView(self.root)


# Punto de entrada de la aplicación (si este archivo se ejecuta directamente)
if __name__ == '__main__':
    # Esto te permite probar la vista de forma independiente
    # La aplicación comenzará desde la pantalla de login.
    LoginInView.independent_login()