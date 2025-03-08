import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw
import os
import threading
import requests
import time
from dotenv import load_dotenv
import pyautogui
import keyboard
import tempfile
from datetime import datetime
from openai import OpenAI
import httpx
import pystray
from pystray import MenuItem as item

class FloatingResultWindow:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Assistant")
        self.window.geometry("400x10")  # Initial minimal size, will be adjusted
        self.window.attributes('-topmost', True)
        
        # Make window transparent and remove decorations
        self.window.attributes('-alpha', 0.85, '-toolwindow', True)
        self.window.overrideredirect(True)
        
        # Main container with transparent appearance
        self.container = tk.Frame(self.window)
        self.container.configure(bg='#ffffff')
        self.container.pack(fill='both', expand=True)
        
        # Response frame
        response_frame = tk.Frame(self.container)
        response_frame.configure(bg='#ffffff')
        response_frame.pack(fill='both', expand=True)
        
        # Timer label
        self.timer_label = tk.Label(
            response_frame,
            text="",
            bg='#ffffff',
            fg='#666666',
            font=("Segoe UI", 9, "italic")
        )
        self.timer_label.pack(anchor='w', padx=5, pady=(5,0))
        
        # Result text area with transparent styling
        self.result_text = tk.Text(
            response_frame,
            wrap=tk.WORD,
            font=("Segoe UI", 11),
            bg='#ffffff',
            fg='#2b2b2b',
            relief='flat',
            padx=5,
            pady=5,
            height=1,  # Start with minimal height
            borderwidth=0,  # Remove border
            highlightthickness=0  # Remove highlight border
        )
        self.result_text.pack(fill='both', expand=True)
        
        # Scrollbar with minimal styling
        scrollbar = tk.Scrollbar(
            self.result_text,
            width=8,
            troughcolor='#ffffff',
            bg='#dddddd'
        )
        scrollbar.pack(side='right', fill='y')
        self.result_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.result_text.yview)
        
        # Make the window draggable from anywhere
        self.result_text.bind('<Button-1>', self.start_drag)
        self.result_text.bind('<B1-Motion>', self.drag)
        
        # Right-click to close
        self.result_text.bind('<Button-3>', lambda e: self.window.withdraw())
        
        # Initially hide the window
        self.window.withdraw()

    def start_drag(self, event):
        self.x = event.x
        self.y = event.y

    def drag(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.window.winfo_x() + deltax
        y = self.window.winfo_y() + deltay
        self.window.geometry(f"+{x}+{y}")

    def adjust_window_size(self):
        # Get the number of lines in the text
        text_content = self.result_text.get("1.0", tk.END)
        num_lines = len(text_content.split('\n'))
        
        # Calculate required height (each line is approximately 25 pixels)
        # Add extra space for timer and padding
        required_height = min(800, max(100, (num_lines * 25) + 50))
        
        # Get screen dimensions
        screen_width = self.window.winfo_screenwidth()
        window_width = 400
        
        # Position on the right side of the screen
        x = screen_width - window_width - 20  # 20 pixels padding from right edge
        y = 50  # Fixed position from top
        
        # Update window size and position
        self.window.geometry(f"{window_width}x{required_height}+{x}+{y}")

    def show(self):
        self.window.deiconify()
        # Adjust size after a short delay to ensure content is rendered
        self.window.after(100, self.adjust_window_size)

    def set_timer_text(self, text):
        self.timer_label.config(text=text)

    def set_text(self, question, answer="Generating response...", timer_text=""):
        # Store question but don't display it
        self._current_question = question
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert('1.0', answer)
        self.set_timer_text(timer_text)
        self.show()

    def update_answer(self, answer, timer_text=""):
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert('1.0', answer)
        self.set_timer_text(timer_text)
        # Adjust window size for new content
        self.adjust_window_size()

class ScreenshotOverlay:
    def __init__(self, callback):
        self.callback = callback
        self.root = tk.Tk()
        self.root.attributes('-alpha', 0.3, '-fullscreen', True, '-topmost', True)
        self.root.configure(bg='grey')

        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        
        self.start_x = None
        self.start_y = None
        self.current_rect = None

        self.canvas.bind('<Button-1>', self.on_click)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)
        # Bind Escape key to cancel
        self.root.bind('<Escape>', self.cancel)
        
        # Add instructions
        self.instructions = tk.Label(
            self.root,
            text="Click and drag to select area. Press Esc to cancel.",
            font=("Helvetica", 16),
            bg='grey',
            fg='white'
        )
        self.instructions.place(relx=0.5, rely=0.1, anchor='center')

    def cancel(self, event=None):
        self.root.destroy()
        self.callback(None)

    def on_click(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def on_drag(self, event):
        if self.current_rect:
            self.canvas.delete(self.current_rect)
        self.current_rect = self.canvas.create_rectangle(
            self.start_x, self.start_y,
            event.x, event.y,
            outline='white',
            fill='white'
        )

    def on_release(self, event):
        if self.start_x is not None:
            x1 = min(self.start_x, event.x)
            y1 = min(self.start_y, event.y)
            x2 = max(self.start_x, event.x)
            y2 = max(self.start_y, event.y)
            
            # Minimum size check
            if x2 - x1 > 10 and y2 - y1 > 10:
                self.root.destroy()
                self.callback((x1, y1, x2, y2))
            else:
                # If selection is too small, clear it
                if self.current_rect:
                    self.canvas.delete(self.current_rect)
                self.start_x = None
                self.start_y = None

class OCRApp:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Get Azure credentials
        self.endpoint = os.getenv('AZURE_VISION_ENDPOINT', '').strip()
        self.api_key = os.getenv('AZURE_VISION_KEY', '').strip()
        self.openai_api_key = os.getenv('OPENAI_API_KEY', '').strip()
        
        if not self.endpoint or not self.api_key:
            messagebox.showerror(
                "Configuration Error",
                "Please set AZURE_VISION_ENDPOINT and AZURE_VISION_KEY in .env file"
            )
            exit(1)

        if not self.openai_api_key:
            messagebox.showerror(
                "Configuration Error",
                "Please set OPENAI_API_KEY in .env file"
            )
            exit(1)
            
        # Initialize OpenAI client with custom httpx client
        http_client = httpx.Client(
            base_url="https://api.openai.com/v1",
            follow_redirects=True
        )
        self.openai_client = OpenAI(
            api_key=self.openai_api_key,
            http_client=http_client
        )
            
        # Ensure endpoint ends with '/'
        if not self.endpoint.endswith('/'):
            self.endpoint += '/'
        
        # Setup window first
        self.window = ctk.CTk()
        self.window.title("OCR Assistant")
        self.window.geometry("800x600")
        self.window.configure(fg_color="#2b2b2b")
        
        # Hide window from taskbar
        self.window.attributes('-alpha', 1)  # Make sure window is visible
        self.window.withdraw()  # Hide the window initially
        
        # Create system tray icon
        self.create_system_tray()
        
        # Now create the StringVar after window initialization
        self.response_format = tk.StringVar(master=self.window, value="Full Response")

        self.selected_image_path = None
        self.screenshot_mode = False
        self.floating_window = FloatingResultWindow()
        self.setup_ui()
        self.setup_screenshot_listener()

    def create_system_tray(self):
        # Create a simple icon (16x16 pixels)
        icon_size = (16, 16)
        icon_image = Image.new('RGB', icon_size, color='black')
        
        # Create menu items
        menu = (
            item('Show', self.show_window),
            item('Hide', self.hide_window),
            item('Exit', self.quit_app)
        )
        
        # Create system tray icon
        self.icon = pystray.Icon("OCR Assistant", icon_image, "OCR Assistant", menu)
        
        # Start system tray icon in a separate thread
        threading.Thread(target=self.icon.run, daemon=True).start()

    def show_window(self):
        self.window.deiconify()
        self.window.lift()
        self.window.focus_force()

    def hide_window(self):
        self.window.withdraw()

    def quit_app(self):
        self.icon.stop()
        self.window.quit()

    def setup_screenshot_listener(self):
        # Register the keyboard shortcut (Ctrl+Shift+S)
        keyboard.on_press_key("s", self.handle_screenshot_key)
        
    def handle_screenshot_key(self, e):
        if keyboard.is_pressed('ctrl+shift'):
            self.start_screenshot()

    def start_screenshot(self):
        if not self.screenshot_mode:
            self.screenshot_mode = True
            # Close the previous floating window if it exists
            self.floating_window.window.withdraw()
            self.window.iconify()  # Minimize the window
            self.window.after(100, self.show_selection_overlay)

    def show_selection_overlay(self):
        overlay = ScreenshotOverlay(self.handle_selection)

    def handle_selection(self, region):
        if region is None:
            # Selection was cancelled
            self.screenshot_mode = False
            return

        try:
            # Create a temporary directory if it doesn't exist
            temp_dir = os.path.join(tempfile.gettempdir(), "ocr_screenshots")
            os.makedirs(temp_dir, exist_ok=True)

            # Take the screenshot of selected region
            screenshot = pyautogui.screenshot(region=region)
            
            # Save the screenshot with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = os.path.join(temp_dir, f"screenshot_{timestamp}.png")
            screenshot.save(screenshot_path)
            
            # Process the screenshot without showing main window
            self.selected_image_path = screenshot_path
            self.process_image(show_main=False)
            
        except Exception as e:
            messagebox.showerror("Screenshot Error", str(e))
        finally:
            self.screenshot_mode = False

    def setup_ui(self):
        # Main frame
        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title with shortcut info
        title_frame = ctk.CTkFrame(self.main_frame)
        title_frame.pack(fill="x", pady=20)
        
        title = ctk.CTkLabel(
            title_frame,
            text="OCR Desktop Application",
            font=("Helvetica", 24, "bold")
        )
        title.pack(pady=(0, 5))
        
        shortcut_label = ctk.CTkLabel(
            title_frame,
            text="Press Ctrl+Shift+S to take a screenshot",
            font=("Helvetica", 12)
        )
        shortcut_label.pack()

        # Image preview frame
        self.preview_frame = ctk.CTkFrame(self.main_frame)
        self.preview_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Default preview label
        self.preview_label = ctk.CTkLabel(
            self.preview_frame,
            text="No image selected\nUse Ctrl+Shift+S to take a screenshot or select an image file",
            font=("Helvetica", 16)
        )
        self.preview_label.pack(expand=True)

        # Button frame
        button_frame = ctk.CTkFrame(self.main_frame)
        button_frame.pack(fill="x", padx=10, pady=10)

        # Left side buttons
        left_buttons_frame = ctk.CTkFrame(button_frame, fg_color="transparent")
        left_buttons_frame.pack(side="left", fill="x")

        # Select Image button
        self.select_btn = ctk.CTkButton(
            left_buttons_frame,
            text="Select Image",
            command=self.select_image,
            font=("Helvetica", 14)
        )
        self.select_btn.pack(side="left", padx=5)

        # Screenshot button
        self.screenshot_btn = ctk.CTkButton(
            left_buttons_frame,
            text="Take Screenshot (Ctrl+Shift+S)",
            command=self.start_screenshot,
            font=("Helvetica", 14)
        )
        self.screenshot_btn.pack(side="left", padx=5)

        # Process Image button
        self.process_btn = ctk.CTkButton(
            left_buttons_frame,
            text="Process Image",
            command=self.process_image,
            state="disabled",
            font=("Helvetica", 14)
        )
        self.process_btn.pack(side="left", padx=5)

        # Close Windows button
        self.close_btn = ctk.CTkButton(
            left_buttons_frame,
            text="Close All Windows",
            command=self.close_all_windows,
            font=("Helvetica", 14)
        )
        self.close_btn.pack(side="left", padx=5)

        # Right side controls
        right_controls_frame = ctk.CTkFrame(button_frame, fg_color="transparent")
        right_controls_frame.pack(side="right", fill="x")

        # Response format dropdown
        self.format_dropdown = ctk.CTkOptionMenu(
            right_controls_frame,
            values=["Full Response", "Answer Only"],
            variable=self.response_format,
            font=("Helvetica", 14)
        )
        self.format_dropdown.pack(side="right", padx=5)
        
        format_label = ctk.CTkLabel(
            right_controls_frame,
            text="Response Format:",
            font=("Helvetica", 14)
        )
        format_label.pack(side="right", padx=5)

        # Result text area
        self.result_text = ctk.CTkTextbox(
            self.main_frame,
            height=150,
            font=("Helvetica", 14)
        )
        self.result_text.pack(fill="x", padx=10, pady=10)

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self.main_frame)
        self.progress_bar.pack(fill="x", padx=10, pady=10)
        self.progress_bar.set(0)
        self.progress_bar.pack_forget()

    def select_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff")
            ]
        )
        if file_path:
            self.selected_image_path = file_path
            self.display_image(file_path)
            self.process_btn.configure(state="normal")
            self.result_text.delete("1.0", tk.END)

    def display_image(self, image_path):
        # Load and resize image for preview
        image = Image.open(image_path)
        # Calculate aspect ratio
        aspect_ratio = image.width / image.height
        new_width = 400
        new_height = int(new_width / aspect_ratio)
        
        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        
        # Update preview
        if hasattr(self, 'image_label'):
            self.image_label.destroy()
        
        self.image_label = tk.Label(self.preview_frame, image=photo)
        self.image_label.image = photo
        self.preview_label.pack_forget()
        self.image_label.pack(expand=True)
        self.process_btn.configure(state="normal")

    def process_image(self, show_main=True):
        self.process_btn.configure(state="disabled")
        self.select_btn.configure(state="disabled")
        self.screenshot_btn.configure(state="disabled")
        
        if show_main:
            self.progress_bar.pack(fill="x", padx=10, pady=10)
        self.progress_bar.set(0.2)
        
        # Start processing in a separate thread
        thread = threading.Thread(target=lambda: self.perform_ocr(show_main))
        thread.start()

    def get_gpt4_response(self, question):
        try:
            # Detect if it's a technical or behavioral question
            question_type_response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert at classifying interview questions. Respond with only 'technical' or 'behavioral'."},
                    {"role": "user", "content": f"Is this a technical or behavioral interview question? Question: {question}"}
                ]
            )
            
            question_type = question_type_response.choices[0].message.content.lower()
            is_full_response = self.response_format.get() == "Full Response"

            # Prepare system prompt based on question type and response format
            if question_type == "technical":
                if is_full_response:
                    system_prompt = """You are an expert technical interviewer. Provide a clear, concise, and technically accurate response to the interview question. 
                    Include code examples if relevant. Format your response in a structured way:
                    1. Direct Answer
                    2. Technical Explanation
                    3. Example (with code if applicable)
                    4. Best Practices/Tips"""
                else:
                    system_prompt = """You are an expert technical interviewer. Provide only a direct, concise answer to the technical question without additional explanation or examples."""
            else:
                if is_full_response:
                    system_prompt = """You are an expert behavioral interviewer. Provide a response using the STAR method:
                    1. Situation: Set up a relevant example
                    2. Task: What was required
                    3. Action: What you did
                    4. Result: The outcome
                    Make the response personal and authentic while highlighting key soft skills."""
                else:
                    system_prompt = """You are an expert behavioral interviewer. Provide a brief, direct answer focusing only on the key points, without using the STAR method or detailed examples."""

            # Get GPT-4 response
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ]
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {str(e)}"

    def perform_ocr(self, show_main=True):
        try:
            start_time = time.time()
            
            if show_main:
                self.result_text.delete("1.0", tk.END)
                self.result_text.insert("end", "Processing image...\n")
            self.floating_window.set_text("Processing image...")
            
            # Read the image file
            with open(self.selected_image_path, "rb") as image_file:
                image_data = image_file.read()

            # API endpoints
            vision_url = f"{self.endpoint}vision/v3.2/read/analyze"
            
            # Request headers
            headers = {
                'Ocp-Apim-Subscription-Key': self.api_key,
                'Content-Type': 'application/octet-stream'
            }

            # Call Azure's OCR API
            self.progress_bar.set(0.4)
            response = requests.post(vision_url, headers=headers, data=image_data)
            
            if response.status_code != 202:
                raise Exception(f"Request failed with status {response.status_code}")

            # Get the operation location URL
            operation_url = response.headers["Operation-Location"]

            # Wait for the operation to complete
            while True:
                time.sleep(1)
                response = requests.get(operation_url, headers={
                    'Ocp-Apim-Subscription-Key': self.api_key
                })
                result = response.json()

                if result.get("status") not in ["notStarted", "running"]:
                    break

            self.progress_bar.set(0.8)

            # Extract and display the text
            if result.get("status") == "succeeded":
                text_results = []
                for read_result in result.get("analyzeResult", {}).get("readResults", []):
                    for line in read_result.get("lines", []):
                        text_results.append(line.get("text", ""))
                
                # Get the question text
                question_text = "\n".join(text_results)
                
                # Calculate OCR processing time
                ocr_time = time.time() - start_time
                timer_text = f"OCR processing time: {ocr_time:.2f}s"
                
                # Show the question and "Generating response..." message
                self.floating_window.set_text(question_text, timer_text=timer_text)
                if show_main:
                    self.result_text.insert("end", f"\n{timer_text}\n\nGenerating GPT-4 response...")
                
                # Get GPT-4 response in a separate thread
                def get_response():
                    gpt_start_time = time.time()
                    response = self.get_gpt4_response(question_text)
                    gpt_time = time.time() - gpt_start_time
                    total_time = time.time() - start_time
                    
                    timer_text = f"OCR processing: {ocr_time:.2f}s\nGPT-4 response: {gpt_time:.2f}s\nTotal time: {total_time:.2f}s"
                    self.floating_window.update_answer(response, timer_text=timer_text)
                    
                    if show_main:
                        self.result_text.delete("1.0", tk.END)
                        self.result_text.insert("end", f"{response}\n\n{timer_text}")
                
                threading.Thread(target=get_response).start()
                
            else:
                error_msg = "Failed to process the image"
                messagebox.showerror("Error", error_msg)
                self.floating_window.set_text(error_msg)

            self.progress_bar.set(1.0)
            
        except Exception as e:
            error_msg = f"An error occurred: {str(e)}"
            messagebox.showerror("Error", error_msg)
            self.floating_window.set_text(error_msg)
        
        finally:
            if show_main:
                self.progress_bar.pack_forget()
            self.process_btn.configure(state="normal")
            self.select_btn.configure(state="normal")
            self.screenshot_btn.configure(state="normal")

    def close_all_windows(self):
        # Close the floating window
        self.floating_window.window.withdraw()

    def run(self):
        # Show window initially
        self.show_window()
        self.window.mainloop()

if __name__ == "__main__":
    app = OCRApp()
    app.run() 