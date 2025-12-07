"""
Button Panel Component - Compact
"""
import tkinter as tk
import config

class ModernButton(tk.Frame):
    def __init__(self, parent, text, command, bg_color):
        super().__init__(parent, bg=parent['bg'])
        
        self.command = command
        self.bg_color = bg_color
        
        self.btn = tk.Label(
            self,
            text=text,
            font=config.FONT_BUTTON,
            bg=bg_color,
            fg=config.COLOR_WHITE,
            pady=6,
            padx=5,
            cursor="hand2"
        )
        self.btn.pack(fill=tk.BOTH, expand=True)
        
        self.btn.bind("<Button-1>", lambda e: self._click())
        self.btn.bind("<Enter>", lambda e: self.btn.config(bg=config.COLOR_BUTTON_HOVER))
        self.btn.bind("<Leave>", lambda e: self.btn.config(bg=self.bg_color))
    
    def _click(self):
        if self.command:
            self.command()


class ButtonPanel(tk.Frame):
    def __init__(self, parent, callbacks):
        super().__init__(parent, bg=config.COLOR_SURFACE, height=config.FOOTER_HEIGHT)
        self.pack_propagate(False)
        
        # Container
        container = tk.Frame(self, bg=config.COLOR_SURFACE)
        container.pack(expand=True, fill=tk.BOTH, padx=6, pady=6)
        
        # Grid config
        for i in range(3):
            container.columnconfigure(i, weight=1)
        container.rowconfigure(0, weight=1)
        
        # Buttons
        ModernButton(
            container, "🔍 SCAN", 
            callbacks.get('scan'), 
            config.COLOR_SUCCESS
        ).grid(row=0, column=0, padx=3, sticky="nsew")
        
        ModernButton(
            container, "📋 DATA", 
            callbacks.get('list'), 
            config.COLOR_SECONDARY
        ).grid(row=0, column=1, padx=3, sticky="nsew")
        
        ModernButton(
            container, "⚙ SETTING", 
            callbacks.get('settings'), 
            config.COLOR_WARNING
        ).grid(row=0, column=2, padx=3, sticky="nsew")