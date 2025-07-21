import tkinter as tk
from tkinter import ttk, font
import time
import threading
from PIL import Image, ImageTk, ImageDraw
import requests
from io import BytesIO
import math
from datetime import datetime, timedelta
import calendar
import random

class PaperPlaneAnimation:
    def __init__(self, parent, callback):
        self.window = tk.Toplevel(parent)
        self.window.title("Sending Confirmation")
        self.window.attributes('-alpha', 0.0)
        
        # Configure window
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        self.window.geometry(f'{screen_width}x{screen_height}')
        self.window.attributes('-fullscreen', True)
        self.window.configure(bg='white')
        
        # Create canvas for animation
        self.canvas = tk.Canvas(self.window, bg='white', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Load and resize paper plane image
        self.plane_image = self.create_paper_plane()
        
        # Animation parameters
        self.x = 100
        self.y = screen_height // 2
        self.angle = 0
        self.amplitude = 100
        self.frequency = 0.01
        self.t = 0
        self.callback = callback
        
        # Start animations
        self.animate_window_appear()

    def create_paper_plane(self):
        # Create a more detailed paper plane shape
        size = 50
        plane = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(plane)
        
        # Draw plane shape with more detail
        body_points = [
            (0, size//2),          # Nose
            (size*3//4, size//3),  # Top wing front
            (size, size//2),       # Tail
            (size*3//4, size*2//3) # Bottom wing front
        ]
        draw.polygon(body_points, fill='#0066cc')
        
        # Add wing details
        wing_top = [
            (size*2//4, size//3),
            (size*3//4, size//3),
            (size*2//4, size//6)
        ]
        wing_bottom = [
            (size*2//4, size*2//3),
            (size*3//4, size*2//3),
            (size*2//4, size*5//6)
        ]
        draw.polygon(wing_top, fill='#3388dd')
        draw.polygon(wing_bottom, fill='#3388dd')
        
        return ImageTk.PhotoImage(plane)

    def animate_window_appear(self):
        alpha = self.window.attributes('-alpha')
        if alpha < 1.0:
            alpha += 0.1
            self.window.attributes('-alpha', alpha)
            self.window.after(20, self.animate_window_appear)
        else:
            self.animate_plane()

    def animate_plane(self):
        if self.x < self.window.winfo_width() + 100:
            # Update position with more natural movement
            self.x += 6
            self.t += self.frequency
            
            # Create a more complex flight path
            base_y = self.window.winfo_height() // 2
            wave_y = math.sin(self.t) * self.amplitude
            bounce_y = math.sin(self.t * 2) * (self.amplitude / 4)
            self.y = base_y + wave_y + bounce_y
            
            # Clear and redraw
            self.canvas.delete('all')
            
            # Enhanced trail effect
            trail_length = 25
            for i in range(trail_length):
                x = self.x - i * 6
                t_offset = self.t - i * self.frequency
                wave_y_trail = math.sin(t_offset) * self.amplitude
                bounce_y_trail = math.sin(t_offset * 2) * (self.amplitude / 4)
                y = base_y + wave_y_trail + bounce_y_trail
                
                # Trail with gradient
                size = (trail_length - i) / trail_length
                r = int(0)
                g = int(102 * size)
                b = int(204 * size)
                color = f'#{r:02x}{g:02x}{b:02x}'
                
                # Main trail
                self.canvas.create_oval(
                    x-1, y-1, x+2, y+2,
                    fill=color, outline=color
                )
                
                # Secondary particles
                if i % 3 == 0:
                    particle_spread = 10 * size
                    for _ in range(2):
                        px = x + random.randint(-int(particle_spread), int(particle_spread))
                        py = y + random.randint(-int(particle_spread), int(particle_spread))
                        p_size = size * 2
                        self.canvas.create_oval(
                            px-p_size, py-p_size, px+p_size, py+p_size,
                            fill=color, outline=color
                        )
            
            # Draw plane with rotation
            angle = math.degrees(math.atan2(wave_y - self.last_y if hasattr(self, 'last_y') else 0, 6))
            self.last_y = wave_y
            
            # Store current plane position for particles
            self.current_plane_pos = (self.x, self.y)
            
            # Draw the plane
            self.canvas.create_image(self.x, self.y, image=self.plane_image)
            
            self.window.after(20, self.animate_plane)
        else:
            self.show_ending_scene()

    def show_ending_scene(self):
        # Clear canvas with fade effect
        def fade_out_canvas(alpha=1.0):
            if alpha > 0:
                alpha -= 0.1
                self.canvas.delete('all')
                self.canvas.configure(bg=f'#{int(255 * alpha):02x}' * 3)
                self.window.after(50, lambda: fade_out_canvas(alpha))
            else:
                self.show_final_message()
        
        fade_out_canvas()

    def show_final_message(self):
        self.canvas.configure(bg='white')
        
        # Create elements with appear animation
        elements = [
            {
                'type': 'text',
                'x': self.window.winfo_width() // 2,
                'y': self.window.winfo_height() // 2 - 50,
                'text': "Tack för din bokning!",
                'font': ('Helvetica', 24, 'bold'),
                'fill': '#0066cc'
            },
            {
                'type': 'text',
                'x': self.window.winfo_width() // 2,
                'y': self.window.winfo_height() // 2 + 10,
                'text': "En bekräftelse har skickats till din e-post.",
                'font': ('Helvetica', 16),
                'fill': '#333333'
            }
        ]
        
        def animate_element(elem, index):
            if elem['type'] == 'text':
                # Create text with fade and slide effect
                self.canvas.create_text(
                    elem['x'],
                    elem['y'] + 20,  # Start below final position
                    text=elem['text'],
                    font=elem['font'],
                    fill=elem['fill'],
                    tags=f'elem_{index}',
                    state='hidden'
                )
                
                # Animate appearance
                def appear_text(progress=0):
                    if progress <= 1:
                        # Update position and opacity
                        y_offset = 20 * (1 - progress)
                        alpha = int(255 * progress)
                        color = elem['fill'][:-2] + f'{alpha:02x}' if elem['fill'].startswith('#') else elem['fill']
                        
                        self.canvas.itemconfigure(f'elem_{index}', state='normal')
                        self.canvas.coords(f'elem_{index}', 
                                         elem['x'],
                                         elem['y'] + y_offset)
                        self.canvas.itemconfigure(f'elem_{index}', fill=color)
                        
                        self.window.after(20, lambda: appear_text(progress + 0.1))
                
                # Start animation with delay based on index
                self.window.after(index * 300, appear_text)
        
        # Animate each element
        for i, elem in enumerate(elements):
            animate_element(elem, i)
        
        # Add logo with special animation
        try:
            logo_url = "https://www.axiestudio.se/logo.jpg"
            logo_response = requests.get(logo_url)
            logo_image = Image.open(BytesIO(logo_response.content))
            logo_image = logo_image.resize((100, 100), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_image)
            
            # Add logo with scale animation
            logo_y = self.window.winfo_height() // 2 + 100
            self.canvas.create_image(
                self.window.winfo_width() // 2,
                logo_y,
                image=self.logo_photo,
                tags='logo',
                state='hidden'
            )
            
            def animate_logo(scale=0.5):
                if scale <= 1:
                    self.canvas.itemconfigure('logo', state='normal')
                    # Apply scale transform
                    self.canvas.scale('logo',
                                    self.window.winfo_width() // 2,
                                    logo_y,
                                    1.1, 1.1)
                    self.window.after(50, lambda: animate_logo(scale + 0.1))
            
            # Start logo animation after text
            self.window.after(len(elements) * 300 + 200, animate_logo)
        except:
            pass
        
        # Start final fade out after delay
        self.window.after(5000, self.fade_out)

    def fade_out(self):
        alpha = self.window.attributes('-alpha')
        if alpha > 0:
            alpha -= 0.1
            self.window.attributes('-alpha', alpha)
            self.window.after(50, self.fade_out)
        else:
            self.window.destroy()
            if self.callback:
                self.callback()

class BookingModal:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Boka Tid - Axie Studio")
        self.parent = parent
        
        # Configure the window
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        window_width = 500
        window_height = 600
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.window.geometry(f'{window_width}x{window_height}+{x}+{y}')
        
        # Make sure booking modal stays on top
        self.window.transient(parent)
        self.window.grab_set()
        
        # Set window style
        self.window.configure(bg='white')
        self.window.attributes('-alpha', 0.0)
        
        # Custom fonts
        self.title_font = font.Font(family="Helvetica", size=16, weight="bold")
        self.header_font = font.Font(family="Helvetica", size=12, weight="bold")
        self.normal_font = font.Font(family="Helvetica", size=10)
        
        # Pre-select Tuesday at 10:00 for the demo
        self.selected_date = None
        self.selected_time = "10:00"
        
        self.setup_ui()
        self.animate_appear()
        
        # Auto-select next Tuesday
        next_tuesday = self.get_next_tuesday()
        self.current_date = next_tuesday
        self.update_calendar()
        self.select_date(next_tuesday.day)
        self.select_time("10:00")

    def get_next_tuesday(self):
        current = datetime.now()
        days_ahead = 1 - current.weekday()  # Tuesday is 1
        if days_ahead <= 0:  # Target day already happened this week
            days_ahead += 7
        return current + timedelta(days=days_ahead)

    def setup_calendar(self, parent):
        calendar_frame = tk.Frame(parent, bg='white')
        calendar_frame.pack(fill=tk.X, pady=10)
        
        # Month navigation
        nav_frame = tk.Frame(calendar_frame, bg='white')
        nav_frame.pack(fill=tk.X)
        
        self.current_date = datetime.now()
        
        tk.Button(nav_frame, text="←", command=self.prev_month).pack(side=tk.LEFT)
        self.month_label = tk.Label(nav_frame, text=self.current_date.strftime("%B %Y"),
                                  font=self.header_font, bg='white')
        self.month_label.pack(side=tk.LEFT, expand=True)
        tk.Button(nav_frame, text="→", command=self.next_month).pack(side=tk.RIGHT)
        
        # Calendar grid
        self.calendar_grid = tk.Frame(calendar_frame, bg='white')
        self.calendar_grid.pack(pady=10)
        self.update_calendar()

    def select_date(self, day):
        self.selected_date = day
        # Update button states
        for widget in self.calendar_grid.winfo_children():
            if isinstance(widget, tk.Button):
                if widget.cget('text') == str(day):
                    widget.configure(bg='#0066cc', fg='white')
                else:
                    widget.configure(bg='#f0f0f0', fg='black')
        self.update_confirm_button()

    def select_time(self, time):
        self.selected_time = time
        # Update button states
        for widget in self.time_slots_frame.winfo_children():
            if isinstance(widget, tk.Button):
                if widget.cget('text') == time:
                    widget.configure(bg='#0066cc', fg='white')
                else:
                    widget.configure(bg='#f0f0f0', fg='black')
        self.update_confirm_button()

    def update_confirm_button(self):
        if self.selected_date and self.selected_time:
            self.confirm_button.configure(state='normal', bg='#0066cc')
        else:
            self.confirm_button.configure(state='disabled', bg='#cccccc')

    def setup_time_slots(self, parent):
        time_frame = tk.Frame(parent, bg='white')
        time_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(time_frame, text="Tillgängliga Tider", font=self.header_font,
                bg='white').pack(anchor='w')
        
        times = ["09:00", "10:00", "11:00", "13:00", "14:00", "15:00"]
        
        self.time_slots_frame = tk.Frame(time_frame, bg='white')
        self.time_slots_frame.pack(fill=tk.X, pady=5)
        
        for i, time in enumerate(times):
            btn = tk.Button(self.time_slots_frame, text=time, font=self.normal_font,
                          bg='#f0f0f0', width=8, command=lambda t=time: self.select_time(t))
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)

    def update_calendar(self):
        # Clear existing calendar
        for widget in self.calendar_grid.winfo_children():
            widget.destroy()
        
        # Add day headers
        days = ["Mån", "Tis", "Ons", "Tor", "Fre", "Lör", "Sön"]
        for i, day in enumerate(days):
            tk.Label(self.calendar_grid, text=day, font=self.normal_font,
                    bg='white').grid(row=0, column=i, padx=2, pady=2)
        
        # Get calendar for current month
        cal = calendar.monthcalendar(self.current_date.year, self.current_date.month)
        
        for i, week in enumerate(cal):
            for j, day in enumerate(week):
                if day != 0:
                    btn = tk.Button(self.calendar_grid, text=str(day),
                                  font=self.normal_font, width=4, height=2)
                    btn.grid(row=i+1, column=j, padx=2, pady=2)
                    btn.bind('<Button-1>', lambda e, d=day: self.select_date(d))

    def prev_month(self):
        self.current_date = self.current_date.replace(day=1) - timedelta(days=1)
        self.month_label.config(text=self.current_date.strftime("%B %Y"))
        self.update_calendar()

    def next_month(self):
        self.current_date = (self.current_date.replace(day=1) + timedelta(days=32)).replace(day=1)
        self.month_label.config(text=self.current_date.strftime("%B %Y"))
        self.update_calendar()

    def confirm_booking(self):
        if self.selected_date and self.selected_time:
            self.animate_disappear()
            # Start paper plane animation
            PaperPlaneAnimation(self.parent, self.cleanup)

    def animate_appear(self):
        alpha = self.window.attributes('-alpha')
        if alpha < 1.0:
            alpha += 0.1
            self.window.attributes('-alpha', alpha)
            self.window.after(20, self.animate_appear)

    def animate_disappear(self):
        alpha = self.window.attributes('-alpha')
        if alpha > 0:
            alpha -= 0.1
            self.window.attributes('-alpha', alpha)
            self.window.after(20, self.animate_disappear)
        else:
            self.cleanup()

    def cleanup(self):
        self.window.destroy()

    def setup_ui(self):
        # Header
        header = tk.Frame(self.window, bg='#0066cc', height=60)
        header.pack(fill=tk.X, pady=0)
        header.pack_propagate(False)
        
        tk.Label(header, text="Boka Konsultation", font=self.title_font,
                bg='#0066cc', fg='white').pack(pady=15)

        # Main content
        content = tk.Frame(self.window, bg='white')
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Calendar section
        self.setup_calendar(content)
        
        # Time slots section
        self.setup_time_slots(content)
        
        # Confirmation button (disabled by default)
        self.confirm_button = tk.Button(content, text="Bekräfta Bokning",
                                      font=self.header_font, bg='#cccccc', fg='white',
                                      state='disabled', command=self.confirm_booking)
        self.confirm_button.pack(pady=20, ipady=10, ipadx=20)

class AnimatedChatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("Axie Studio Kundservice")
        
        # Configure the window
        self.root.configure(bg='#ffffff')
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = 400
        window_height = 600
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f'{window_width}x{window_height}+{x}+{y}')
        
        # Create custom font
        self.custom_font = font.Font(family="Helvetica", size=10)
        self.header_font = font.Font(family="Helvetica", size=12, weight="bold")
        
        # Initialize colors and styles
        self.colors = {
            'primary': '#0066cc',
            'secondary': '#f8f9fa',
            'text': '#333333',
            'bot_bg': '#0066cc',
            'user_bg': '#e9ecef',
            'bot_text': '#ffffff',
            'user_text': '#333333'
        }
        
        self.setup_ui()
        self.setup_demo_conversation()
        
        # Maximum visible messages (rest will fade)
        self.max_visible_messages = 4
        
        # Start the animation loop
        self.start_demo()

    def setup_ui(self):
        # Header Frame
        self.header_frame = tk.Frame(self.root, bg=self.colors['primary'], height=60)
        self.header_frame.pack(fill=tk.X, pady=0)
        self.header_frame.pack_propagate(False)
        
        # Load and display logo
        try:
            logo_url = "https://www.axiestudio.se/logo.jpg"
            logo_response = requests.get(logo_url)
            logo_image = Image.open(BytesIO(logo_response.content))
            logo_image = logo_image.resize((40, 40), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_image)
            self.logo_label = tk.Label(self.header_frame, image=self.logo_photo, bg=self.colors['primary'])
            self.logo_label.pack(side=tk.LEFT, padx=10)
        except:
            self.logo_label = tk.Label(self.header_frame, text="AS", font=self.header_font, 
                                     bg=self.colors['primary'], fg='white')
            self.logo_label.pack(side=tk.LEFT, padx=10)

        # Header text
        header_text = tk.Frame(self.header_frame, bg=self.colors['primary'])
        header_text.pack(side=tk.LEFT, padx=5)
        
        tk.Label(header_text, text="Axie Studio", font=self.header_font,
                bg=self.colors['primary'], fg='white').pack(anchor='w')
        tk.Label(header_text, text="Online • Redo att hjälpa dig", font=("Helvetica", 8),
                bg=self.colors['primary'], fg='white').pack(anchor='w')

        # Chat display with canvas for smooth animations
        self.chat_frame = tk.Frame(self.root, bg='white')
        self.chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.canvas = tk.Canvas(self.chat_frame, bg='white', highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.chat_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg='white')

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        self.scrollable_frame.bind('<Configure>', self.on_frame_configure)
        self.canvas.bind('<Configure>', self.on_canvas_configure)
        
        # Typing indicator (always visible at bottom)
        self.typing_frame = tk.Frame(self.scrollable_frame, bg='white')
        self.typing_dots = []
        for _ in range(3):
            dot = tk.Label(self.typing_frame, text="•", font=("Helvetica", 24), bg='white', fg=self.colors['primary'])
            dot.pack(side=tk.LEFT, padx=2)
            self.typing_dots.append(dot)

        # Input area
        self.input_frame = tk.Frame(self.root, bg='white', height=50)
        self.input_frame.pack(fill=tk.X, pady=(0, 10), padx=10)
        self.input_frame.pack_propagate(False)
        
        self.message_var = tk.StringVar()
        self.input_field = tk.Entry(self.input_frame, textvariable=self.message_var,
                                  font=self.custom_font, bg='#f8f9fa', relief=tk.FLAT)
        self.input_field.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 10), pady=5)
        
        self.send_button = tk.Button(self.input_frame, text="Skicka", font=self.custom_font,
                                   bg=self.colors['primary'], fg='white', relief=tk.FLAT)
        self.send_button.pack(side=tk.RIGHT, padx=5, pady=5, ipadx=10)

    def setup_demo_conversation(self):
        self.demo_conversation = [
            ("bot", "Hej! Välkommen till Axie Studio! 👋"),
            ("bot", "Vi hjälper företag med AI och chatbot-lösningar."),
            ("user", "Hej! Jag är intresserad av era tjänster."),
            ("bot", "Vad bra! Jag kan hjälpa dig att boka en demo."),
            ("user", "Det låter perfekt! När kan vi ses?"),
            ("bot", "Vi har lediga tider nästa vecka. Passar tisdag eller onsdag?"),
            ("user", "Tisdag skulle fungera bra!"),
            ("bot", "Utmärkt! Jag öppnar bokningssystemet nu..."),
            ("system", "OPEN_BOOKING_MODAL")
        ]

    def on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_frame, width=event.width)

    def fade_old_messages(self):
        messages = [w for w in self.scrollable_frame.winfo_children() if isinstance(w, tk.Frame) and w != self.typing_frame]
        if len(messages) > self.max_visible_messages:
            for msg in messages[:-self.max_visible_messages]:
                self.fade_widget(msg)

    def fade_widget(self, widget, current_alpha=1.0):
        if current_alpha > 0:
            current_alpha -= 0.1
            color_value = int(240 + (15 * (1-current_alpha)))
            widget.configure(bg=f'#{color_value:02x}{color_value:02x}{color_value:02x}')
            for child in widget.winfo_children():
                if isinstance(child, tk.Label):
                    text_color = int(51 + (204 * (1-current_alpha)))
                    child.configure(fg=f'#{text_color:02x}{text_color:02x}{text_color:02x}')
            self.root.after(50, lambda: self.fade_widget(widget, current_alpha))
        else:
            widget.destroy()

    def add_message(self, text, is_bot):
        # Create message bubble with background
        bubble_frame = tk.Frame(self.scrollable_frame, bg='white')
        bubble_frame.pack(anchor='w' if is_bot else 'e', padx=10, pady=5, fill=tk.X)
        
        # Message with rounded corners
        message = tk.Label(bubble_frame, text="", font=self.custom_font, wraplength=250,
                         bg=self.colors['bot_bg'] if is_bot else self.colors['user_bg'],
                         fg=self.colors['bot_text'] if is_bot else self.colors['user_text'],
                         justify=tk.LEFT, padx=12, pady=8)
        message.pack(anchor='w' if is_bot else 'e')
        
        # Type text character by character
        for i in range(len(text) + 1):
            message.configure(text=text[:i])
            self.root.update()
            time.sleep(0.02)
        
        # Fade old messages
        self.fade_old_messages()
        
        # Keep typing indicator visible
        self.typing_frame.pack_forget()
        self.typing_frame.pack(anchor='w', padx=10, pady=5)
        
        # Scroll to bottom
        self.canvas.yview_moveto(1.0)

    def animate_text(self, label, text):
        def update_text(index=0):
            if index <= len(text):
                label.configure(text=text[:index])
                if index < len(text):
                    label.after(30, lambda: update_text(index + 1))
        update_text()

    def simulate_typing(self, text):
        for char in text:
            self.message_var.set(self.message_var.get() + char)
            self.root.update()
            time.sleep(0.05)
        time.sleep(0.5)
        self.message_var.set("")

    def animate_typing_dots(self):
        def animate():
            while True:
                for dot in self.typing_dots:
                    dot.configure(fg=self.colors['primary'])
                    time.sleep(0.1)
                    self.root.update()
                for dot in self.typing_dots:
                    dot.configure(fg='#ccc')
                    time.sleep(0.1)
                    self.root.update()
        
        thread = threading.Thread(target=animate, daemon=True)
        thread.start()

    def start_demo(self):
        def demo_loop():
            while True:
                try:
                    # Clear previous messages
                    for widget in self.scrollable_frame.winfo_children():
                        if widget != self.typing_frame:
                            widget.destroy()
                    self.root.update()
                    
                    # Start typing indicator animation
                    self.animate_typing_dots()
                    
                    # Run through demo conversation
                    for sender, message in self.demo_conversation:
                        if sender == "system" and message == "OPEN_BOOKING_MODAL":
                            time.sleep(1)
                            # Create booking modal and wait for it
                            self.root.after(0, lambda: BookingModal(self.root))
                            break
                        elif sender == "bot":
                            time.sleep(1)
                            self.add_message(message, True)
                        else:
                            self.simulate_typing(message)
                            self.add_message(message, False)
                        
                        time.sleep(2)  # Slightly longer pause between messages
                    
                    # Don't restart immediately
                    time.sleep(10)
                    
                except Exception as e:
                    print(f"Error in demo loop: {e}")
                    time.sleep(1)

        # Start demo in separate thread
        demo_thread = threading.Thread(target=demo_loop, daemon=True)
        demo_thread.start()

def main():
    root = tk.Tk()
    app = AnimatedChatbot(root)
    root.mainloop()

if __name__ == "__main__":
    main() 