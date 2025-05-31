"""
    vista
"""
import tkinter as tk

from src.controlador.login_controller import LoginController


class RootView:

    componentes = {}

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("600x400")
        self.root.config(bg='white')
        self.root.title('TO DO LIST')


    def __comprobate_existe(self, name):
        if componente := self.componentes.get(name):
            componente.destroy()

    def create_button(self, name: str, funcion, text: str = '', place: [int, int] = 'pack', bg='#f0f0f0', fg='black'):
        self.__comprobate_existe(name)
        bt = tk.Button(self.root, text=text, command=funcion, bg=bg, fg=fg)
        if place == 'pack':
            bt.pack()
        else:
            bt.place(x=place[0], y=place[1])
        self.componentes[name] = bt

    def create_input(self, name, place: [int,int]='pack', secret=False):
        self.__comprobate_existe(name)
        inp = tk.Entry(self.root, show='•' if secret else '')
        if place == 'pack':
            inp.pack()
        else:
            inp.place(x=place[0], y=place[1])

        self.componentes[name] = inp

    def main(self):
        self.root.mainloop()

    def create_label(self, name, text:str='', fg:str='Black', place: [int, int] = 'pack'):
        self.__comprobate_existe(name)
        lbl = tk.Label(self.root, text=text, fg=fg)
        if place == 'pack':
            lbl.pack()
        else:
            lbl.place(x=place[0], y=place[1])

        self.componentes[name] = lbl

    def btn_cambiar_secret_input(self, name_input: str, name_button: str):
        simbolo = '•' if self.componentes.get(name_input).cget('show') == '' else ''
        self.componentes.get(name_input).config(show=simbolo)

        self.componentes.get(name_button).config(text='Mostrar contraseña' if simbolo == '•'
                                                else 'Ocultar contraseña')

    def limpiar_componentes(self):
        for componente in self.componentes:
            self.componentes[componente].destroy()
        self.componentes.clear()

    def btn_change_color(self, name_button:str, bg=None, fg=None):
        try:
            if bg:
                self.componentes.get(name_button).config(bg=bg)
            if fg:
                self.componentes.get(name_button).config(fg=fg)
        except Exception as E:
            return E

class LoginInView:

    def __init__(self, root: RootView):
        self.root = root
        self.create_login()
        self.root.main()

    @staticmethod
    def independent_login():
        root = RootView()
        return LoginInView(root)

    def create_login(self):
        self.root.create_input(name='alias')
        self.root.create_input(name='password', secret=True)
        self.root.create_button(name='btnOcultarPassLogin', text='Mostrar contraseña', funcion=self.btn_mostrar_contrasena)
        self.root.create_button(name='btnLogin', funcion=self.btn_login, text='Login')
        self.root.create_button(name='btnRegistrase', funcion=self.go_to_register, text='Registrarse')

    def go_to_register(self):
        self.root.limpiar_componentes()
        RegisterUserView(root=self.root)

    def btn_mostrar_contrasena(self):
        self.root.btn_cambiar_secret_input(name_input='password', name_button='btnOcultarPassLogin')

    def btn_login(self):
        alias = self.root.componentes.get('alias').get()
        password = self.root.componentes.get('password').get()
        is_login, response = LoginController.login(alias, password)

        if is_login:
            self.root.limpiar_componentes()
            MainView(self.root)
            return
        self.root.create_label(name='login_success', text=f'{response}', fg='RED')


from src.controlador.register_controller import RegisterUserController

