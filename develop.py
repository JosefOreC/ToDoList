from src.vista.vista import LoginInView
from src.modelo.service.task_service.task_service_data import TaskServiceData as tsd

if __name__ == '__main__':
    LoginInView.independent_login()

while (comand := input("test>")) != "exit":
    try:
        exec(comand)
    except Exception as E:
        print(E)

