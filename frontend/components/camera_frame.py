"""
Camera Frame Component - True Transparent Icon (Large)
"""
import tkinter as tk
from PIL import Image, ImageTk, ImageEnhance, ImageDraw, ImageFont
import config
import os


class CameraFrame(tk.Frame):
    def __init__(self, parent, on_settings_click=None):
        super().__init__(parent, bg=config.COLOR_BLACK)
        
        self.on_settings_click = on_settings_click
        self.photo = None
        self.settings_icon_normal = None
        self.settings_icon_hover = None
        self.is_hovering = False
        
        # ========================================
        # SETTINGS ICON - KONFIGURASI
        # ========================================
        self.icon_x = 15        # Posisi X (dari kiri)
        self.icon_y = 15        # Posisi Y (dari atas)  
        self.icon_size = 56     # Ukuran icon (BESAR)
        # ========================================
        
        # Load settings icon
        self._load_settings_icon()
        
        # Camera display
        self.camera_label = tk.Label(
            self, 
            bg=config.COLOR_BLACK,
            cursor="arrow"
        )
        self.camera_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Bind events
        self.camera_label.bind("<Button-1>", self._on_click)
        self.camera_label.bind("<Motion>", self._on_mouse_move)
    
    def _load_settings_icon(self):
        """Load settings icon"""
        try:
            if os.path.exists(config.ICON_SETTINGS):
                # Load image dengan RGBA
                img = Image.open(config.ICON_SETTINGS).convert('RGBA')
                
                # Resize sesuai icon_size
                img = img.resize((self.icon_size, self.icon_size), Image.Resampling.LANCZOS)
                
                self.settings_icon_normal = img.copy()
                
                # Hover version - lebih terang
                enhancer = ImageEnhance.Brightness(img)
                self.settings_icon_hover = enhancer.enhance(1.5)
                
                print(f"✅ Settings icon loaded ({self.icon_size}x{self.icon_size})")
            else:
                print(f"⚠️ Icon not found: {config.ICON_SETTINGS}")
                self._create_fallback_icon()
                
        except Exception as e:
            print(f"❌ Error loading icon: {e}")
            self._create_fallback_icon()
    
    def _create_fallback_icon(self):
        """Create fallback gear icon"""
        # Create transparent image
        img = Image.new('RGBA', (self.icon_size, self.icon_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Font size proportional to icon size
        font_size = int(self.icon_size * 0.7)
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Center text
        text_x = self.icon_size // 6
        text_y = self.icon_size // 10
        draw.text((text_x, text_y), "⚙", fill=(255, 255, 255, 255), font=font)
        
        self.settings_icon_normal = img.copy()
        
        # Hover version
        enhancer = ImageEnhance.Brightness(img)
        self.settings_icon_hover = enhancer.enhance(1.5)
        
        print(f"✅ Fallback icon created ({self.icon_size}x{self.icon_size})")
    
    def _is_over_icon(self, x, y):
        """Check if mouse is over settings icon"""
        return (self.icon_x <= x <= self.icon_x + self.icon_size and
                self.icon_y <= y <= self.icon_y + self.icon_size)
    
    def _on_click(self, event):
        """Handle click"""
        if self._is_over_icon(event.x, event.y):
            if self.on_settings_click:
                self.on_settings_click()
    
    def _on_mouse_move(self, event):
        """Handle mouse movement for hover effect"""
        over_icon = self._is_over_icon(event.x, event.y)
        
        if over_icon and not self.is_hovering:
            self.is_hovering = True
            self.camera_label.config(cursor="hand2")
        elif not over_icon and self.is_hovering:
            self.is_hovering = False
            self.camera_label.config(cursor="arrow")
    
    def update_frame(self, frame):
        """Update camera display with icon overlay"""
        if frame is None:
            return
        
        try:
            display_w = self.winfo_width()
            display_h = self.winfo_height()
            
            if display_w < 10 or display_h < 10:
                return
            
            # Convert frame to PIL
            pil_image = Image.fromarray(frame)
            img_w, img_h = pil_image.size
            
            # Calculate scale (fit, no crop)
            scale = min(display_w / img_w, display_h / img_h)
            new_w = int(img_w * scale)
            new_h = int(img_h * scale)
            
            # Resize camera frame
            resized = pil_image.resize((new_w, new_h), Image.Resampling.LANCZOS)
            
            # Create background
            background = Image.new('RGBA', (display_w, display_h), (0, 0, 0, 255))
            
            # Center paste camera frame
            offset_x = (display_w - new_w) // 2
            offset_y = (display_h - new_h) // 2
            background.paste(resized, (offset_x, offset_y))
            
            # Overlay settings icon (TRUE TRANSPARENCY)
            icon = self.settings_icon_hover if self.is_hovering else self.settings_icon_normal
            if icon:
                background.paste(icon, (self.icon_x, self.icon_y), icon)
            
            # Convert to PhotoImage
            self.photo = ImageTk.PhotoImage(background)
            self.camera_label.configure(image=self.photo)
            
        except Exception as e:
            pass