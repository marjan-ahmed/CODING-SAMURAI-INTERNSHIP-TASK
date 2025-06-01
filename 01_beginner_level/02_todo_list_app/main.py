tasks = []

print("Welcome to To-Do List Application".center(50))

def main():
    while (True):
        print(
            """\n Operations:-
                1: Add Task
                2: Delete Task
                3: View Task
                4: Update Task 
                5: Exit
            """
        )
        user_opr = int(input("Which operation would you like to perform (1,2,3,4,5): "))

        if user_opr == 1:
            input_task = input("Enter task to add: ")
            tasks.append(input_task)
            
        elif user_opr == 2:
            if len(tasks) > 0:
                del_task = input("Enter a task to remove: ")
                tasks.remove(del_task)
            else:
                print("No task available to remove")
            
        elif user_opr == 3:
            if len(tasks) > 0:
                print(tasks)
            else:
                print("No task available to view")
        
        elif user_opr == 4:
            if len(tasks) > 0:
                replaced_task = input("Which task would you update: ")
                updated_task = input("Enter your updated task: ")
                replaced_task_index = tasks.index(replaced_task)
                tasks.remove(replaced_task)
                tasks.insert(replaced_task_index, updated_task)
            else:
                print("No tasks available to update")
                
        elif user_opr == 5:
            break

        else:
            print("Invalid Operation")
            
if __name__ == '__main__':
    main()