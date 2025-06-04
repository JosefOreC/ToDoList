import tkinter as tk
from tkinter import Toplevel
from tkinter import messagebox  # ### NUEVO ###: Importar para diálogos de confirmación

# Importaciones de tus controladores (asegúrate de que las rutas sean correctas)
from src.controlador.login_controller import LoginController
from src.controlador.register_controller import RegisterUserController
from src.controlador.main_view_controller import MainViewController
from src.controlador.task_controller import TaskController
from src.controlador.group_controller import GroupController
from src.controlador.user_controller import UserController


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
        self.root.geometry("950x600")  # Aumentamos un poco el ancho para los nuevos botones
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

    def __comprobate_existe(self, name):
        if componente := self.componentes.get(name):
            componente.destroy()

    def create_button(self, container, name: str, funcion, text: str = '',
                      bg=COLOR_PRIMARY, fg=COLOR_TEXT_LIGHT, pack_info=None):
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
        if font_style is None:
            font_style = self.FONT_BODY
        if pack_info is None:
            pack_info = {'pady': 2}
        self.__comprobate_existe(name)

        lbl = tk.Label(container, text=text, fg=fg, bg=container.cget('bg'), font=font_style)
        lbl.pack(**pack_info)
        self.componentes[name] = lbl

    def btn_cambiar_secret_input(self, name_input: str, name_button: str):
        simbolo = '' if self.componentes[name_input].cget('show') else '•'
        self.componentes[name_input].config(show=simbolo)
        texto_boton = 'Ocultar' if simbolo == '' else 'Mostrar'
        self.componentes[name_button].config(text=texto_boton)

    def limpiar_componentes(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.componentes.clear()

    def main(self):
        self.root.mainloop()

    def cerrar_ventana(self):
        self.root.destroy()


class LoginInView:
    # ... (Sin cambios en esta clase)
    def __init__(self, root: RootView):
        self.root = root
        self.create_login()

    @staticmethod
    def independent_login():
        root = RootView()
        login_view = LoginInView(root)
        root.main()
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
        alias = self.root.componentes.get('alias').get()
        password = self.root.componentes.get('password').get()
        is_login, response = LoginController.login(alias, password)

        if is_login:
            MainView(self.root)
            return

        container = self.root.componentes.get('btnLogin').master
        self.root.create_label(container, name='login_error', text=response,
                               fg=self.root.COLOR_DANGER, font_style=(self.root.FONT_BODY[0], 10, "italic"))


class RegisterUserView:
    # ... (Sin cambios en esta clase)
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
        self.root.limpiar_componentes()
        header_frame = tk.Frame(self.root.root, bg=self.root.COLOR_FRAME, padx=20, pady=10)
        header_frame.pack(fill='x')

        # ### NUEVO ###: Botón para refrescar la lista de tareas
        self.root.create_button(header_frame, name='btnRefreshTasks', text='Refrescar 🔄',
                                funcion=self.refresh_tasks_view, bg='#17A2B8',  # Un color cian para distinguirlo
                                pack_info={'side': 'left', 'padx': 10})

        self.root.create_button(header_frame, name='btnCrearTarea', text='✚ Nueva Tarea',
                                funcion=self.go_to_create_tarea, bg=self.root.COLOR_PRIMARY,
                                pack_info={'side': 'left', 'padx': 10})
        self.root.create_button(header_frame, name='btnCrearGrupo', text='✚ Nuevo Grupo',
                                funcion=self.go_to_create_group, bg=self.root.COLOR_SUCCESS,
                                pack_info={'side': 'left', 'padx': 10})
        self.root.create_button(header_frame, name='btnMiPerfil', text='Mi Perfil',
                                funcion=self.go_to_profile, bg='#6C757D',
                                pack_info={'side': 'right', 'padx': 10})
        self.root.create_button(header_frame, name='btnLogOut', text='Cerrar Sesión',
                                funcion=self.go_to_login, bg=self.root.COLOR_DANGER,
                                pack_info={'side': 'right', 'padx': 10})

        self.tasks_container = tk.Frame(self.root.root, bg=self.root.COLOR_BACKGROUND, padx=20, pady=20)
        self.tasks_container.pack(fill='both', expand=True)
        self.root.create_label(self.tasks_container, name='lblTasksTitle', text='Tareas para Hoy',
                               font_style=self.root.FONT_TITLE, pack_info={'pady': (0, 20)})
        self.create_tasks_view()

    def create_tasks_view(self):
        for widget in self.tasks_container.winfo_children():
            if widget.winfo_name() != 'lblTasksTitle':
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

        task_header = tk.Frame(self.tasks_container, name='task_header', bg=self.tasks_container.cget('bg'))
        task_header.pack(fill='x', pady=(0, 10))
        headers = ['Nombre', 'Grupo', 'Fecha', 'Prioridad', 'Acciones']

        col_weights = [3, 2, 2, 1, 4]
        for i, h in enumerate(headers):
            task_header.grid_columnconfigure(i, weight=col_weights[i])
            tk.Label(task_header, text=h, font=self.root.FONT_LABEL, bg=task_header.cget('bg')).grid(row=0, column=i,
                                                                                                     sticky='ew')
        for i, tarea in enumerate(self.tareas):
            self.insert_task_view(tarea, i)

    def insert_task_view(self, tarea: dict, index: int):
        task_id = tarea.get('id')
        task_frame = tk.Frame(self.tasks_container, name=f'frameTask{task_id}',
                              bg=self.root.COLOR_FRAME, relief='solid', borderwidth=1, padx=10, pady=10)
        task_frame.pack(fill='x', pady=5)

        col_weights = [3, 2, 2, 1, 4]
        for i in range(len(col_weights)):
            task_frame.grid_columnconfigure(i, weight=col_weights[i])

        tk.Label(task_frame, text=tarea.get('nombre'), font=self.root.FONT_BODY, bg=task_frame.cget('bg')).grid(row=0,
                                                                                                                column=0,
                                                                                                                sticky='w')
        tk.Label(task_frame, text=tarea.get('grupo', 'N/A'), font=self.root.FONT_BODY, bg=task_frame.cget('bg')).grid(
            row=0, column=1, sticky='w')

        fecha_obj = tarea.get('fecha')
        fecha_str = fecha_obj.strftime("%d-%m-%Y") if hasattr(fecha_obj, 'strftime') else fecha_obj
        tk.Label(task_frame, text=fecha_str, font=self.root.FONT_BODY, bg=task_frame.cget('bg')).grid(row=0,
                                                                                                      column=2,
                                                                                                      sticky='w')
        tk.Label(task_frame, text=f"Prioridad: {tarea.get('prioridad')}", font=self.root.FONT_BODY,
                 bg=task_frame.cget('bg')).grid(row=0, column=3, sticky='w')

        actions_frame = tk.Frame(task_frame, bg=task_frame.cget('bg'))
        actions_frame.grid(row=0, column=4, sticky='e')

        realizado = tarea.get('realizado')
        check_bg = self.root.COLOR_SUCCESS if realizado else self.root.COLOR_DANGER
        check_text = '✔' if realizado else '✖'
        btn_check = tk.Button(actions_frame, name=f'btnCheckTask{task_id}', text=check_text,
                              bg=check_bg, fg=self.root.COLOR_TEXT_LIGHT, font=self.root.FONT_BUTTON,
                              relief='flat', cursor="hand2",
                              command=lambda id=task_id, idx=index: self.btn_check_task(id, idx))
        btn_check.pack(side='left', padx=2)

        btn_edit = tk.Button(actions_frame, name=f'btnEditTask{task_id}', text='Editar',
                             bg='#6C757D', fg=self.root.COLOR_TEXT_LIGHT, font=self.root.FONT_BUTTON,
                             relief='flat', cursor="hand2",
                             command=lambda id=task_id, idx=index: self.btn_edit_task(id, idx))
        btn_edit.pack(side='left', padx=2)

        btn_archive = tk.Button(actions_frame, name=f'btnArchiveTask{task_id}', text='Archivar',
                                bg='#5D6D7E', fg=self.root.COLOR_TEXT_LIGHT, font=self.root.FONT_BUTTON,
                                relief='flat', cursor="hand2",
                                command=lambda id=task_id: self.btn_archive_task(id))
        btn_archive.pack(side='left', padx=2)

        btn_delete = tk.Button(actions_frame, name=f'btnDeleteTask{task_id}', text='Eliminar',
                               bg=self.root.COLOR_DANGER, fg=self.root.COLOR_TEXT_LIGHT, font=self.root.FONT_BUTTON,
                               relief='flat', cursor="hand2",
                               command=lambda id=task_id: self.btn_delete_task(id))
        btn_delete.pack(side='left', padx=2)

    def btn_check_task(self, id_tarea, indice):
        estado_actual = self.tareas[indice]['realizado']
        nuevo_estado = not estado_actual
        is_change_task, response = TaskController.event_update_task_session_manager(id_tarea, realizado=nuevo_estado)
        if is_change_task:
            self.refresh_tasks_view()
        else:
            print(f"Error al actualizar la tarea: {response}")

    def btn_edit_task(self, id_task, indice):
        task_data = self.tareas[indice]
        if task_data.get('id') == id_task:
            EditTaskView(self.root, self, task_data)
        else:
            print("Error de consistencia de datos: El ID de la tarea no coincide.")

    def btn_archive_task(self, id_tarea):
        confirm = messagebox.askyesno(
            title="Confirmar Archivar",
            message=f"¿Estás seguro de que deseas archivar esta tarea?"
        )
        if not confirm:
            return

        is_archived, response = TaskController.event_archive_task(id_tarea)
        if is_archived:
            self.refresh_tasks_view()
        else:
            messagebox.showerror("Error", f"No se pudo archivar la tarea:\n{response}")

    def btn_delete_task(self, id_tarea):
        confirm = messagebox.askyesno(
            title="Confirmar Eliminación",
            message=f"¡ADVERTENCIA!\n\n¿Estás seguro de que deseas eliminar esta tarea?\nEsta acción es definitiva.",
            icon='warning'
        )
        if not confirm:
            return

        is_deleted, response = TaskController.event_delete_task(id_tarea)
        if is_deleted:
            self.refresh_tasks_view()
        else:
            messagebox.showerror("Error", f"No se pudo eliminar la tarea:\n{response}")

    def refresh_tasks_view(self):
        """Refresca la lista de tareas, volviendo a consultar la base de datos."""
        self.create_tasks_view()

    def go_to_create_tarea(self):
        RegisterTareaUserView(self.root)

    def go_to_login(self):
        MainViewController.log_out()
        LoginInView(self.root)

    def go_to_create_group(self):
        GroupRegisterView(self.root)

    def go_to_profile(self):
        ProfileView(self.root)


# ... (Resto de las clases: EditTaskView, GroupRegisterView, etc. sin cambios)
class EditTaskView:
    def __init__(self, root: RootView, main_view: MainView, task_data: dict):
        self.root = root
        self.main_view = main_view
        self.task_data = task_data
        self.top = Toplevel(root.root)
        self.top.title("Editar Tarea")
        self.top.config(bg=root.COLOR_BACKGROUND)
        self.top.resizable(False, False)
        self.top.transient(root.root)
        self.top.grab_set()
        self.create_edit_form()
        self.root.center_window(self.top)
        self.top.wait_window()

    def create_edit_form(self):
        main_frame = tk.Frame(self.top, bg=self.root.COLOR_FRAME, padx=30, pady=30)
        main_frame.pack(expand=True)

        tk.Label(main_frame, text='Editar Tarea', font=self.root.FONT_TITLE,
                 bg=main_frame.cget('bg'), fg=self.root.COLOR_TEXT_DARK).pack(pady=(0, 20))

        form_frame = tk.Frame(main_frame, bg=main_frame.cget('bg'))
        form_frame.pack()

        labels_texts = ['Nombre:', 'Fecha (dd-mm-aaaa):', 'Prioridad (1-5):', 'Detalle:']
        self.inputs = {}

        for i, text in enumerate(labels_texts):
            lbl = tk.Label(form_frame, text=text, font=self.root.FONT_LABEL, bg=form_frame.cget('bg'),
                           fg=self.root.COLOR_TEXT_DARK)
            lbl.grid(row=i, column=0, sticky='w', pady=5, padx=5)

            inp = tk.Entry(form_frame, font=self.root.FONT_BODY, bg=self.root.COLOR_BACKGROUND,
                           fg=self.root.COLOR_TEXT_DARK, relief='solid', borderwidth=1)
            inp.grid(row=i, column=1, sticky='ew', pady=5, padx=5, ipady=4)

            key = text.replace(':', '').split(' ')[0].lower()
            self.inputs[key] = inp

        self.inputs['nombre'].insert(0, self.task_data.get('nombre', ''))
        fecha_obj = self.task_data.get('fecha')
        fecha_str = fecha_obj.strftime("%d-%m-%Y") if hasattr(fecha_obj, 'strftime') else fecha_obj
        self.inputs['fecha'].insert(0, fecha_str)
        self.inputs['prioridad'].insert(0, str(self.task_data.get('prioridad', '')))
        self.inputs['detalle'].insert(0, self.task_data.get('detalle', ''))

        buttons_frame = tk.Frame(main_frame, bg=main_frame.cget('bg'))
        buttons_frame.pack(fill='x', pady=(15, 0))

        self.btn_save = tk.Button(buttons_frame, text="Guardar Cambios", command=self.save_changes,
                                  bg=self.root.COLOR_SUCCESS, fg=self.root.COLOR_TEXT_LIGHT,
                                  font=self.root.FONT_BUTTON, relief='flat', cursor="hand2")
        self.btn_save.pack(side='left', expand=True, padx=5)

        self.btn_cancel = tk.Button(buttons_frame, text="Cancelar", command=self.close_window,
                                    bg='#6C757D', fg=self.root.COLOR_TEXT_LIGHT,
                                    font=self.root.FONT_BUTTON, relief='flat', cursor="hand2")
        self.btn_cancel.pack(side='right', expand=True, padx=5)

        self.lbl_response = tk.Label(main_frame, text="", bg=main_frame.cget('bg'), font=("Helvetica", 10, "italic"))
        self.lbl_response.pack(pady=(10, 0))

    def save_changes(self):
        nombre = self.inputs['nombre'].get()
        fecha = self.inputs['fecha'].get()
        prioridad = self.inputs['prioridad'].get()
        detalle = self.inputs['detalle'].get()

        is_updated, response = TaskController.event_update_task_session_manager(
            id_tarea=self.task_data.get('id'),
            nombre=nombre,
            fecha=fecha,
            prioridad=prioridad,
            detalle=detalle
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
    # ... (Sin cambios)
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
        self.root.create_label(form_frame, 'lblGroupName', 'Nombre del Grupo:', font_style=self.root.FONT_LABEL,
                               pack_info={'anchor': 'w'})
        self.root.create_input(form_frame, 'inpGroupName')
        self.root.create_label(form_frame, 'lblGroupDesc', 'Descripción (Opcional):', font_style=self.root.FONT_LABEL,
                               pack_info={'anchor': 'w', 'pady': (10, 0)})
        self.root.create_input(form_frame, 'inpGroupDesc')
        members_section_frame = tk.Frame(main_frame, bg=main_frame.cget('bg'), pady=10)
        members_section_frame.pack(fill='x', expand=True)
        self.root.create_label(members_section_frame, 'lblAddMemberTitle', 'Añadir Miembros (por alias):',
                               font_style=self.root.FONT_LABEL, pack_info={'anchor': 'w'})
        add_member_input_frame = tk.Frame(members_section_frame, bg=members_section_frame.cget('bg'))
        add_member_input_frame.pack(fill='x')
        inp_alias = tk.Entry(add_member_input_frame, font=self.root.FONT_BODY, bg=self.root.COLOR_BACKGROUND,
                             fg=self.root.COLOR_TEXT_DARK, relief='solid', borderwidth=1)
        inp_alias.pack(side='left', fill='x', expand=True, ipady=4, pady=5, padx=(0, 10))
        inp_alias.bind("<Key>", self.clear_member_error)
        self.root.componentes['inpMemberAlias'] = inp_alias
        btn_add = tk.Button(add_member_input_frame, text="Añadir Miembro", command=self.btn_add_member,
                            bg=self.root.COLOR_PRIMARY, fg=self.root.COLOR_TEXT_LIGHT, font=self.root.FONT_BUTTON,
                            relief='flat', cursor="hand2")
        btn_add.pack(side='right', ipady=5, ipadx=10)
        self.root.componentes['btnAddMember'] = btn_add
        self.root.create_label(members_section_frame, 'lblMemberError', text="", fg=self.root.COLOR_DANGER,
                               pack_info={'anchor': 'w'})
        self.root.create_label(members_section_frame, 'lblCurrentMembers', 'Miembros a Agregar:',
                               font_style=self.root.FONT_LABEL, pack_info={'anchor': 'w', 'pady': (10, 5)})
        self.members_frame = tk.Frame(members_section_frame, bg=self.root.COLOR_BACKGROUND,
                                      relief='solid', borderwidth=1, padx=10, pady=10)
        self.members_frame.pack(fill='both', expand=True)
        self.update_members_display()
        action_buttons_frame = tk.Frame(main_frame, bg=main_frame.cget('bg'))
        action_buttons_frame.pack(fill='x', pady=(20, 0))
        self.root.create_button(action_buttons_frame, name='btnRegisterGroup', text='Guardar Grupo',
                                funcion=self.btn_register_group, bg=self.root.COLOR_SUCCESS,
                                pack_info={'side': 'left', 'expand': True, 'padx': 5})
        self.root.create_button(action_buttons_frame, 'btnBackToMain', text='Volver',
                                funcion=self.go_to_main, bg='#6C757D',
                                pack_info={'side': 'right', 'expand': True, 'padx': 5})

    def btn_add_member(self):
        alias_input = self.root.componentes.get('inpMemberAlias')
        alias = alias_input.get().strip()
        if not alias:
            return
        if alias in self.miembros_alias:
            self.root.componentes['lblMemberError'].config(text=f"El usuario '{alias}' ya está en la lista.")
            return
        is_valid, _ = GroupController.is_user_exits(alias)
        if is_valid:
            self.miembros_alias.append(alias)
            self.update_members_display()
            alias_input.delete(0, tk.END)
            self.clear_member_error()
        else:
            self.root.componentes['lblMemberError'].config(text=f"Error: El usuario con alias '{alias}' no existe.")

    def update_members_display(self):
        for widget in self.members_frame.winfo_children():
            widget.destroy()
        if not self.miembros_alias:
            tk.Label(self.members_frame, text="No hay miembros agregados.",
                     font=self.root.FONT_BODY, bg=self.members_frame.cget('bg'),
                     fg='#6C757D').pack(pady=10)
            return
        for alias in self.miembros_alias:
            member_item_frame = tk.Frame(self.members_frame, bg=self.members_frame.cget('bg'))
            member_item_frame.pack(fill='x', pady=2)
            lbl = tk.Label(member_item_frame, text=f"• {alias}", font=self.root.FONT_BODY,
                           bg=member_item_frame.cget('bg'))
            lbl.pack(side='left', padx=(0, 10))
            btn_remove = tk.Button(member_item_frame, text="Quitar",
                                   command=lambda a=alias: self.remove_member(a),
                                   bg=self.root.COLOR_DANGER, fg=self.root.COLOR_TEXT_LIGHT,
                                   font=("Helvetica", 8, "bold"), relief='flat', cursor="hand2")
            btn_remove.pack(side='right')

    def remove_member(self, alias_to_remove):
        if alias_to_remove in self.miembros_alias:
            self.miembros_alias.remove(alias_to_remove)
            self.update_members_display()

    def clear_member_error(self, event=None):
        if lbl_error := self.root.componentes.get('lblMemberError'):
            lbl_error.config(text="")

    def btn_register_group(self):
        nombre = self.root.componentes.get('inpGroupName').get()
        descripcion = self.root.componentes.get('inpGroupDesc').get()
        is_registered, response = GroupController.register_group(
            nombre=nombre,
            descripcion=descripcion,
            miembros_alias=self.miembros_alias
        )
        container = self.root.componentes.get('btnRegisterGroup').master.master
        color = self.root.COLOR_SUCCESS if is_registered else self.root.COLOR_DANGER
        self.root.create_label(container, 'lblGroupResponse', response, fg=color, pack_info={'pady': 10})
        if is_registered:
            self.root.componentes.get('btnRegisterGroup').config(state='disabled')
            self.root.componentes.get('btnAddMember').config(state='disabled')
            self.root.create_button(container, 'btnAcceptGroup', text='Aceptar',
                                    funcion=self.go_to_main, bg=self.root.COLOR_PRIMARY)

    def go_to_main(self):
        MainView(self.root)


class ProfileView:
    # ... (Sin cambios)
    def __init__(self, root: RootView):
        self.root = root
        self.create_profile_interface()

    def create_profile_interface(self):
        self.root.limpiar_componentes()
        main_frame = tk.Frame(self.root.root, bg=self.root.COLOR_FRAME, padx=40, pady=40)
        main_frame.pack(expand=True)
        self.root.create_label(main_frame, 'lblProfileTitle', 'Actualizar Mi Perfil',
                               font_style=self.root.FONT_TITLE, pack_info={'pady': (0, 20)})
        form_frame = tk.Frame(main_frame, bg=main_frame.cget('bg'))
        form_frame.pack(fill='x')
        labels = ['Nombres:', 'Apellidos:', 'Alias:', 'Nueva Contraseña (opcional):']
        inputs = ['inpNombres', 'inpApellidos', 'inpAlias', 'inpPassword']
        current_user_data = UserController.get_data_session_manager()
        for i, text in enumerate(labels):
            self.root.create_label(form_frame, f'lbl{inputs[i]}', text, font_style=self.root.FONT_LABEL,
                                   pack_info={'anchor': 'w', 'pady': (10, 0)})
            inp = tk.Entry(form_frame, font=self.root.FONT_BODY, bg=self.root.COLOR_BACKGROUND,
                           fg=self.root.COLOR_TEXT_DARK, relief='solid', borderwidth=1)
            self.root.componentes[inputs[i]] = inp
            if 'Nombres' in text:
                inp.insert(0, current_user_data.get('nombres', ''))
            elif 'Apellidos' in text:
                inp.insert(0, current_user_data.get('apellidos', ''))
            elif 'Alias' in text:
                inp.insert(0, current_user_data.get('alias', ''))
            elif 'Contraseña' in text:
                inp.config(show='•')
            inp.pack(pady=5, ipady=4, fill='x')
        self.root.create_button(main_frame, 'btnUpdateUser', text='Guardar Cambios',
                                funcion=self.btn_update_user, bg=self.root.COLOR_SUCCESS)
        self.root.create_button(main_frame, 'btnBackToMainFromProfile', text='Volver',
                                funcion=self.go_to_main, bg='#6C757D')

    def btn_update_user(self):
        nombres = self.root.componentes.get('inpNombres').get()
        apellidos = self.root.componentes.get('inpApellidos').get()
        alias = self.root.componentes.get('inpAlias').get()
        password = self.root.componentes.get('inpPassword').get()
        is_updated, response = UserController.event_update_user(
            nombres=nombres, apellidos=apellidos, alias=alias,
            password=password if password else None
        )
        container = self.root.componentes.get('btnUpdateUser').master
        color = self.root.COLOR_SUCCESS if is_updated else self.root.COLOR_DANGER
        self.root.create_label(container, 'lblUpdateResponse', response, fg=color, pack_info={'pady': 5})

    def go_to_main(self):
        MainView(self.root)


class RegisterTareaUserView:
    # ... (Sin cambios)
    def __init__(self, root: RootView):
        self.root = root
        self.create_fomulate_tarea()

    def create_fomulate_tarea(self):
        self.root.limpiar_componentes()
        main_frame = tk.Frame(self.root.root, bg=self.root.COLOR_FRAME, padx=40, pady=40)
        main_frame.pack(expand=True)
        self.root.create_label(main_frame, name='lblCreateTaskTitle', text='Registrar Nueva Tarea',
                               font_style=self.root.FONT_TITLE, pack_info={'pady': (0, 20)})
        form_frame = tk.Frame(main_frame, bg=main_frame.cget('bg'))
        form_frame.pack()
        labels_texts = ['Nombre de la Tarea:', 'Fecha (dd-mm-aaaa):', 'Prioridad (1-5):', 'Detalle:']
        inputs_names = ['inpNombreCreateTareaUser', 'inpFechaProgramadaCreateTareaUser', 'inpPrioridadCreateTarea',
                        'inpDetalleCreateTarea']
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
            nombre=nombre, fecha=fecha, prioridad=prioridad, detalle=detalle)
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


if __name__ == '__main__':
    LoginInView.independent_login()