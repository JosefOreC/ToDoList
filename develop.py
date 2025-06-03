from threading import Thread

from src.vista.vista import LoginInView, RootView
from src.modelo.service.task_service.task_service_data import TaskServiceData as tsd
from src.controlador.group_controller import GroupController as GC
import threading



if __name__ == '__main__':


    def develop():
        while (comand := input("test>")) != "exit":
            try:
                exec(comand)
            except Exception as E:
                print(E)


    Thread(target=develop).start()
    LoginInView.independent_login()


