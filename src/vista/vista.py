"""
    vista
"""
import tkinter as tk
from tkinter import ttk
from tkinter import Toplevel
from tkinter import messagebox
from tkinter import Text
from src.controlador.login_controller import LoginController
from src.controlador.session_controller import SessionController
from src.controlador.group_controller import GroupController
from src.controlador.task_controller import TaskController
from src.controlador.user_controller import UserController
from src.controlador.register_controller import RegisterUserController
from src.controlador.main_view_controller import MainViewController
import datetime
import calendar
import locale

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
        self.root.geometry("1150x750")
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
        if name in self.componentes:
            componente = self.componentes.pop(name)
            if componente and componente.winfo_exists():
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
            return
        inp_widget = self.componentes[name_input]
        btn_widget = self.componentes[name_button]
        if not (inp_widget.winfo_exists() and btn_widget.winfo_exists()):
            return
        simbolo = '' if inp_widget.cget('show') else '•'
        inp_widget.config(show=simbolo)
        texto_boton = 'Ocultar' if simbolo == '' else 'Mostrar'
        btn_widget.config(text=texto_boton)

    def limpiar_componentes(self):
        widget_names_to_remove = list(self.componentes.keys())
        for name in widget_names_to_remove:
            self.comprobate_existe(name=name)
        for widget in self.root.winfo_children():
            if widget.winfo_exists():
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

    @staticmethod
    def independent_login():
        root_app = RootView()
        LoginInView(root=root_app)
        root_app.main()

    def create_login(self):
        self.root.limpiar_componentes()
        main_frame = tk.Frame(self.root.root, bg=self.root.COLOR_FRAME, padx=40, pady=40)
        main_frame.pack(expand=True)
        self.root.create_label(container=main_frame, name='lblLoginTitle', text='Inicio de Sesión', font_style=self.root.FONT_TITLE, pack_info={'pady': (0, 20)})
        self.root.create_label(container=main_frame, name='lblAliasLogin', text='Alias de Usuario', font_style=self.root.FONT_LABEL, pack_info={'pady': (10, 0), 'anchor': 'w'})
        self.root.create_input(container=main_frame, name='alias')
        self.root.create_label(container=main_frame, name='lblPasswordLogin', text='Contraseña', font_style=self.root.FONT_LABEL, pack_info={'pady': (10, 0), 'anchor': 'w'})
        self.root.create_input(container=main_frame, name='password', secret=True)
        self.root.create_button(container=main_frame, name='btnOcultarPassLogin', funcion=self.btn_mostrar_contrasena, text='Mostrar', bg='#6C757D', pack_info={'pady': 5, 'ipadx': 10, 'ipady': 2, 'anchor': 'e'})
        self.root.create_button(container=main_frame, name='btnLogin', funcion=self.btn_login, text='Ingresar')
        self.root.create_label(container=main_frame, name='lblGoToRegister', text='¿No tienes una cuenta?')
        self.root.create_button(container=main_frame, name='btnRegistrase', funcion=self.go_to_register, text='Regístrate Aquí', bg=self.root.COLOR_SUCCESS)

    def go_to_register(self):
        RegisterUserView(root=self.root)

    def btn_mostrar_contrasena(self):
        self.root.btn_cambiar_secret_input(name_input='password', name_button='btnOcultarPassLogin')

    def btn_login(self):
        alias = self.root.componentes.get('alias').get()
        password = self.root.componentes.get('password').get()
        is_login, response = LoginController.login(alias=alias, password=password)
        if is_login:
            MainView(root=self.root)
        else:
            messagebox.showerror(title="Error de Inicio de Sesión", message=response)

class RegisterUserView:
    def __init__(self, root: RootView):
        self.root = root
        self.create_register_interface()

    def create_register_interface(self):
        self.root.limpiar_componentes()
        main_frame = tk.Frame(self.root.root, bg=self.root.COLOR_FRAME, padx=40, pady=40)
        main_frame.pack(expand=True)
        self.root.create_label(container=main_frame, name='lblRegisterTitle', text='Crear Cuenta', font_style=self.root.FONT_TITLE, pack_info={'pady': (0, 20)})
        form_frame = tk.Frame(main_frame, bg=main_frame.cget('bg'))
        form_frame.pack()
        labels_texts = ['Nombres:', 'Apellidos:', 'Alias:', 'Contraseña:', 'Confirmar Contraseña:']
        inputs_names = ['inpNombreRegistro', 'inpApellidoRegistro', 'inpAliasRegistro', 'inpContraseñaRegistro', 'inpConfirmarContraseñaRegistro']
        for i, text in enumerate(labels_texts):
            tk.Label(form_frame, text=text, font=self.root.FONT_LABEL, bg=form_frame.cget('bg'), fg=self.root.COLOR_TEXT_DARK).grid(row=i, column=0, sticky='w', pady=5, padx=5)
            is_secret = 'Contraseña' in text
            inp = tk.Entry(form_frame, show='•' if is_secret else '', font=self.root.FONT_BODY, bg=self.root.COLOR_BACKGROUND, fg=self.root.COLOR_TEXT_DARK, relief='solid', borderwidth=1)
            inp.grid(row=i, column=1, sticky='ew', pady=5, padx=5, ipady=4)
            self.root.componentes[inputs_names[i]] = inp
        self.root.create_button(container=main_frame, name='btnRegistrarUsuario', funcion=self.btn_registrar_usuario, text='Registrarse', bg=self.root.COLOR_SUCCESS)
        self.root.create_button(container=main_frame, name='btnRegresarLogin', funcion=self.go_to_login, text='Volver al Inicio', bg='#6C757D')

    def btn_registrar_usuario(self):
        nombres = self.root.componentes['inpNombreRegistro'].get()
        apellidos = self.root.componentes['inpApellidoRegistro'].get()
        alias = self.root.componentes['inpAliasRegistro'].get()
        password = self.root.componentes['inpContraseñaRegistro'].get()
        confirm_password = self.root.componentes['inpConfirmarContraseñaRegistro'].get()
        is_user_save, response = RegisterUserController.register_user(
            nombres=nombres,
            apellidos=apellidos,
            alias=alias,
            password=password,
            confirm_password=confirm_password
        )
        if is_user_save:
            messagebox.showinfo(title="Registro Exitoso", message=response)
            self.go_to_login()
        else:
            messagebox.showerror(title="Error de Registro", message=response)

    def go_to_login(self):
        LoginInView(root=self.root)


