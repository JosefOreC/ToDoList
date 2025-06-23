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
from src.controlador.group_controller import GroupController, Rol
from src.controlador.task_controller import TaskController
from src.controlador.user_controller import UserController
from src.controlador.register_controller import RegisterUserController
from src.controlador.main_view_controller import MainViewController
import datetime
import calendar


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
        self.root.geometry("1250x850")
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
        self.recuperar = 'normal'
        self.funcion_recover_task = {'normal': lambda:MainViewController.recover_task_for_date(self.current_date),
                                     'archivadas':MainViewController.recover_task_archivade}

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
        self.root.create_button(container=header_frame, name='btnManageGroups', funcion=self.go_to_manage_groups,
                                text='👥 Gestionar Grupos', bg=self.root.COLOR_SUCCESS, pack_info=pack_info_btn)

        self.root.create_button(container=header_frame, name='btnVerArchivados', funcion=self.event_change_type_archivate,
                                text='📂Archivados', bg=self.root.COLOR_SUCCESS, pack_info=pack_info_btn)

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

    def event_change_type_archivate(self):
        self.recuperar = 'archivadas'
        self.root.componentes.get('btnVerArchivados').config(text='Volver',
                                                             command=self.event_change_type_normal)
        self.setup_task_display()

    def event_change_type_normal(self):
        self.recuperar = 'normal'
        self.root.componentes.get('btnVerArchivados').config(text='📂Archivados',
                                                             command=self.event_change_type_archivate)
        self.setup_task_display()

    def setup_task_display(self):
        """Función central que carga datos para la fecha actual y refresca toda la UI."""
        self.update_date_labels()

        request = self.funcion_recover_task.get(self.recuperar)()

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

        if self.recuperar=='archivadas':
            tk.Label(info_frame, text=f"Fecha: {tarea.get('fecha')}", font=("Helvetica", 10), bg=info_frame.cget('bg'),
                     fg='#566573', anchor='w').pack(fill='y', pady=(5, 0))

        actions_frame = tk.Frame(task_frame, bg=task_frame.cget('bg'))
        actions_frame.pack(side='right', fill='y', padx=(10, 0))

        disponible, es_de_grupo, rol = tarea.get('disponible', True), tarea.get('is_in_group', False), tarea.get('rol',
                                                                                                                 None)
        can_edit = disponible and (not es_de_grupo or rol not in ['miembro'])
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

        if can_edit:
            btn_edit = tk.Button(actions_frame, text='Editar', bg='#6C757D', fg=self.root.COLOR_TEXT_LIGHT,
                                 font=self.root.FONT_BUTTON, relief='flat',
                                 command=lambda id_t=task_id: self.btn_edit_task(id_tarea=id_t))
            btn_edit.config(state='normal' if can_edit else 'disabled', cursor="hand2" if can_edit else "arrow")
            btn_edit.pack(side='left', padx=2)

        btn_archive = tk.Button(actions_frame, text='Archivar' if not tarea.get('archivado') else 'Desarchivar'
                                , bg='#5D6D7E' if not tarea.get('archivado') else
                                self.root.COLOR_SUCCESS, fg=self.root.COLOR_TEXT_LIGHT,
                                font=self.root.FONT_BUTTON, relief='flat',
                                command=lambda id_t=task_id: (self.btn_archive_task(id_tarea=id_t)
                                if not tarea.get('archivado')
                                else self.btn_unarchivate_task(id_t)))
        btn_archive.config(state='normal', cursor="hand2")
        btn_archive.pack(side='left', padx=2)


        if not can_delete:
            return

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
            response = TaskController.event_archive_task(id_tarea=id_tarea)
            if response.get('success'):
                messagebox.showinfo(title="Tarea Archivada", message=response.get('response'))
                self.setup_task_display()
            else:
                messagebox.showerror(title="Error", message=f"No se pudo archivar la tarea:\n{response.get('response')}")

    def btn_unarchivate_task(self, id_tarea):

        task = self.find_task_by_id(id_tarea)
        if not task: return
        if messagebox.askyesno(title="Confirmar Desarchivar",
                               message=f"¿Estás seguro de que deseas desarchivar la tarea:\n\n'{task.get('nombre')}'?"):
            response = TaskController.event_unarchive_task(id_tarea=id_tarea)
            if response.get('success'):
                messagebox.showinfo(title="Tarea Desarchivada", message=response.get('response'))
                self.setup_task_display()
            else:
                messagebox.showerror(title="Error",
                                     message=f"No se pudo desarchivar la tarea:\n{response.get('response')}")



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

    def go_to_manage_groups(self):
        ManageGroupsView(root=self.root)

    def refresh_view(self):
        self.setup_task_display()