class RegisterUserView:
    def __init__(self, root: RootView):
        self.root = root
        self.create_register_interface()

    def create_register_interface(self):
        self.root.create_button(name='btnRegresarLogin', text='Volver', funcion=self.go_to_login)
        self.root.create_label(name='lblNombreRegistro', text='Nombres: ', fg='BLACK')
        self.root.create_input(name='inpNombreRegistro')
        self.root.create_label(name='lblApellidoRegistro', text='Apellidos: ')
        self.root.create_input(name='inpApellidoRegistro')
        self.root.create_label(name='lblAliasRegistro', text='Alias: ')
        self.root.create_input(name='inpAliasRegistro')
        self.root.create_label(name='lblContraseñaRegistro', text='Contraseña: ')
        self.root.create_input(name='inpContraseñaRegistro', secret=True)
        self.root.create_button(name='btnVerContraseñaRegistro', text='Mostrar contraseña',
                                funcion=self.btn_mostrar_contrasena_registro)
        self.root.create_label(name='lblConfirmarContraseñaRegistro', text='Confirmar Contraseña')
        self.root.create_input(name='inpConfirmarContraseñaRegistro', secret=True)
        #self.root.create_button(name='btnVerConfirmarContraseñaRegistro', text='Mostrar contraseña',
        #                        funcion=self.btn_mostrar_contrasena_confirmacion_registro)
        self.root.create_button(name='btnRegistrarUsuario', text='Registrarse', funcion=self.btn_registrar_usuario)

    def btn_mostrar_contrasena_registro(self):
        self.root.btn_cambiar_secret_input(name_input='inpContraseñaRegistro', name_button='btnVerContraseñaRegistro')

    #def btn_mostrar_contrasena_confirmacion_registro(self):
    #    self.root.btn_cambiar_secret_input(name_input='inpConfirmarContraseñaRegistro',
    #                                       name_button='btnVerConfirmarContraseñaRegistro')

    def btn_registrar_usuario(self):
        nombres = self.root.componentes.get('inpNombreRegistro').get()
        apellidos = self.root.componentes.get('inpApellidoRegistro').get()
        alias = self.root.componentes.get('inpAliasRegistro').get()
        password = self.root.componentes.get('inpContraseñaRegistro').get()
        confirm_password = self.root.componentes.get('inpConfirmarContraseñaRegistro').get()
        is_user_save, response = RegisterUserController.register_user(nombres=nombres,
                                             apellidos=apellidos,
                                             alias=alias,
                                             password=password,
                                             confirm_password=confirm_password)

        self.root.create_label(name='lblRegistroSuccess', text=response, fg='Green' if is_user_save else 'Red')

        if is_user_save:
            self.root.create_button(name='btnAceptarRegistro', text='Aceptar', funcion=self.go_to_login)


    def go_to_login(self):
        self.root.limpiar_componentes()
        LoginInView(self.root)

    def go_to_main(self):
        self.root.limpiar_componentes()
        MainView(self.root)