class CalendarPicker(Toplevel):
    """Ventana emergente que muestra un calendario para seleccionar una fecha."""

    def __init__(self, parent, on_date_select_callback):
        super().__init__(parent)
        self.on_date_select_callback = on_date_select_callback
        self.today = datetime.date.today()
        self.current_year = self.today.year
        self.current_month = self.today.month

        self.title("Seleccionar Fecha")
        self.config(bg=RootView.COLOR_BACKGROUND)
        self.transient(parent)
        self.grab_set()

        self.create_widgets()
        self.draw_calendar()

        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f'+{x}+{y}')

    def create_widgets(self):
        # Frame de navegación del mes
        nav_frame = tk.Frame(self, bg=self.cget('bg'))
        nav_frame.pack(pady=5, fill='x')

        tk.Button(nav_frame, text="◀", command=self.prev_month, relief='flat', bg=self.cget('bg')).pack(side='left',
                                                                                                        padx=10)
        self.month_year_label = tk.Label(nav_frame, text="", font=("Helvetica", 12, "bold"), bg=self.cget('bg'))
        self.month_year_label.pack(side='left', expand=True)
        tk.Button(nav_frame, text="▶", command=self.next_month, relief='flat', bg=self.cget('bg')).pack(side='right',
                                                                                                        padx=10)

        # Frame para los días de la semana y el calendario
        self.calendar_frame = tk.Frame(self, bg=self.cget('bg'))
        self.calendar_frame.pack(padx=10, pady=10)

        days = ["Lu", "Ma", "Mi", "Ju", "Vi", "Sá", "Do"]
        for i, day in enumerate(days):
            tk.Label(self.calendar_frame, text=day, font=("Helvetica", 10, "bold"), bg=self.cget('bg')).grid(row=0,
                                                                                                             column=i,
                                                                                                             padx=5,
                                                                                                             pady=5)

    def draw_calendar(self):
        for widget in self.calendar_frame.grid_slaves():
            if int(widget.grid_info()["row"]) > 0:
                widget.grid_forget()

        month_name = self.today.replace(month=self.current_month, day=1).strftime('%B').capitalize()
        self.month_year_label.config(text=f"{month_name} {self.current_year}")

        cal = calendar.monthcalendar(self.current_year, self.current_month)

        for r, week in enumerate(cal, start=1):
            for c, day in enumerate(week):
                if day != 0:
                    btn = tk.Button(self.calendar_frame, text=str(day), command=lambda d=day: self.select_date(d),
                                    relief='flat')
                    if self.current_year == self.today.year and self.current_month == self.today.month and day == self.today.day:
                        btn.config(bg='#AED6F1', relief='solid', borderwidth=1)  # Resaltar hoy
                    btn.grid(row=r, column=c, padx=2, pady=2, ipadx=5, ipady=5)

    def prev_month(self):
        self.current_month -= 1
        if self.current_month == 0:
            self.current_month = 12
            self.current_year -= 1
        self.draw_calendar()

    def next_month(self):
        self.current_month += 1
        if self.current_month == 13:
            self.current_month = 1
            self.current_year += 1
        self.draw_calendar()

    def select_date(self, day):
        selected_date = datetime.date(self.current_year, self.current_month, day)
        self.on_date_select_callback(selected_date)
        self.destroy()