class EditTaskView:
    def __init__(self, root: RootView, main_view, task_data: dict):
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
            self.main_view.refresh_view()
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
        self.root.create_button(container=action_buttons, name='btnBackToMain', funcion=self.go_to_last_vista, text='Volver', bg='#6C757D', pack_info={'side': 'right', 'expand': True, 'padx': 5, 'ipady':3})

    def btn_add_member(self):
        alias = self.root.componentes.get('inpMemberAlias').get().strip()
        if not alias: return
        if alias in self.miembros_alias:
            messagebox.showwarning(title="Miembro Duplicado", message=f"El usuario '{alias}' ya está en la lista.")
            return
        is_valid, response = GroupController.is_user_exits(alias_usuario=alias)
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
            self.go_to_last_vista()
        else:
            messagebox.showerror(title="Error de Registro de Grupo", message=response)

    def go_to_last_vista(self): ManageGroupsView(root=self.root)

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
        self.current_user_alias = SessionController.get_alias_user() # Use SessionController
        self.master_alias_of_selected_group = None
        self.all_group_members_data = {}  # Stores {alias: rol}
        self.members_to_assign = {} # {alias: {'var': BooleanVar, 'rol': str, 'is_fixed': bool}}
        self.member_display_frames = {}
        self.selected_date = datetime.date.today()
        self.date_display_label = None

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

        labels_texts = ['Nombre de la Tarea:', 'Fecha:', 'Prioridad (1-5):', 'Detalle:']
        inputs_names = ['inpNombreCreateTareaUser', 'inpFechaProgramadaCreateTareaUser', 'inpPrioridadCreateTarea',
                        'inpDetalleCreateTarea']
        for i, text in enumerate(labels_texts):
            tk.Label(form_content_frame, text=text, font=self.root.FONT_LABEL, bg=form_content_frame.cget('bg')).grid(
                row=i, column=0, sticky='nw', pady=5, padx=5)
            if text == 'Detalle:':
                inp = Text(form_content_frame, font=self.root.FONT_BODY, height=6, wrap=tk.WORD, relief='solid',
                           borderwidth=1)
                inp.grid(row=i, column=1, sticky='ew', pady=5, padx=5)
            elif text == 'Fecha:':
                date_frame = tk.Frame(form_content_frame, bg=form_content_frame.cget('bg'))
                date_frame.grid(row=i, column=1, sticky='ew', pady=5, padx=5)
                self.date_display_label = tk.Label(date_frame, text=self.selected_date.strftime('%d-%m-%Y'),
                                                   font=self.root.FONT_BODY, relief='solid', borderwidth=1, anchor='w')
                self.date_display_label.pack(side='left', fill='x', expand=True, ipady=4, padx=(0, 5))
                tk.Button(date_frame, text="📅", command=self.open_calendar, relief='flat').pack(side='left')
                inp = self.date_display_label  # El input "lógico" ahora es el label
            else:
                inp = tk.Entry(form_content_frame, font=self.root.FONT_BODY, relief='solid', borderwidth=1)
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

    def open_calendar(self):
        CalendarPicker(parent=self.root.root, on_date_select_callback=self.on_date_selected)

    def on_date_selected(self, new_date: datetime.date):
        self.selected_date = new_date
        self.date_display_label.config(text=self.selected_date.strftime('%d-%m-%Y'))

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
            if (self.master_alias_of_selected_group and
                    self.master_alias_of_selected_group in self.all_group_members_data):
                self.add_member_to_assign_list(self.master_alias_of_selected_group, True, is_fixed=True)

            # 2. Add Current User (Task Creator) if they are part of the group and not already added as master
            # The fact that they could select this group implies they are master or editor.
            # So, we just need to check if they are in the group's member list and not the master
            # (if master was already added).
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
        fecha = self.selected_date.strftime('%d-%m-%Y')
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

class ManageGroupsView:
    def __init__(self, root: 'RootView'):
        self.root = root
        self.todos_los_grupos, self.current_page, self.groups_per_page, self.total_pages = [], 1, 20, 1
        self.groups_frame, self.pagination_frame = None, None
        self.create_manage_groups_interface()

    def create_manage_groups_interface(self):
        self.root.limpiar_componentes()
        content_frame = tk.Frame(self.root.root, bg=self.root.COLOR_BACKGROUND, padx=20, pady=20)
        content_frame.pack(fill='both', expand=True)
        header_frame = tk.Frame(content_frame, bg=content_frame.cget('bg'))
        header_frame.pack(fill='x', pady=(0, 20))
        tk.Label(header_frame, text="Gestionar Grupos", font=self.root.FONT_TITLE, bg=header_frame.cget('bg')).pack(
            side='left')
        self.root.create_button(container=header_frame, name='btnBackToMain', funcion=self.go_to_main_view,
                                text='← Volver a Tareas', bg='#6C757D',
                                pack_info={'side': 'right', 'padx': 5, 'ipady': 3, 'ipadx': 10})
        self.root.create_button(container=header_frame, name='btnCreateGroup', funcion=self.go_to_create_group,
                                text='✚ Nuevo Grupo', bg=self.root.COLOR_SUCCESS,
                                pack_info={'side': 'right', 'padx': 5, 'ipady': 3, 'ipadx': 10})
        self.groups_frame = tk.Frame(content_frame, bg=content_frame.cget('bg'))
        self.groups_frame.pack(fill='both', expand=True)
        self.pagination_frame = tk.Frame(content_frame, bg=content_frame.cget('bg'))
        self.pagination_frame.pack(fill='x', pady=(10, 0))
        self.setup_groups_display()

    def setup_groups_display(self):
        request = GroupController.get_all_groups_of_session_manager()
        if not request['success']:
            messagebox.showerror(title="Error", message=request['response'])
            self.todos_los_grupos = []
        else:
            self.todos_los_grupos = request['data']['grupos'] or []
        num_groups = len(self.todos_los_grupos)
        self.total_pages = (num_groups + self.groups_per_page - 1) // self.groups_per_page or 1
        self.current_page = 1
        self.display_current_page()
        self.setup_pagination_controls()

    def display_current_page(self):
        for widget in self.groups_frame.winfo_children(): widget.destroy()
        if not self.todos_los_grupos:
            self.root.create_label(container=self.groups_frame, name='lblNoGroups',
                                   text='No perteneces a ningún grupo.', fg='#6C757D',
                                   font_style=("Helvetica", 14, "italic"), pack_info={'pady': 20})
            if self.pagination_frame: self.pagination_frame.pack_forget()
            return

        headers, col_weights = ["Nombre", "Descripción", "Rol", "Acciones"], [2, 5, 2, 3]
        for i, weight in enumerate(col_weights): self.groups_frame.grid_columnconfigure(i, weight=weight)

        header_bg = self.root.COLOR_FRAME
        for i, header in enumerate(headers):
            header_cell = tk.Frame(self.groups_frame, bg=header_bg)
            header_cell.grid(row=0, column=i, sticky='nsew')
            tk.Label(header_cell, text=header, font=self.root.FONT_LABEL, bg=header_bg).pack(padx=5, pady=5, anchor='w')

        start_index = (self.current_page - 1) * self.groups_per_page
        groups_to_display = self.todos_los_grupos[start_index: start_index + self.groups_per_page]
        for i, group_data in enumerate(groups_to_display):
            self.insert_group_row(group=group_data, row_index=i + 1)
        self.update_pagination_controls()

    def insert_group_row(self, group: dict, row_index: int):
        bg_color = self.root.COLOR_BACKGROUND if row_index % 2 != 0 else self.root.COLOR_FRAME
        tk.Label(self.groups_frame, text=group.get('nombre', 'N/A'), bg=bg_color, anchor='w', padx=5, pady=5).grid(
            row=row_index, column=0, sticky='nsew')
        tk.Label(self.groups_frame, text=group.get('descripcion', ''), bg=bg_color, anchor='w', wraplength=450,
                 justify='left', padx=5, pady=5).grid(row=row_index, column=1, sticky='nsew')
        tk.Label(self.groups_frame, text=group.get('rol_usuario', 'N/A').capitalize(), bg=bg_color, anchor='w', padx=5,
                 pady=5).grid(row=row_index, column=2, sticky='nsew')
        actions_frame = tk.Frame(self.groups_frame, bg=bg_color)
        actions_frame.grid(row=row_index, column=3, sticky='nsew', padx=5, pady=5)

        # --- CORRECCIÓN: Botón "Gestionar" habilitado y funcional ---
        tk.Button(actions_frame, text="Gestionar", font=("Helvetica", 9),
                  command=lambda id_g=group.get('id_grupo'): self.go_to_view_group(group_id=id_g)).pack(side='left',
                                                                                                        padx=2)
        tk.Button(actions_frame, text="Salir", state='disabled', font=("Helvetica", 9), bg='#E74C3C', fg='white').pack(
            side='left', padx=2)

    def setup_pagination_controls(self):
        # ... (sin cambios)
        pass

    def update_pagination_controls(self):
        # ... (sin cambios)
        pass

    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.display_current_page()

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.display_current_page()

    def go_to_main_view(self):
        MainView(root=self.root)

    def go_to_create_group(self):
        GroupRegisterView(root=self.root)

    def go_to_view_group(self, group_id: int):
        ViewGroupDetailsView(root=self.root, group_id=group_id)


