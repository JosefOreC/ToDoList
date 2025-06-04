import flet as ft
from datetime import datetime
import src.controlador.login_controller as login_controller
import src.controlador.register_controller as register_controller
import src.controlador.main_view_controller as main_view_controller
import src.controlador.task_controller as task_controller
import src.controlador.group_controller as group_controller
import src.controlador.user_controller as user_controller

# Constantes de estilo
COLOR_BACKGROUND = '#FDFEFE'
COLOR_PRIMARY = '#0A79DF'
COLOR_SUCCESS = '#28B463'
COLOR_DANGER = '#E74C3C'
COLOR_WARNING = '#F39C12'
COLOR_INFO = '#17A2B8'
COLOR_TEXT_LIGHT = '#FEFEFE'
COLOR_TEXT_DARK = '#212529'
COLOR_FRAME = '#F2F3F4'


class TodoApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "TO-DO LIST | By Gemini"
        self.page.window_width = 950
        self.page.window_height = 600
        self.page.window_resizable = False
        self.page.bgcolor = COLOR_BACKGROUND
        self.page.padding = 0
        self.page.fonts = {
            "title": "Helvetica Bold",
            "body": "Helvetica",
            "button": "Helvetica Bold",
            "label": "Helvetica Bold"
        }

        self.login_view = LoginView(self)
        self.register_view = RegisterView(self)
        self.main_view = MainView(self)
        self.task_view = TaskView(self)
        self.group_view = GroupView(self)
        self.profile_view = ProfileView(self)

        self.page.on_route_change = self.route_change
        self.page.go('/login')

    def route_change(self, route):
        self.page.views.clear()

        if route.route == "/login":
            self.page.views.append(self.login_view.build())
        elif route.route == "/register":
            self.page.views.append(self.register_view.build())
        elif route.route == "/main":
            self.page.views.append(self.main_view.build())
        elif route.route == "/task":
            self.page.views.append(self.task_view.build())
        elif route.route == "/group":
            self.page.views.append(self.group_view.build())
        elif route.route == "/profile":
            self.page.views.append(self.profile_view.build())

        self.page.update()