class MainView:
    def __init__(self, root: 'RootView'):
        self.root = root
        # Atributos de estado
        self.current_date = datetime.date.today()
        self.todas_las_tareas = []
        self.current_page = 1
        self.tasks_per_page = 5
        self.total_pages = 1

        # Widgets que necesitan ser referenciados
        self.title_label = None
        self.date_display_label = None
        self.pagination_frame = None
        self.prev_button = None
        self.next_button = None
        self.page_label = None

        self.create_main_interface()

    def create_main_interface(self):
        self.root.limpiar_componentes()
        header_frame = tk.Frame(self.root.root, bg=self.root.COLOR_FRAME, padx=20, pady=10)
        header_frame.pack(fill='x')
        pack_info_btn = {'side': 'left', 'padx': 5, 'ipady': 3, 'ipadx': 10}

        self.root.create_button(container=header_frame, name='btnRefreshTasks', funcion=self.setup_task_display,
                                text='Refrescar 🔄', bg='#17A2B8', pack_info=pack_info_btn)
        self.root.create_button(container=header_frame, name='btnCrearTarea', funcion=self.go_to_create_tarea,
                                text='✚ Nueva Tarea', bg=self.root.COLOR_PRIMARY, pack_info=pack_info_btn)
        self.root.create_button(container=header_frame, name='btnCrearGrupo', funcion=self.go_to_create_group,
                                text='✚ Nuevo Grupo', bg=self.root.COLOR_SUCCESS, pack_info=pack_info_btn)
        self.root.create_button(container=header_frame, name='btnMiPerfil', funcion=self.go_to_profile,
                                text='Mi Perfil', bg='#6C757D',
                                pack_info={'side': 'right', 'padx': 10, 'ipady': 3, 'ipadx': 10})
        self.root.create_button(container=header_frame, name='btnLogOut', funcion=self.go_to_login,
                                text='Cerrar Sesión', bg=self.root.COLOR_DANGER,
                                pack_info={'side': 'right', 'padx': 10, 'ipady': 3, 'ipadx': 10})

        content_frame = tk.Frame(self.root.root, bg=self.root.COLOR_BACKGROUND, padx=20, pady=20)
        content_frame.pack(fill='both', expand=True)

        title_frame = tk.Frame(content_frame, bg=content_frame.cget('bg'))
        title_frame.pack(fill='x', pady=(0, 10))

        self.title_label = tk.Label(title_frame, text="", font=self.root.FONT_TITLE, bg=title_frame.cget('bg'),
                                    fg=self.root.COLOR_TEXT_DARK)
        self.title_label.pack()

        date_control_frame = tk.Frame(title_frame, bg=title_frame.cget('bg'))
        date_control_frame.pack()

        tk.Button(date_control_frame, text="◀", command=self.prev_day, relief='flat', font=("Helvetica", 14),
                  bg=date_control_frame.cget('bg'), cursor="hand2").pack(side='left', padx=10)
        self.date_display_label = tk.Label(date_control_frame, text="", font=("Helvetica", 12),
                                           bg=date_control_frame.cget('bg'))
        self.date_display_label.pack(side='left')
        tk.Button(date_control_frame, text="▶", command=self.next_day, relief='flat', font=("Helvetica", 14),
                  bg=date_control_frame.cget('bg'), cursor="hand2").pack(side='left', padx=10)
        tk.Button(date_control_frame, text="📅", command=self.open_calendar, relief='flat', font=("Helvetica", 14),
                  bg=date_control_frame.cget('bg'), cursor="hand2").pack(side='left', padx=10)

        self.tasks_widgets_frame = tk.Frame(content_frame, bg=content_frame.cget('bg'))
        self.tasks_widgets_frame.pack(fill='both', expand=True)

        self.pagination_frame = tk.Frame(content_frame, bg=content_frame.cget('bg'))
        self.pagination_frame.pack(fill='x', pady=(10, 0))

        self.setup_task_display()

    def setup_task_display(self):
        """Función central que carga datos para la fecha actual y refresca toda la UI."""
        self.update_date_labels()

        request = MainViewController.recover_task_for_date(fecha=self.current_date)

        if not request['success']:
            messagebox.showerror(title="Error al Cargar Tareas", message=request['response'])
            self.todas_las_tareas = []
        else:
            tareas_sin_ordenar = request['data']['tareas'] or []
            self.todas_las_tareas = sorted(tareas_sin_ordenar, key=lambda t: t.get('prioridad', 99))

        num_tasks = len(self.todas_las_tareas)
        self.total_pages = (num_tasks + self.tasks_per_page - 1) // self.tasks_per_page or 1
        self.current_page = 1

        self.display_current_page()
        self.setup_pagination_controls()

    def update_date_labels(self):
        """Actualiza el título principal y la etiqueta de fecha."""
        hoy = datetime.date.today()
        if self.current_date == hoy:
            self.title_label.config(text="Tareas para Hoy")
        else:
            self.title_label.config(text="Tareas para el")

        try:
            fecha_formateada = self.current_date.strftime('%A, %d de %B de %Y').capitalize()
        except UnicodeEncodeError:  # Fallback por si el locale no funciona
            fecha_formateada = self.current_date.strftime('%Y-%m-%d')

        self.date_display_label.config(text=fecha_formateada)

    def prev_day(self):
        self.current_date -= datetime.timedelta(days=1)
        self.setup_task_display()

    def next_day(self):
        self.current_date += datetime.timedelta(days=1)
        self.setup_task_display()

    def open_calendar(self):
        CalendarPicker(parent=self.root.root, on_date_select_callback=self.on_date_selected)

    def on_date_selected(self, new_date):
        if new_date:
            self.current_date = new_date
            self.setup_task_display()

    def display_current_page(self):
        for widget in self.tasks_widgets_frame.winfo_children(): widget.destroy()
        if not self.todas_las_tareas:
            self.root.create_label(container=self.tasks_widgets_frame, name='lblNoTasks',
                                   text='🎉 ¡Felicidades! No hay tareas para esta fecha.', fg='#6C757D',
                                   font_style=("Helvetica", 14, "italic"), pack_info={'pady': 20})
            if self.pagination_frame: self.pagination_frame.pack_forget()
            return

        if self.pagination_frame: self.pagination_frame.pack(fill='x', pady=(10, 0))
        start_index = (self.current_page - 1) * self.tasks_per_page
        tasks_to_display = self.todas_las_tareas[start_index: start_index + self.tasks_per_page]
        for tarea in tasks_to_display: self.insert_task_view(tarea=tarea)
        if hasattr(self, 'page_label') and self.page_label: self.update_pagination_controls()

    def setup_pagination_controls(self):
        for widget in self.pagination_frame.winfo_children(): widget.destroy()
        self.prev_button = tk.Button(self.pagination_frame, text="◀ Anterior", command=self.prev_page,
                                     font=self.root.FONT_BUTTON, relief='flat', cursor="hand2")
        self.prev_button.pack(side='left', padx=10)
        self.page_label = tk.Label(self.pagination_frame, text="", font=("Helvetica", 12, "bold"),
                                   bg=self.pagination_frame.cget('bg'))
        self.page_label.pack(side='left', expand=True)
        self.next_button = tk.Button(self.pagination_frame, text="Siguiente ▶", command=self.next_page,
                                     font=self.root.FONT_BUTTON, relief='flat', cursor="hand2")
        self.next_button.pack(side='right', padx=10)
        self.update_pagination_controls()

    def update_pagination_controls(self):
        if not hasattr(self, 'page_label') or not self.page_label: return

        if not self.todas_las_tareas:
            self.page_label.config(text="")
            self.prev_button.config(state='disabled')
            self.next_button.config(state='disabled')
            return

        self.page_label.config(text=f"Página {self.current_page} de {self.total_pages}")
        self.prev_button.config(state='normal' if self.current_page > 1 else 'disabled')
        self.next_button.config(state='normal' if self.current_page < self.total_pages else 'disabled')

    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.display_current_page()

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.display_current_page()

    def insert_task_view(self, tarea: dict):
        task_id = tarea.get('id_tarea')
        task_frame = tk.Frame(self.tasks_widgets_frame, bg=self.root.COLOR_FRAME, relief='solid', borderwidth=1,
                              padx=10, pady=10)
        task_frame.pack(fill='x', pady=5, expand=True)

        info_frame = tk.Frame(task_frame, bg=task_frame.cget('bg'))
        info_frame.pack(side='left', fill='x', expand=True)
        tk.Label(info_frame, text=tarea.get('nombre'), font=("Helvetica", 14, "bold"), bg=info_frame.cget('bg'),
                 fg=self.root.COLOR_TEXT_DARK, anchor='w', justify='left', wraplength=600).pack(fill='x')
        tk.Label(info_frame, text=tarea.get('nombre_prioridad', ''), font=("Helvetica", 10, "italic"),
                 bg=info_frame.cget('bg'), fg=self.root.COLOR_TEXT_DARK, anchor='w').pack(fill='x', pady=(2, 0))
        if tarea.get('grupo'):
            tk.Label(info_frame, text=f"Grupo: {tarea.get('grupo')}", font=("Helvetica", 10), bg=info_frame.cget('bg'),
                     fg='#566573', anchor='w').pack(fill='x', pady=(5, 0))

        actions_frame = tk.Frame(task_frame, bg=task_frame.cget('bg'))
        actions_frame.pack(side='right', fill='y', padx=(10, 0))

        disponible, es_de_grupo, rol = tarea.get('disponible', True), tarea.get('is_in_group', False), tarea.get('rol',
                                                                                                                 None)
        can_edit = disponible and (not es_de_grupo or rol not in ['miembro'])
        can_archive = disponible or (es_de_grupo and rol not in ['miembro']) or (not es_de_grupo)
        can_delete = not es_de_grupo or rol not in ['miembro', 'editor']
        realizado = tarea.get('realizado', False)

        btn_check = tk.Button(actions_frame, text='✔' if realizado else '✖',
                              bg=self.root.COLOR_SUCCESS if realizado else self.root.COLOR_DANGER,
                              fg=self.root.COLOR_TEXT_LIGHT, font=self.root.FONT_BUTTON, relief='flat', width=3,
                              command=lambda id_t=task_id: self.btn_check_task(id_tarea=id_t), cursor="hand2")
        btn_check.pack(side='left', padx=2)

        btn_details = tk.Button(actions_frame, text='Detalle', bg='#17A2B8', fg=self.root.COLOR_TEXT_LIGHT,
                                font=self.root.FONT_BUTTON, relief='flat',
                                command=lambda t=tarea: self.show_task_details(tarea=t), cursor="hand2")
        btn_details.pack(side='left', padx=2)

        btn_edit = tk.Button(actions_frame, text='Editar', bg='#6C757D', fg=self.root.COLOR_TEXT_LIGHT,
                             font=self.root.FONT_BUTTON, relief='flat',
                             command=lambda id_t=task_id: self.btn_edit_task(id_tarea=id_t))
        btn_edit.config(state='normal' if can_edit else 'disabled', cursor="hand2" if can_edit else "arrow")
        btn_edit.pack(side='left', padx=2)

        btn_archive = tk.Button(actions_frame, text='Archivar', bg='#5D6D7E', fg=self.root.COLOR_TEXT_LIGHT,
                                font=self.root.FONT_BUTTON, relief='flat',
                                command=lambda id_t=task_id: self.btn_archive_task(id_tarea=id_t))
        btn_archive.config(state='normal' if can_archive else 'disabled', cursor="hand2" if can_archive else "arrow")
        btn_archive.pack(side='left', padx=2)

        btn_delete = tk.Button(actions_frame, text='Eliminar', bg=self.root.COLOR_DANGER, fg=self.root.COLOR_TEXT_LIGHT,
                               font=self.root.FONT_BUTTON, relief='flat',
                               command=lambda id_t=task_id: self.btn_delete_task(id_tarea=id_t))
        btn_delete.config(state='normal' if can_delete else 'disabled', cursor="hand2" if can_delete else "arrow")
        btn_delete.pack(side='left', padx=2)

    def find_task_by_id(self, task_id):
        return next((task for task in self.todas_las_tareas if task.get('id_tarea') == task_id), None)

    def show_task_details(self, tarea: dict):
        nombre = tarea.get('nombre', 'Detalles de la Tarea')
        detalle = tarea.get('detalle', 'No hay detalles disponibles para esta tarea.')
        if not detalle or not detalle.strip():
            detalle = 'No hay detalles disponibles para esta tarea.'
        messagebox.showinfo(title=nombre, message=detalle)

    def btn_check_task(self, id_tarea):
        task = self.find_task_by_id(id_tarea)
        if not task: return

        nuevo_estado = not task.get('realizado', False)
        is_change, response = TaskController.event_check_in_task(id_tarea=id_tarea, realizado=nuevo_estado)
        if is_change:
            self.setup_task_display()
        else:
            messagebox.showerror(title="Error", message=response)

    def btn_edit_task(self, id_tarea):
        task_data = self.find_task_by_id(id_tarea)
        if task_data:
            EditTaskView(root=self.root, main_view=self, task_data=task_data)

    def btn_archive_task(self, id_tarea):
        task = self.find_task_by_id(id_tarea)
        if not task: return

        if messagebox.askyesno(title="Confirmar Archivar",
                               message=f"¿Estás seguro de que deseas archivar la tarea:\n\n'{task.get('nombre')}'?"):
            is_archived, response = TaskController.event_archive_task(id_tarea=id_tarea)
            if is_archived:
                messagebox.showinfo(title="Tarea Archivada", message=response)
                self.setup_task_display()
            else:
                messagebox.showerror(title="Error", message=f"No se pudo archivar la tarea:\n{response}")

    def btn_delete_task(self, id_tarea):
        task = self.find_task_by_id(id_tarea)
        if not task: return

        if messagebox.askyesno(title="Confirmar Eliminación",
                               message=f"¡ADVERTENCIA!\n\n¿Estás seguro de que deseas eliminar la tarea:\n\n'{task.get('nombre')}'?\n\nEsta acción es definitiva.",
                               icon='warning'):
            is_deleted, response = TaskController.event_delete_task(id_tarea=id_tarea)
            if is_deleted:
                messagebox.showinfo(title="Tarea Eliminada", message=response)
                self.setup_task_display()
            else:
                messagebox.showerror(title="Error", message=f"No se pudo eliminar la tarea:\n{response}")

    def go_to_create_tarea(self):
        RegisterTareaUserView(root=self.root)

    def go_to_login(self):
        MainViewController.log_out()
        LoginInView(root=self.root)

    def go_to_create_group(self):
        GroupRegisterView(root=self.root)

    def go_to_profile(self):
        ProfileView(root=self.root)

