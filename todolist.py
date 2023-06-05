import task

if __name__ == '__main__':
    menu = "\n".join(["\n", "1) Today's tasks", "2) Week's tasks", "3) All tasks",
                      "4) Missed tasks", "5) Add a task", "6) Delete a task", "0) Exit", "\n"])
    while (choice := int(input(menu))) != 0:
        task.options[choice]()
    print("Bye!")
