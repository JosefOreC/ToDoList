from src.vista.vista import ft, TodoApp

if __name__=='__main__':
    def main(page: ft.Page):
        app = TodoApp(page)
        page.update()


    ft.app(target=main)