class EditTaskView:
    def __init__(self, root: RootView, main_view: MainView, task_data: dict):
        self.root, self.main_view, self.task_data = root, main_view, task_data
        self.top = Toplevel(root.root)
        self.top.title("Editar Tarea")
        self.top.config(bg=root.COLOR_BACKGROUND)
        self.top.minsize(500, 450)
        self.top.transient(root.root)
        self.top.grab_set()
        self.create_edit_form()
        self.root.center_window(top_level_window=self.top)

    def create_edit_form(self):
        outer_frame = tk.Frame(self.top, bg=self.root.COLOR_FRAME, padx=20, pady=20)
        outer_frame.pack(expand=True, fill='both')
        tk.Label(outer_frame, text='Editar Tarea', font=self.root.FONT_TITLE, bg=outer_frame.cget('bg'), fg=self.root.COLOR_TEXT_DARK).pack(pady=(0, 20))
        form_frame = tk.Frame(outer_frame, bg=outer_frame.cget('bg'))
        form_frame.pack(fill='x')
        form_frame.grid_columnconfigure(1, weight=1)
        labels_texts = ['Nombre:', 'Fecha (dd-mm-aaaa):', 'Prioridad (1-5):', 'Detalle:']
        self.inputs = {}
        for i, text in enumerate(labels_texts):
            tk.Label(form_frame, text=text, font=self.root.FONT_LABEL, bg=form_frame.cget('bg'), fg=self.root.COLOR_TEXT_DARK).grid(row=i, column=0, sticky='nw', pady=5, padx=5)
            key = text.split(' ')[0].lower().replace(':', '')
            if key == 'detalle':
                inp = Text(form_frame, font=self.root.FONT_BODY, bg=self.root.COLOR_BACKGROUND, fg=self.root.COLOR_TEXT_DARK, relief='solid', borderwidth=1, height=7, wrap=tk.WORD)
                inp.grid(row=i, column=1, sticky='ew', pady=5, padx=5)
            else:
                inp = tk.Entry(form_frame, font=self.root.FONT_BODY, bg=self.root.COLOR_BACKGROUND, fg=self.root.COLOR_TEXT_DARK, relief='solid', borderwidth=1)
                inp.grid(row=i, column=1, sticky='ew', pady=5, padx=5, ipady=4)
            self.inputs[key] = inp
        self.inputs['nombre'].insert(0, self.task_data.get('nombre', ''))
        self.inputs['fecha'].insert(0, self.task_data.get('fecha', ''))
        self.inputs['prioridad'].insert(0, str(self.task_data.get('prioridad', '')))
        self.inputs['detalle'].insert('1.0', self.task_data.get('detalle', ''))
        buttons_frame = tk.Frame(outer_frame, bg=outer_frame.cget('bg'))
        buttons_frame.pack(fill='x', pady=(20, 0))
        tk.Button(buttons_frame, text="Guardar Cambios", command=self.save_changes, bg=self.root.COLOR_SUCCESS, fg=self.root.COLOR_TEXT_LIGHT, font=self.root.FONT_BUTTON, relief='flat', cursor="hand2").pack(side='left', expand=True, padx=5, ipady=3)
        tk.Button(buttons_frame, text="Cancelar", command=self.close_window, bg='#6C757D', fg=self.root.COLOR_TEXT_LIGHT, font=self.root.FONT_BUTTON, relief='flat', cursor="hand2").pack(side='right', expand=True, padx=5, ipady=3)

    def save_changes(self):
        update_payload = {
            'nombre': self.inputs['nombre'].get(),
            'fecha': self.inputs['fecha'].get(),
            'prioridad': self.inputs['prioridad'].get(),
            'detalle': self.inputs['detalle'].get("1.0", tk.END).strip()
        }
        is_updated, response = TaskController.event_edit_task_session_manager(id_tarea=self.task_data.get('id_tarea'), **update_payload)
        if is_updated:
            messagebox.showinfo(title="Edición Exitosa", message=response)
            self.main_view.refresh_tasks_view()
            self.close_window()
        else:
            messagebox.showerror(title="Error al Guardar", message=response)

    def close_window(self):
        self.top.destroy()

