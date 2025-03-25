from tkinter import *
from tkinter import messagebox, ttk
import math
import re

class EnhancedCalculator:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.create_variables()
        self.create_widgets()
        self.setup_layout()
        self.load_history()
        self.setup_bindings()
        
    def setup_window(self):
        self.root.title("Enhanced Calculator")
        self.root.geometry("600x850+100+100")
        self.root.minsize(500, 700)
        self.root.configure(bg="#1e1e1e")
        
        # Set window icon (replace with actual icon path if available)
        try:
            self.root.iconbitmap('calculator.ico')
        except:
            pass
        
    def create_variables(self):
        self.scientific_mode = False
        self.angle_mode = StringVar(value="DEG")
        self.memory = [""]
        self.current_theme = "dark"
        self.history = []
        
    def create_widgets(self):
        # Font styles
        self.display_font = ("Segoe UI", 32)
        self.button_font = ("Segoe UI", 18)
        self.small_button_font = ("Segoe UI", 12)
        
        # Main display
        self.display = Entry(self.root, font=self.display_font, bd=0, 
                           bg="#2a2d36", fg="white", justify=RIGHT, 
                           insertbackground="white")
        self.display.pack(fill=X, padx=10, pady=(20, 10), ipady=10)
        
        # Memory and angle indicators
        self.indicator_frame = Frame(self.root, bg="#1e1e1e")
        self.indicator_frame.pack(fill=X, padx=10)
        
        self.memory_indicator = Label(self.indicator_frame, text="", 
                                    font=("Segoe UI", 12), bg="#1e1e1e", 
                                    fg="#ff5555")
        self.memory_indicator.pack(side=LEFT)
        
        self.angle_mode_label = Label(self.indicator_frame, 
                                    textvariable=self.angle_mode, 
                                    font=("Segoe UI", 12), bg="#1e1e1e", 
                                    fg="#aaaaaa")
        self.angle_mode_label.pack(side=RIGHT)
        
        # History panel
        self.history_frame = LabelFrame(self.root, text="History", 
                                       font=("Segoe UI", 12), bg="#1e1e1e", 
                                       fg="white", bd=2, relief=GROOVE)
        self.history_frame.pack(fill=BOTH, padx=10, pady=10, expand=True)
        
        self.history_list = Listbox(self.history_frame, font=("Segoe UI", 12), 
                                  bg="#2a2d36", fg="white", selectbackground="#555555", 
                                  selectforeground="white", bd=0)
        self.history_list.pack(fill=BOTH, expand=True, padx=5, pady=5)
        
        self.history_scrollbar = ttk.Scrollbar(self.history_list, 
                                             orient=VERTICAL, 
                                             command=self.history_list.yview)
        self.history_list.config(yscrollcommand=self.history_scrollbar.set)
        self.history_scrollbar.pack(side=RIGHT, fill=Y)
        
        # Button frames
        self.main_button_frame = Frame(self.root, bg="#1e1e1e")
        self.main_button_frame.pack(fill=BOTH, expand=True, padx=10, pady=(0, 10))
        
        self.sci_button_frame = Frame(self.root, bg="#1e1e1e", bd=0)
        
        # Create buttons
        self.create_buttons()
        
    def create_buttons(self):
        # Main buttons
        button_layout = [
            ("C", 0, 0, 1, "red"), ("⌫", 0, 1, 1, "red"), ("%", 0, 2, 1, "blue"), ("/", 0, 3, 1, "blue"),
            ("7", 1, 0, 1), ("8", 1, 1, 1), ("9", 1, 2, 1), ("*", 1, 3, 1, "blue"),
            ("4", 2, 0, 1), ("5", 2, 1, 1), ("6", 2, 2, 1), ("-", 2, 3, 1, "blue"),
            ("1", 3, 0, 1), ("2", 3, 1, 1), ("3", 3, 2, 1), ("+", 3, 3, 1, "blue"),
            ("0", 4, 0, 2), (".", 4, 2, 1), ("=", 4, 3, 1, "green")
        ]
        
        self.main_buttons = []
        for btn in button_layout:
            text, row, col, col_span = btn[:4]
            color = btn[4] if len(btn) > 4 else None
            
            btn = Button(self.main_button_frame, text=text, font=self.button_font,
                        bd=0, relief=RAISED, command=lambda t=text: self.on_button_click(t))
            self.style_button(btn, color)
            
            self.main_buttons.append((btn, row, col, col_span))
        
        # Scientific buttons
        sci_button_layout = [
            ("sin", 0, 0, 1), ("cos", 0, 1, 1), ("tan", 0, 2, 1),
            ("log", 1, 0, 1), ("ln", 1, 1, 1), ("π", 1, 2, 1),
            ("x²", 2, 0, 1), ("√", 2, 1, 1), ("x^y", 2, 2, 1),
            ("(", 3, 0, 1), (")", 3, 1, 1), ("EXP", 3, 2, 1),
            ("DEG/RAD", 4, 0, 2), ("Theme", 4, 2, 1)
        ]
        
        self.sci_buttons = []
        for btn in sci_button_layout:
            text, row, col, col_span = btn[:4]
            
            btn = Button(self.sci_button_frame, text=text, font=self.small_button_font,
                        bd=0, relief=RAISED, command=lambda t=text: self.on_button_click(t))
            self.style_button(btn)
            
            self.sci_buttons.append((btn, row, col, col_span))
        
        # Memory buttons
        self.memory_frame = Frame(self.root, bg="#1e1e1e")
        self.memory_frame.pack(fill=X, padx=10, pady=(0, 10))
        
        memory_buttons = [
            ("MC", "red"), ("MR", "blue"), ("M+", "green"), ("MS", "blue")
        ]
        
        self.memory_btns = []
        for text, color in memory_buttons:
            btn = Button(self.memory_frame, text=text, font=self.small_button_font,
                       bd=0, command=lambda t=text: self.on_button_click(t))
            self.style_button(btn, color)
            btn.pack(side=LEFT, expand=True, fill=X, padx=2)
            self.memory_btns.append(btn)
    
    def style_button(self, button, color=None):
        if color == "red":
            button.configure(bg="#ff6b6b", activebackground="#ff5252", fg="white")
        elif color == "blue":
            button.configure(bg="#4ecdc4", activebackground="#48b9b1", fg="white")
        elif color == "green":
            button.configure(bg="#51cf66", activebackground="#40c057", fg="white")
        else:
            button.configure(bg="#3a3f4b", activebackground="#4a4f5b", fg="white")
        
        button.bind("<Enter>", lambda e, b=button: b.config(bg=b.cget("activebackground")))
        button.bind("<Leave>", lambda e, b=button: b.config(bg=b.cget("bg")))
    
    def setup_layout(self):
        # Configure grid for main buttons
        for i in range(5):
            self.main_button_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.main_button_frame.grid_columnconfigure(i, weight=1)
        
        # Place main buttons
        for btn, row, col, col_span in self.main_buttons:
            btn.grid(row=row, column=col, columnspan=col_span, 
                    sticky="nsew", padx=2, pady=2)
        
        # Configure grid for scientific buttons
        for i in range(5):
            self.sci_button_frame.grid_rowconfigure(i, weight=1)
        for i in range(3):
            self.sci_button_frame.grid_columnconfigure(i, weight=1)
        
        # Place scientific buttons
        for btn, row, col, col_span in self.sci_buttons:
            btn.grid(row=row, column=col, columnspan=col_span, 
                    sticky="nsew", padx=2, pady=2)
    
    def setup_bindings(self):
        self.root.bind("<Key>", self.on_key_press)
        self.root.bind("<Configure>", self.on_window_resize)
        
        # Bind history list double-click
        self.history_list.bind("<Double-Button-1>", self.on_history_select)
    
    def on_window_resize(self, event):
        # Adjust layout based on window size
        if self.scientific_mode:
            self.adjust_scientific_layout()
    
    def adjust_scientific_layout(self):
        # Adjust layout when in scientific mode
        pass
    
    def on_button_click(self, text):
        current_text = self.display.get()
        
        if text == "=":
            self.calculate_result()
        elif text == "C":
            self.display.delete(0, END)
        elif text == "⌫":
            self.display.delete(len(current_text)-1, END)
        elif text == "√":
            self.display.delete(0, END)
            self.display.insert(0, "sqrt(")
        elif text == "x²":
            self.display.insert(END, "**2")
        elif text == "x^y":
            self.display.insert(END, "**")
        elif text == "MS":
            self.memory[0] = current_text
            self.update_memory_indicator()
        elif text == "MR":
            if self.memory[0]:
                self.display.insert(END, self.memory[0])
        elif text == "MC":
            self.memory[0] = ""
            self.update_memory_indicator()
        elif text == "M+":
            try:
                self.memory[0] = str(eval(f"{self.memory[0]}+{current_text}"))
                self.update_memory_indicator()
            except:
                self.display.delete(0, END)
                self.display.insert(0, "Error")
        elif text == "sin":
            self.display.insert(END, "sin(")
        elif text == "cos":
            self.display.insert(END, "cos(")
        elif text == "tan":
            self.display.insert(END, "tan(")
        elif text == "log":
            self.display.insert(END, "log10(")
        elif text == "ln":
            self.display.insert(END, "log(")
        elif text == "π":
            self.display.insert(END, str(math.pi))
        elif text == "e":
            self.display.insert(END, str(math.e))
        elif text == "DEG/RAD":
            self.toggle_angle_mode()
        elif text == "EXP":
            self.display.insert(END, "e+")
        elif text == "Theme":
            self.toggle_theme()
        else:
            self.display.insert(END, text)
    
    def calculate_result(self):
        try:
            expression = self.display.get()
            if not expression:
                return
                
            # Replace special functions and constants
            expression = expression.replace("sqrt(", "math.sqrt(")
            expression = expression.replace("sin(", f"math.sin({'math.radians(' if self.angle_mode.get() == 'DEG' else ''}")
            expression = expression.replace("cos(", f"math.cos({'math.radians(' if self.angle_mode.get() == 'DEG' else ''}")
            expression = expression.replace("tan(", f"math.tan({'math.radians(' if self.angle_mode.get() == 'DEG' else ''}")
            expression = expression.replace("log10(", "math.log10(")
            expression = expression.replace("log(", "math.log(")
            
            # Handle percentage calculations
            expression = re.sub(r'(\d+(\.\d+)?)%', r'(\1/100)', expression)
            
            result = str(eval(expression))
            self.display.delete(0, END)
            self.display.insert(0, result)
            
            # Add to history
            self.add_to_history(f"{expression} = {result}")
        except ZeroDivisionError:
            self.display.delete(0, END)
            self.display.insert(0, "Error: Division by zero")
        except Exception as e:
            self.display.delete(0, END)
            self.display.insert(0, "Error")
    
    def add_to_history(self, entry):
        self.history_list.insert(0, entry)
        self.history.insert(0, entry)
        if len(self.history) > 50:  # Limit history to 50 entries
            self.history_list.delete(END)
            self.history.pop()
        self.save_history()
    
    def on_history_select(self, event):
        selected = self.history_list.get(self.history_list.curselection())
        # Extract the expression part (before " = ")
        expression = selected.split(" = ")[0]
        self.display.delete(0, END)
        self.display.insert(0, expression)
    
    def save_history(self):
        try:
            with open("calculator_history.txt", "w") as f:
                for item in self.history:
                    f.write(item + "\n")
        except Exception as e:
            print(f"Error saving history: {e}")
    
    def load_history(self):
        try:
            with open("calculator_history.txt", "r") as f:
                for line in f.readlines():
                    if line.strip():
                        self.history.append(line.strip())
                        self.history_list.insert(0, line.strip())
        except FileNotFoundError:
            pass
    
    def toggle_angle_mode(self):
        self.angle_mode.set("RAD" if self.angle_mode.get() == "DEG" else "DEG")
    
    def toggle_theme(self):
        if self.current_theme == "dark":
            # Light theme
            self.root.configure(bg="#f5f5f5")
            self.display.configure(bg="white", fg="black", insertbackground="black")
            self.indicator_frame.configure(bg="#f5f5f5")
            self.memory_indicator.configure(bg="#f5f5f5", fg="#ff0000")
            self.angle_mode_label.configure(bg="#f5f5f5", fg="#333333")
            self.history_frame.configure(bg="#f5f5f5", fg="#333333")
            self.history_list.configure(bg="white", fg="black", selectbackground="#dddddd")
            
            for btn, _, _, _ in self.main_buttons + self.sci_buttons:
                btn.configure(bg="#e0e0e0", fg="black", activebackground="#d0d0d0")
            
            for btn in self.memory_btns:
                if btn.cget("text") == "MC":
                    btn.configure(bg="#ff6b6b", activebackground="#ff5252")
                elif btn.cget("text") in ("MR", "MS"):
                    btn.configure(bg="#4ecdc4", activebackground="#48b9b1")
                elif btn.cget("text") == "M+":
                    btn.configure(bg="#51cf66", activebackground="#40c057")
            
            self.current_theme = "light"
        else:
            # Dark theme
            self.root.configure(bg="#1e1e1e")
            self.display.configure(bg="#2a2d36", fg="white", insertbackground="white")
            self.indicator_frame.configure(bg="#1e1e1e")
            self.memory_indicator.configure(bg="#1e1e1e", fg="#ff5555")
            self.angle_mode_label.configure(bg="#1e1e1e", fg="#aaaaaa")
            self.history_frame.configure(bg="#1e1e1e", fg="white")
            self.history_list.configure(bg="#2a2d36", fg="white", selectbackground="#555555")
            
            for btn, _, _, _ in self.main_buttons + self.sci_buttons:
                if btn.cget("text") in ("C", "⌫"):
                    btn.configure(bg="#ff6b6b", activebackground="#ff5252")
                elif btn.cget("text") in ("%", "/", "*", "-", "+"):
                    btn.configure(bg="#4ecdc4", activebackground="#48b9b1")
                elif btn.cget("text") == "=":
                    btn.configure(bg="#51cf66", activebackground="#40c057")
                else:
                    btn.configure(bg="#3a3f4b", activebackground="#4a4f5b")
            
            for btn in self.memory_btns:
                if btn.cget("text") == "MC":
                    btn.configure(bg="#ff6b6b", activebackground="#ff5252")
                elif btn.cget("text") in ("MR", "MS"):
                    btn.configure(bg="#4ecdc4", activebackground="#48b9b1")
                elif btn.cget("text") == "M+":
                    btn.configure(bg="#51cf66", activebackground="#40c057")
            
            self.current_theme = "dark"
    
    def update_memory_indicator(self):
        self.memory_indicator.config(text="M" if self.memory[0] else "")
    
    def on_key_press(self, event):
        key = event.char
        if key in "0123456789+-*/.%()":
            self.display.insert(END, key)
        elif key == "\r":  # Enter key
            self.calculate_result()
        elif key == "\x08":  # Backspace
            self.display.event_generate("<BackSpace>")
        elif key == "\x1b":  # Escape
            self.display.delete(0, END)
    
    def toggle_scientific_mode(self):
        self.scientific_mode = not self.scientific_mode
        if self.scientific_mode:
            self.sci_button_frame.pack(fill=BOTH, padx=10, pady=(0, 10), expand=True)
            self.root.geometry("800x850")
        else:
            self.sci_button_frame.pack_forget()
            self.root.geometry("600x850")

if __name__ == "__main__":
    root = Tk()
    app = EnhancedCalculator(root)
    root.mainloop()