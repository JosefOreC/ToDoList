import tkinter as tk
from tkinter import ttk
from tkinter import Toplevel
from tkinter import messagebox
from tkinter import Text # For multiline details


from src.controlador.login_controller import LoginController
from src.controlador.register_controller import RegisterUserController
from src.controlador.main_view_controller import MainViewController
from src.controlador.task_controller import TaskController
from src.controlador.group_controller import GroupController
from src.controlador.user_controller import UserController
from src.controlador.session_controller import SessionController

class RootView:
    # --- TEMA DE LA APLICACIÓN ---
    COLOR_BACKGROUND = '#FDFEFE'
    COLOR_FRAME = '#F2F3F4'
    COLOR_PRIMARY = '#0A79DF'
    COLOR_SUCCESS = '#28B463'
    COLOR_DANGER = '#E74C3C'
    COLOR_TEXT_LIGHT = '#FEFEFE'
    COLOR_TEXT_DARK = '#212529'
    FONT_TITLE = ("Helvetica", 22, "bold")
    FONT_BODY = ("Helvetica", 12)
    FONT_BUTTON = ("Helvetica", 11, "bold")
    FONT_LABEL = ("Helvetica", 12, "bold")
    componentes = {}

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1150x750") # Adjusted size
        self.root.config(bg=self.COLOR_BACKGROUND)
        self.root.title('TO-DO LIST | By Gemini')
        self.center_window()

    def center_window(self, top_level_window=None):
        window = top_level_window if top_level_window else self.root
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')

    def comprobate_existe(self, name):
        # Si el componente existe en el diccionario y el widget aún existe en Tkinter
        if name in self.componentes:
            componente = self.componentes.pop(name) # Quitar del diccionario
            if componente and componente.winfo_exists(): # Verificar si el widget existe
                 componente.destroy()


    def create_button(self, container, name: str, funcion, text: str = '',
                      bg=COLOR_PRIMARY, fg=COLOR_TEXT_LIGHT, pack_info=None):
        self.comprobate_existe(name)
        if pack_info is None:
            pack_info = {'pady': 10, 'ipadx': 20, 'ipady': 5, 'fill': 'x'}

        bt = tk.Button(container, text=text, command=funcion, bg=bg, fg=fg,
                       font=self.FONT_BUTTON, relief='flat', borderwidth=0,
                       activebackground=self.COLOR_SUCCESS, activeforeground=self.COLOR_TEXT_LIGHT,
                       cursor="hand2")
        bt.pack(**pack_info)
        self.componentes[name] = bt
        return bt

    def create_input(self, container, name, secret=False, pack_info=None):
        self.comprobate_existe(name)
        if pack_info is None:
            pack_info = {'pady': 5, 'ipady': 4, 'fill': 'x'}

        inp = tk.Entry(container, show='•' if secret else '', font=self.FONT_BODY,
                       bg=self.COLOR_BACKGROUND, fg=self.COLOR_TEXT_DARK,
                       relief='solid', borderwidth=1)
        inp.pack(**pack_info)
        self.componentes[name] = inp
        return inp

    def create_label(self, container, name, text: str = '', fg: str = COLOR_TEXT_DARK,
                     font_style=None, pack_info=None):
        if font_style is None:
            font_style = self.FONT_BODY
        if pack_info is None:
            pack_info = {'pady': 2}
        self.comprobate_existe(name)

        lbl = tk.Label(container, text=text, fg=fg, bg=container.cget('bg'), font=font_style)
        lbl.pack(**pack_info)
        self.componentes[name] = lbl
        return lbl

    def btn_cambiar_secret_input(self, name_input: str, name_button: str):
        if name_input not in self.componentes or name_button not in self.componentes:
            # print(f"Warning: Input '{name_input}' or button '{name_button}' not found in componentes.")
            return
        inp_widget = self.componentes[name_input]
        btn_widget = self.componentes[name_button]

        if not (inp_widget.winfo_exists() and btn_widget.winfo_exists()):
            # print(f"Warning: Input '{name_input}' or button '{name_button}' widget does not exist.")
            return

        simbolo = '' if inp_widget.cget('show') else '•'
        inp_widget.config(show=simbolo)
        texto_boton = 'Ocultar' if simbolo == '' else 'Mostrar'
        btn_widget.config(text=texto_boton)


    def limpiar_componentes(self):
        # Destruye los widgets que están almacenados en el diccionario de componentes
        widget_names_to_remove = list(self.componentes.keys())
        for name in widget_names_to_remove:
            self.comprobate_existe(name) # Esto también los elimina del diccionario

        # Destruye cualquier otro widget hijo directo de root que no estuviera en el diccionario
        for widget in self.root.winfo_children():
            if widget.winfo_exists(): # Por si acaso alguno ya fue destruido
                widget.destroy()
        self.componentes.clear() # El diccionario ya debería estar vacío

    def main(self):
        self.root.mainloop()

    def cerrar_ventana(self):
        self.root.destroy()


class LoginInView:
    def __init__(self, root: RootView):
        self.root = root
        self.create_login()

    @staticmethod
    def independent_login():
        root_app = RootView()
        # If you have a SessionManager that persists login state across app runs (unlikely for Tkinter simple setup)
        # you might check SessionController.get_alias_user() here.
        # For typical Tkinter, LoginInView is always the entry.
        login_view = LoginInView(root_app)
        root_app.main()
        return login_view

    def create_login(self):
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
        alias_entry = self.root.componentes.get('alias')
        password_entry = self.root.componentes.get('password')

        if not alias_entry or not password_entry : # Check if components exist
            messagebox.showerror("Error Interno", "Componentes de login no encontrados.")
            return

        alias = alias_entry.get()
        password = password_entry.get()
        is_login, response = LoginController.login(alias, password)

        if is_login:
            MainView(self.root)
            return

        container = self.root.componentes.get('btnLogin').master # Get parent frame
        # Ensure only one error label is shown/updated
        if 'login_error' in self.root.componentes:
            if self.root.componentes['login_error'].winfo_exists():
                 self.root.componentes['login_error'].config(text=response)
            else: # Widget was destroyed, recreate
                 del self.root.componentes['login_error'] # Remove from dict
                 self.root.create_label(container, name='login_error', text=response,
                                   fg=self.root.COLOR_DANGER, font_style=(self.root.FONT_BODY[0], 10, "italic"))
        else:
            self.root.create_label(container, name='login_error', text=response,
                                   fg=self.root.COLOR_DANGER, font_style=(self.root.FONT_BODY[0], 10, "italic"))