class GroupRegisterView:
    def __init__(self, root: RootView):
        self.root, self.miembros_alias = root, []
        self.create_group_form()

    def create_group_form(self):
        self.root.limpiar_componentes()
        main_frame = tk.Frame(self.root.root, bg=self.root.COLOR_FRAME, padx=40, pady=40)
        main_frame.pack(expand=True, fill='both')
        self.root.create_label(container=main_frame, name='lblGroupTitle', text='Registrar Nuevo Grupo', font_style=self.root.FONT_TITLE, pack_info={'pady': (0, 20)})
        form_frame = tk.Frame(main_frame, bg=main_frame.cget('bg'))
        form_frame.pack(fill='x', pady=10)
        self.root.create_label(container=form_frame, name='lblGroupName', text='Nombre del Grupo:', font_style=self.root.FONT_LABEL, pack_info={'anchor': 'w'})
        self.root.create_input(container=form_frame, name='inpGroupName')
        self.root.create_label(container=form_frame, name='lblGroupDesc', text='Descripción (Opcional):', font_style=self.root.FONT_LABEL, pack_info={'anchor': 'w', 'pady': (10, 0)})
        self.root.create_input(container=form_frame, name='inpGroupDesc')
        members_section = tk.Frame(main_frame, bg=main_frame.cget('bg'), pady=10)
        members_section.pack(fill='x', expand=True)
        self.root.create_label(container=members_section, name='lblAddMemberTitle', text='Añadir Miembros (por alias):', font_style=self.root.FONT_LABEL, pack_info={'anchor': 'w'})
        add_member_input = tk.Frame(members_section, bg=members_section.cget('bg'))
        add_member_input.pack(fill='x')
        inp_alias = tk.Entry(add_member_input, font=self.root.FONT_BODY, bg=self.root.COLOR_BACKGROUND, fg=self.root.COLOR_TEXT_DARK, relief='solid', borderwidth=1)
        inp_alias.pack(side='left', fill='x', expand=True, ipady=4, pady=5, padx=(0, 10))
        self.root.componentes['inpMemberAlias'] = inp_alias
        tk.Button(add_member_input, text="Añadir Miembro", command=self.btn_add_member, bg=self.root.COLOR_PRIMARY, fg=self.root.COLOR_TEXT_LIGHT, font=self.root.FONT_BUTTON, relief='flat', cursor="hand2").pack(side='right', ipady=5, ipadx=10)
        self.root.create_label(container=members_section, name='lblCurrentMembers', text='Miembros a Agregar:', font_style=self.root.FONT_LABEL, pack_info={'anchor': 'w', 'pady': (10, 5)})
        self.members_frame = tk.Frame(members_section, bg=self.root.COLOR_BACKGROUND, relief='solid', borderwidth=1, padx=10, pady=10)
        self.members_frame.pack(fill='both', expand=True)
        self.update_members_display()
        action_buttons = tk.Frame(main_frame, bg=main_frame.cget('bg'))
        action_buttons.pack(fill='x', pady=(20, 0))
        self.root.create_button(container=action_buttons, name='btnRegisterGroup', funcion=self.btn_register_group, text='Guardar Grupo', bg=self.root.COLOR_SUCCESS, pack_info={'side': 'left', 'expand': True, 'padx': 5, 'ipady':3})
        self.root.create_button(container=action_buttons, name='btnBackToMain', funcion=self.go_to_main, text='Volver', bg='#6C757D', pack_info={'side': 'right', 'expand': True, 'padx': 5, 'ipady':3})

    def btn_add_member(self):
        alias = self.root.componentes.get('inpMemberAlias').get().strip()
        if not alias: return
        if alias in self.miembros_alias:
            messagebox.showwarning(title="Miembro Duplicado", message=f"El usuario '{alias}' ya está en la lista.")
            return
        is_valid, response = GroupController.is_user_exits(alias=alias)
        if is_valid:
            self.miembros_alias.append(alias)
            self.update_members_display()
            self.root.componentes.get('inpMemberAlias').delete(0, tk.END)
        else:
            messagebox.showerror(title="Error al Añadir Miembro", message=response)

    def update_members_display(self):
        for widget in self.members_frame.winfo_children(): widget.destroy()
        if not self.miembros_alias:
            tk.Label(self.members_frame, text="No hay miembros agregados.", font=self.root.FONT_BODY, bg=self.members_frame.cget('bg'), fg='#6C757D').pack(pady=10)
            return
        for alias in self.miembros_alias:
            item_frame = tk.Frame(self.members_frame, bg=self.members_frame.cget('bg'))
            item_frame.pack(fill='x', pady=2)
            tk.Label(item_frame, text=f"• {alias}", font=self.root.FONT_BODY, bg=item_frame.cget('bg')).pack(side='left', padx=(0, 10))
            tk.Button(item_frame, text="Quitar", command=lambda a=alias: self.remove_member(alias_to_remove=a), bg=self.root.COLOR_DANGER, fg=self.root.COLOR_TEXT_LIGHT, font=("Helvetica", 8, "bold"), relief='flat', cursor="hand2").pack(side='right')

    def remove_member(self, alias_to_remove):
        if alias_to_remove in self.miembros_alias:
            self.miembros_alias.remove(alias_to_remove)
            self.update_members_display()

    def btn_register_group(self):
        nombre = self.root.componentes.get('inpGroupName').get()
        descripcion = self.root.componentes.get('inpGroupDesc').get()
        is_registered, response = GroupController.register_group(nombre=nombre, descripcion=descripcion, miembros_alias=self.miembros_alias)
        if is_registered:
            messagebox.showinfo(title="Grupo Registrado", message=response)
            self.go_to_main()
        else:
            messagebox.showerror(title="Error de Registro de Grupo", message=response)

    def go_to_main(self): MainView(root=self.root)

