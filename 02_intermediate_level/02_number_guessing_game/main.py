import tkinter as tk 
from random import randint

root = tk.Tk()
root.geometry("500x300")
num = tk.IntVar()

random_num = randint(1, 101)

label = tk.Label(root, text="Welcome to Number Guessing Game", font=("Arial", 16))
label.grid(row=0, column=0, columnspan=3)

def submit():
    global random_num  
    random_num = randint(1, 101)  

    user_num = num.get()
    num.set('')

    
    for widget in root.grid_slaves():
        if int(widget.grid_info()["row"]) in (3, 4):
            widget.destroy()

    if user_num > random_num:
        result_label = tk.Label(root, text="High Guess", font=('calibre', 10, 'bold'))
        result_label.grid(row=3, column=0, columnspan=2)
        comp_label = tk.Label(root, text=f"Computer Guess: {random_num}")
        comp_label.grid(row=4, column=0, columnspan=2)
    elif user_num < random_num:
        result_label = tk.Label(root, text="Low Guess", font=('calibre', 10, 'bold'))
        result_label.grid(row=3, column=0, columnspan=2)
        comp_label = tk.Label(root, text=f"Computer Guess: {random_num}")
        comp_label.grid(row=4, column=0, columnspan=2)
    else:
        result_label = tk.Label(root, text="Congratulations! You guessed right", fg='green', font=('calibre', 12, 'bold'))
        result_label.grid(row=3, column=0, columnspan=2)
        comp_label = tk.Label(root, text=f"Computer Guess: {random_num}")
        comp_label.grid(row=4, column=0, columnspan=2)


name_label = tk.Label(root, text='Enter a number:', font=('calibre', 10, 'bold'))
name_entry = tk.Entry(root, textvariable=num, font=('calibre', 10, 'normal'))

sub_btn = tk.Button(root, text='Submit', command=submit)

name_label.grid(row=1, column=0)
name_entry.grid(row=1, column=1)
sub_btn.grid(row=2, column=1)

root.mainloop()
