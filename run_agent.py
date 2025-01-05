import argparse, sys
import tkinter as tk
from threading import Lock
from ai_character import AICharacterAgent

class FullscreenDisplayAgent(AICharacterAgent):
    def __init__(self, config_path, debug=False):
        super().__init__(config_path, debug)
        self.display_lock = Lock()
        self.root = None
        self.label = None
        self._setup_display()
        self.add_display_callback(self._show_display)
    
    def _setup_display(self):
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.configure(background='black')
        
        # Create label for text
        self.label = tk.Label(
            self.root,
            text="",
            fg='white',
            bg='black',
            wraplength=self.root.winfo_screenwidth() - 40,  # Leave some margin
            justify="center"
        )
        self.label.pack(expand=True)
        
        # Bind escape key to toggle fullscreen
        self.root.bind('<Escape>', lambda e: self.root.attributes('-fullscreen', False))
        self.root.bind('<F11>', lambda e: self.root.attributes('-fullscreen', True))
        
        # Update the window without blocking
        self.root.update()
    
    def _show_display(self, text):
        with self.display_lock:
            if text:
                # Clear existing text
                self.label.config(text="")
                self.root.update()
                
                # Start with a large font size and adjust down if needed
                font_size = 100
                self.label.config(font=('Arial', font_size))
                self.label.config(text=text)
                
                # Adjust font size until text fits
                while (self.label.winfo_reqwidth() > self.root.winfo_width() * 0.9 or 
                       self.label.winfo_reqheight() > self.root.winfo_height() * 0.9) and font_size > 10:
                    font_size -= 5
                    self.label.config(font=('Arial', font_size))
                
                self.root.update()
            else:
                self.label.config(text="")
                self.root.update()
    
    def run(self):
        """Override run to handle GUI updates"""
        try:
            super().run()
        finally:
            if self.root:
                self.root.destroy()
    
    def stop(self):
        """Override stop to cleanup GUI"""
        super().stop()
        if self.root:
            self.root.quit()

def main():
    parser = argparse.ArgumentParser(description="Runner for AICharacterAgent")
    parser.add_argument("--config", required=True, help="Path to config YAML")
    parser.add_argument("--debug", action="store_true", help="Enable debug")
    args = parser.parse_args()

    agent = FullscreenDisplayAgent(args.config, debug=args.debug)
    try:
        agent.run()
    except KeyboardInterrupt:
        agent.stop()
        print("\nStopped by user.")
        sys.exit(0)

if __name__ == "__main__":
    main()
