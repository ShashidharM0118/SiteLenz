import tkinter as tk
from tkinter import scrolledtext, messagebox
from audio_logger import AudioToTextLogger
import threading

class AudioRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Recorder - Desktop App")
        self.root.geometry("700x600")
        self.root.configure(bg="#f0f0f0")
        
        # Initialize logger
        self.logger = AudioToTextLogger(engine="google")
        self.is_recording = False
        
        # UI Elements
        self.create_widgets()
        
        # Update thread
        self.update_transcripts()
    
    def create_widgets(self):
        # Header Frame
        header_frame = tk.Frame(self.root, bg="#667eea", height=80)
        header_frame.pack(fill=tk.X)
        
        # Title
        title = tk.Label(header_frame, text="🎤 Audio-to-Text Logger", 
                        font=("Arial", 24, "bold"),
                        bg="#667eea", fg="white")
        title.pack(pady=20)
        
        # Main Container
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Buttons Frame
        btn_frame = tk.Frame(main_frame, bg="#f0f0f0")
        btn_frame.pack(pady=10)
        
        # Start Button
        self.start_btn = tk.Button(btn_frame, text="▶ Start Recording",
                                   command=self.start_recording,
                                   bg="#4CAF50", fg="white",
                                   font=("Arial", 14, "bold"),
                                   padx=30, pady=15,
                                   relief=tk.RAISED,
                                   cursor="hand2")
        self.start_btn.grid(row=0, column=0, padx=10)
        
        # Stop Button
        self.stop_btn = tk.Button(btn_frame, text="⏹ Stop Recording",
                                  command=self.stop_recording,
                                  bg="#f44336", fg="white",
                                  font=("Arial", 14, "bold"),
                                  padx=30, pady=15,
                                  relief=tk.RAISED,
                                  state=tk.DISABLED,
                                  cursor="hand2")
        self.stop_btn.grid(row=0, column=1, padx=10)
        
        # Status Frame
        status_frame = tk.Frame(main_frame, bg="white", relief=tk.RIDGE, bd=2)
        status_frame.pack(pady=10, fill=tk.X)
        
        # Status Label
        self.status_label = tk.Label(status_frame, text="⚪ Status: Idle",
                                     font=("Arial", 12, "bold"),
                                     bg="white", fg="#333")
        self.status_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Session Info
        self.session_label = tk.Label(status_frame, text="Session: -",
                                      font=("Arial", 10),
                                      bg="white", fg="#666")
        self.session_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Transcript Count
        self.count_label = tk.Label(status_frame, text="Transcripts: 0",
                                    font=("Arial", 10),
                                    bg="white", fg="#666")
        self.count_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Search Frame
        search_frame = tk.Frame(main_frame, bg="#f0f0f0")
        search_frame.pack(pady=10, fill=tk.X)
        
        tk.Label(search_frame, text="🔍 Search Keywords:",
                font=("Arial", 10, "bold"),
                bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        
        self.search_entry = tk.Entry(search_frame, font=("Arial", 10), width=40)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        
        search_btn = tk.Button(search_frame, text="Search",
                              command=self.search_keywords,
                              bg="#667eea", fg="white",
                              font=("Arial", 10, "bold"),
                              padx=15, pady=5,
                              cursor="hand2")
        search_btn.pack(side=tk.LEFT, padx=5)
        
        # Transcripts Display
        tk.Label(main_frame, text="📝 Transcripts:", 
                font=("Arial", 12, "bold"),
                bg="#f0f0f0").pack(anchor=tk.W, pady=(10, 5))
        
        # Text widget with scrollbar
        text_frame = tk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.transcript_text = scrolledtext.ScrolledText(
            text_frame, width=80, height=15, 
            font=("Consolas", 10),
            bg="white", fg="#333",
            relief=tk.RIDGE, bd=2)
        self.transcript_text.pack(fill=tk.BOTH, expand=True)
        
        # Initial message
        self.transcript_text.insert(tk.END, 
            "No transcripts yet. Click 'Start Recording' to begin.\n\n"
            "Speak clearly into your microphone.\n"
            "Audio will be processed every 5 seconds.")
    
    def start_recording(self):
        """Start recording on button click."""
        try:
            session_id = self.logger.start_recording()
            self.is_recording = True
            
            # Update UI
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.status_label.config(text="🔴 Status: Recording...", fg="red")
            self.session_label.config(text=f"Session: {session_id}")
            
            # Clear transcript display
            self.transcript_text.delete(1.0, tk.END)
            self.transcript_text.insert(tk.END, "🎤 Recording in progress...\n\n")
            
            messagebox.showinfo("Recording Started", 
                              "Recording started!\n\n"
                              "Speak into your microphone.\n"
                              "Audio will be processed every 5 seconds.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start recording:\n{e}")
    
    def stop_recording(self):
        """Stop recording on button click."""
        try:
            summary = self.logger.stop_recording()
            self.is_recording = False
            
            # Update UI
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.status_label.config(text="⚪ Status: Idle", fg="black")
            
            # Show transcripts
            self.update_transcripts()
            
            messagebox.showinfo("Recording Stopped", 
                              f"Recording stopped successfully!\n\n"
                              f"Transcripts: {summary['transcript_count']}\n"
                              f"Session: {summary['session_id']}\n\n"
                              f"Files saved to:\n{summary['transcript_file']}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop recording:\n{e}")
    
    def update_transcripts(self):
        """Update transcript display."""
        if self.is_recording or self.logger.get_transcripts():
            transcripts = self.logger.get_transcripts()
            
            # Update count
            self.count_label.config(text=f"Transcripts: {len(transcripts)}")
            
            if transcripts:
                self.transcript_text.delete(1.0, tk.END)
                for i, t in enumerate(transcripts, 1):
                    timestamp = t['timestamp'].split('T')[1].split('.')[0]
                    self.transcript_text.insert(tk.END, 
                        f"[{i}] {timestamp}\n", "timestamp")
                    self.transcript_text.insert(tk.END, 
                        f"{t['text']}\n\n", "text")
                    self.transcript_text.insert(tk.END, 
                        f"🎵 {t['audio_file']}\n", "audio")
                    self.transcript_text.insert(tk.END, "-" * 70 + "\n\n")
                
                # Configure tags
                self.transcript_text.tag_config("timestamp", foreground="#667eea", font=("Arial", 9, "bold"))
                self.transcript_text.tag_config("text", foreground="#333", font=("Consolas", 10))
                self.transcript_text.tag_config("audio", foreground="#999", font=("Arial", 8, "italic"))
                
                # Auto-scroll to bottom
                self.transcript_text.see(tk.END)
        
        # Schedule next update (every 3 seconds if recording)
        if self.is_recording:
            self.root.after(3000, self.update_transcripts)
    
    def search_keywords(self):
        """Search for keywords in transcripts."""
        keywords_input = self.search_entry.get().strip()
        
        if not keywords_input:
            messagebox.showwarning("No Keywords", "Please enter keywords to search.")
            return
        
        keywords = [k.strip() for k in keywords_input.split(',')]
        matches = self.logger.search_keywords(keywords)
        
        if not matches:
            messagebox.showinfo("No Matches", 
                              f"No matches found for:\n{', '.join(keywords)}")
        else:
            # Display matches
            self.transcript_text.delete(1.0, tk.END)
            self.transcript_text.insert(tk.END, 
                f"🔍 Search Results ({len(matches)} matches)\n"
                f"Keywords: {', '.join(keywords)}\n\n", "header")
            
            for i, match in enumerate(matches, 1):
                timestamp = match['timestamp'].split('T')[1].split('.')[0]
                self.transcript_text.insert(tk.END, 
                    f"[{i}] {timestamp}\n", "timestamp")
                self.transcript_text.insert(tk.END, 
                    f"{match['text']}\n", "text")
                self.transcript_text.insert(tk.END, 
                    f"✓ Matched: {', '.join(match['matched_keywords'])}\n", "match")
                self.transcript_text.insert(tk.END, "-" * 70 + "\n\n")
            
            # Configure tags
            self.transcript_text.tag_config("header", foreground="#667eea", font=("Arial", 12, "bold"))
            self.transcript_text.tag_config("match", foreground="#4CAF50", font=("Arial", 9, "bold"))
            
            messagebox.showinfo("Search Complete", 
                              f"Found {len(matches)} matches!")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = AudioRecorderApp(root)
    
    # Center window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()