class RegisterUserView:
    def __init__(self, root: RootView):
        self.root = root
        self.create_register_interface()

    def create_register_interface(self):
        self.root.limpiar_componentes()
        main_frame = tk.Frame(self.root.root, bg=self.root.COLOR_FRAME, padx=40, pady=40)
        main_frame.pack(expand=True)
        self.root.create_label(main_frame, name='lblRegisterTitle', text='Crear Cuenta',
                               font_style=self.root.FONT_TITLE, pack_info={'pady': (0, 20)})
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
            self.root.componentes[inputs_names[i]] = inp # Store input field
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

        if 'lblRegistroSuccess' in self.root.componentes:
            if self.root.componentes['lblRegistroSuccess'].winfo_exists():
                self.root.componentes['lblRegistroSuccess'].config(text=response, fg=color)
            else:
                del self.root.componentes['lblRegistroSuccess']
                self.root.create_label(container, name='lblRegistroSuccess', text=response, fg=color)
        else:
            self.root.create_label(container, name='lblRegistroSuccess', text=response, fg=color)

        if is_user_save:
            self.root.componentes.get('btnRegistrarUsuario').config(state='disabled')
            self.root.create_button(container, name='btnAceptarRegistro', text='Aceptar',
                                    funcion=self.go_to_login, bg=self.root.COLOR_PRIMARY)

    def go_to_login(self):
        LoginInView(self.root)