class LoginView:
    def __init__(self, app: TodoApp):
        self.app = app
        self.page = app.page
        self.show_password = False

    def build(self):
        self.alias_field = ft.TextField(
            label="Alias de Usuario",
            border_color=COLOR_PRIMARY,
            text_size=14,
            height=50
        )

        self.password_field = ft.TextField(
            label="Contraseña",
            password=not self.show_password,
            can_reveal_password=True,
            border_color=COLOR_PRIMARY,
            text_size=14,
            height=50
        )

        self.error_label = ft.Text(
            color=COLOR_DANGER,
            size=12,
            italic=True
        )

        return ft.View(
            "/login",
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Inicio de Sesión", size=22, weight="bold", color=COLOR_TEXT_DARK),
                            ft.Container(height=20),
                            self.alias_field,
                            self.password_field,
                            ft.ElevatedButton(
                                "Mostrar Contraseña",
                                on_click=self.toggle_password,
                                bgcolor="#6C757D",
                                color=COLOR_TEXT_LIGHT,
                                height=40
                            ),
                            ft.ElevatedButton(
                                "Ingresar",
                                on_click=self.login,
                                bgcolor=COLOR_PRIMARY,
                                color=COLOR_TEXT_LIGHT,
                                height=45
                            ),
                            self.error_label,
                            ft.Row(
                                [
                                    ft.Text("¿No tienes una cuenta?", color=COLOR_TEXT_DARK),
                                    ft.TextButton(
                                        "Regístrate Aquí",
                                        on_click=lambda _: self.page.go("/register"),
                                        style=ft.ButtonStyle(color=COLOR_SUCCESS)
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=40,
                    bgcolor=COLOR_FRAME,
                    border_radius=10,
                    width=400
                )
            ],
            padding=40,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def toggle_password(self, e):
        self.show_password = not self.show_password
        self.password_field.password = not self.show_password
        self.password_field.can_reveal_password = True
        self.page.update()

    def login(self, e):
        alias = self.alias_field.value
        password = self.password_field.value

        is_login, response = login_controller.LoginController.login(alias, password)

        if is_login:
            self.page.go("/main")
        else:
            self.error_label.value = response
            self.page.update()


class RegisterView:
    def __init__(self, app: TodoApp):
        self.app = app
        self.page = app.page
        self.show_password = False
        self.show_confirm_password = False

    def build(self):
        self.nombre_field = ft.TextField(
            label="Nombres",
            border_color=COLOR_PRIMARY,
            text_size=14,
            height=50
        )

        self.apellido_field = ft.TextField(
            label="Apellidos",
            border_color=COLOR_PRIMARY,
            text_size=14,
            height=50
        )

        self.alias_field = ft.TextField(
            label="Alias",
            border_color=COLOR_PRIMARY,
            text_size=14,
            height=50
        )

        self.password_field = ft.TextField(
            label="Contraseña",
            password=not self.show_password,
            can_reveal_password=True,
            border_color=COLOR_PRIMARY,
            text_size=14,
            height=50
        )

        self.confirm_password_field = ft.TextField(
            label="Confirmar Contraseña",
            password=not self.show_confirm_password,
            can_reveal_password=True,
            border_color=COLOR_PRIMARY,
            text_size=14,
            height=50
        )

        self.response_label = ft.Text(
            color=COLOR_SUCCESS,
            size=12,
            italic=True
        )

        return ft.View(
            "/register",
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Crear Cuenta", size=22, weight="bold", color=COLOR_TEXT_DARK),
                            ft.Container(height=20),
                            self.nombre_field,
                            self.apellido_field,
                            self.alias_field,
                            self.password_field,
                            self.confirm_password_field,
                            ft.Row(
                                [
                                    ft.ElevatedButton(
                                        "Mostrar Contraseña",
                                        on_click=lambda _: self.toggle_password("password"),
                                        bgcolor="#6C757D",
                                        color=COLOR_TEXT_LIGHT,
                                        height=40
                                    ),
                                    ft.ElevatedButton(
                                        "Mostrar Confirmación",
                                        on_click=lambda _: self.toggle_password("confirm"),
                                        bgcolor="#6C757D",
                                        color=COLOR_TEXT_LIGHT,
                                        height=40
                                    )
                                ],
                                spacing=10
                            ),
                            ft.ElevatedButton(
                                "Registrarse",
                                on_click=self.register,
                                bgcolor=COLOR_SUCCESS,
                                color=COLOR_TEXT_LIGHT,
                                height=45
                            ),
                            self.response_label,
                            ft.ElevatedButton(
                                "Volver al Inicio",
                                on_click=lambda _: self.page.go("/login"),
                                bgcolor="#6C757D",
                                color=COLOR_TEXT_LIGHT,
                                height=40
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=40,
                    bgcolor=COLOR_FRAME,
                    border_radius=10,
                    width=400
                )
            ],
            padding=40,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def toggle_password(self, field_type):
        if field_type == "password":
            self.show_password = not self.show_password
            self.password_field.password = not self.show_password
        else:
            self.show_confirm_password = not self.show_confirm_password
            self.confirm_password_field.password = not self.show_confirm_password

        self.page.update()

    def register(self, e):
        nombres = self.nombre_field.value
        apellidos = self.apellido_field.value
        alias = self.alias_field.value
        password = self.password_field.value
        confirm_password = self.confirm_password_field.value

        is_user_save, response = register_controller.RegisterUserController.register_user(
            nombres=nombres,
            apellidos=apellidos,
            alias=alias,
            password=password,
            confirm_password=confirm_password
        )

        if is_user_save:
            self.response_label.value = response
            self.response_label.color = COLOR_SUCCESS
            self.page.update()
        else:
            self.response_label.value = response
            self.response_label.color = COLOR_DANGER
            self.page.update()


class MainView:
    def __init__(self, app: TodoApp):
        self.app = app
        self.page = app.page
        self.tasks = []

    def build(self):
        # Header buttons
        header = ft.Row(
            [
                ft.ElevatedButton(
                    "Refrescar 🔄",
                    on_click=self.refresh_tasks,
                    bgcolor=COLOR_INFO,
                    color=COLOR_TEXT_LIGHT,
                    height=40
                ),
                ft.ElevatedButton(
                    "✚ Nueva Tarea",
                    on_click=lambda _: self.page.go("/task"),
                    bgcolor=COLOR_PRIMARY,
                    color=COLOR_TEXT_LIGHT,
                    height=40
                ),
                ft.ElevatedButton(
                    "✚ Nuevo Grupo",
                    on_click=lambda _: self.page.go("/group"),
                    bgcolor=COLOR_SUCCESS,
                    color=COLOR_TEXT_LIGHT,
                    height=40
                ),
                ft.ElevatedButton(
                    "Mi Perfil",
                    on_click=lambda _: self.page.go("/profile"),
                    bgcolor="#6C757D",
                    color=COLOR_TEXT_LIGHT,
                    height=40
                ),
                ft.ElevatedButton(
                    "Cerrar Sesión",
                    on_click=self.logout,
                    bgcolor=COLOR_DANGER,
                    color=COLOR_TEXT_LIGHT,
                    height=40
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            spacing=10,
        )

        # Tasks title
        title = ft.Text("Tareas para Hoy", size=22, weight="bold", color=COLOR_TEXT_DARK)

        # Tasks list container
        self.tasks_container = ft.Column(
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )

        # Load tasks
        self.load_tasks()

        return ft.View(
            "/main",
            [
                header,
                ft.Container(
                    content=ft.Column(
                        [
                            title,
                            ft.Container(height=20),
                            self.tasks_container
                        ],
                        expand=True
                    ),
                    padding=20,
                    expand=True
                )
            ],
            padding=0
        )

    def load_tasks(self):
        self.tasks_container.controls.clear()

        is_task_recover, response = main_view_controller.MainViewController.recover_task_today_with_format()

        if not is_task_recover:
            self.tasks_container.controls.append(
                ft.Text(response, color=COLOR_DANGER)
            )
            return

        self.tasks = response

        if not self.tasks:
            self.tasks_container.controls.append(
                ft.Text("🎉 ¡Felicidades! No hay tareas pendientes para hoy.",
                        color="#6C757D", size=14, italic=True)
            )
            return

        # Create table header
        header_row = ft.DataRow(
            cells=[
                ft.DataCell(ft.Text("Nombre", weight="bold")),
                ft.DataCell(ft.Text("Grupo", weight="bold")),
                ft.DataCell(ft.Text("Fecha", weight="bold")),
                ft.DataCell(ft.Text("Prioridad", weight="bold")),
                ft.DataCell(ft.Text("Acciones", weight="bold"))
            ]
        )

        data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("")),
                ft.DataColumn(ft.Text("")),
                ft.DataColumn(ft.Text("")),
                ft.DataColumn(ft.Text("")),
                ft.DataColumn(ft.Text(""))
            ],
            rows=[header_row]
        )

        for task in self.tasks:
            fecha_obj = task.get('fecha')
            fecha_str = fecha_obj.strftime("%d-%m-%Y") if hasattr(fecha_obj, 'strftime') else fecha_obj

            actions_row = ft.Row(
                [
                    ft.IconButton(
                        icon=ft.Icons.CHECK if task.get('realizado') else ft.Icons.CLOSE,
                        icon_color=COLOR_SUCCESS if task.get('realizado') else COLOR_DANGER,
                        on_click=lambda e, t=task: self.toggle_task_status(t)
                    ),
                    ft.IconButton(
                        icon=ft.Icons.EDIT,
                        icon_color=COLOR_PRIMARY,
                        on_click=lambda e, t=task: self.edit_task(t)
                    ),
                    ft.IconButton(
                        icon=ft.Icons.ARCHIVE,
                        icon_color="#5D6D7E",
                        on_click=lambda e, t=task: self.archive_task(t)
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        icon_color=COLOR_DANGER,
                        on_click=lambda e, t=task: self.delete_task(t)
                    )
                ],
                spacing=5
            )

            data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(task.get('nombre'))),
                        ft.DataCell(ft.Text(task.get('grupo', 'N/A'))),
                        ft.DataCell(ft.Text(fecha_str)),
                        ft.DataCell(ft.Text(f"Prioridad: {task.get('prioridad')}")),
                        ft.DataCell(actions_row)
                    ]
                )
            )

        self.tasks_container.controls.append(data_table)
        self.page.update()

    def toggle_task_status(self, task):
        estado_actual = task['realizado']
        nuevo_estado = not estado_actual
        is_change_task, response = task_controller.TaskController.event_update_task_session_manager(
            id_tarea=task['id'],
            realizado=nuevo_estado
        )

        if is_change_task:
            self.load_tasks()
        else:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error al actualizar la tarea: {response}"))
            self.page.snack_bar.open = True
            self.page.update()

    def edit_task(self, task):
        self.app.task_view.set_task_data(task)
        self.page.go("/task")

    def archive_task(self, task):
        def confirm_archive(e):
            is_archived, response = task_controller.TaskController.event_archive_task(task['id'])
            if is_archived:
                self.load_tasks()
            else:
                self.page.snack_bar = ft.SnackBar(ft.Text(f"No se pudo archivar la tarea: {response}"))
                self.page.snack_bar.open = True
                self.page.update()
            self.page.dialog.open = False
            self.page.update()

        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Confirmar Archivar"),
            content=ft.Text("¿Estás seguro de que deseas archivar esta tarea?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: setattr(self.page.dialog, "open", False)),
                ft.TextButton("Archivar", on_click=confirm_archive)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.dialog.open = True
        self.page.update()

    def delete_task(self, task):
        def confirm_delete(e):
            is_deleted, response = task_controller.TaskController.event_delete_task(task['id'])
            if is_deleted:
                self.load_tasks()
            else:
                self.page.snack_bar = ft.SnackBar(ft.Text(f"No se pudo eliminar la tarea: {response}"))
                self.page.snack_bar.open = True
                self.page.update()
            self.page.dialog.open = False
            self.page.update()

        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Confirmar Eliminación"),
            content=ft.Text(
                "¡ADVERTENCIA!\n\n¿Estás seguro de que deseas eliminar esta tarea?\nEsta acción es definitiva."),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: setattr(self.page.dialog, "open", False)),
                ft.TextButton("Eliminar", on_click=confirm_delete)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.dialog.open = True
        self.page.update()

    def refresh_tasks(self, e):
        self.load_tasks()

    def logout(self, e):
        main_view_controller.MainViewController.log_out()
        self.page.go("/login")


