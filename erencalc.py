import customtkinter as ctk
import math

LARGE_FONT_STYLE = ("Arial", 40, "bold")
SMALL_FONT_STYLE = ("Arial", 16)
DIGITS_FONT_STYLE = ("Arial", 24, "bold")
DEFAULT_FONT_STYLE = ("Arial", 20)
HISTORY_FONT_STYLE = ("Arial", 18)

FENER_LACIVERT = "#001450"
FENER_SARI = "#FBB100"
FENER_BEYAZ = "#FFFFFF"
DISPLAY_BG_COLOR = "#DDE2E5"
ADVANCED_OP_COLOR = "#27AE60"
DEL_COLOR = "#D60000"
WHITE = "#FFFFFF"

class CalculationLogic:
    def __init__(self):
        self.total_expression = ""
        self.current_expression = ""
        self.history = [] 

    def add_to_expression(self, value):
        self.current_expression += str(value)

    def append_operator(self, operator):
        if self.current_expression:
            self.total_expression += self.current_expression
            self.current_expression = ""
        self.total_expression += operator

    def delete_last(self):
        if self.current_expression:
            self.current_expression = self.current_expression[:-1]

    def clear(self):
        self.current_expression, self.total_expression = "", ""

    def evaluate(self):
        full_expression = self.total_expression + self.current_expression
        if not full_expression: return
        
        try:
            result = eval(full_expression)
            formatted_result = self._format_result(result)
            
            history_entry = f"{self._format_expression_for_history(full_expression)} = {formatted_result}"
            self.history.append(history_entry)
            
            self.current_expression = str(formatted_result)
            self.total_expression = ""
        except Exception:
            self.current_expression = "Hata"
            self.total_expression = ""

    def toggle_sign(self):
        if not self.current_expression: return
        self.current_expression = self.current_expression[1:] if self.current_expression.startswith('-') else '-' + self.current_expression

    def calculate_sqrt(self):
        if not self.current_expression: return
        try:
            result = math.sqrt(float(self.current_expression))
            self.current_expression = str(self._format_result(result))
        except ValueError: self.current_expression = "Hata"

    def calculate_factorial(self):
        if not self.current_expression: return
        try:
            result = math.factorial(int(self.current_expression))
            self.current_expression = str(self._format_result(result))
        except (ValueError, TypeError): self.current_expression = "Hata"
    
    def trigo_sin(self):
        if not self.current_expression: return
        try:
            val = math.radians(float(self.current_expression))
            result = math.sin(val)
            self.current_expression = str(self._format_result(result))
        except ValueError:
            self.current_expression = "Hata"

    def trigo_cos(self):
        if not self.current_expression: return
        try:
            val = math.radians(float(self.current_expression))
            result = math.cos(val)
            self.current_expression = str(self._format_result(result))
        except ValueError:
            self.current_expression = "Hata"

    def trigo_tan(self):
        if not self.current_expression: return
        try:
            val = math.radians(float(self.current_expression))
            result = math.tan(val)
            self.current_expression = str(self._format_result(result))
        except ValueError:
            self.current_expression = "Hata"

    def calculate_log(self):
        if not self.current_expression: return
        try:
            result = math.log10(float(self.current_expression))
            self.current_expression = str(self._format_result(result))
        except ValueError:
            self.current_expression = "Hata"

    def calculate_ln(self):
        if not self.current_expression: return
        try:
            result = math.log(float(self.current_expression))
            self.current_expression = str(self._format_result(result))
        except ValueError:
            self.current_expression = "Hata"

    def calculate_percentage(self):
        if not self.current_expression: return
        try:
            result = float(self.current_expression) / 100
            self.current_expression = str(self._format_result(result))
        except ValueError:
            self.current_expression = "Hata"

    def _format_result(self, result):
        return int(result) if result == int(result) else f"{result:.4f}"

    def _format_expression_for_history(self, expression):
        return expression.replace("**", "^").replace("/", "÷").replace("*", "×")