class MainView:
    tareas: list = []

    def __init__(self, root: 'RootView'):
        self.root = root
        self.tasks_widgets_frame = None # Frame to hold task_header and individual task_frames
        self.create_main_interface()

    def create_main_interface(self):
        self.root.limpiar_componentes() # Clears self.root.componentes too

        header_frame = tk.Frame(self.root.root, bg=self.root.COLOR_FRAME, padx=20, pady=10)
        header_frame.pack(fill='x')
        self.root.componentes['main_header_frame'] = header_frame

        pack_info_header_btn = {'side': 'left', 'padx': 5, 'ipady':3, 'ipadx':10} # Consistent padding
        self.root.create_button(header_frame, name='btnRefreshTasks', text='Refrescar 🔄',
                                funcion=self.refresh_tasks_view, bg='#17A2B8', pack_info=pack_info_header_btn)
        self.root.create_button(header_frame, name='btnCrearTarea', text='✚ Nueva Tarea',
                                funcion=self.go_to_create_tarea, bg=self.root.COLOR_PRIMARY, pack_info=pack_info_header_btn)
        self.root.create_button(header_frame, name='btnCrearGrupo', text='✚ Nuevo Grupo',
                                funcion=self.go_to_create_group, bg=self.root.COLOR_SUCCESS, pack_info=pack_info_header_btn)
        self.root.create_button(header_frame, name='btnMiPerfil', text='Mi Perfil',
                                funcion=self.go_to_profile, bg='#6C757D',
                                pack_info={'side': 'right', 'padx': 10, 'ipady':3, 'ipadx':10})
        self.root.create_button(header_frame, name='btnLogOut', text='Cerrar Sesión',
                                funcion=self.go_to_login, bg=self.root.COLOR_DANGER,
                                pack_info={'side': 'right', 'padx': 10, 'ipady':3, 'ipadx':10})

        content_frame = tk.Frame(self.root.root, bg=self.root.COLOR_BACKGROUND, padx=20, pady=20)
        content_frame.pack(fill='both', expand=True)
        self.root.componentes['main_content_frame'] = content_frame

        lbl_tasks_title = tk.Label(content_frame, text='Tareas para Hoy',
                                   font=self.root.FONT_TITLE, bg=content_frame.cget('bg'),
                                   fg=self.root.COLOR_TEXT_DARK)
        lbl_tasks_title.pack(pady=(0, 10))
        self.root.componentes['lblTasksTitle'] = lbl_tasks_title

        self.tasks_widgets_frame = tk.Frame(content_frame, bg=content_frame.cget('bg'))
        self.tasks_widgets_frame.pack(fill='both', expand=True)
        self.root.componentes['tasks_widgets_frame_container'] = self.tasks_widgets_frame

        self.create_tasks_view()

    def create_tasks_view(self):
        for widget in self.tasks_widgets_frame.winfo_children():
            for name, comp_widget in list(self.root.componentes.items()):
                if comp_widget == widget:
                    del self.root.componentes[name]
                    break
            widget.destroy()
        self.root.comprobate_existe('lblNoTasksError')
        self.root.comprobate_existe('lblAreNoTasks')

        is_task_recover, response_data = MainViewController.recover_task_today_with_format()

        if not is_task_recover:
            self.root.create_label(self.tasks_widgets_frame, name='lblNoTasksError', text=response_data,
                                   fg=self.root.COLOR_DANGER, font_style=self.root.FONT_BODY, pack_info={'pady': 20})
            return

        self.tareas = response_data
        if not self.tareas:
            self.root.create_label(self.tasks_widgets_frame, name='lblAreNoTasks',
                                   text='🎉 ¡Felicidades! No hay tareas pendientes para hoy.',
                                   fg='#6C757D', font_style=("Helvetica", 14, "italic"), pack_info={'pady': 20})
            return

        task_header_display_frame = tk.Frame(self.tasks_widgets_frame, name='task_header_display_frame', bg=self.tasks_widgets_frame.cget('bg'))
        task_header_display_frame.pack(fill='x', pady=(0, 5))

        headers = ['Nombre', 'Grupo', 'Fecha', 'Prioridad', 'Acciones']
        col_weights = [4, 2, 2, 1, 5]
        for i, h_text in enumerate(headers):
            task_header_display_frame.grid_columnconfigure(i, weight=col_weights[i])
            tk.Label(task_header_display_frame, text=h_text, font=self.root.FONT_LABEL,
                     bg=task_header_display_frame.cget('bg'), fg=self.root.COLOR_TEXT_DARK).grid(row=0, column=i, sticky='nsew', padx=2)

        for i, tarea_dict in enumerate(self.tareas):
            self.insert_task_view(tarea_dict, i)

    def insert_task_view(self, tarea: dict, index: int):
        task_id = tarea.get('id_tarea') # USE 'id_tarea'

        disponible_para_usuario = tarea.get('disponible', True) # Already using 'disponible'
        es_de_grupo = tarea.get('is_in_group', False)       # USE 'is_in_group'
        rol_usuario_en_grupo = tarea.get('rol', None)       # Already using 'rol'

        task_frame_name = f'frameTask_{task_id}_{index}'
        task_frame = tk.Frame(self.tasks_widgets_frame, name=task_frame_name,
                              bg=self.root.COLOR_FRAME, relief='solid', borderwidth=1, padx=5, pady=5)
        task_frame.pack(fill='x', pady=3)
        self.root.componentes[task_frame_name] = task_frame

        col_weights = [4, 2, 2, 1, 5]
        for i in range(len(col_weights)): task_frame.grid_columnconfigure(i, weight=col_weights[i])

        tk.Label(task_frame, text=tarea.get('nombre'), font=self.root.FONT_BODY, bg=task_frame.cget('bg'),
                 fg=self.root.COLOR_TEXT_DARK, anchor='w', justify='left', wraplength=300).grid(row=0, column=0, sticky='w', padx=2)
        tk.Label(task_frame, text=tarea.get('grupo', 'N/A'), font=self.root.FONT_BODY, bg=task_frame.cget('bg'),
                 fg=self.root.COLOR_TEXT_DARK, anchor='w').grid(row=0, column=1, sticky='w', padx=2)
        fecha_str = tarea.get('fecha', 'N/A')
        tk.Label(task_frame, text=fecha_str, font=self.root.FONT_BODY, bg=task_frame.cget('bg'),
                 fg=self.root.COLOR_TEXT_DARK, anchor='w').grid(row=0, column=2, sticky='w', padx=2)
        tk.Label(task_frame, text=f"P: {tarea.get('prioridad')}", font=self.root.FONT_BODY,
                 bg=task_frame.cget('bg'), fg=self.root.COLOR_TEXT_DARK, anchor='w').grid(row=0, column=3, sticky='w', padx=2)

        actions_frame = tk.Frame(task_frame, bg=task_frame.cget('bg'))
        actions_frame.grid(row=0, column=4, sticky='e', padx=2)

        # A.1 & A.2: Permission Logic
        can_check = disponible_para_usuario
        can_edit = disponible_para_usuario and (not es_de_grupo or rol_usuario_en_grupo not in ['miembro'])
        # User can archive if not a member of a group task, OR if it's their own task.
        # If task is available to them, they can archive. If they are master/editor, they can archive.
        can_archive = (disponible_para_usuario and es_de_grupo) or \
                      (es_de_grupo and rol_usuario_en_grupo not in ['miembro']) or \
                      (not es_de_grupo) # Individual tasks always archivable by owner (disponible should be true)

        can_delete = not es_de_grupo or rol_usuario_en_grupo not in ['miembro'] # Only non-members of group tasks, or masters/editors

        realizado = tarea.get('realizado', False)
        check_bg = self.root.COLOR_SUCCESS if realizado else self.root.COLOR_DANGER
        check_text = '✔' if realizado else '✖'
        btn_check_name = f'btnCheckTask_{task_id}_{index}'
        btn_check = tk.Button(actions_frame, name=btn_check_name, text=check_text, bg=check_bg, fg=self.root.COLOR_TEXT_LIGHT,
                              font=self.root.FONT_BUTTON, relief='flat', width=3,
                              command=lambda id_t=task_id, idx=index: self.btn_check_task(id_t, idx))
        if not can_check: btn_check.config(state='disabled', bg='#CCCCCC', fg='#666666', cursor="arrow")
        else: btn_check.config(cursor="hand2")
        btn_check.pack(side='left', padx=1)

        btn_edit_name = f'btnEditTask_{task_id}_{index}'
        btn_edit = tk.Button(actions_frame, name=btn_edit_name, text='Editar', bg='#6C757D', fg=self.root.COLOR_TEXT_LIGHT,
                             font=self.root.FONT_BUTTON, relief='flat',
                             command=lambda id_t=task_id, idx=index: self.btn_edit_task(id_t, idx))
        if not can_edit: btn_edit.config(state='disabled', bg='#CCCCCC', fg='#666666', cursor="arrow")
        else: btn_edit.config(cursor="hand2")
        btn_edit.pack(side='left', padx=1)

        btn_archive_name = f'btnArchiveTask_{task_id}_{index}'
        btn_archive = tk.Button(actions_frame, name=btn_archive_name, text='Archivar', bg='#5D6D7E', fg=self.root.COLOR_TEXT_LIGHT,
                                font=self.root.FONT_BUTTON, relief='flat',
                                command=lambda id_t=task_id: self.btn_archive_task(id_t))
        # A.1: User can archive if the task is available to them (even if they can't edit broadly)
        # A.2: Members cannot archive group tasks (unless it's specifically made available and they have rights)
        # Combining: if it's a group task AND user is just a member AND it's NOT available to them for action, disable archive.
        # Simpler: if `can_archive` is false, disable.
        if not can_archive:
             btn_archive.config(state='disabled', bg='#CCCCCC', fg='#666666', cursor="arrow")
        else: btn_archive.config(cursor="hand2")
        btn_archive.pack(side='left', padx=1)


        btn_delete_name = f'btnDeleteTask_{task_id}_{index}'
        btn_delete = tk.Button(actions_frame, name=btn_delete_name, text='Eliminar', bg=self.root.COLOR_DANGER, fg=self.root.COLOR_TEXT_LIGHT,
                               font=self.root.FONT_BUTTON, relief='flat',
                               command=lambda id_t=task_id: self.btn_delete_task(id_t))
        if not can_delete: btn_delete.config(state='disabled', bg='#CCCCCC', fg='#666666', cursor="arrow")
        else: btn_delete.config(cursor="hand2")
        btn_delete.pack(side='left', padx=1)

    def btn_check_task(self, id_tarea_from_btn, indice):
        if not (0 <= indice < len(self.tareas)): return
        tarea_actual = self.tareas[indice]
        if not tarea_actual.get('disponible', False):
            messagebox.showinfo("Información", "No tienes permiso para marcar/desmarcar esta tarea.")
            return
        nuevo_estado = not tarea_actual.get('realizado', False)
        is_change_task, response = TaskController.event_update_task_session_manager(id_tarea_from_btn, realizado=nuevo_estado)
        if is_change_task: self.refresh_tasks_view()
        else: messagebox.showerror("Error", f"No se pudo actualizar la tarea:\n{response}")

    def btn_edit_task(self, id_tarea_from_btn, indice):
        if not (0 <= indice < len(self.tareas)): return
        task_data = self.tareas[indice]
        es_de_grupo = task_data.get('is_in_group', False)
        rol_usuario_en_grupo = task_data.get('rol', None)
        can_edit = task_data.get('disponible', True) and (not es_de_grupo or rol_usuario_en_grupo not in ['miembro'])
        if not can_edit:
            messagebox.showinfo("Información", "No tienes permiso para editar esta tarea.")
            return
        if task_data.get('id_tarea') == id_tarea_from_btn: # USE 'id_tarea'
            EditTaskView(self.root, self, task_data)
        else: messagebox.showerror("Error", "Error de consistencia de datos: El ID de la tarea no coincide.")

    def btn_archive_task(self, id_tarea_from_btn):
        task_data = next((t for t in self.tareas if t.get('id_tarea') == id_tarea_from_btn), None) # USE 'id_tarea'
        if not task_data: return

        es_de_grupo = task_data.get('is_in_group', False)
        rol_usuario_en_grupo = task_data.get('rol', None)
        disponible_para_usuario = task_data.get('disponible', False)

        can_archive = (disponible_para_usuario and es_de_grupo) or \
                      (es_de_grupo and rol_usuario_en_grupo not in ['miembro']) or \
                      (not es_de_grupo)

        if not can_archive:
            messagebox.showinfo("Información", "No tienes permiso para archivar esta tarea.")
            return
        confirm = messagebox.askyesno(title="Confirmar Archivar", message="¿Estás seguro de que deseas archivar esta tarea?")
        if not confirm: return
        is_archived, response = TaskController.event_archive_task(id_tarea_from_btn) # Actual controller call
        if is_archived: self.refresh_tasks_view()
        else: messagebox.showerror("Error", f"No se pudo archivar la tarea:\n{response}")

    def btn_delete_task(self, id_tarea_from_btn):
        task_data = next((t for t in self.tareas if t.get('id_tarea') == id_tarea_from_btn), None) # USE 'id_tarea'
        if not task_data: return
        es_de_grupo = task_data.get('is_in_group', False)
        rol_usuario_en_grupo = task_data.get('rol', None)
        can_delete = not es_de_grupo or rol_usuario_en_grupo not in ['miembro']
        if not can_delete:
            messagebox.showinfo("Información", "No tienes permiso para eliminar esta tarea.")
            return
        confirm = messagebox.askyesno(title="Confirmar Eliminación", message="¡ADVERTENCIA!\n\n¿Estás seguro de que deseas eliminar esta tarea?\nEsta acción es definitiva.", icon='warning')
        if not confirm: return
        is_deleted, response = TaskController.event_delete_task(id_tarea_from_btn) # Actual controller call
        if is_deleted: self.refresh_tasks_view()
        else: messagebox.showerror("Error", f"No se pudo eliminar la tarea:\n{response}")

    def refresh_tasks_view(self): self.create_tasks_view()
    def go_to_create_tarea(self): RegisterTareaUserView(self.root)
    def go_to_login(self): MainViewController.log_out(); LoginInView(self.root)
    def go_to_create_group(self): GroupRegisterView(self.root)
    def go_to_profile(self): ProfileView(self.root)