class ProfileView:
    def __init__(self, root: RootView):
        self.root = root
        self.create_profile_interface()

    def create_profile_interface(self):
        self.root.limpiar_componentes()
        main_frame = tk.Frame(self.root.root, bg=self.root.COLOR_FRAME, padx=40, pady=40)
        main_frame.pack(expand=True, fill="both")
        self.root.create_label(container=main_frame, name='lblProfileTitle', text='Actualizar Mi Perfil', font_style=self.root.FONT_TITLE, pack_info={'pady': (0, 20)})
        form_frame = tk.Frame(main_frame, bg=main_frame.cget('bg'))
        form_frame.pack(fill='x')
        labels, names = ['Nombres:', 'Apellidos:', 'Alias:', 'Nueva Contraseña (opcional):'], ['inpNombres', 'inpApellidos', 'inpAlias', 'inpPassword']
        user_data = UserController.get_data_session_manager()
        for i, text in enumerate(labels):
            self.root.create_label(container=form_frame, name=f'lbl{names[i]}', text=text, font_style=self.root.FONT_LABEL, pack_info={'anchor': 'w', 'pady': (10, 0)})
            inp = tk.Entry(form_frame, font=self.root.FONT_BODY, bg=self.root.COLOR_BACKGROUND, fg=self.root.COLOR_TEXT_DARK, relief='solid', borderwidth=1)
            if 'Nombres' in text: inp.insert(0, user_data.get('nombres', ''))
            elif 'Apellidos' in text: inp.insert(0, user_data.get('apellidos', ''))
            elif 'Alias' in text:
                inp.insert(0, user_data.get('alias', ''))
                inp.config(state='readonly', fg='grey')
            elif 'Contraseña' in text: inp.config(show='•')
            inp.pack(pady=5, ipady=4, fill='x')
            self.root.componentes[names[i]] = inp
        action_buttons = tk.Frame(main_frame, bg=main_frame.cget('bg'))
        action_buttons.pack(fill='x', pady=(20,0))
        self.root.create_button(container=action_buttons, name='btnUpdateUser', funcion=self.btn_update_user, text='Guardar Cambios', bg=self.root.COLOR_SUCCESS, pack_info={'side':'left', 'expand':True, 'padx':5, 'ipady':3})
        self.root.create_button(container=action_buttons, name='btnBackToMainFromProfile', funcion=self.go_to_main, text='Volver', bg='#6C757D', pack_info={'side':'right', 'expand':True, 'padx':5, 'ipady':3})

    def btn_update_user(self):
        nombres = self.root.componentes['inpNombres'].get()
        apellidos = self.root.componentes['inpApellidos'].get()
        alias = self.root.componentes['inpAlias'].get()
        password = self.root.componentes['inpPassword'].get()
        is_updated, response = UserController.event_update_user(
            nombres=nombres,
            apellidos=apellidos,
            alias=alias,
            password=password if password else None
        )
        if is_updated:
            messagebox.showinfo(title="Perfil Actualizado", message=response)
            if 'btnUpdateUser' in self.root.componentes: self.root.componentes['btnUpdateUser'].config(state='disabled')
        else:
            messagebox.showerror(title="Error al Actualizar", message=response)

    def go_to_main(self): MainView(root=self.root)

