"""
    vista
"""
import tkinter as tk
from importlib.metadata import pass_none

from src.logica.auth_service.login import LoginIn

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


class LoginInView:

    password_ocult = True

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
        self.root.create_button(name='ocult_pass', text='Mostrar contraseña', funcion=self.btn_mostrar_contrasena)
        self.root.create_button(name='btnLogin', funcion=self.btn_login, text='Login')

    def btn_mostrar_contrasena(self):
        self.password_ocult = not self.password_ocult
        if self.password_ocult:
            self.root.componentes.get('ocult_pass').config(text='Mostrar contraseña')
            self.root.componentes.get('password').config(show='•')
            return
        self.root.componentes.get('ocult_pass').config(text='Ocultar contraseña')
        self.root.componentes.get('password').config(show='')


    def btn_login(self):
        alias = self.root.componentes.get('alias').get()
        password = self.root.componentes.get('password').get()
        is_login, response = LoginIn.event_login(alias, password)

        if is_login:

            self.root.create_label(name='login_success', text=response, fg='Green')
        else:
            self.root.create_label(name='login_success', text=f'LOGIN NO EXITOSO: \n{response}', fg='RED')




