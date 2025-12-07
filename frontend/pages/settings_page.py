"""
Settings Page
"""
import tkinter as tk
from tkinter import ttk, messagebox
import config

class SettingsPage(tk.Frame):
    def __init__(self, parent, on_back, camera_handler, settings_manager):
        super().__init__(parent, bg=config.COLOR_BLACK)
        
        self.on_back = on_back
        self.camera_handler = camera_handler
        self.settings_manager = settings_manager
        
        self._create_ui()
    
    def _create_ui(self):
        """Create settings UI"""
        # Header
        header = tk.Frame(self, bg=config.COLOR_PRIMARY, height=45)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)
        
        # Back button
        back_btn = tk.Label(
            header,
            text=" ← Kembali ",
            font=(config.FONT_FAMILY, 11, "bold"),
            bg=config.COLOR_SECONDARY,
            fg=config.COLOR_WHITE,
            cursor="hand2",
            padx=10,
            pady=5
        )
        back_btn.pack(side=tk.LEFT, padx=10, pady=8)
        back_btn.bind("<Button-1>", lambda e: self.on_back())
        back_btn.bind("<Enter>", lambda e: back_btn.config(bg=config.COLOR_HOVER))
        back_btn.bind("<Leave>", lambda e: back_btn.config(bg=config.COLOR_SECONDARY))
        
        # Title
        tk.Label(
            header,
            text="⚙ Pengaturan",
            font=(config.FONT_FAMILY, 14, "bold"),
            bg=config.COLOR_PRIMARY,
            fg=config.COLOR_WHITE
        ).pack(side=tk.LEFT, padx=10)
        
        # Content
        content = tk.Frame(self, bg=config.COLOR_SURFACE)
        content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Camera Section
        self._create_camera_section(content)
        
        # Display Section
        self._create_display_section(content)
        
        # System Section
        self._create_system_section(content)
    
    def _create_camera_section(self, parent):
        """Camera settings"""
        section = tk.LabelFrame(
            parent,
            text=" 📷 Kamera ",
            font=(config.FONT_FAMILY, 10, "bold"),
            bg=config.COLOR_WHITE,
            fg=config.COLOR_PRIMARY,
            padx=10,
            pady=8
        )
        section.pack(fill=tk.X, pady=(0, 10))
        
        # Row 1: Camera selection
        row1 = tk.Frame(section, bg=config.COLOR_WHITE)
        row1.pack(fill=tk.X, pady=5)
        
        tk.Label(
            row1,
            text="Pilih Kamera:",
            font=(config.FONT_FAMILY, 10),
            bg=config.COLOR_WHITE
        ).pack(side=tk.LEFT)
        
        # Use current camera index, don't scan for others yet
        current_cam = self.settings_manager.get_camera_index()
        
        self.camera_var = tk.StringVar(value=f"Kamera {current_cam}")
        self.camera_combo = ttk.Combobox(
            row1,
            textvariable=self.camera_var,
            values=[f"Kamera {current_cam}"],  # Start with current only
            state="readonly",
            width=12
        )
        self.camera_combo.pack(side=tk.LEFT, padx=10)
        
        # Refresh button - scan cameras only when clicked
        refresh_btn = tk.Label(
            row1,
            text=" 🔄 ",
            font=(config.FONT_FAMILY, 10),
            bg=config.COLOR_WARNING,
            fg=config.COLOR_WHITE,
            cursor="hand2",
            padx=5
        )
        refresh_btn.pack(side=tk.LEFT, padx=2)
        refresh_btn.bind("<Button-1>", lambda e: self._refresh_cameras())
        
        # Apply button
        apply_btn = tk.Label(
            row1,
            text=" Terapkan ",
            font=(config.FONT_FAMILY, 9),
            bg=config.COLOR_SUCCESS,
            fg=config.COLOR_WHITE,
            cursor="hand2",
            padx=10,
            pady=3
        )
        apply_btn.pack(side=tk.LEFT, padx=5)
        apply_btn.bind("<Button-1>", lambda e: self._apply_camera())
        
        # Row 2: Flip options
        row2 = tk.Frame(section, bg=config.COLOR_WHITE)
        row2.pack(fill=tk.X, pady=5)
        
        self.flip_h_var = tk.BooleanVar(value=self.settings_manager.get_camera_flip_horizontal())
        tk.Checkbutton(
            row2,
            text="Flip Horizontal",
            variable=self.flip_h_var,
            font=(config.FONT_FAMILY, 9),
            bg=config.COLOR_WHITE,
            command=self._on_flip_h
        ).pack(side=tk.LEFT)
        
        self.flip_v_var = tk.BooleanVar(value=self.settings_manager.get_camera_flip_vertical())
        tk.Checkbutton(
            row2,
            text="Flip Vertical",
            variable=self.flip_v_var,
            font=(config.FONT_FAMILY, 9),
            bg=config.COLOR_WHITE,
            command=self._on_flip_v
        ).pack(side=tk.LEFT, padx=20)
        
        # Status
        self.status_label = tk.Label(
            section,
            text="",
            font=(config.FONT_FAMILY, 9),
            bg=config.COLOR_WHITE,
            fg=config.COLOR_SUCCESS
        )
        self.status_label.pack(fill=tk.X)
    
    def _create_display_section(self, parent):
        """Display settings"""
        section = tk.LabelFrame(
            parent,
            text=" 🖥 Tampilan ",
            font=(config.FONT_FAMILY, 10, "bold"),
            bg=config.COLOR_WHITE,
            fg=config.COLOR_PRIMARY,
            padx=10,
            pady=8
        )
        section.pack(fill=tk.X, pady=(0, 10))
        
        row = tk.Frame(section, bg=config.COLOR_WHITE)
        row.pack(fill=tk.X, pady=5)
        
        self.fullscreen_var = tk.BooleanVar(value=self.settings_manager.get_fullscreen())
        tk.Checkbutton(
            row,
            text="Fullscreen",
            variable=self.fullscreen_var,
            font=(config.FONT_FAMILY, 9),
            bg=config.COLOR_WHITE,
            command=self._on_fullscreen
        ).pack(side=tk.LEFT)
        
        self.fps_var = tk.BooleanVar(value=self.settings_manager.get_show_fps())
        tk.Checkbutton(
            row,
            text="Tampilkan FPS",
            variable=self.fps_var,
            font=(config.FONT_FAMILY, 9),
            bg=config.COLOR_WHITE,
            command=self._on_fps
        ).pack(side=tk.LEFT, padx=20)
    
    def _create_system_section(self, parent):
        """System settings"""
        section = tk.LabelFrame(
            parent,
            text=" 🔧 Sistem ",
            font=(config.FONT_FAMILY, 10, "bold"),
            bg=config.COLOR_WHITE,
            fg=config.COLOR_PRIMARY,
            padx=10,
            pady=8
        )
        section.pack(fill=tk.X)
        
        row = tk.Frame(section, bg=config.COLOR_WHITE)
        row.pack(fill=tk.X, pady=5)
        
        # Reset button
        reset_btn = tk.Label(
            row,
            text=" 🔄 Reset Default ",
            font=(config.FONT_FAMILY, 9),
            bg=config.COLOR_DANGER,
            fg=config.COLOR_WHITE,
            cursor="hand2",
            padx=10,
            pady=3
        )
        reset_btn.pack(side=tk.LEFT)
        reset_btn.bind("<Button-1>", lambda e: self._reset())
        
        # Version
        tk.Label(
            row,
            text=f"v{config.APP_VERSION}",
            font=(config.FONT_FAMILY, 9),
            bg=config.COLOR_WHITE,
            fg=config.COLOR_PRIMARY
        ).pack(side=tk.RIGHT)
    
    # ===== Handlers =====
    def _refresh_cameras(self):
        """Refresh camera list"""
        self._show_status("🔄 Mencari kamera...", config.COLOR_WARNING)
        self.update()
        
        # Clear cache and get cameras
        from backend import CameraHandler
        CameraHandler.clear_camera_cache()
        
        cameras = self.camera_handler.get_available_cameras()
        self.camera_combo['values'] = [f"Kamera {i}" for i in cameras]
        
        self._show_status(f"✅ Ditemukan {len(cameras)} kamera", config.COLOR_SUCCESS)
    
    def _apply_camera(self):
        """Apply camera selection"""
        try:
            selected = self.camera_var.get()
            idx = int(selected.replace("Kamera ", ""))
            
            if idx == self.camera_handler.camera_index:
                self._show_status("ℹ️ Kamera sudah aktif", config.COLOR_SECONDARY)
                return
            
            self._show_status("🔄 Mengganti kamera...", config.COLOR_WARNING)
            self.update()
            
            if self.camera_handler.change_camera(idx):
                self.settings_manager.set_camera_index(idx)
                self._show_status("✅ Kamera berhasil diganti!", config.COLOR_SUCCESS)
            else:
                self._show_status("❌ Gagal mengganti kamera", config.COLOR_DANGER)
        except Exception as e:
            self._show_status(f"❌ Error: {e}", config.COLOR_DANGER)
    
    def _on_flip_h(self):
        val = self.flip_h_var.get()
        self.settings_manager.set_camera_flip_horizontal(val)
        self.camera_handler.flip_horizontal = val
    
    def _on_flip_v(self):
        val = self.flip_v_var.get()
        self.settings_manager.set_camera_flip_vertical(val)
        self.camera_handler.flip_vertical = val
    
    def _on_fullscreen(self):
        self.settings_manager.set_fullscreen(self.fullscreen_var.get())
    
    def _on_fps(self):
        self.settings_manager.set_show_fps(self.fps_var.get())
    
    def _reset(self):
        if messagebox.askyesno("Konfirmasi", "Reset semua pengaturan?"):
            self.settings_manager.reset_to_default()
            messagebox.showinfo("Info", "Pengaturan direset. Restart aplikasi.")
    
    def _show_status(self, text, color):
        self.status_label.config(text=text, fg=color)
        self.after(3000, lambda: self.status_label.config(text=""))