class RegisterTareaUserView:
    def __init__(self, root: 'RootView'):
        self.root = root
        self.selected_group_id = None
        self.current_user_alias = SessionController.get_alias_user()
        self.members_to_assign = {}
        # NOTE: La lógica completa de asignación de miembros no está implementada
        # en este ejemplo para mantenerlo conciso, pero la estructura está aquí.
        self.create_fomulate_tarea()

    def create_fomulate_tarea(self):
        self.root.limpiar_componentes()
        outer_frame = tk.Frame(self.root.root, bg=self.root.COLOR_FRAME, padx=30, pady=30)
        outer_frame.pack(expand=True, fill='both')
        self.root.create_label(container=outer_frame, name='lblCreateTaskTitle', text='Registrar Nueva Tarea', font_style=self.root.FONT_TITLE, pack_info={'pady': (0, 15)})
        form_content_frame = tk.Frame(outer_frame, bg=outer_frame.cget('bg'))
        form_content_frame.pack(expand=True, fill='x')
        form_content_frame.grid_columnconfigure(1, weight=1)
        labels = ['Nombre de la Tarea:', 'Fecha (dd-mm-aaaa):', 'Prioridad (1-5):', 'Detalle:']
        names = ['inpNombreCreateTareaUser', 'inpFechaProgramadaCreateTareaUser', 'inpPrioridadCreateTarea', 'inpDetalleCreateTarea']
        for i, text in enumerate(labels):
             tk.Label(form_content_frame, text=text, font=self.root.FONT_LABEL, bg=form_content_frame.cget('bg'), fg=self.root.COLOR_TEXT_DARK).grid(row=i, column=0, sticky='nw', pady=5, padx=5)
             if text == 'Detalle:':
                 inp = Text(form_content_frame, font=self.root.FONT_BODY, relief='solid', borderwidth=1, height=6, wrap=tk.WORD)
                 inp.grid(row=i, column=1, sticky='ew', pady=5, padx=5)
             else:
                 inp = tk.Entry(form_content_frame, font=self.root.FONT_BODY, relief='solid', borderwidth=1)
                 inp.grid(row=i, column=1, sticky='ew', pady=5, padx=5, ipady=4)
             self.root.componentes[names[i]] = inp
        action_buttons = tk.Frame(outer_frame, bg=outer_frame.cget('bg'))
        action_buttons.pack(pady=(15,0), fill='x')
        self.root.create_button(container=action_buttons, name='btnRegistrarTarea', funcion=self.btn_registrar_tarea, text='Guardar Tarea', bg=self.root.COLOR_SUCCESS, pack_info={'side': 'left', 'expand': True, 'padx': 5, 'ipady':3})
        self.root.create_button(container=action_buttons, name='btnVolver', funcion=self.btn_volver, text='Volver', bg='#6C757D', pack_info={'side': 'right', 'expand': True, 'padx': 5, 'ipady':3})

    def btn_registrar_tarea(self):
        nombre = self.root.componentes['inpNombreCreateTareaUser'].get()
        fecha = self.root.componentes['inpFechaProgramadaCreateTareaUser'].get()
        prioridad_str = self.root.componentes['inpPrioridadCreateTarea'].get()
        detalle = self.root.componentes['inpDetalleCreateTarea'].get("1.0", tk.END).strip()
        if not all([nombre, fecha, prioridad_str]):
            messagebox.showerror(title="Datos Incompletos", message="Nombre, Fecha y Prioridad son obligatorios.")
            return
        try:
            prioridad = int(prioridad_str)
            if not (1 <= prioridad <= 5): raise ValueError("Rango")
        except ValueError:
            messagebox.showerror(title="Dato Inválido", message="Prioridad debe ser un número entre 1 y 5.")
            return
        is_registered, response = TaskController.event_register_task_user(
            nombre=nombre,
            fecha=fecha,
            prioridad=prioridad,
            detalle=detalle
        )
        if is_registered:
            messagebox.showinfo(title="Tarea Registrada", message=response)
            self.btn_aceptar_crear_tarea()
        else:
            messagebox.showerror(title="Error al Registrar Tarea", message=response)

    def btn_volver(self): MainView(root=self.root)
    def btn_aceptar_crear_tarea(self): MainView(root=self.root)