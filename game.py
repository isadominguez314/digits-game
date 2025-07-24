import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import re

def generate_game(difficulty):
    lower_bound = (difficulty - 1) * 100 + 1
    upper_bound = difficulty * 100
    target = random.randint(lower_bound, upper_bound)
    if target < 300:
        numbers = random.sample(range(1, 11), 4) + random.sample(range(11, 21), 2)
    else:
        numbers = random.sample(range(1, 11), 3) + random.sample(range(11, 21), 2) + random.sample(range(21, 31), 1)
    random.shuffle(numbers)
    return numbers, target

def perform_operation(num1, num2, operator):
    if operator == '+':
        return num1 + num2
    elif operator == '-':
        return num1 - num2
    elif operator == '*':
        return num1 * num2
    elif operator == '/' and num2 != 0 and num1 % num2 == 0:
        return num1 // num2
    return None

def update_numbers(numbers, num1, num2, result, history):
    numbers.remove(num1)
    numbers.remove(num2)
    numbers.append(result)
    history.append((num1, num2, result))

def undo_last_operation(numbers, history, update_ui):
    if history:
        num1, num2, result = history.pop()
        numbers.remove(result)
        numbers.extend([num1, num2])
        update_ui()
    else:
        messagebox.showinfo("Info", "No operations to undo.")

class DigitsGameGUI:
    def __init__(self, master):
        self.master = master
        master.title("Digits Game")
        
        # Update target number display style and position
        self.target_label = tk.Label(master, text="", font=('Helvetica', '20'), fg='purple')
        self.target_label.pack(pady=(5, 0))

        self.canvas = tk.Canvas(master, width=400, height=200)
        self.canvas.pack(pady=(5, 0))

        self.prompt_for_difficulty()

        self.entry_operation = tk.Entry(master)
        self.entry_operation.pack(pady=(5, 10))  # Reduce space around the entry box


        self.submit_button = tk.Button(master, text="Submit", command=self.submit)
        self.submit_button.pack(pady=(0, 5))  # Reduce space above the submit button

        self.undo_button = tk.Button(master, text="Undo", command=self.undo)
        self.undo_button.pack(pady=(0, 5))  # Reduce space above the undo button

        self.new_game_button = tk.Button(master, text="New Game", command=self.new_game)
        self.new_game_button.pack(pady=(0, 5))  # Reduce space above the new game button

        self.stop_button = tk.Button(master, text="Stop", command=master.quit)
        self.stop_button.pack(pady=(0, 10))  # Reduce space above the stop button

        master.bind("<Return>", lambda event: self.submit())  # Bind the Enter key to the submit function

    def draw_circles(self):
        self.canvas.delete("all")  # Clear the canvas
        num_circles = len(self.numbers)
        canvas_width = self.canvas.winfo_width()
        spacing = canvas_width // (num_circles + 1)
        for index, number in enumerate(self.numbers):
            x = spacing * (index + 1)  # Calculate x position to center circles
            y = 100  # Vertical position for the circles
            self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, outline="#000", width=2)
            self.canvas.create_text(x, y, text=str(number), font=('Helvetica', '16'))
       
    def prompt_for_difficulty(self):
        self.difficulty = simpledialog.askinteger("Difficulty Level", "Enter a difficulty level (1-10):", minvalue=1, maxvalue=10)
        if not self.difficulty:  # If the user cancels or enters an invalid number, default to 1
            self.difficulty = 1
        self.numbers, self.target = generate_game(self.difficulty)
        self.history = []
        self.target_label.config(text=f"Target: {self.target}")  # Update the target label
        self.draw_circles()

    def update_ui(self):
        self.target_label.config(text=f"Target: {self.target}")  # Ensure target number is updated
        self.draw_circles()
        self.entry_operation.delete(0, tk.END)

    def submit(self, event=None):
        user_input = self.entry_operation.get()
        success, message = self.parse_and_execute_operations(user_input)
        if success:
            self.update_ui()
            if self.numbers[-1] == self.target:
                self.show_new_game_option()
        else:
            messagebox.showinfo("Result", message)

    def show_new_game_option(self):
        # Clear the canvas or adjust it to show new game option in-app
        response = messagebox.askyesno("Congratulations!", "You've reached the target! Would you like to play again?")
        if response:
            self.new_game()
        else:
            self.target_label.config(text="Game Over. Restart to play again.")

    def parse_and_execute_operations(self, user_input):
        tokens = re.split('([+\-*/])', user_input.replace(" ", ""))
        it = iter(tokens)
        try:
            num1 = int(next(it))
            while True:
                operator = next(it)
                num2 = int(next(it))
                if num1 in self.numbers and num2 in self.numbers:
                    result = perform_operation(num1, num2, operator)
                    if result is not None:
                        update_numbers(self.numbers, num1, num2, result, self.history)
                        num1 = result  # Update for the next operation
                        continue
                    else:
                        return False, f"Operation not allowed or doesn't result in an integer."
                else:
                    return False, "Numbers used are not in the current list."
        except StopIteration:
            return True, "Operations completed. Current numbers: " + ", ".join(map(str, self.numbers))
        except ValueError:
            return False, "Invalid input. Please ensure to use valid integers and operators."

    def undo(self):
        undo_last_operation(self.numbers, self.history, self.update_ui)

    def new_game(self):
        self.prompt_for_difficulty()
        self.update_ui()

if __name__ == "__main__":
    root = tk.Tk()
    gui = DigitsGameGUI(root)
    root.mainloop()