class TaskView:
    def __init__(self, app: TodoApp):
        self.app = app
        self.page = app.page
        self.task_data = None
        self.is_edit_mode = False

    def set_task_data(self, task_data):
        self.task_data = task_data
        self.is_edit_mode = True

    def build(self):
        self.nombre_field = ft.TextField(
            label="Nombre de la Tarea",
            border_color=COLOR_PRIMARY,
            text_size=14,
            height=50
        )

        self.fecha_field = ft.TextField(
            label="Fecha (dd-mm-aaaa)",
            border_color=COLOR_PRIMARY,
            text_size=14,
            height=50
        )

        self.prioridad_field = ft.TextField(
            label="Prioridad (1-5)",
            border_color=COLOR_PRIMARY,
            text_size=14,
            height=50
        )

        self.detalle_field = ft.TextField(
            label="Detalle",
            border_color=COLOR_PRIMARY,
            text_size=14,
            height=50,
            multiline=True,
            min_lines=3,
            max_lines=5
        )

        self.response_label = ft.Text(
            color=COLOR_SUCCESS,
            size=12,
            italic=True
        )

        if self.is_edit_mode and self.task_data:
            self.nombre_field.value = self.task_data.get('nombre', '')

            fecha_obj = self.task_data.get('fecha')
            if hasattr(fecha_obj, 'strftime'):
                self.fecha_field.value = fecha_obj.strftime("%d-%m-%Y")
            else:
                self.fecha_field.value = str(fecha_obj)

            self.prioridad_field.value = str(self.task_data.get('prioridad', ''))
            self.detalle_field.value = self.task_data.get('detalle', '')

        return ft.View(
            "/task",
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                "Editar Tarea" if self.is_edit_mode else "Registrar Nueva Tarea",
                                size=22,
                                weight="bold",
                                color=COLOR_TEXT_DARK
                            ),
                            ft.Container(height=20),
                            self.nombre_field,
                            self.fecha_field,
                            self.prioridad_field,
                            self.detalle_field,
                            ft.ElevatedButton(
                                "Guardar" if self.is_edit_mode else "Registrar Tarea",
                                on_click=self.save_task,
                                bgcolor=COLOR_SUCCESS,
                                color=COLOR_TEXT_LIGHT,
                                height=45
                            ),
                            self.response_label,
                            ft.ElevatedButton(
                                "Volver",
                                on_click=lambda _: self.page.go("/main"),
                                bgcolor="#6C757D",
                                color=COLOR_TEXT_LIGHT,
                                height=40
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=40,
                    bgcolor=COLOR_FRAME,
                    border_radius=10,
                    width=500
                )
            ],
            padding=40,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def save_task(self, e):
        nombre = self.nombre_field.value
        fecha = self.fecha_field.value
        prioridad = self.prioridad_field.value
        detalle = self.detalle_field.value

        if self.is_edit_mode:
            is_updated, response = task_controller.TaskController.event_update_task_session_manager(
                id_tarea=self.task_data.get('id'),
                nombre=nombre,
                fecha=fecha,
                prioridad=prioridad,
                detalle=detalle
            )

            if is_updated:
                self.response_label.value = response
                self.response_label.color = COLOR_SUCCESS
                self.page.update()
                self.page.go("/main")
            else:
                self.response_label.value = response
                self.response_label.color = COLOR_DANGER
                self.page.update()
        else:
            is_registered_task, response = task_controller.TaskController.event_register_task_user(
                nombre=nombre,
                fecha=fecha,
                prioridad=prioridad,
                detalle=detalle
            )

            if is_registered_task:
                self.response_label.value = response
                self.response_label.color = COLOR_SUCCESS
                self.page.update()
                self.page.go("/main")
            else:
                self.response_label.value = response
                self.response_label.color = COLOR_DANGER
                self.page.update()