class ViewGroupDetailsView:
    def __init__(self, root: 'RootView', group_id: int):
        self.root = root
        self.group_id = group_id

        # --- Atributos para la nueva funcionalidad ---
        self.pending_role_changes = {}
        self.member_widgets = {}  # Guarda los widgets de cada miembro para poder modificarlos
        self.save_roles_button = None

        # Datos cargados
        self.group_data, self.user_role, self.members = {}, None, []

        # Estado para tareas y su paginación
        self.tasks_widgets_frame, self.date_display_label = None, None
        self.current_date = datetime.date.today()
        self.all_tasks_for_date = []
        self.task_pagination_frame, self.task_prev_button, self.task_next_button, self.task_page_label = None, None, None, None
        self.current_task_page, self.tasks_per_page, self.total_task_pages = 1, 5, 1

        self.create_view_group_interface()

    def create_view_group_interface(self):
        self.root.limpiar_componentes()
        request = GroupController.get_data_to_view(id_grupo=self.group_id)
        if not request['success']:
            messagebox.showerror("Error al Cargar Grupo", request['response'])
            ManageGroupsView(root=self.root)
            return

        self.group_data = request['data'].get('grupo', {})
        self.user_role = request['data'].get('usuario', {}).get('rol')
        self.members = request['data'].get('miembros', [])
        self.all_tasks_for_date = sorted(request['data'].get('tareas', []) or [], key=lambda t: t.get('prioridad', 99))

        main_frame = tk.Frame(self.root.root, bg=self.root.COLOR_BACKGROUND, padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        group_header_frame = tk.Frame(main_frame, bg=main_frame.cget('bg'))
        group_header_frame.pack(fill='x', pady=(0, 15))
        tk.Label(group_header_frame, text=self.group_data.get('nombre', 'Grupo'), font=self.root.FONT_TITLE,
                 bg=group_header_frame.cget('bg')).pack(anchor='w')
        tk.Label(group_header_frame, text=self.group_data.get('descripcion', ''), font=("Helvetica", 12, "italic"),
                 fg='#566573', bg=group_header_frame.cget('bg'), wraplength=800, justify='left').pack(anchor='w')

        paned_window = ttk.PanedWindow(main_frame, orient='horizontal')
        paned_window.pack(fill='both', expand=True)
        tasks_container = tk.Frame(paned_window, bg=self.root.COLOR_BACKGROUND, padx=10)
        self.create_task_view(parent=tasks_container)
        paned_window.add(tasks_container, weight=3)
        members_container = tk.Frame(paned_window, bg=self.root.COLOR_BACKGROUND, padx=10)
        self.create_members_view(parent=members_container)
        paned_window.add(members_container, weight=1)

        footer_frame = tk.Frame(main_frame, bg=main_frame.cget('bg'), pady=10)
        footer_frame.pack(fill='x')
        self.create_footer_buttons(parent=footer_frame)
        self.setup_task_display()

    def create_members_view(self, parent):
        tk.Label(parent, text="Miembros", font=("Helvetica", 16, "bold"), bg=parent.cget('bg')).pack(anchor='w')
        canvas_frame = tk.Frame(parent);
        canvas_frame.pack(fill='both', expand=True)
        canvas = tk.Canvas(canvas_frame, bg=self.root.COLOR_FRAME, highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.root.COLOR_FRAME)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.member_widgets = {}  # Limpiar widgets de miembros
        for member in self.members:
            self.insert_member_row(scrollable_frame, member)

        # Botón para guardar cambios de roles, inicialmente oculto
        self.save_roles_button = tk.Button(parent, text="Guardar Cambios de Roles", command=self.save_role_changes,
                                           bg=self.root.COLOR_SUCCESS, fg='white')
        # Se mostrará con .pack() cuando sea necesario

    def insert_member_row(self, parent, member):
        alias = member['alias']
        rol = member['rol']

        member_frame = tk.Frame(parent, bg=self.root.COLOR_FRAME, pady=3, padx=5)
        member_frame.pack(fill='x')

        tk.Label(member_frame, text=f"{alias}", font=("Helvetica", 11, "bold"), bg=member_frame.cget('bg')).pack(
            side='left')

        # Contenedor para el widget de rol (Label o OptionMenu)
        role_widget_container = tk.Frame(member_frame, bg=member_frame.cget('bg'))
        role_widget_container.pack(side='left', padx=4)

        role_label = tk.Label(role_widget_container, text=f"({rol.name})", font=("Helvetica", 10),
                              bg=member_frame.cget('bg'))
        role_label.pack()

        # Botón de edición de rol
        edit_button = tk.Button(member_frame, text="Editar Rol", font=("Helvetica", 8),
                                command=lambda a=alias: self.enable_role_editing(a))

        # El master puede editar a todos menos a otros masters y a sí mismo
        can_edit = self.user_role == 'master' and rol != 'master' and alias != SessionController.get_alias_user()
        edit_button.config(state='normal' if can_edit else 'disabled')
        edit_button.pack(side='right')

        # Guardar referencia a los widgets de este miembro
        self.member_widgets[alias] = {'frame': member_frame, 'role_container': role_widget_container,
                                      'edit_button': edit_button}

    def enable_role_editing(self, alias: str):
        widgets = self.member_widgets.get(alias)
        if not widgets: return

        # Ocultar botón de editar para evitar clics múltiples
        widgets['edit_button'].pack_forget()

        # Limpiar el contenedor del widget de rol
        for w in widgets['role_container'].winfo_children():
            w.destroy()

        # Crear y mostrar el OptionMenu
        role_options = ["editor", "miembro"]
        selected_role = tk.StringVar(value=self.pending_role_changes.get(alias, self.get_member_role(alias).name))

        # Asociar el cambio en el menú a nuestro manejador de cambios
        selected_role.trace("w", lambda *args: self.on_role_changed(alias, selected_role))

        option_menu = ttk.OptionMenu(widgets['role_container'], selected_role, selected_role.get(), *role_options)
        option_menu.pack()

        # Mostrar el botón de guardar si es la primera vez que se edita
        if not self.save_roles_button.winfo_ismapped():
            self.save_roles_button.pack(pady=10)

    def on_role_changed(self, alias: str, selected_role_var: tk.StringVar):
        new_role = selected_role_var.get()
        # Actualizar el diccionario de cambios pendientes
        self.pending_role_changes[alias] = new_role

    def save_role_changes(self):
        if not self.pending_role_changes:
            messagebox.showinfo("Sin cambios", "No se ha modificado ningún rol.")
            return
        roles = {'miembro':Rol.miembro, 'editor': Rol.editor}
        lista_de_cambios = [[alias, roles.get(rol)] for alias, rol in self.pending_role_changes.items()]

        request = GroupController.set_rol_members(id_grupo=self.group_id, lista_cambios=lista_de_cambios)

        if request['success']:
            messagebox.showinfo("Éxito", request['response'])
        else:
            # Mostrar un error por cada respuesta fallida
            for error_msg in request['response']:
                messagebox.showerror("Error al Guardar", error_msg)

        # Recargar la vista para reflejar los cambios y salir del modo de edición
        self.create_view_group_interface()

    def get_member_role(self, alias: str):
        """Función auxiliar para obtener el rol actual de un miembro."""
        for member in self.members:
            if member['alias'] == alias:
                return member['rol']
        return ""

    # --- El resto de métodos permanecen sin cambios ---
    def create_task_view(self, parent):
        tk.Label(parent, text="Tareas del Grupo", font=("Helvetica", 16, "bold"), bg=parent.cget('bg')).pack()
        date_control_frame = tk.Frame(parent, bg=parent.cget('bg'))
        date_control_frame.pack(fill='x', pady=5)
        tk.Button(date_control_frame, text="◀", command=self.prev_day, relief='flat', font=("Helvetica", 14),
                  bg=date_control_frame.cget('bg'), cursor="hand2").pack(side='left')
        self.date_display_label = tk.Label(date_control_frame, text="", font=("Helvetica", 11),
                                           bg=date_control_frame.cget('bg'))
        self.date_display_label.pack(side='left', padx=5)
        tk.Button(date_control_frame, text="▶", command=self.next_day, relief='flat', font=("Helvetica", 14),
                  bg=date_control_frame.cget('bg'), cursor="hand2").pack(side='left')
        tk.Button(date_control_frame, text="📅", command=self.open_calendar, relief='flat', font=("Helvetica", 14),
                  bg=date_control_frame.cget('bg'), cursor="hand2").pack(side='left')
        self.tasks_widgets_frame = tk.Frame(parent, bg=parent.cget('bg'))
        self.tasks_widgets_frame.pack(fill='both', expand=True)
        self.task_pagination_frame = tk.Frame(parent, bg=parent.cget('bg'))
        self.task_pagination_frame.pack(fill='x', pady=5)

    def setup_task_display(self):
        self.date_display_label.config(text=self.current_date.strftime('%A, %d de %B').capitalize())
        req = TaskController.get_tasks_of_group_date(fecha=self.current_date, id_grupo=self.group_id)
        self.all_tasks_for_date = sorted(req['data'].get('tareas', []) or [], key=lambda t: t.get('prioridad', 99))
        num_tasks = len(self.all_tasks_for_date)
        self.total_task_pages = (num_tasks + self.tasks_per_page - 1) // self.tasks_per_page or 1
        self.current_task_page = 1
        self.setup_task_pagination_controls()
        self.display_current_task_page()

    def display_current_task_page(self):
        for widget in self.tasks_widgets_frame.winfo_children(): widget.destroy()
        if not self.all_tasks_for_date:
            tk.Label(self.tasks_widgets_frame, text="No hay tareas para esta fecha.", fg='#6C757D',
                     bg=self.tasks_widgets_frame.cget('bg')).pack(pady=20)
        else:
            start_idx = (self.current_task_page - 1) * self.tasks_per_page
            tasks_to_show = self.all_tasks_for_date[start_idx: start_idx + self.tasks_per_page]
            for task in tasks_to_show: self.insert_task_card(tarea=task)
        self.update_task_pagination_controls()

    def insert_task_card(self, tarea: dict):
        task_id = tarea.get('id_tarea')
        task_frame = tk.Frame(self.tasks_widgets_frame, bg=self.root.COLOR_FRAME, relief='solid', borderwidth=1,
                              padx=10, pady=10)
        task_frame.pack(fill='x', pady=5, expand=True)
        info_frame = tk.Frame(task_frame, bg=task_frame.cget('bg'))
        info_frame.pack(side='left', fill='x', expand=True)
        tk.Label(info_frame, text=tarea.get('nombre'), font=("Helvetica", 14, "bold"), bg=info_frame.cget('bg'),
                 fg=self.root.COLOR_TEXT_DARK, anchor='w', justify='left', wraplength=400).pack(fill='x')
        tk.Label(info_frame, text=tarea.get('nombre_prioridad', ''), font=("Helvetica", 10, "italic"),
                 bg=info_frame.cget('bg'), fg=self.root.COLOR_TEXT_DARK, anchor='w').pack(fill='x', pady=(2, 0))
        is_archived = tarea.get('archivado', False)
        if is_archived: tk.Label(info_frame, text="Archivado", font=("Helvetica", 9, "italic"), fg='grey',
                                 bg=info_frame.cget('bg'), anchor='w').pack(fill='x', pady=(5, 0))
        actions_frame = tk.Frame(task_frame, bg=task_frame.cget('bg'))
        actions_frame.pack(side='right', fill='y', padx=(10, 0))
        realizado = tarea.get('realizado', False)
        can_edit = self.user_role in ['master', 'editor'] and tarea.get('disponible')
        can_archive_permission = True
        can_delete = self.user_role == 'master'

        btn_check = tk.Button(actions_frame, text='✔' if realizado else '✖',
                              bg=self.root.COLOR_SUCCESS if realizado else self.root.COLOR_DANGER,
                              fg=self.root.COLOR_TEXT_LIGHT, font=self.root.FONT_BUTTON, relief='flat', width=3,
                              command=lambda id_t=task_id: self.btn_check_task(id_tarea=id_t), cursor="hand2")
        btn_check.config(state='disabled' if is_archived else 'normal')

        btn_check.pack(pady=2, fill='x')
        btn_details = tk.Button(actions_frame, text='Detalle', bg='#17A2B8', fg=self.root.COLOR_TEXT_LIGHT,
                                font=self.root.FONT_BUTTON, relief='flat',
                                command=lambda t=tarea: self.show_task_details(tarea=t), cursor="hand2")
        btn_details.pack(pady=2, fill='x')

        if can_edit:
            btn_edit = tk.Button(actions_frame, text='Editar', bg='#6C757D', fg=self.root.COLOR_TEXT_LIGHT,
                                 font=self.root.FONT_BUTTON, relief='flat',
                                 command=lambda t=tarea: self.btn_edit_task(task_data=t))
            btn_edit.pack(pady=2, fill='x')

        btn_archive_unarchive = tk.Button(actions_frame, font=self.root.FONT_BUTTON, relief='flat',
                                          fg=self.root.COLOR_TEXT_LIGHT)
        if is_archived:
            btn_archive_unarchive.config(text="Desarchivar", bg=self.root.COLOR_SUCCESS,
                                         command=lambda id_t=task_id: self.btn_unarchive_task(id_tarea=id_t),
                                         state='normal' if can_archive_permission else 'disabled',
                                         cursor="hand2" if can_archive_permission else "arrow")
        else:
            btn_archive_unarchive.config(text="Archivar", bg='#5D6D7E',
                                         command=lambda id_t=task_id: self.btn_archive_task(id_tarea=id_t),
                                         state='normal' if can_archive_permission else 'disabled',
                                         cursor="hand2" if can_archive_permission else "arrow")
        btn_archive_unarchive.pack(pady=2, fill='x')
        if not can_edit:
            return
        btn_delete = tk.Button(actions_frame, text='Eliminar', bg=self.root.COLOR_DANGER, fg=self.root.COLOR_TEXT_LIGHT,
                               font=self.root.FONT_BUTTON, relief='flat',
                               command=lambda id_t=task_id: self.btn_delete_task(id_tarea=id_t))
        btn_delete.config(state='normal' if can_delete else 'disabled', cursor="hand2" if can_delete else "arrow")
        btn_delete.pack(pady=2, fill='x')

    def setup_task_pagination_controls(self):
        for widget in self.task_pagination_frame.winfo_children(): widget.destroy()
        self.task_prev_button = tk.Button(self.task_pagination_frame, text="◀", command=self.prev_task_page,
                                          font=self.root.FONT_BUTTON, relief='flat', cursor="hand2")
        self.task_prev_button.pack(side='left')
        self.task_page_label = tk.Label(self.task_pagination_frame, text="", font=("Helvetica", 10),
                                        bg=self.task_pagination_frame.cget('bg'))
        self.task_page_label.pack(side='left', expand=True)
        self.task_next_button = tk.Button(self.task_pagination_frame, text="▶", command=self.next_task_page,
                                          font=self.root.FONT_BUTTON, relief='flat', cursor="hand2")
        self.task_next_button.pack(side='left')
        self.update_task_pagination_controls()

    def update_task_pagination_controls(self):
        if not hasattr(self, 'task_page_label') or not self.task_page_label: return
        if not self.all_tasks_for_date:
            self.task_page_label.config(text="")
            self.task_prev_button.config(state='disabled')
            self.task_next_button.config(state='disabled')
        else:
            self.task_page_label.config(text=f"Pág. {self.current_task_page} de {self.total_task_pages}")
            self.task_prev_button.config(state='normal' if self.current_task_page > 1 else 'disabled')
            self.task_next_button.config(
                state='normal' if self.current_task_page < self.total_task_pages else 'disabled')

    def next_task_page(self):
        if self.current_task_page < self.total_task_pages: self.current_task_page += 1; self.display_current_task_page()

    def prev_task_page(self):
        if self.current_task_page > 1: self.current_task_page -= 1; self.display_current_task_page()

    def create_footer_buttons(self, parent):
        pack_info = {'side': 'right', 'padx': 5, 'ipady': 3, 'ipadx': 10}
        self.root.create_button(container=parent, name='btnBackToGroups', funcion=self.go_to_manage_groups,
                                text='← Volver', bg='#6C757D', pack_info=pack_info)
        if self.user_role == 'master':
            self.root.create_button(container=parent, name='btnAddMember',
                                              funcion=self.open_add_member_window,
                                              text='Agregar Miembro', bg=self.root.COLOR_SUCCESS, pack_info=pack_info)

        if self.user_role in ['master', 'editor']:
            self.root.create_button(container=parent, name='btnCreateTaskForGroup',
                                                      funcion=self.open_create_task_window,
                                                      text='✚ Nueva Tarea', bg=self.root.COLOR_PRIMARY,
                                                      pack_info=pack_info)
        if self.user_role == 'master':
            btn_edit = self.root.create_button(container=parent, name='btnEditGroup',
                                               funcion=lambda: messagebox.showinfo("WIP",
                                                                                   "Funcionalidad para editar grupo no implementada."),
                                               text='Editar Grupo', bg='#5D6D7E', pack_info=pack_info)
            btn_edit.config(state='normal' if self.user_role == 'master' else 'disabled')

    def go_to_manage_groups(self):
        ManageGroupsView(root=self.root)

    def prev_day(self):
        self.current_date -= datetime.timedelta(days=1); self.setup_task_display()

    def next_day(self):
        self.current_date += datetime.timedelta(days=1); self.setup_task_display()

    def open_calendar(self):
        CalendarPicker(parent=self.root.root, on_date_select_callback=self.on_date_selected)

    def on_date_selected(self, new_date):
        if new_date: self.current_date = new_date; self.setup_task_display()

    def find_task_by_id_in_date(self, task_id):
        return next((task for task in self.all_tasks_for_date if task.get('id_tarea') == task_id), None)

    def show_task_details(self, tarea: dict):
        messagebox.showinfo(title=tarea.get('nombre', 'Detalles'),
                            message=tarea.get('detalle') or "No hay detalles para esta tarea.")

    def btn_check_task(self, id_tarea):
        task = self.find_task_by_id_in_date(id_tarea)
        if not task: return
        is_change, response = TaskController.event_check_in_task(id_tarea=id_tarea,
                                                                 realizado=not task.get('realizado', False))
        if is_change:
            self.setup_task_display()
        else:
            messagebox.showerror(title="Error", message=response)

    def btn_edit_task(self, task_data):
        EditTaskView(root=self.root, main_view=self, task_data=task_data)

    def refresh_view(self):
        """Recarga toda la vista para reflejar cambios (como nuevos miembros)."""

        self.create_view_group_interface()

    def btn_archive_task(self, id_tarea):
        if messagebox.askyesno("Confirmar", f"¿Archivar esta tarea?"): messagebox.showinfo("WIP",
                                                                                           "Funcionalidad de archivar no conectada."); self.setup_task_display()

    def btn_unarchive_task(self, id_tarea):
        if messagebox.askyesno("Confirmar", f"¿Desarchivar esta tarea?"): messagebox.showinfo("WIP",
                                                                                              "Funcionalidad de desarchivar no conectada."); self.setup_task_display()

    def btn_delete_task(self, id_tarea):
        if messagebox.askyesno("¡PELIGRO!", f"¿ELIMINAR esta tarea? Esta acción no se puede deshacer.",
                               icon='warning'): messagebox.showinfo("WIP",
                                                                    "Funcionalidad de eliminar no conectada."); self.setup_task_display()

    def open_create_task_window(self):
        """Abre la ventana emergente para crear una tarea para este grupo específico."""
        RegisterTaskForGroupView(
            parent_root_view=self.root,
            parent_view=self,
            group_id=self.group_id,
            group_name=self.group_data.get('nombre', 'Grupo'),
            group_members=self.members
        )

    def open_add_member_window(self):
        """Abre la ventana emergente para agregar nuevos miembros."""
        AddMembersView(
            parent_root_view=self.root,
            parent_view=self,
            group_id=self.group_id,
            current_members=self.members
        )

class AddMembersView(Toplevel):
    def __init__(self, parent_root_view: 'RootView', parent_view: 'ViewGroupDetailsView', group_id: int,
                 current_members: list):
        super().__init__(parent_root_view.root)
        self.root_view = parent_root_view
        self.parent_view = parent_view
        self.group_id = group_id
        self.current_members_aliases = [m['alias'] for m in current_members]

        self.members_to_add = []

        self.title("Agregar Miembros")
        self.config(bg=self.root_view.COLOR_BACKGROUND, padx=20, pady=20)
        self.transient(self.root_view.root)
        self.grab_set()

        self.create_widgets()
        self.root_view.center_window(top_level_window=self)

    def create_widgets(self):
        tk.Label(self, text="Agregar Nuevos Miembros", font=self.root_view.FONT_TITLE, bg=self.cget('bg')).pack(
            pady=(0, 20))

        input_frame = tk.Frame(self, bg=self.cget('bg'))
        input_frame.pack(fill='x')

        self.alias_entry = tk.Entry(input_frame, font=self.root_view.FONT_BODY)
        self.alias_entry.pack(side='left', fill='x', expand=True, ipady=4, padx=(0, 10))

        tk.Button(input_frame, text="Añadir a la lista", command=self.add_member_to_list,
                  bg=self.root_view.COLOR_PRIMARY, fg='white').pack(side='left')

        tk.Label(self, text="Miembros para agregar:", font=self.root_view.FONT_LABEL, bg=self.cget('bg')).pack(
            anchor='w', pady=(15, 5))

        self.members_frame = tk.Frame(self, bg=self.root_view.COLOR_FRAME, relief='sunken', borderwidth=1)
        self.members_frame.pack(fill='both', expand=True, ipady=10)

        self.update_members_display()

        footer_frame = tk.Frame(self, bg=self.cget('bg'))
        footer_frame.pack(fill='x', pady=(20, 0))

        tk.Button(footer_frame, text="Guardar Miembros", command=self.save_new_members, bg=self.root_view.COLOR_SUCCESS,
                  fg='white').pack(side='left', expand=True, padx=5)
        tk.Button(footer_frame, text="Cancelar", command=self.destroy, bg='#6C757D', fg='white').pack(side='right',
                                                                                                      expand=True,
                                                                                                      padx=5)

    def add_member_to_list(self):
        alias = self.alias_entry.get().strip()
        if not alias: return

        if alias in self.members_to_add:
            messagebox.showwarning("Duplicado", f"El usuario '{alias}' ya está en la lista para agregar.", parent=self)
            return

        if alias in self.current_members_aliases:
            messagebox.showerror("Error", f"El usuario '{alias}' ya es miembro de este grupo.", parent=self)
            return

        is_valid, response = GroupController.is_user_exits(alias_usuario=alias)
        if not is_valid:
            messagebox.showerror("Usuario no válido", response, parent=self)
            return

        self.members_to_add.append(alias)
        self.update_members_display()
        self.alias_entry.delete(0, 'end')

    def update_members_display(self):
        for widget in self.members_frame.winfo_children():
            widget.destroy()

        if not self.members_to_add:
            tk.Label(self.members_frame, text="Aún no hay miembros en la lista.", bg=self.members_frame.cget('bg'),
                     fg='grey').pack(pady=10)
            return

        for alias in self.members_to_add:
            row_frame = tk.Frame(self.members_frame, bg=self.members_frame.cget('bg'))
            row_frame.pack(fill='x', padx=10, pady=2)
            tk.Label(row_frame, text=f"• {alias}", bg=row_frame.cget('bg')).pack(side='left')
            tk.Button(row_frame, text="Quitar", command=lambda a=alias: self.remove_member_from_list(a),
                      bg=self.root_view.COLOR_DANGER, fg='white', font=("Helvetica", 8)).pack(side='right')

    def remove_member_from_list(self, alias: str):
        self.members_to_add.remove(alias)
        self.update_members_display()

    def save_new_members(self):
        if not self.members_to_add:
            messagebox.showinfo("Información", "La lista de nuevos miembros está vacía.", parent=self)
            return

        success, response = GroupController.add_members_to_group(id_grupo=self.group_id, miembros=self.members_to_add)

        if success:
            messagebox.showinfo("Éxito", response, parent=self)
            self.parent_view.refresh_view()  # Refrescar la vista anterior
            self.destroy()
        else:
            messagebox.showerror("Error", response, parent=self)


class RegisterTaskForGroupView(Toplevel):
    """
    Ventana emergente para registrar una nueva tarea para un grupo específico.
    Incluye lógica completa para la asignación de miembros.
    """

    def __init__(self, parent_root_view: 'RootView', parent_view: 'ViewGroupDetailsView', group_id: int,
                 group_name: str, group_members: list):
        super().__init__(parent_root_view.root)
        self.root = parent_root_view
        self.parent_view = parent_view
        self.group_id = group_id
        self.group_name = group_name
        # Estado
        self.selected_date = datetime.date.today()
        self.current_user_alias = SessionController.get_alias_user()
        self.all_group_members_data = {m['alias']: m['rol'] for m in group_members}
        self.members_to_assign = {}

        # Widgets
        self.date_display_label = None
        self.assignment_frame = None
        self.members_selection_frame = None
        self.member_combobox = None
        self.selected_members_display_frame = None

        self.title(f"Nueva Tarea para: {self.group_name}")
        self.config(bg=self.root.COLOR_BACKGROUND, padx=20, pady=20)
        self.transient(self.root.root)
        self.grab_set()
        self.minsize(width=1000, height=650)
        self.create_formulate_tarea()
        self.root.center_window(top_level_window=self)

    def create_formulate_tarea(self):
        canvas = tk.Canvas(self, bg=self.cget('bg'), highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        form_content_frame = tk.Frame(canvas, bg=self.cget('bg'))
        form_content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=form_content_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        tk.Label(form_content_frame, text=f"Nueva Tarea para '{self.group_name}'", font=self.root.FONT_TITLE,
                 bg=self.cget('bg')).grid(row=0, column=0, columnspan=2, pady=(0, 15))
        form_content_frame.grid_columnconfigure(1, weight=1)

        labels_texts = ['Nombre de la Tarea:', 'Fecha:', 'Prioridad (1-5):', 'Detalle:']
        self.inputs = {}
        for i, text in enumerate(labels_texts):
            tk.Label(form_content_frame, text=text, font=self.root.FONT_LABEL, bg=self.cget('bg')).grid(row=i + 1,
                                                                                                        column=0,
                                                                                                        sticky='nw',
                                                                                                        pady=5, padx=5)
            key = text.split(' ')[0].lower().replace(':', '')
            if key == 'detalle':
                inp = Text(form_content_frame, font=self.root.FONT_BODY, height=6, wrap=tk.WORD, relief='solid',
                           borderwidth=1)
                inp.grid(row=i + 1, column=1, sticky='ew', pady=5, padx=5)
            elif key == 'fecha':
                date_frame = tk.Frame(form_content_frame, bg=self.cget('bg'))
                date_frame.grid(row=i + 1, column=1, sticky='ew', pady=5, padx=5)
                self.date_display_label = tk.Label(date_frame, text=self.selected_date.strftime('%d-%m-%Y'),
                                                   font=self.root.FONT_BODY, relief='solid', borderwidth=1, anchor='w')
                self.date_display_label.pack(side='left', fill='x', expand=True, ipady=4, padx=(0, 5))
                tk.Button(date_frame, text="📅", command=self.open_calendar, relief='flat').pack(side='left')
                inp = self.date_display_label
            else:
                inp = tk.Entry(form_content_frame, font=self.root.FONT_BODY, relief='solid', borderwidth=1)
                inp.grid(row=i + 1, column=1, sticky='ew', pady=5, padx=5, ipady=4)
            self.inputs[key] = inp

        row_idx = len(labels_texts) + 1

        self.assignment_frame = tk.Frame(form_content_frame, bg=self.cget('bg'))
        self.assignment_frame.grid(row=row_idx, column=0, columnspan=2, sticky='ew', pady=(10, 0));
        row_idx += 1
        self.assignment_type_var = tk.StringVar(value="todos")
        tk.Radiobutton(self.assignment_frame, text="Asignar a todos", variable=self.assignment_type_var, value="todos",
                       bg=self.cget('bg'), command=self.on_assignment_type_changed).pack(side='left')
        tk.Radiobutton(self.assignment_frame, text="Personalizado", variable=self.assignment_type_var,
                       value="personalizado", bg=self.cget('bg'), command=self.on_assignment_type_changed).pack(
            side='left')

        self.members_selection_frame = tk.Frame(form_content_frame, bg=self.cget('bg'))
        self.members_selection_frame.grid(row=row_idx, column=0, columnspan=2, sticky='ew', pady=5);
        row_idx += 1

        tk.Label(self.members_selection_frame, text="Miembros Asignados:", font=self.root.FONT_LABEL,
                 bg=self.cget('bg')).pack(anchor='w')
        self.selected_members_display_frame = tk.Frame(self.members_selection_frame, bg=self.root.COLOR_FRAME,
                                                       relief='sunken', borderwidth=1)
        self.selected_members_display_frame.pack(fill='both', expand=True, pady=(5, 10), ipady=5)

        self.member_combobox = ttk.Combobox(self.members_selection_frame, state='readonly')
        self.member_combobox.pack(fill='x', pady=5)
        self.member_combobox.bind("<<ComboboxSelected>>", self.add_selected_member)
        self.members_selection_frame.grid_remove()

        action_buttons_frame = tk.Frame(form_content_frame, bg=self.cget('bg'))
        action_buttons_frame.grid(row=row_idx, column=0, columnspan=2, pady=(20, 0), sticky='ew')
        tk.Button(action_buttons_frame, text='Guardar Tarea', command=self.btn_registrar_tarea,
                  bg=self.root.COLOR_SUCCESS, fg='white').pack(side='left', expand=True, padx=5, ipady=3)
        tk.Button(action_buttons_frame, text='Cancelar', command=self.destroy, bg='#6C757D', fg='white').pack(
            side='right', expand=True, padx=5, ipady=3)

        self.on_assignment_type_changed()

    def open_calendar(self):
        CalendarPicker(parent=self, on_date_select_callback=self.on_date_selected)

    def on_date_selected(self, new_date: datetime.date):
        self.selected_date = new_date
        self.date_display_label.config(text=self.selected_date.strftime('%d-%m-%Y'))

    def on_assignment_type_changed(self):
        self.members_to_assign.clear()
        if self.assignment_type_var.get() == 'personalizado':
            self.members_selection_frame.grid()
            master_alias = next((alias for alias, rol in self.all_group_members_data.items() if rol == 'master'), None)
            if master_alias:
                self.add_member_to_assignment_list(alias=master_alias, is_fixed=True)
            if self.current_user_alias in self.all_group_members_data and self.current_user_alias != master_alias:
                self.add_member_to_assignment_list(alias=self.current_user_alias, is_fixed=True)
            self.update_members_display()
        else:
            self.members_selection_frame.grid_remove()

    def add_member_to_assignment_list(self, alias: str, is_fixed: bool):
        if alias not in self.members_to_assign:
            self.members_to_assign[alias] = {'var': tk.BooleanVar(value=True), 'is_fixed': is_fixed}

    def update_members_display(self):
        for w in self.selected_members_display_frame.winfo_children(): w.destroy()

        if not self.members_to_assign:
            tk.Label(self.selected_members_display_frame, text="Nadie asignado.",
                     bg=self.selected_members_display_frame.cget('bg')).pack()

        for alias, data in self.members_to_assign.items():
            row = tk.Frame(self.selected_members_display_frame, bg=self.selected_members_display_frame.cget('bg'))
            row.pack(anchor='w', fill='x')

            cb = tk.Checkbutton(row, text=alias, variable=data['var'], bg=row.cget('bg'))
            cb.pack(side='left')

            # --- INICIO DE LA CORRECCIÓN 1: Deshabilitar checkbox si el miembro es fijo ---
            if data.get('is_fixed', False):
                cb.config(state='disabled')
            else:
                # --- INICIO DE LA CORRECCIÓN 2: Añadir botón "Quitar" solo si el miembro NO es fijo ---
                tk.Button(row, text="Quitar", command=lambda a=alias: self.remove_member_from_list(a),
                          bg=self.root.COLOR_DANGER, fg='white', font=("Helvetica", 8), relief='flat').pack(side='left',
                                                                                                            padx=10)

        self.update_member_combobox()

    def remove_member_from_list(self, alias: str):
        if alias in self.members_to_assign:
            del self.members_to_assign[alias]
            self.update_members_display()

    def update_member_combobox(self):
        available = [f"{alias} ({rol})" for alias, rol in self.all_group_members_data.items() if
                     alias not in self.members_to_assign]
        self.member_combobox['values'] = available
        self.member_combobox.set('Añadir miembro...' if available else 'No hay más miembros')

    def add_selected_member(self, event=None):
        selection = self.member_combobox.get()
        if '...' in selection or not selection: return
        alias = selection.split(' (')[0]
        if alias not in self.members_to_assign:
            self.add_member_to_assignment_list(alias=alias, is_fixed=False)
            self.update_members_display()

    def btn_registrar_tarea(self):
        nombre = self.inputs['nombre'].get()
        prioridad_str = self.inputs['prioridad'].get()
        detalle = self.inputs['detalle'].get("1.0", "end-1c")

        is_valid, msg = TaskController.validar_datos(fecha=self.selected_date, prioridad=prioridad_str)
        if not nombre or not is_valid:
            messagebox.showerror("Datos Inválidos",
                                 f"Por favor, corrige los errores:\n- El nombre es obligatorio.\n- {msg}", parent=self)
            return

        fecha_str = self.selected_date.strftime('%d-%m-%Y')
        prioridad = int(prioridad_str)

        miembros_disponible = 'all'
        if self.assignment_type_var.get() == 'personalizado':
            miembros_disponible = [[alias, data['var'].get()] for alias, data in self.members_to_assign.items()]
            if not miembros_disponible:
                messagebox.showerror("Datos incompletos",
                                     "Debe seleccionar al menos un miembro para la asignación personalizada.",
                                     parent=self)
                return

        is_registered, response = TaskController.event_register_task_group(
            id_grupo=self.group_id, nombre=nombre, fecha=fecha_str,
            prioridad=prioridad, detalle=detalle, miembros_disponible=miembros_disponible
        )

        if is_registered:
            messagebox.showinfo("Éxito", response, parent=self)
            self.parent_view.refresh_view()
            self.destroy()
        else:
            messagebox.showerror("Error", response, parent=self)