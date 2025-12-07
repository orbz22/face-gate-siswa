"""
Register Page - Halaman Pendaftaran User
"""
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import config
import cv2


class RegisterPage(tk.Frame):
    def __init__(self, parent, on_back, camera_handler, user_manager, face_recognition):
        super().__init__(parent, bg=config.COLOR_SURFACE)
        
        self.on_back = on_back
        self.camera_handler = camera_handler
        self.user_manager = user_manager
        self.face_recognition = face_recognition
        
        self.current_user = None
        self.capture_count = 0
        self.max_captures = 10
        self.is_capturing = False
        self.photo = None
        
        self._create_ui()
        self._update_preview()
    
    def _create_ui(self):
        """Create UI"""
        # Header
        header = tk.Frame(self, bg=config.COLOR_PRIMARY, height=45)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)
        
        # Back button
        back_btn = tk.Label(
            header,
            text=" ← Kembali ",
            font=(config.FONT_FAMILY, 10, "bold"),
            bg=config.COLOR_SECONDARY,
            fg=config.COLOR_WHITE,
            cursor="hand2",
            padx=8,
            pady=4
        )
        back_btn.pack(side=tk.LEFT, padx=10, pady=8)
        back_btn.bind("<Button-1>", lambda e: self._go_back())
        back_btn.bind("<Enter>", lambda e: back_btn.config(bg=config.COLOR_HOVER))
        back_btn.bind("<Leave>", lambda e: back_btn.config(bg=config.COLOR_SECONDARY))
        
        # Title
        tk.Label(
            header,
            text="📝 Pendaftaran Wajah",
            font=(config.FONT_FAMILY, 12, "bold"),
            bg=config.COLOR_PRIMARY,
            fg=config.COLOR_WHITE
        ).pack(side=tk.LEFT, padx=10)
        
        # Main content
        content = tk.Frame(self, bg=config.COLOR_SURFACE)
        content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left side - Form
        left_frame = tk.Frame(content, bg=config.COLOR_SURFACE)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self._create_form(left_frame)
        
        # Right side - Camera preview
        right_frame = tk.Frame(content, bg=config.COLOR_BLACK, width=180)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        right_frame.pack_propagate(False)
        
        self._create_preview(right_frame)
    
    def _create_form(self, parent):
        """Create form fields"""
        form = tk.Frame(parent, bg=config.COLOR_WHITE, padx=15, pady=15)
        form.pack(fill=tk.BOTH, expand=True)
        
        # Nama Orang Tua
        tk.Label(
            form,
            text="Nama Orang Tua:",
            font=(config.FONT_FAMILY, 9, "bold"),
            bg=config.COLOR_WHITE,
            fg=config.COLOR_PRIMARY
        ).pack(anchor=tk.W, pady=(0, 3))
        
        self.entry_ortu = tk.Entry(
            form,
            font=(config.FONT_FAMILY, 10),
            width=25
        )
        self.entry_ortu.pack(fill=tk.X, pady=(0, 10))
        
        # Nama Anak
        tk.Label(
            form,
            text="Nama Anak:",
            font=(config.FONT_FAMILY, 9, "bold"),
            bg=config.COLOR_WHITE,
            fg=config.COLOR_PRIMARY
        ).pack(anchor=tk.W, pady=(0, 3))
        
        self.entry_anak = tk.Entry(
            form,
            font=(config.FONT_FAMILY, 10),
            width=25
        )
        self.entry_anak.pack(fill=tk.X, pady=(0, 10))
        
        # Kelas
        tk.Label(
            form,
            text="Kelas:",
            font=(config.FONT_FAMILY, 9, "bold"),
            bg=config.COLOR_WHITE,
            fg=config.COLOR_PRIMARY
        ).pack(anchor=tk.W, pady=(0, 3))
        
        self.combo_kelas = ttk.Combobox(
            form,
            values=["TK A", "TK B", "Kelas 1", "Kelas 2", "Kelas 3", "Kelas 4", "Kelas 5", "Kelas 6"],
            font=(config.FONT_FAMILY, 10),
            state="readonly",
            width=23
        )
        self.combo_kelas.pack(fill=tk.X, pady=(0, 15))
        self.combo_kelas.current(0)
        
        # Register button
        self.btn_register = tk.Label(
            form,
            text="📝 Daftar & Lanjut Capture Wajah",
            font=(config.FONT_FAMILY, 10, "bold"),
            bg=config.COLOR_SUCCESS,
            fg=config.COLOR_WHITE,
            cursor="hand2",
            pady=10
        )
        self.btn_register.pack(fill=tk.X, pady=(0, 10))
        self.btn_register.bind("<Button-1>", lambda e: self._register_user())
        self.btn_register.bind("<Enter>", lambda e: self.btn_register.config(bg=config.COLOR_HOVER))
        self.btn_register.bind("<Leave>", lambda e: self.btn_register.config(bg=config.COLOR_SUCCESS))
        
        # Capture section (hidden initially)
        self.capture_frame = tk.Frame(form, bg=config.COLOR_WHITE)
        
        # Capture status
        self.lbl_capture_status = tk.Label(
            self.capture_frame,
            text="Capture: 0/10",
            font=(config.FONT_FAMILY, 10, "bold"),
            bg=config.COLOR_WHITE,
            fg=config.COLOR_PRIMARY
        )
        self.lbl_capture_status.pack(pady=(0, 10))
        
        # Capture button
        self.btn_capture = tk.Label(
            self.capture_frame,
            text="📷 CAPTURE WAJAH",
            font=(config.FONT_FAMILY, 10, "bold"),
            bg=config.COLOR_WARNING,
            fg=config.COLOR_WHITE,
            cursor="hand2",
            pady=10
        )
        self.btn_capture.pack(fill=tk.X, pady=(0, 10))
        self.btn_capture.bind("<Button-1>", lambda e: self._capture_face())
        
        # Finish button
        self.btn_finish = tk.Label(
            self.capture_frame,
            text="✅ SELESAI",
            font=(config.FONT_FAMILY, 10, "bold"),
            bg=config.COLOR_SUCCESS,
            fg=config.COLOR_WHITE,
            cursor="hand2",
            pady=10
        )
        self.btn_finish.pack(fill=tk.X)
        self.btn_finish.bind("<Button-1>", lambda e: self._finish_registration())
        
        # Status label
        self.lbl_status = tk.Label(
            form,
            text="",
            font=(config.FONT_FAMILY, 9),
            bg=config.COLOR_WHITE,
            fg=config.COLOR_SUCCESS
        )
        self.lbl_status.pack(fill=tk.X, pady=(10, 0))
    
    def _create_preview(self, parent):
        """Create camera preview"""
        # Title
        tk.Label(
            parent,
            text="Preview",
            font=(config.FONT_FAMILY, 9, "bold"),
            bg=config.COLOR_BLACK,
            fg=config.COLOR_WHITE
        ).pack(pady=(5, 0))
        
        # Preview label
        self.preview_label = tk.Label(
            parent,
            bg=config.COLOR_BLACK
        )
        self.preview_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def _update_preview(self):
        """Update camera preview"""
        try:
            frame = self.camera_handler.get_frame()
            
            if frame is not None:
                # Detect faces
                faces = self.face_recognition.detect_faces(frame)
                
                # Draw face rectangles
                if len(faces) > 0:
                    frame = self.face_recognition.draw_faces(frame, faces)
                
                # Resize for preview
                preview_w = 170
                preview_h = 130
                
                from PIL import Image
                img = Image.fromarray(frame)
                img = img.resize((preview_w, preview_h), Image.Resampling.LANCZOS)
                
                self.photo = ImageTk.PhotoImage(img)
                self.preview_label.config(image=self.photo)
                
        except Exception as e:
            pass
        
        # Continue updating
        self.after(50, self._update_preview)
    
    def _register_user(self):
        """Register new user"""
        nama_ortu = self.entry_ortu.get().strip()
        nama_anak = self.entry_anak.get().strip()
        kelas = self.combo_kelas.get()
        
        # Validation
        if not nama_ortu:
            self._show_status("❌ Nama orang tua harus diisi!", config.COLOR_DANGER)
            return
        
        if not nama_anak:
            self._show_status("❌ Nama anak harus diisi!", config.COLOR_DANGER)
            return
        
        # Check duplicate
        if self.user_manager.get_user_by_name(nama_anak):
            self._show_status("❌ Nama anak sudah terdaftar!", config.COLOR_DANGER)
            return
        
        # Add user
        self.current_user = self.user_manager.add_user(nama_ortu, nama_anak, kelas)
        
        # Show capture section
        self.btn_register.pack_forget()
        self.capture_frame.pack(fill=tk.X)
        
        # Disable form
        self.entry_ortu.config(state=tk.DISABLED)
        self.entry_anak.config(state=tk.DISABLED)
        self.combo_kelas.config(state=tk.DISABLED)
        
        self._show_status(f"✅ User terdaftar! Silakan capture wajah.", config.COLOR_SUCCESS)
    
    def _capture_face(self):
        """Capture face"""
        if not self.current_user:
            return
        
        frame = self.camera_handler.get_frame()
        if frame is None:
            self._show_status("❌ Tidak ada frame kamera!", config.COLOR_DANGER)
            return
        
        # Detect faces
        faces = self.face_recognition.detect_faces(frame)
        
        if len(faces) == 0:
            self._show_status("❌ Wajah tidak terdeteksi!", config.COLOR_DANGER)
            return
        
        if len(faces) > 1:
            self._show_status("❌ Terdeteksi lebih dari 1 wajah!", config.COLOR_DANGER)
            return
        
        # Save face
        count = self.face_recognition.save_face(
            frame,
            faces[0],
            self.current_user["id"],
            self.current_user["face_dir"]
        )
        
        if count > 0:
            self.capture_count = count
            self.user_manager.update_face_count(self.current_user["id"], count)
            self.lbl_capture_status.config(text=f"Capture: {count}/{self.max_captures}")
            self._show_status(f"✅ Wajah ke-{count} tersimpan!", config.COLOR_SUCCESS)
            
            if count >= self.max_captures:
                self.btn_capture.config(bg=config.COLOR_SECONDARY, text="📷 CUKUP!")
    
    def _finish_registration(self):
        """Finish registration"""
        if self.capture_count < 3:
            self._show_status("❌ Minimal capture 3 wajah!", config.COLOR_DANGER)
            return
        
        # Train recognizer
        self._show_status("🔄 Training model...", config.COLOR_WARNING)
        self.update()
        
        users = self.user_manager.get_all_users()
        success = self.face_recognition.train(users)
        
        if success:
            messagebox.showinfo("Berhasil", f"User {self.current_user['nama_anak']} berhasil didaftarkan!")
            self._go_back()
        else:
            self._show_status("⚠️ Training gagal, tapi data tersimpan", config.COLOR_WARNING)
    
    def _show_status(self, text, color):
        """Show status message"""
        self.lbl_status.config(text=text, fg=color)
    
    def _go_back(self):
        """Go back to main page"""
        self.is_capturing = False
        self.on_back()