from src.controlador.main_view_controller import MainViewController
class MainView:

    tareas : list

    def __init__(self, root: RootView):
        self.root = root
        self.create_main_interface()

    def create_main_interface(self):
        self.root.create_button(name='btnCrearTarea', text='Crear Tarea', funcion=self.go_to_create_tarea)
        self.root.create_button(name='btnLogOut', text='Deslogearse', funcion=self.go_to_login)
        self.create_tasks_view()

    def delete_tasks_labels_buttons(self):
        for nombre in list(self.root.componentes.keys()):
            if ('lbl' in nombre or 'btn' in nombre) and 'Task' in nombre:
                self.root.componentes.get(nombre).destroy()
                del(self.root.componentes[nombre])

    def create_tasks_view(self):
        self.delete_tasks_labels_buttons()
        is_task_recover, response = MainViewController.recover_task_today_with_format()

        if not is_task_recover:
            self.root.create_label(name='lblNotRecoverTask', text=response, fg='RED')
            return
        self.tareas = response
        if not self.tareas:
            self.root.create_label(name='lblAreNoTasks', text='No hay tareas para hoy :)', fg='Grey')
            return
        self.root.create_label(name='lblTaskData', text='\tNombre\t\tFecha\tPrioridad\tRealizado')
        for tarea in self.tareas:
            self.insert_task_view(tarea)

    def insert_task_view(self, tarea:dict):
        nombrelbl = f'lblTask{tarea.get('id')}'
        nombrebtnedit = f'btnEditTask{tarea.get('id')}'
        nombrebtncomplete = f'btnCheckTask{tarea.get('id')}'
        texto = f'{tarea.get('nombre')} |\t{tarea.get('fecha')}\t|{tarea.get('prioridad')}'
        self.root.create_label(name=nombrelbl, text=texto, fg='Black')
        self.root.create_button(name=nombrebtncomplete, text='Check', bg='Green' if tarea.get('realizado') else 'Red',
                                funcion=lambda:self.btn_check_task(tarea.get('id'), tarea.get('realizado'),
                                                                   self.tareas.index(tarea)))
        self.root.create_button(name=nombrebtnedit, text='Editar Tarea',
                                funcion=lambda:self.btn_edit_task(tarea.get('id'), self.tareas.index(tarea)))

    def btn_edit_task(self, id_task, indice):
        pass

    def btn_check_task(self, id_tarea, realizado, indice):
        print(realizado)
        realizado = not realizado
        is_change_task, response = TaskController.event_update_task_session_manager(id_tarea, realizado=realizado)
        print(realizado, is_change_task, response)
        if not is_change_task:
            return
        self.tareas[indice]['realizado'] = realizado
        self.root.btn_change_color(f'btnCheckTask{id_tarea}', bg='Green' if realizado else 'Red')



    def go_to_create_tarea(self):
        self.root.limpiar_componentes()
        RegisterTareaUserView(self.root)
    def go_to_login(self):
        self.root.limpiar_componentes()
        MainViewController.log_out()
        LoginInView(self.root)

from src.controlador.task_controller import TaskController

class RegisterTareaUserView:
    def __init__(self, root):
        self.root = root
        self.create_fomulate_tarea()

    def create_fomulate_tarea(self):
        self.root.create_button(name='btnVolverCreateTareaUser', text='Volver', funcion=self.btn_volver)
        self.root.create_label(name='lblNombreCreateTareaUser', text='Nombre: ')
        self.root.create_input(name='inpNombreCreateTareaUser')
        self.root.create_label(name='lblFechaProgramadaCreateTareaUser', text='Fecha de accion (dd-mm-aaaa): ')
        self.root.create_input(name='inpFechaProgramadaCreateTareaUser')
        self.root.create_label(name='lblPrioridadCreateTarea', text='Prioridad: ')
        self.root.create_input(name='inpPrioridadCreateTarea')
        self.root.create_button(name='btnRegistrarTareaCreateTarea', text='Registrar Tarea', funcion=self.btn_registrar_tarea)

    def btn_registrar_tarea(self):
        nombre = self.root.componentes.get('inpNombreCreateTareaUser').get()
        fecha = self.root.componentes.get('inpFechaProgramadaCreateTareaUser').get()
        prioridad = self.root.componentes.get('inpPrioridadCreateTarea').get()

        is_regitered_task, response = TaskController.event_register_task_user(nombre=nombre,
                                                                              fecha=fecha,
                                                                              prioridad=prioridad)

        if is_regitered_task:
            self.root.componentes.get('btnRegistrarTareaCreateTarea').config(state='disabled')
            if self.root.componentes.get('lblErrorCreateTarea'):
                self.root.componentes.get('lblErrorCreateTarea').destroy()
                del(self.root.componentes['lblErrorCreateTarea'])
            self.root.create_label(name='lblTareaAñadida', text=response, fg='Green')
            self.root.create_button(name='btnAceptarRegistroCreateTarea', text='Aceptar', funcion = self.btn_aceptar_crear_tarea)
            return

        self.root.create_label(name='lblErrorCreateTarea', text=response, fg='Red')

    def btn_volver(self):
        self.root.limpiar_componentes()
        MainView(self.root)

    def btn_aceptar_crear_tarea(self):
        self.root.limpiar_componentes()
        MainView(self.root)




