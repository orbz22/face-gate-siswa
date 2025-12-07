"""
Button Panel Component - 3 Tombol di Bawah
"""
import tkinter as tk
import config


class ButtonPanel(tk.Frame):
    def __init__(self, parent, callbacks):
        super().__init__(parent, bg=config.COLOR_DARK, height=60)
        self.pack_propagate(False)
        
        self.callbacks = callbacks
        self.scan_active = False
        
        self._create_buttons()
    
    def _create_buttons(self):
        """Create 3 buttons"""
        # Container
        container = tk.Frame(self, bg=config.COLOR_DARK)
        container.pack(expand=True, fill=tk.BOTH, padx=10, pady=8)
        
        # Grid config
        for i in range(3):
            container.columnconfigure(i, weight=1)
        container.rowconfigure(0, weight=1)
        
        # Button 1: Scan On/Off
        self.btn_scan = tk.Label(
            container,
            text="🔴 SCAN OFF",
            font=(config.FONT_FAMILY, 10, "bold"),
            bg=config.COLOR_DANGER,
            fg=config.COLOR_WHITE,
            cursor="hand2",
            pady=8
        )
        self.btn_scan.grid(row=0, column=0, padx=5, sticky="nsew")
        self.btn_scan.bind("<Button-1>", self._on_scan_click)
        self.btn_scan.bind("<Enter>", lambda e: self._hover_enter(self.btn_scan))
        self.btn_scan.bind("<Leave>", lambda e: self._hover_leave_scan())
        
        # Button 2: Daftar User
        self.btn_register = tk.Label(
            container,
            text="📝 DAFTAR",
            font=(config.FONT_FAMILY, 10, "bold"),
            bg=config.COLOR_SECONDARY,
            fg=config.COLOR_WHITE,
            cursor="hand2",
            pady=8
        )
        self.btn_register.grid(row=0, column=1, padx=5, sticky="nsew")
        self.btn_register.bind("<Button-1>", lambda e: self._callback('register'))
        self.btn_register.bind("<Enter>", lambda e: self._hover_enter(self.btn_register))
        self.btn_register.bind("<Leave>", lambda e: self.btn_register.config(bg=config.COLOR_SECONDARY))
        
        # Button 3: Info/Riwayat
        self.btn_info = tk.Label(
            container,
            text="📋 RIWAYAT",
            font=(config.FONT_FAMILY, 10, "bold"),
            bg=config.COLOR_PRIMARY,
            fg=config.COLOR_WHITE,
            cursor="hand2",
            pady=8
        )
        self.btn_info.grid(row=0, column=2, padx=5, sticky="nsew")
        self.btn_info.bind("<Button-1>", lambda e: self._callback('info'))
        self.btn_info.bind("<Enter>", lambda e: self._hover_enter(self.btn_info))
        self.btn_info.bind("<Leave>", lambda e: self.btn_info.config(bg=config.COLOR_PRIMARY))
    
    def _hover_enter(self, btn):
        """Hover effect"""
        btn.config(bg=config.COLOR_HOVER)
    
    def _hover_leave_scan(self):
        """Reset scan button color based on state"""
        if self.scan_active:
            self.btn_scan.config(bg=config.COLOR_SUCCESS)
        else:
            self.btn_scan.config(bg=config.COLOR_DANGER)
    
    def _on_scan_click(self, event=None):
        """Toggle scan on/off"""
        self.scan_active = not self.scan_active
        
        if self.scan_active:
            self.btn_scan.config(text="🟢 SCAN ON", bg=config.COLOR_SUCCESS)
        else:
            self.btn_scan.config(text="🔴 SCAN OFF", bg=config.COLOR_DANGER)
        
        self._callback('scan', self.scan_active)
    
    def _callback(self, name, *args):
        """Call callback function"""
        if name in self.callbacks and self.callbacks[name]:
            self.callbacks[name](*args)
    
    def set_scan_state(self, active):
        """Set scan state from outside"""
        self.scan_active = active
        if active:
            self.btn_scan.config(text="🟢 SCAN ON", bg=config.COLOR_SUCCESS)
        else:
            self.btn_scan.config(text="🔴 SCAN OFF", bg=config.COLOR_DANGER)