class CalculatorUI:
    def __init__(self, window, logic):
        self.window = window
        self.logic = logic
        self.history_window_open = False

        self.container_frame = ctk.CTkFrame(window, fg_color=FENER_LACIVERT, corner_radius=0)
        self.container_frame.pack(expand=True, fill="both")

        self.display_frame = self._create_display_frame()
        self.buttons_frame = self._create_buttons_frame()

        self.total_label, self.label = self._create_display_labels()
        
        for i in range(5): self.buttons_frame.rowconfigure(i, weight=1)
        for i in range(6): self.buttons_frame.columnconfigure(i, weight=1)
        
        self._create_all_buttons()
        self._bind_keys()

    def _create_button(self, text, command, row, col, style_options=None, parent=None):
        if parent is None: parent = self.buttons_frame
        button = ctk.CTkButton(parent, text=text, command=command,
                               font=DEFAULT_FONT_STYLE, corner_radius=12)
        if style_options: button.configure(**style_options)
        button.grid(row=row, column=col, sticky="nsew", padx=4, pady=4)

    def _create_all_buttons(self):
        # digit and decimal buttons
        digits = {
            7: (1, 0), 8: (1, 1), 9: (1, 2),
            4: (2, 0), 5: (2, 1), 6: (2, 2),
            1: (3, 0), 2: (3, 1), 3: (3, 2),
            0: (4, 0), '.': (4, 1)
        }
        
        digit_options = {"fg_color": FENER_BEYAZ, "text_color": FENER_LACIVERT, "font": DIGITS_FONT_STYLE, "hover_color": "#EAEAEA"}
        for digit, pos in digits.items():
            self._create_button(str(digit), self._make_command(self.logic.add_to_expression, digit),
                                pos[0], pos[1], digit_options)
            
        op_options = {"fg_color": FENER_SARI, "text_color": FENER_LACIVERT, "font": ("Arial", 20, "bold"), "hover_color": "#FFE082"}
        sci_options = {"fg_color": ADVANCED_OP_COLOR, "text_color": WHITE, "hover_color": "#2ECC71"}
        del_options = {"fg_color": DEL_COLOR, "text_color": WHITE, "hover_color": "#D60000"}
        his_options = {"fg_color": FENER_LACIVERT, "hover_color": "#002884"}

        # sign toggle button
        self._create_button("+/-", self._make_command(self.logic.toggle_sign), 4, 2, digit_options)
        
        # operator buttons
        self._create_button(self._get_op_symbol("/"), self._make_command(self.logic.append_operator, "/"), 0, 3, op_options)
        self._create_button(self._get_op_symbol("*"), self._make_command(self.logic.append_operator, "*"), 1, 3, op_options)
        self._create_button(self._get_op_symbol("-"), self._make_command(self.logic.append_operator, "-"), 2, 3, op_options)
        self._create_button(self._get_op_symbol("+"), self._make_command(self.logic.append_operator, "+"), 3, 3, op_options)
        self._create_button("=", self._make_command(self.logic.evaluate), 4, 3, op_options)

        # delete and clear buttons
        self._create_button("DEL", self._make_command(self.logic.delete_last), 0, 4, del_options)
        self._create_button("AC", self._make_command(self.logic.clear), 0, 5, del_options)

        # scientific buttons
        self._create_button("sin", self._make_command(self.logic.trigo_sin), 0, 0, sci_options)
        self._create_button("cos", self._make_command(self.logic.trigo_cos), 0, 1, sci_options)
        self._create_button("tan", self._make_command(self.logic.trigo_tan), 0, 2, sci_options)

        self._create_button("log", self._make_command(self.logic.calculate_log), 1, 4, sci_options)
        self._create_button("ln", self._make_command(self.logic.calculate_ln), 1, 5, sci_options)

        self._create_button("xʸ", self._make_command(self.logic.append_operator, "**"), 3, 4, sci_options)
        self._create_button("√x", self._make_command(self.logic.calculate_sqrt), 3, 5, sci_options)
        self._create_button("x!", self._make_command(self.logic.calculate_factorial), 4, 4, sci_options)
        self._create_button("(", self._make_command(self.logic.append_operator, "("), 2, 4, sci_options)
        self._create_button(")", self._make_command(self.logic.append_operator, ")"), 2, 5, sci_options)
        
        # history button
        self._create_button("⎋", self._show_history_window, 4, 5, his_options)

        # YER KALMADI
        #self._create_button("%", self._make_command(self.logic.calculate_percentage), 3, 5, sci_options)

        # BUNU BAŞARAMADIM
            # subframe for brackets
            # parent_frame = ctk.CTkFrame(self.buttons_frame, fg_color="transparent")
            # parent_frame.grid(row=4, column=4, sticky="nsew", padx=4, pady=4)
            # parent_frame.columnconfigure(0, weight=1)
            # parent_frame.columnconfigure(1, weight=1)
            # self._create_button("(", self._make_command(self.logic.append_operator, "("), 0, 0, sci_options, parent=parent_frame)
            # self._create_button(")", self._make_command(self.logic.append_operator, ")"), 0, 1, sci_options, parent=parent_frame)
        
    def _show_history_window(self):
        if self.history_window_open: return
        
        history_win = ctk.CTkToplevel(self.window)
        history_win.title("Hesaplama Geçmişi")
        history_win.geometry("300x400")
        history_win.resizable(False, False)

        def on_close():
            self.history_window_open = False
            history_win.destroy()
        
        history_win.protocol("WM_DELETE_WINDOW", on_close)
        self.history_window_open = True
        
        scroll_frame = ctk.CTkScrollableFrame(history_win, label_text="Geçmiş İşlemler")
        scroll_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        if not self.logic.history:
            ctk.CTkLabel(scroll_frame, text="Henüz bir işlem yapılmadı.", font=HISTORY_FONT_STYLE).pack(pady=10)
        else:
            for item in reversed(self.logic.history):
                ctk.CTkLabel(scroll_frame, text=item, font=HISTORY_FONT_STYLE, anchor="w").pack(fill="x", padx=10, pady=5)

    def _make_command(self, func, *args):
        return lambda: (func(*args), self._update_display())

    def _update_display(self):
        self.label.configure(text=self.logic.current_expression[:11])
        expression = self.logic.total_expression
        for op, symbol in {"/": " \u00F7 ", "*": " \u00D7 ", "**": " ^ "}.items():
            expression = expression.replace(op, symbol)
        self.total_label.configure(text=expression)

    def _create_display_frame(self):
        frame = ctk.CTkFrame(self.container_frame, fg_color=DISPLAY_BG_COLOR, corner_radius=12)
        frame.pack(expand=True, fill="both", pady=(0, 10))
        frame.pack_propagate(False)
        return frame

    def _create_buttons_frame(self):
        frame = ctk.CTkFrame(self.container_frame, fg_color="transparent")
        frame.pack(expand=True, fill="both")
        return frame

    def _create_display_labels(self):
        total_label = ctk.CTkLabel(self.display_frame, text="", anchor="e", text_color=FENER_LACIVERT, font=SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill='both', padx=24)
        label = ctk.CTkLabel(self.display_frame, text="", anchor="e", text_color=FENER_LACIVERT, font=LARGE_FONT_STYLE)
        label.pack(expand=True, fill='both', padx=24)
        return total_label, label

    def _bind_keys(self):
        self.window.bind("<Return>", lambda event: self._make_command(self.logic.evaluate)())
        self.window.bind("<BackSpace>", lambda event: self._make_command(self.logic.clear)())
        for key in "7894561230.": self.window.bind(key, lambda event, d=key: self._make_command(self.logic.add_to_expression, d)())
        for key in "/*-+%": self.window.bind(key, lambda event, o=key: self._make_command(self.logic.append_operator, o)())
        self.window.bind("!", lambda event: self._make_command(self.logic.calculate_factorial)())

    def _get_op_symbol(self, op): return {"/": "\u00F7", "*": "\u00D7", "**": " ^ "}.get(op, op)


class CalculatorApp:
    def __init__(self):
        ctk.set_appearance_mode("Dark")
        self.window = ctk.CTk()
        self.window.geometry("500x667")
        self.window.resizable(0, 0)
        self.window.title("OOP Bilimsel Hesap Makinesi")
        
        self.logic = CalculationLogic()
        
        self.ui = CalculatorUI(self.window, self.logic)
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = CalculatorApp()
    app.run()