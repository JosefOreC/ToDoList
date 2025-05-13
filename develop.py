while (comand := input("test>")) != "exit":
    try:
        exec (comand)
    except Exception as E:
        print(E)

