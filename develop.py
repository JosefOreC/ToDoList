from threading import Thread

from src.vista.vista import LoginInView, RootView
from src.modelo.service.task_service.task_service_data import TaskServiceData as tsd
from src.controlador.group_controller import GroupController as GC
import threading
from src.modelo.service.group_service.group_service_data import GroupServiceData as gsd
from src.controlador.task_controller import TaskController as TS
from src.controlador.group_finder_controller import GroupFinderController
from src.controlador.task_finder_controller import TaskFinderController as TFC
from src.controlador.task_finder_controller import  TaskFinder as TF
from src.controlador.login_controller import LoginController

if __name__ == '__main__':

    LoginController.login('admin','admin')

    while (comand := input("test>")) != "exit":
        try:
            exec(comand)
        except Exception as E:
            print(E)


    #Thread(target=develop).start()
    #LoginInView.independent_login()


