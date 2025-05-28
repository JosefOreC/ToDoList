"""
    vista
"""
import tkinter as tk
from multiprocessing.spawn import set_executable

from src.controlador.login_controller import LoginController

class RootView:

    componentes = {}

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("600x400")
        self.root.config(bg = 'white')
        self.root.title('TO DO LIST')

    def __comprobate_existe(self, name):
        if componente:=self.componentes.get(name):
            componente.destroy()


    def create_button(self, name:str, funcion, text:str ='', place: [int,int] = 'pack'):
        self.__comprobate_existe(name)
        bt = tk.Button(self.root, text=text, command=funcion)
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

            self.root.create_label(name='login_success', text=response, fg='Green')
        else:
            self.root.create_label(name='login_success', text=f'LOGIN NO EXITOSO: \n{response}', fg='RED')


from src.controlador.register_controller import RegisterUserController

class RegisterUserView:
    def __init__(self, root):
        self.root = root
        self.create_register_interface()

    def create_register_interface(self):
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