class EditTaskView:
    def __init__(self, root: RootView, main_view: MainView, task_data: dict):
        self.root = root
        self.main_view = main_view
        self.task_data = task_data # Contains 'id_tarea', 'id_grupo', 'is_in_group', 'rol'
        self.current_user_alias = SessionController.get_alias_user() # Uses SessionController

        self.user_role_in_group = self.task_data.get('rol') # Use 'rol' from task_data
        self.can_edit_member_availability = self.task_data.get('is_in_group') and \
                                            self.user_role_in_group in ['master', 'editor']

        self.top = Toplevel(root.root)
        self.top.title("Editar Tarea")
        self.top.config(bg=root.COLOR_BACKGROUND)
        self.top.minsize(500, 450) # Adjusted min size
        self.top.resizable(True, True)
        self.top.transient(root.root)
        self.top.grab_set()
        self.create_edit_form()
        self.root.center_window(self.top)
        # self.top.wait_window() # Removed to allow interaction if messagebox appears

    def create_edit_form(self):
        # Main frame for better structure if scrollbar needed later for many members
        outer_frame = tk.Frame(self.top, bg=self.root.COLOR_FRAME)
        outer_frame.pack(expand=True, fill='both', padx=20, pady=20)

        tk.Label(outer_frame, text='Editar Tarea', font=self.root.FONT_TITLE,
                 bg=outer_frame.cget('bg'), fg=self.root.COLOR_TEXT_DARK).pack(pady=(0, 20))

        form_frame = tk.Frame(outer_frame, bg=outer_frame.cget('bg'))
        form_frame.pack(fill='x')
        form_frame.grid_columnconfigure(1, weight=1)

        labels_texts = ['Nombre:', 'Fecha (dd-mm-aaaa):', 'Prioridad (1-5):', 'Detalle:']
        self.inputs = {}
        self.member_availability_vars = {}

        for i, text in enumerate(labels_texts):
            lbl = tk.Label(form_frame, text=text, font=self.root.FONT_LABEL, bg=form_frame.cget('bg'),
                           fg=self.root.COLOR_TEXT_DARK)
            lbl.grid(row=i, column=0, sticky='nw', pady=5, padx=5) # Use 'nw' for alignment

            key = text.replace(':', '').split(' ')[0].lower()
            if key == 'detalle': # B.2: Detail as Text widget
                inp = Text(form_frame, font=self.root.FONT_BODY, bg=self.root.COLOR_BACKGROUND,
                           fg=self.root.COLOR_TEXT_DARK, relief='solid', borderwidth=1, height=7, wrap=tk.WORD) # Increased height
                inp.grid(row=i, column=1, sticky='ew', pady=5, padx=5)
            else:
                inp = tk.Entry(form_frame, font=self.root.FONT_BODY, bg=self.root.COLOR_BACKGROUND,
                               fg=self.root.COLOR_TEXT_DARK, relief='solid', borderwidth=1)
                inp.grid(row=i, column=1, sticky='ew', pady=5, padx=5, ipady=4)
            self.inputs[key] = inp

        self.inputs['nombre'].insert(0, self.task_data.get('nombre', ''))
        self.inputs['fecha'].insert(0, self.task_data.get('fecha', '')) # Date is string
        self.inputs['prioridad'].insert(0, str(self.task_data.get('prioridad', '')))
        self.inputs['detalle'].insert(tk.END, self.task_data.get('detalle', ''))

        # B.1: Section for editing member availability
        if self.can_edit_member_availability and self.task_data.get('id_grupo'):
            self.members_availability_frame = tk.Frame(outer_frame, bg=outer_frame.cget('bg'), pady=10)
            self.members_availability_frame.pack(fill='x', expand=True, pady=(10,0))
            tk.Label(self.members_availability_frame, text="Disponibilidad para Miembros:",
                     font=self.root.FONT_LABEL, bg=self.members_availability_frame.cget('bg')).pack(anchor='w', pady=(0,5))

            # This is where TaskController.get_task_availability_for_members would be crucial
            group_members = GroupController.get_all_members_with_rol(self.task_data.get('id_grupo'))
            # Ensure your TaskController.get_task_availability_for_members is implemented
            current_task_availability = TaskController.get_task_availability_for_members(self.task_data.get('id_tarea'))

            member_list_display_frame = tk.Frame(self.members_availability_frame, bg=self.members_availability_frame.cget('bg'))
            member_list_display_frame.pack(fill='x')

            cols = 2 # Display members in 2 columns for better space usage
            for idx, (alias, rol) in enumerate(group_members):
                member_check_frame = tk.Frame(member_list_display_frame, bg=self.members_availability_frame.cget('bg'))
                member_check_frame.grid(row=idx // cols, column=idx % cols, sticky='w', padx=5)

                var = tk.BooleanVar(value=current_task_availability.get(alias, False)) # Default to False if not specified
                self.member_availability_vars[alias] = var
                cb = tk.Checkbutton(member_check_frame, text=f"{alias} ({rol})", variable=var,
                                    font=self.root.FONT_BODY, bg=self.members_availability_frame.cget('bg'),
                                    activebackground=self.members_availability_frame.cget('bg'), anchor='w')
                cb.pack(side='left')


        buttons_frame = tk.Frame(outer_frame, bg=outer_frame.cget('bg'))
        buttons_frame.pack(fill='x', pady=(20, 0))

        self.btn_save = tk.Button(buttons_frame, text="Guardar Cambios", command=self.save_changes,
                                  bg=self.root.COLOR_SUCCESS, fg=self.root.COLOR_TEXT_LIGHT,
                                  font=self.root.FONT_BUTTON, relief='flat', cursor="hand2")
        self.btn_save.pack(side='left', expand=True, padx=5, ipady=3)

        self.btn_cancel = tk.Button(buttons_frame, text="Cancelar", command=self.close_window,
                                    bg='#6C757D', fg=self.root.COLOR_TEXT_LIGHT,
                                    font=self.root.FONT_BUTTON, relief='flat', cursor="hand2")
        self.btn_cancel.pack(side='right', expand=True, padx=5, ipady=3)

        self.lbl_response = tk.Label(outer_frame, text="", bg=outer_frame.cget('bg'),
                                     font=("Helvetica", 10, "italic"), wraplength=400) # Wraplength for long messages
        self.lbl_response.pack(pady=(10, 0), fill='x')

    def save_changes(self):
        nombre = self.inputs['nombre'].get()
        fecha = self.inputs['fecha'].get()
        prioridad_str = self.inputs['prioridad'].get() # Get as string
        detalle = self.inputs['detalle'].get("1.0", tk.END).strip() # Get from Text widget

        update_payload = {
            'nombre': nombre, 'fecha': fecha, 'prioridad': prioridad_str, 'detalle': detalle
        }

        if self.can_edit_member_availability:
            members_availability_data = [{'alias': alias, 'disponible': var.get()}
                                         for alias, var in self.member_availability_vars.items()]
            update_payload['members_availability'] = members_availability_data

        # TaskController.event_update_task_session_manager should handle validation (e.g., for priority)
        is_updated, response = TaskController.event_update_task_session_manager(
            id_tarea=self.task_data.get('id_tarea'), # USE 'id_tarea'
            **update_payload
        )

        color = self.root.COLOR_SUCCESS if is_updated else self.root.COLOR_DANGER
        self.lbl_response.config(text=response, fg=color)

        if is_updated:
            self.btn_save.config(state='disabled')
            self.btn_cancel.config(text='Cerrar')
            self.main_view.refresh_tasks_view()

    def close_window(self):
        self.top.destroy()


class GroupRegisterView:
    def __init__(self, root: RootView):
        self.root = root
        self.miembros_alias = []
        self.create_group_form()

    def create_group_form(self):
        self.root.limpiar_componentes()
        main_frame = tk.Frame(self.root.root, bg=self.root.COLOR_FRAME, padx=40, pady=40)
        main_frame.pack(expand=True, fill='both')

        self.root.create_label(main_frame, 'lblGroupTitle', 'Registrar Nuevo Grupo',
                               font_style=self.root.FONT_TITLE, pack_info={'pady': (0, 20)})
        form_frame = tk.Frame(main_frame, bg=main_frame.cget('bg'))
        form_frame.pack(fill='x', pady=10)
        self.root.create_label(form_frame, 'lblGroupName', 'Nombre del Grupo:', font_style=self.root.FONT_LABEL, pack_info={'anchor': 'w'})
        self.root.create_input(form_frame, 'inpGroupName')
        self.root.create_label(form_frame, 'lblGroupDesc', 'Descripción (Opcional):', font_style=self.root.FONT_LABEL, pack_info={'anchor': 'w', 'pady': (10, 0)})
        self.root.create_input(form_frame, 'inpGroupDesc')

        members_section_frame = tk.Frame(main_frame, bg=main_frame.cget('bg'), pady=10)
        members_section_frame.pack(fill='x', expand=True)
        self.root.create_label(members_section_frame, 'lblAddMemberTitle', 'Añadir Miembros (por alias):', font_style=self.root.FONT_LABEL, pack_info={'anchor': 'w'})
        add_member_input_frame = tk.Frame(members_section_frame, bg=members_section_frame.cget('bg'))
        add_member_input_frame.pack(fill='x')
        inp_alias = tk.Entry(add_member_input_frame, font=self.root.FONT_BODY, bg=self.root.COLOR_BACKGROUND, fg=self.root.COLOR_TEXT_DARK, relief='solid', borderwidth=1)
        inp_alias.pack(side='left', fill='x', expand=True, ipady=4, pady=5, padx=(0, 10))
        inp_alias.bind("<Key>", self.clear_member_error_label)
        self.root.componentes['inpMemberAlias'] = inp_alias
        btn_add = tk.Button(add_member_input_frame, text="Añadir Miembro", command=self.btn_add_member, bg=self.root.COLOR_PRIMARY, fg=self.root.COLOR_TEXT_LIGHT, font=self.root.FONT_BUTTON, relief='flat', cursor="hand2")
        btn_add.pack(side='right', ipady=5, ipadx=10)
        self.root.componentes['btnAddMember'] = btn_add

        self.root.create_label(members_section_frame, 'lblMemberError', text="", fg=self.root.COLOR_DANGER, pack_info={'anchor': 'w'})
        self.root.create_label(members_section_frame, 'lblCurrentMembers', 'Miembros a Agregar:', font_style=self.root.FONT_LABEL, pack_info={'anchor': 'w', 'pady': (10, 5)})
        self.members_frame = tk.Frame(members_section_frame, bg=self.root.COLOR_BACKGROUND, relief='solid', borderwidth=1, padx=10, pady=10)
        self.members_frame.pack(fill='both', expand=True)
        self.update_members_display()

        action_buttons_frame = tk.Frame(main_frame, bg=main_frame.cget('bg'))
        action_buttons_frame.pack(fill='x', pady=(20, 0))
        self.root.create_button(action_buttons_frame, name='btnRegisterGroup', text='Guardar Grupo', funcion=self.btn_register_group, bg=self.root.COLOR_SUCCESS, pack_info={'side': 'left', 'expand': True, 'padx': 5, 'ipady':3})
        self.root.create_button(action_buttons_frame, 'btnBackToMain', text='Volver', funcion=self.go_to_main, bg='#6C757D', pack_info={'side': 'right', 'expand': True, 'padx': 5, 'ipady':3})

    def btn_add_member(self):
        alias_input = self.root.componentes.get('inpMemberAlias')
        alias = alias_input.get().strip()
        lbl_error = self.root.componentes.get('lblMemberError')

        if not alias: return
        if alias in self.miembros_alias:
            if lbl_error: lbl_error.config(text=f"El usuario '{alias}' ya está en la lista.", fg=self.root.COLOR_DANGER)
            return

        # D.1: Use the full response message from the controller
        is_valid, response_message = GroupController.is_user_exits(alias) # This controller handles the self-add message

        if is_valid:
            self.miembros_alias.append(alias)
            self.update_members_display()
            alias_input.delete(0, tk.END)
            if lbl_error: lbl_error.config(text="") # Clear error on success
        else:
            if lbl_error: lbl_error.config(text=response_message, fg=self.root.COLOR_DANGER) # Show controller's message

    def update_members_display(self):
        for widget in self.members_frame.winfo_children(): widget.destroy()
        if not self.miembros_alias:
            tk.Label(self.members_frame, text="No hay miembros agregados.", font=self.root.FONT_BODY, bg=self.members_frame.cget('bg'), fg='#6C757D').pack(pady=10)
            return
        for alias in self.miembros_alias:
            member_item_frame = tk.Frame(self.members_frame, bg=self.members_frame.cget('bg'))
            member_item_frame.pack(fill='x', pady=2)
            lbl = tk.Label(member_item_frame, text=f"• {alias}", font=self.root.FONT_BODY, bg=member_item_frame.cget('bg'))
            lbl.pack(side='left', padx=(0, 10))
            btn_remove = tk.Button(member_item_frame, text="Quitar", command=lambda a=alias: self.remove_member(a), bg=self.root.COLOR_DANGER, fg=self.root.COLOR_TEXT_LIGHT, font=("Helvetica", 8, "bold"), relief='flat', cursor="hand2")
            btn_remove.pack(side='right')

    def remove_member(self, alias_to_remove):
        if alias_to_remove in self.miembros_alias:
            self.miembros_alias.remove(alias_to_remove)
            self.update_members_display()

    def clear_member_error_label(self, event=None): # Renamed to be more specific
        if lbl_error := self.root.componentes.get('lblMemberError'):
            if lbl_error.winfo_exists(): lbl_error.config(text="")

    def btn_register_group(self):
        nombre = self.root.componentes.get('inpGroupName').get()
        descripcion = self.root.componentes.get('inpGroupDesc').get()
        # Controller should handle adding the creator as master, view sends other members
        is_registered, response = GroupController.register_group(nombre=nombre, descripcion=descripcion, miembros_alias=self.miembros_alias)
        container = self.root.componentes.get('btnRegisterGroup').master.master
        color = self.root.COLOR_SUCCESS if is_registered else self.root.COLOR_DANGER

        if 'lblGroupResponse' in self.root.componentes:
            if self.root.componentes['lblGroupResponse'].winfo_exists():
                self.root.componentes['lblGroupResponse'].config(text=response, fg=color)
            else:
                del self.root.componentes['lblGroupResponse']
                self.root.create_label(container, 'lblGroupResponse', response, fg=color, pack_info={'pady': (10,0)})
        else:
            self.root.create_label(container, 'lblGroupResponse', response, fg=color, pack_info={'pady': (10,0)})

        if is_registered:
            self.root.componentes.get('btnRegisterGroup').config(state='disabled')
            if self.root.componentes.get('btnAddMember'): self.root.componentes.get('btnAddMember').config(state='disabled')
            self.root.create_button(container, 'btnAcceptGroup', text='Aceptar', funcion=self.go_to_main, bg=self.root.COLOR_PRIMARY)
    def go_to_main(self): MainView(self.root)


class ProfileView:
    def __init__(self, root: RootView):
        self.root = root
        self.create_profile_interface()

    def create_profile_interface(self):
        self.root.limpiar_componentes()
        main_frame = tk.Frame(self.root.root, bg=self.root.COLOR_FRAME, padx=40, pady=40)
        main_frame.pack(expand=True, fill="both")
        self.root.create_label(main_frame, 'lblProfileTitle', 'Actualizar Mi Perfil', font_style=self.root.FONT_TITLE, pack_info={'pady': (0, 20)})
        form_frame = tk.Frame(main_frame, bg=main_frame.cget('bg'))
        form_frame.pack(fill='x')
        labels = ['Nombres:', 'Apellidos:', 'Alias:', 'Nueva Contraseña (opcional):']
        inputs_names = ['inpNombres', 'inpApellidos', 'inpAlias', 'inpPassword']
        current_user_data = UserController.get_data_session_manager() # Uses actual controller

        for i, text in enumerate(labels):
            self.root.create_label(form_frame, f'lbl{inputs_names[i]}', text, font_style=self.root.FONT_LABEL, pack_info={'anchor': 'w', 'pady': (10, 0)})
            inp = tk.Entry(form_frame, font=self.root.FONT_BODY, bg=self.root.COLOR_BACKGROUND, fg=self.root.COLOR_TEXT_DARK, relief='solid', borderwidth=1)
            if 'Nombres' in text: inp.insert(0, current_user_data.get('nombres', ''))
            elif 'Apellidos' in text: inp.insert(0, current_user_data.get('apellidos', ''))
            elif 'Alias' in text:
                inp.insert(0, current_user_data.get('alias', ''))
                inp.config(state='readonly', fg='grey') # Alias typically not editable
            elif 'Contraseña' in text: inp.config(show='•')
            inp.pack(pady=5, ipady=4, fill='x')
            self.root.componentes[inputs_names[i]] = inp # Store after config

        action_buttons_frame = tk.Frame(main_frame, bg=main_frame.cget('bg'))
        action_buttons_frame.pack(fill='x', pady=(20,0))
        self.root.create_button(action_buttons_frame, 'btnUpdateUser', text='Guardar Cambios', funcion=self.btn_update_user, bg=self.root.COLOR_SUCCESS, pack_info={'side':'left', 'expand':True, 'padx':5, 'ipady':3})
        self.root.create_button(action_buttons_frame, 'btnBackToMainFromProfile', text='Volver', funcion=self.go_to_main, bg='#6C757D', pack_info={'side':'right', 'expand':True, 'padx':5, 'ipady':3})

    def btn_update_user(self):
        nombres = self.root.componentes.get('inpNombres').get()
        apellidos = self.root.componentes.get('inpApellidos').get()
        alias = self.root.componentes.get('inpAlias').get() # Get even if readonly for controller
        password = self.root.componentes.get('inpPassword').get()
        is_updated, response = UserController.event_update_user(nombres=nombres, apellidos=apellidos, alias=alias, password=password if password else None)
        container = self.root.componentes.get('btnUpdateUser').master.master # main_frame
        color = self.root.COLOR_SUCCESS if is_updated else self.root.COLOR_DANGER

        if 'lblUpdateResponse' in self.root.componentes:
            if self.root.componentes['lblUpdateResponse'].winfo_exists():
                self.root.componentes['lblUpdateResponse'].config(text=response, fg=color)
            else: # Recreate if destroyed
                del self.root.componentes['lblUpdateResponse']
                self.root.create_label(container, 'lblUpdateResponse', response, fg=color, pack_info={'pady': (10,0)})
        else:
            self.root.create_label(container, 'lblUpdateResponse', response, fg=color, pack_info={'pady': (10,0)})
        if is_updated and 'btnUpdateUser' in self.root.componentes : self.root.componentes.get('btnUpdateUser').config(state='disabled')

    def go_to_main(self): MainView(self.root)


class RegisterTareaUserView:
    def __init__(self, root: 'RootView'):
        self.root = root
        self.selected_group_id = None
        self.current_user_alias = SessionController.get_alias_user() # Use SessionController
        self.master_alias_of_selected_group = None
        self.all_group_members_data = {}  # Stores {alias: rol}
        self.members_to_assign = {} # {alias: {'var': BooleanVar, 'rol': str, 'is_fixed': bool}}
        self.member_display_frames = {}
        self.create_fomulate_tarea()

    def create_fomulate_tarea(self):
        self.root.limpiar_componentes()
        outer_frame = tk.Frame(self.root.root, bg=self.root.COLOR_FRAME, padx=30, pady=30)
        outer_frame.pack(expand=True, fill='both')

        self.root.create_label(outer_frame, name='lblCreateTaskTitle', text='Registrar Nueva Tarea', font_style=self.root.FONT_TITLE, pack_info={'pady': (0, 15)})

        # Main form content in a scrollable area
        canvas = tk.Canvas(outer_frame, bg=outer_frame.cget('bg'), highlightthickness=0)
        scrollbar = ttk.Scrollbar(outer_frame, orient="vertical", command=canvas.yview)
        scrollable_form_frame = tk.Frame(canvas, bg=outer_frame.cget('bg'))

        scrollable_form_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_form_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # --- Content of the form goes into scrollable_form_frame ---
        form_content_frame = tk.Frame(scrollable_form_frame, bg=outer_frame.cget('bg'))
        form_content_frame.pack(expand=True, fill='x')
        form_content_frame.grid_columnconfigure(1, weight=1) # Allow inputs to expand

        labels_texts = ['Nombre de la Tarea:', 'Fecha (dd-mm-aaaa):', 'Prioridad (1-5):', 'Detalle:']
        inputs_names = ['inpNombreCreateTareaUser', 'inpFechaProgramadaCreateTareaUser', 'inpPrioridadCreateTarea', 'inpDetalleCreateTarea']
        for i, text in enumerate(labels_texts):
            lbl = tk.Label(form_content_frame, text=text, font=self.root.FONT_LABEL, bg=form_content_frame.cget('bg'), fg=self.root.COLOR_TEXT_DARK)
            lbl.grid(row=i, column=0, sticky='nw', pady=5, padx=5)
            if text == 'Detalle:': # C.3: Text widget for detail
                inp = Text(form_content_frame, font=self.root.FONT_BODY, bg=self.root.COLOR_BACKGROUND, fg=self.root.COLOR_TEXT_DARK, relief='solid', borderwidth=1, height=6, wrap=tk.WORD) # Adjusted height
                inp.grid(row=i, column=1, sticky='ew', pady=5, padx=5)
            else:
                inp = tk.Entry(form_content_frame, font=self.root.FONT_BODY, bg=self.root.COLOR_BACKGROUND, fg=self.root.COLOR_TEXT_DARK, relief='solid', borderwidth=1)
                inp.grid(row=i, column=1, sticky='ew', pady=5, padx=5, ipady=4)
            self.root.componentes[inputs_names[i]] = inp

        # Group Selection
        row_idx = len(labels_texts)
        tk.Label(form_content_frame, text='Pertenencia a Grupo:', font=self.root.FONT_LABEL, bg=form_content_frame.cget('bg'), fg=self.root.COLOR_TEXT_DARK).grid(row=row_idx, column=0, sticky='w', pady=5, padx=5)
        groups = GroupController.get_groups_editable() # Uses actual controller
        self.group_options = {"Seleccionar Grupo": None}; self.group_options.update({name: id_ for id_, name in groups})
        self.group_combobox_var = tk.StringVar(value="Seleccionar Grupo")
        group_combobox = ttk.Combobox(form_content_frame, textvariable=self.group_combobox_var, values=list(self.group_options.keys()), state='readonly', font=self.root.FONT_BODY, width=30)
        group_combobox.grid(row=row_idx, column=1, sticky='ew', pady=5, padx=5, ipady=2); row_idx += 1
        group_combobox.bind("<<ComboboxSelected>>", self.on_group_selected); self.root.componentes['cmbGroupSelection'] = group_combobox

        # Assignment Type (Todos / Personalizado)
        self.assignment_frame = tk.Frame(form_content_frame, bg=form_content_frame.cget('bg'))
        self.assignment_frame.grid(row=row_idx, column=0, columnspan=2, sticky='ew', pady=(10,0)); row_idx += 1
        self.assignment_frame.grid_remove()
        self.assignment_type_var = tk.StringVar(value="todos")
        tk.Radiobutton(self.assignment_frame, text="Asignar a Todos los Miembros", variable=self.assignment_type_var, value="todos", font=self.root.FONT_BODY, bg=self.assignment_frame.cget('bg'), command=self.on_assignment_type_changed, activebackground=self.assignment_frame.cget('bg')).pack(side='left', padx=5)
        tk.Radiobutton(self.assignment_frame, text="Asignación Personalizada", variable=self.assignment_type_var, value="personalizado", font=self.root.FONT_BODY, bg=self.assignment_frame.cget('bg'), command=self.on_assignment_type_changed, activebackground=self.assignment_frame.cget('bg')).pack(side='left', padx=5)

        # Member Selection (Personalizado)
        self.members_selection_frame = tk.Frame(form_content_frame, bg=form_content_frame.cget('bg'))
        self.members_selection_frame.grid(row=row_idx, column=0, columnspan=2, sticky='ew', pady=5); row_idx += 1
        self.members_selection_frame.grid_remove()
        self.members_selection_frame.grid_columnconfigure(1, weight=1) # Allow combobox to expand

        tk.Label(self.members_selection_frame, text='Añadir Miembro Específico:', font=self.root.FONT_LABEL, bg=self.members_selection_frame.cget('bg'), fg=self.root.COLOR_TEXT_DARK).grid(row=0, column=0, sticky='w', pady=(5,0), padx=5)
        self.member_combobox_var = tk.StringVar()
        self.member_combobox = ttk.Combobox(self.members_selection_frame, textvariable=self.member_combobox_var, state='readonly', font=self.root.FONT_BODY, width=28)
        self.member_combobox.grid(row=0, column=1, sticky='ew', pady=5, padx=5, ipady=2)
        self.member_combobox.bind("<<ComboboxSelected>>", self.add_selected_member_from_combobox)
        self.root.componentes['cmbMemberSelection'] = self.member_combobox

        self.selected_members_display_frame = tk.Frame(self.members_selection_frame, bg=self.root.COLOR_BACKGROUND, relief="sunken", borderwidth=1, padx=5, pady=5)
        self.selected_members_display_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', pady=(5,10), ipady=5)
        # self.members_selection_frame.grid_rowconfigure(1, weight=1) # Allow this to expand a bit


        # Action Buttons (outside scrollable area, directly in outer_frame)
        action_buttons_frame = tk.Frame(outer_frame, bg=outer_frame.cget('bg'))
        action_buttons_frame.pack(pady=(15,0), fill='x')
        self.root.create_button(action_buttons_frame, name='btnRegistrarTareaCreateTarea', text='Guardar Tarea', funcion=self.btn_registrar_tarea, bg=self.root.COLOR_SUCCESS, pack_info={'side': 'left', 'expand': True, 'padx': 5, 'ipady':3})
        self.root.create_button(action_buttons_frame, name='btnVolverCreateTareaUser', text='Volver', funcion=self.btn_volver, bg='#6C757D', pack_info={'side': 'right', 'expand': True, 'padx': 5, 'ipady':3})
        self.lbl_task_response = self.root.create_label(outer_frame, 'lblTaskResponseCreate', '', pack_info={'pady': (10,0), 'fill':'x'})
        self.lbl_task_response.config(wraplength=400)


    def on_group_selected(self, event=None):
        selected_name = self.group_combobox_var.get()
        self.selected_group_id = self.group_options.get(selected_name)
        self.master_alias_of_selected_group = None
        self.all_group_members_data.clear()
        self.clear_members_display_and_assignment()

        if self.selected_group_id:
            self.assignment_frame.grid()
            self.master_alias_of_selected_group = GroupController.get_group_master_alias(self.selected_group_id) # Uses actual controller
            self.load_group_members_data()
            self.on_assignment_type_changed() # This will set defaults for "Personalizado"
        else:
            self.assignment_frame.grid_remove()
            self.members_selection_frame.grid_remove()

    def on_assignment_type_changed(self, event=None):
        self.clear_members_display_and_assignment()  # Important to clear before adding defaults

        if self.assignment_type_var.get() == "personalizado" and self.selected_group_id:
            self.members_selection_frame.grid()

            # 1. Add Master by default (if they exist and are part of the group members list)
            if self.master_alias_of_selected_group and self.master_alias_of_selected_group in self.all_group_members_data:
                self.add_member_to_assign_list(self.master_alias_of_selected_group, True, is_fixed=True)

            # 2. Add Current User (Task Creator) if they are part of the group and not already added as master
            # The fact that they could select this group implies they are master or editor.
            # So, we just need to check if they are in the group's member list and not the master (if master was already added).
            if self.current_user_alias in self.all_group_members_data and \
                    self.current_user_alias != self.master_alias_of_selected_group:
                self.add_member_to_assign_list(self.current_user_alias, True, is_fixed=True)

            self.update_member_combobox()
        else:
            self.members_selection_frame.grid_remove()

    def load_group_members_data(self):
        self.all_group_members_data.clear()
        if self.selected_group_id:
            members_with_roles = GroupController.get_all_members_with_rol(self.selected_group_id) # Uses actual controller
            for alias, rol in members_with_roles: self.all_group_members_data[alias] = rol

    def update_member_combobox(self):
        # C.1 & C.2: Show "alias (rol)", exclude already fixed/added members
        available_for_combobox = [f"{alias} ({rol})" for alias, rol in self.all_group_members_data.items()
                                  if alias not in self.members_to_assign]
        self.member_combobox['values'] = available_for_combobox
        if available_for_combobox: self.member_combobox.set('Seleccionar para Añadir')
        else: self.member_combobox.set('No más miembros'); self.member_combobox_var.set('')

    def clear_members_display_and_assignment(self):
        for frame in self.member_display_frames.values():
            if frame.winfo_exists(): frame.destroy()
        self.member_display_frames.clear()
        self.members_to_assign.clear()

    def add_selected_member_from_combobox(self, event=None):
        selected_display_string = self.member_combobox_var.get()
        if not selected_display_string or selected_display_string in ['Seleccionar para Añadir', 'No más miembros']: return
        alias = selected_display_string.split(" (")[0] # Parse alias
        if alias and alias not in self.members_to_assign:
            self.add_member_to_assign_list(alias, True, is_fixed=False)
            self.update_member_combobox()

    def add_member_to_assign_list(self, alias, disponible: bool, is_fixed: bool):
        if alias not in self.members_to_assign:
            var = tk.BooleanVar(value=disponible)
            rol = self.all_group_members_data.get(alias, 'miembro')
            self.members_to_assign[alias] = {'var': var, 'rol': rol, 'is_fixed': is_fixed}
            self.display_assigned_member(alias, var, rol, is_fixed)

    def display_assigned_member(self, alias, var, rol, is_fixed):
        member_frame_name = f"member_assign_frame_{alias}"
        # self.root.comprobate_existe(member_frame_name) # Not needed if clearing display_frame children

        member_frame = tk.Frame(self.selected_members_display_frame, bg=self.root.COLOR_FRAME, padx=5, pady=2)
        member_frame.pack(fill='x', pady=1) # Keep compact
        self.member_display_frames[alias] = member_frame # For potential direct destruction

        lbl_alias_rol = tk.Label(member_frame, text=f"{alias} ({rol})", font=self.root.FONT_BODY, bg=member_frame.cget('bg'), fg=self.root.COLOR_TEXT_DARK, anchor='w')
        lbl_alias_rol.pack(side='left', padx=(0,10), fill='x', expand=True)

        disponible_cb = tk.Checkbutton(member_frame, text="Disp.", variable=var, font=("Helvetica", 10), bg=member_frame.cget('bg'), activebackground=member_frame.cget('bg'))
        disponible_cb.pack(side='left', padx=5)

        if is_fixed: var.set(True); disponible_cb.config(state='disabled')
        else:
            btn_remove = tk.Button(member_frame, text="X", font=("Helvetica", 8, "bold"), width=2, bg=self.root.COLOR_DANGER, fg='white', relief='flat', command=lambda a=alias: self.remove_member_from_assign_list(a))
            btn_remove.pack(side='right')

    def remove_member_from_assign_list(self, alias):
        if alias in self.members_to_assign and not self.members_to_assign[alias]['is_fixed']:
            del self.members_to_assign[alias]
            if alias in self.member_display_frames:
                if self.member_display_frames[alias].winfo_exists(): self.member_display_frames[alias].destroy()
                del self.member_display_frames[alias]
            self.update_member_combobox()

    def btn_registrar_tarea(self):
        nombre = self.root.componentes.get('inpNombreCreateTareaUser').get()
        fecha = self.root.componentes.get('inpFechaProgramadaCreateTareaUser').get()
        prioridad_str = self.root.componentes.get('inpPrioridadCreateTarea').get()
        detalle = self.root.componentes.get('inpDetalleCreateTarea').get("1.0", tk.END).strip() # From Text widget
        self.lbl_task_response.config(text="") # Clear previous

        if not all([nombre, fecha, prioridad_str]): # Detalle can be optional based on your rules
            self.lbl_task_response.config(text='Nombre, Fecha y Prioridad son obligatorios.', fg=self.root.COLOR_DANGER); return
        try:
            prioridad = int(prioridad_str)
            if not (1 <= prioridad <= 5): raise ValueError("Rango")
        except ValueError:
            self.lbl_task_response.config(text='Prioridad debe ser un número entre 1 y 5.', fg=self.root.COLOR_DANGER); return

        miembros_a_asignar_final = 'all'
        if self.selected_group_id:
            if self.assignment_type_var.get() == "personalizado":
                if not self.members_to_assign:
                    self.lbl_task_response.config(text='Debe haber al menos un miembro asignado para tarea personalizada.', fg=self.root.COLOR_DANGER); return
                miembros_a_asignar_final = [[alias, data['var'].get()] for alias, data in self.members_to_assign.items()]
            is_registered_task, response_msg = TaskController.event_register_task_group(id_grupo=self.selected_group_id, nombre=nombre, fecha=fecha, prioridad=prioridad, detalle=detalle, miembros_disponible=miembros_a_asignar_final)
        else:
            is_registered_task, response_msg = TaskController.event_register_task_user(nombre=nombre, fecha=fecha, prioridad=prioridad, detalle=detalle)

        self.lbl_task_response.config(text=response_msg, fg=self.root.COLOR_SUCCESS if is_registered_task else self.root.COLOR_DANGER)
        if is_registered_task:
            self.root.componentes.get('btnRegistrarTareaCreateTarea').config(state='disabled')
            # Assuming button exists in components dict (created by create_button)
            if 'btnAceptarRegistroCreateTarea' in self.root.componentes:
                 if self.root.componentes['btnAceptarRegistroCreateTarea'].winfo_exists(): self.root.componentes['btnAceptarRegistroCreateTarea'].config(state='normal')
            else:
                self.root.create_button(self.lbl_task_response.master, 'btnAceptarRegistroCreateTarea', text='Aceptar', funcion=self.btn_aceptar_crear_tarea, pack_info={'pady':(5,0)})

    def btn_volver(self): MainView(self.root)
    def btn_aceptar_crear_tarea(self): MainView(self.root)

if __name__ == '__main__':
    LoginInView.independent_login()