import customtkinter as ctk
import math

# --- Stil ve Font Tanımlamaları ---
LARGE_FONT_STYLE = ("Arial", 40, "bold")
SMALL_FONT_STYLE = ("Arial", 16)
DIGITS_FONT_STYLE = ("Arial", 24, "bold")
DEFAULT_FONT_STYLE = ("Arial", 20)
HISTORY_FONT_STYLE = ("Arial", 18)

# Geliştirilmiş Renk Paleti
FENER_LACIVERT = "#001450"
FENER_SARI = "#FBB100"
FENER_BEYAZ = "#FFFFFF"
DISPLAY_BG_COLOR = "#DDE2E5"
ADVANCED_OP_COLOR = "#27AE60"
WHITE = "#FFFFFF"

# =============================================================================
# SINIF 1: HESAPLAMA MOTORU (BEYİN)
# =============================================================================
class CalculationLogic:
    def __init__(self):
        self.total_expression = ""
        self.current_expression = ""
        self.history = [] # <-- YENİ: Geçmiş listesi

    def add_to_expression(self, value):
        self.current_expression += str(value)

    def append_operator(self, operator):
        if self.current_expression:
            self.total_expression += self.current_expression + operator
            self.current_expression = ""

    def clear(self):
        self.current_expression, self.total_expression = "", ""

    def evaluate(self):
        full_expression = self.total_expression + self.current_expression
        if not full_expression: return
        
        try:
            result = eval(full_expression)
            formatted_result = self._format_result(result)
            
            # Başarılı hesaplamayı geçmişe ekle
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

    def _format_result(self, result):
        return int(result) if result == int(result) else f"{result:.4f}"

    def _format_expression_for_history(self, expression):
        return expression.replace("**", "^").replace("/", "÷").replace("*", "×")

# =============================================================================
# SINIF 2: KULLANICI ARAYÜZÜ (GÖRÜNÜM)
# =============================================================================
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
        
        for i in range(6): self.buttons_frame.rowconfigure(i, weight=1)
        for i in range(4): self.buttons_frame.columnconfigure(i, weight=1)
        
        self._create_all_buttons()
        self._bind_keys()

    def _create_button(self, text, command, row, col, style_options=None, **grid_options):
        button = ctk.CTkButton(self.buttons_frame, text=text, command=command,
                               font=DEFAULT_FONT_STYLE, corner_radius=12)
        if style_options: button.configure(**style_options)
        grid_options.setdefault("sticky", "nsew")
        grid_options.setdefault("padx", 4)
        grid_options.setdefault("pady", 4)
        button.grid(row=row, column=col, **grid_options)

    def _create_all_buttons(self):
        digits = {
            7: (2, 0), 8: (2, 1), 9: (2, 2), 4: (3, 0), 5: (3, 1), 6: (3, 2),
            1: (4, 0), 2: (4, 1), 3: (4, 2), 0: (5, 0), '.': (5, 2)
        }
        digit_options = {"fg_color": FENER_BEYAZ, "text_color": FENER_LACIVERT, "font": DIGITS_FONT_STYLE, "hover_color": "#EAEAEA"}
        for digit, pos in digits.items():
            self._create_button(str(digit), self._make_command(self.logic.add_to_expression, digit),
                                pos[0], pos[1], digit_options, **({"columnspan": 2} if digit == 0 else {}))

        op_options = {"fg_color": FENER_SARI, "text_color": FENER_LACIVERT, "font": ("Arial", 20, "bold"), "hover_color": "#FFE082"}
        sci_options = {"fg_color": ADVANCED_OP_COLOR, "text_color": WHITE, "hover_color": "#2ECC71"}
        
        self._create_button("C", self._make_command(self.logic.clear), 1, 0, op_options)
        self._create_button("+/-", self._make_command(self.logic.toggle_sign), 1, 1, op_options)
        self._create_button("%", self._make_command(self.logic.append_operator, "%"), 1, 2, op_options)
        self._create_button(self._get_op_symbol("/"), self._make_command(self.logic.append_operator, "/"), 1, 3, op_options)
        self._create_button(self._get_op_symbol("*"), self._make_command(self.logic.append_operator, "*"), 2, 3, op_options)
        self._create_button(self._get_op_symbol("-"), self._make_command(self.logic.append_operator, "-"), 3, 3, op_options)
        self._create_button(self._get_op_symbol("+"), self._make_command(self.logic.append_operator, "+"), 4, 3, op_options)
        self._create_button("=", self._make_command(self.logic.evaluate), 5, 3, op_options)
        
        self._create_button("√x", self._make_command(self.logic.calculate_sqrt), 0, 0, sci_options)
        self._create_button("xʸ", self._make_command(self.logic.append_operator, "**"), 0, 1, sci_options)
        self._create_button("x!", self._make_command(self.logic.calculate_factorial), 0, 2, sci_options)
        
        # Geçmiş Butonu
        self._create_button("⎋", self._show_history_window, 0, 3, {"fg_color": FENER_LACIVERT, "hover_color": "#002884"})

    # Geçmiş Penceresini gösteren fonksiyon
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

# =============================================================================
# SINIF 3: UYGULAMA YÖNETİCİSİ (ORKESTRA ŞEFİ)
# =============================================================================
class CalculatorApp:
    def __init__(self):
        ctk.set_appearance_mode("Dark")
        self.window = ctk.CTk()
        self.window.geometry("375x667")
        self.window.resizable(0, 0)
        self.window.title("OOP Bilimsel Hesap Makinesi")
        
        self.logic = CalculationLogic()
        self.ui = CalculatorUI(self.window, self.logic)
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = CalculatorApp()
    app.run()