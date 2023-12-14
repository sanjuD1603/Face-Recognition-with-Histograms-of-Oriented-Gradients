import tkinter as tk
from tkinter import messagebox
import random

class CricketQuizGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cricket Quiz App")

        self.questions = [
            {
                'question': 'Who is known as the "Little Master" in cricket?',
                'options': ['Sachin Tendulkar', 'Virat Kohli', 'Ricky Ponting', 'Brian Lara'],
                'answer': 'Sachin Tendulkar'
            },
            {
                'question': 'Which country has won the most Cricket World Cups?',
                'options': ['India', 'Australia', 'West Indies', 'Pakistan'],
                'answer': 'Australia'
            },
            {
                'question': 'Who is the highest run-scorer in international cricket?',
                'options': ['Sachin Tendulkar', 'Virat Kohli', 'Ricky Ponting', 'Brian Lara'],
                'answer': 'Sachin Tendulkar'
            }
            # Add more questions here
        ]
        self.score = 0
        self.current_question_index = 0

        self.label_question = tk.Label(root, text="", font=("Helvetica", 12))
        self.label_question.pack(pady=10)

        self.radio_var = tk.StringVar()
        self.radio_buttons = []
        for i in range(4):
            radio_button = tk.Radiobutton(root, text="", variable=self.radio_var, value=str(i + 1))
            self.radio_buttons.append(radio_button)
            radio_button.pack(pady=5)

        self.button_next = tk.Button(root, text="Next", command=self.next_question)
        self.button_next.pack(pady=10)

        self.run_quiz()

    def display_question(self, question):
        self.label_question.config(text=question['question'])
        for i, option in enumerate(question['options']):
            self.radio_buttons[i].config(text=option)

    def next_question(self):
        user_answer = self.radio_var.get()
        if user_answer and 1 <= int(user_answer) <= len(self.questions[self.current_question_index]['options']):
            selected_option = self.questions[self.current_question_index]['options'][int(user_answer) - 1]
            if selected_option == self.questions[self.current_question_index]['answer']:
                messagebox.showinfo("Correct", "Correct answer!")
                self.score += 1
            else:
                correct_answer = self.questions[self.current_question_index]['answer']
                messagebox.showinfo("Incorrect", f"Wrong! The correct answer is {correct_answer}")

            self.current_question_index += 1
            if self.current_question_index < len(self.questions):
                self.display_question(self.questions[self.current_question_index])
            else:
                self.show_final_score()
        else:
            messagebox.showwarning("Invalid Input", "Please select a valid option.")

    def show_final_score(self):
        messagebox.showinfo("Quiz Completed", f"Quiz completed! Your final score is {self.score}/{len(self.questions)}.")

    def run_quiz(self):
        random.shuffle(self.questions)
        self.display_question(self.questions[self.current_question_index])

if __name__ == "__main__":
    root = tk.Tk()
    app = CricketQuizGUI(root)
    root.mainloop()