class GroupView:
    def __init__(self, app: TodoApp):
        self.app = app
        self.page = app.page
        self.miembros_alias = []

    def build(self):
        self.nombre_field = ft.TextField(
            label="Nombre del Grupo",
            border_color=COLOR_PRIMARY,
            text_size=14,
            height=50
        )

        self.descripcion_field = ft.TextField(
            label="Descripción (Opcional)",
            border_color=COLOR_PRIMARY,
            text_size=14,
            height=50
        )

        self.member_alias_field = ft.TextField(
            label="Alias del Miembro",
            border_color=COLOR_PRIMARY,
            text_size=14,
            height=50,
            on_change=self.clear_member_error
        )

        self.member_error_label = ft.Text(
            color=COLOR_DANGER,
            size=12,
            italic=True
        )

        self.members_list = ft.Column(
            spacing=5,
            scroll=ft.ScrollMode.AUTO,
            height=150
        )

        self.update_members_display()

        self.response_label = ft.Text(
            color=COLOR_SUCCESS,
            size=12,
            italic=True
        )

        return ft.View(
            "/group",
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Registrar Nuevo Grupo", size=22, weight="bold", color=COLOR_TEXT_DARK),
                            ft.Container(height=20),
                            self.nombre_field,
                            self.descripcion_field,
                            ft.Text("Añadir Miembros (por alias):", size=14, weight="bold", color=COLOR_TEXT_DARK),
                            ft.Row(
                                [
                                    self.member_alias_field,
                                    ft.ElevatedButton(
                                        "Añadir Miembro",
                                        on_click=self.add_member,
                                        bgcolor=COLOR_PRIMARY,
                                        color=COLOR_TEXT_LIGHT,
                                        height=40
                                    )
                                ],
                                spacing=10
                            ),
                            self.member_error_label,
                            ft.Text("Miembros a Agregar:", size=14, weight="bold", color=COLOR_TEXT_DARK),
                            ft.Container(
                                content=self.members_list,
                                bgcolor=COLOR_BACKGROUND,
                                border=ft.border.all(1, "#DEE2E6"),
                                padding=10,
                                border_radius=5
                            ),
                            ft.ElevatedButton(
                                "Guardar Grupo",
                                on_click=self.save_group,
                                bgcolor=COLOR_SUCCESS,
                                color=COLOR_TEXT_LIGHT,
                                height=45
                            ),
                            self.response_label,
                            ft.ElevatedButton(
                                "Volver",
                                on_click=lambda _: self.page.go("/main"),
                                bgcolor="#6C757D",
                                color=COLOR_TEXT_LIGHT,
                                height=40
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=40,
                    bgcolor=COLOR_FRAME,
                    border_radius=10,
                    width=500
                )
            ],
            padding=40,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def add_member(self, e):
        alias = self.member_alias_field.value.strip()
        if not alias:
            return

        if alias in self.miembros_alias:
            self.member_error_label.value = f"El usuario '{alias}' ya está en la lista."
            self.page.update()
            return

        is_valid, _ = group_controller.GroupController.is_user_exits(alias)
        if is_valid:
            self.miembros_alias.append(alias)
            self.update_members_display()
            self.member_alias_field.value = ""
            self.clear_member_error()
            self.page.update()
        else:
            self.member_error_label.value = f"Error: El usuario con alias '{alias}' no existe."
            self.page.update()

    def update_members_display(self):
        self.members_list.controls.clear()

        if not self.miembros_alias:
            self.members_list.controls.append(
                ft.Text("No hay miembros agregados.", color="#6C757D")
            )
            return

        for alias in self.miembros_alias:
            row = ft.Row(
                [
                    ft.Text(f"• {alias}"),
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        icon_color=COLOR_DANGER,
                        on_click=lambda e, a=alias: self.remove_member(a),
                        icon_size=20
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
            self.members_list.controls.append(row)

        self.page.update()

    def remove_member(self, alias):
        if alias in self.miembros_alias:
            self.miembros_alias.remove(alias)
            self.update_members_display()

    def clear_member_error(self, e=None):
        self.member_error_label.value = ""
        self.page.update()

    def save_group(self, e):
        nombre = self.nombre_field.value
        descripcion = self.descripcion_field.value

        is_registered, response = group_controller.GroupController.register_group(
            nombre=nombre,
            descripcion=descripcion,
            miembros_alias=self.miembros_alias
        )

        if is_registered:
            self.response_label.value = response
            self.response_label.color = COLOR_SUCCESS
            self.page.update()
            self.page.go("/main")
        else:
            self.response_label.value = response
            self.response_label.color = COLOR_DANGER
            self.page.update()


class ProfileView:
    def __init__(self, app: TodoApp):
        self.app = app
        self.page = app.page

    def build(self):
        current_user_data = user_controller.UserController.get_data_session_manager()

        self.nombre_field = ft.TextField(
            label="Nombres",
            border_color=COLOR_PRIMARY,
            text_size=14,
            height=50,
            value=current_user_data.get('nombres', '')
        )

        self.apellido_field = ft.TextField(
            label="Apellidos",
            border_color=COLOR_PRIMARY,
            text_size=14,
            height=50,
            value=current_user_data.get('apellidos', '')
        )

        self.alias_field = ft.TextField(
            label="Alias",
            border_color=COLOR_PRIMARY,
            text_size=14,
            height=50,
            value=current_user_data.get('alias', '')
        )

        self.password_field = ft.TextField(
            label="Nueva Contraseña (opcional)",
            password=True,
            can_reveal_password=True,
            border_color=COLOR_PRIMARY,
            text_size=14,
            height=50
        )

        self.response_label = ft.Text(
            color=COLOR_SUCCESS,
            size=12,
            italic=True
        )

        return ft.View(
            "/profile",
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Actualizar Mi Perfil", size=22, weight="bold", color=COLOR_TEXT_DARK),
                            ft.Container(height=20),
                            self.nombre_field,
                            self.apellido_field,
                            self.alias_field,
                            self.password_field,
                            ft.ElevatedButton(
                                "Guardar Cambios",
                                on_click=self.update_profile,
                                bgcolor=COLOR_SUCCESS,
                                color=COLOR_TEXT_LIGHT,
                                height=45
                            ),
                            self.response_label,
                            ft.ElevatedButton(
                                "Volver",
                                on_click=lambda _: self.page.go("/main"),
                                bgcolor="#6C757D",
                                color=COLOR_TEXT_LIGHT,
                                height=40
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=40,
                    bgcolor=COLOR_FRAME,
                    border_radius=10,
                    width=400
                )
            ],
            padding=40,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def update_profile(self, e):
        nombres = self.nombre_field.value
        apellidos = self.apellido_field.value
        alias = self.alias_field.value
        password = self.password_field.value

        is_updated, response = user_controller.UserController.event_update_user(
            nombres=nombres,
            apellidos=apellidos,
            alias=alias,
            password=password if password else None
        )

        if is_updated:
            self.response_label.value = response
            self.response_label.color = COLOR_SUCCESS
            self.page.update()
            self.page.go("/main")
        else:
            self.response_label.value = response
            self.response_label.color = COLOR_DANGER
            self.page.update()


def main(page: ft.Page):
    app = TodoApp(page)
    page.update()

if __name__=='__main__':
    ft.app(target=main)