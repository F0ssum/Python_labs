import tkinter as tk
from tkinter import messagebox
import re

class Calc:
    def __init__(self):
        # Операции
        self.ops = {
            "+": lambda x, y: x + y,  
            "-": lambda x, y: x - y, 
            "*": lambda x, y: x * y,  
            "/": lambda x, y: x / y,  
            "^": lambda x, y: x**y,   
        }
        # Приоритеты
        self.prior = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}

    def to_rpn(self, expr):
        expr = re.sub(r"([+\-*/^])", r" \1 ", expr)
        tokens = expr.split()
        out = []
        stack = []
        for t in tokens:
            if t in self.ops:
                while stack and self.prior.get(stack[-1], 0) >= self.prior[t]:
                    out.append(stack.pop())
                stack.append(t)
            else:
                out.append(float(t))
        while stack:
            out.append(stack.pop())
        return out

    def calc_rpn(self, rpn):
        stack = []
        for t in rpn:
            if isinstance(t, float):
                stack.append(t)
            else:
                y = stack.pop()
                x = stack.pop()
                stack.append(self.ops[t](x, y))
        return stack[0]

    def calculate(self, expr):

        try:
            rpn = self.to_rpn(expr)
            return self.calc_rpn(rpn)
        except:
            return "Ошибка!"

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор")
        self.calc = Calc()
        self.make_gui()

    def make_gui(self):
        self.entry = tk.Entry(self.root)
        self.entry.grid(row=0, column=0, columnspan=4, padx=5, pady=5)
        self.entry.insert(0, "")

        buttons = [
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
            ("0", 4, 0), (".", 4, 1), ("+", 4, 2), ("^", 4, 3),
        ]

        # Добавляем кнопки
        for text, row, col in buttons:
            btn = tk.Button(self.root, text=text, command=lambda x=text: self.click(x))
            btn.grid(row=row, column=col, padx=5, pady=5)

        eq_btn = tk.Button(self.root, text="=", command=lambda: self.click("="))
        eq_btn.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        clear_btn = tk.Button(self.root, text="C", command=lambda: self.click("C"))
        clear_btn.grid(row=5, column=2, columnspan=2, padx=5, pady=5)

    def click(self, char):
        if char == "=":
            expr = self.entry.get()
            if expr:
                result = self.calc.calculate(expr)
                self.entry.delete(0, tk.END)
                if isinstance(result, str):
                    messagebox.showerror("Ошибка", result)
                else:
                    self.entry.insert(0, str(result))
        elif char == "C":
            self.entry.delete(0, tk.END)
            self.entry.insert(0, "")
        else:
            current = self.entry.get()
            self.entry.delete(0, tk.END)
            self.entry.insert(0, current + char)

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()