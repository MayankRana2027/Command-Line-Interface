"""
GUI interface for CCLI
Handles the tkinter-based user interface
"""

import tkinter as tk
from tkinter import scrolledtext
from environment import CCLIEnvironment
from executor import CommandExecutor

class CCLIGUI:
    """Main GUI class for CCLI"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("CCLI - Custom Command Line Interface")
        self.root.geometry("900x600")
        
        # Set colors
        self.bg_color = '#0C0C0C'
        self.fg_color = '#CCCCCC'
        self.prompt_color = '#00FF00'
        self.error_color = '#FF5555'
        self.success_color = '#50FA7B'
        self.info_color = '#8BE9FD'
        self.dir_color = '#BD93F9'
        
        # Configure root window
        self.root.configure(bg=self.bg_color)
        
        # Create environment and executor
        self.env = CCLIEnvironment()
        self.executor = CommandExecutor(self.env, self.display_output)
        
        # History navigation
        self.history_index = -1
        
        self.setup_ui()
        self.display_welcome()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Create main frame
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title bar
        title_frame = tk.Frame(main_frame, bg='#1E1E1E', height=40)
        title_frame.pack(fill=tk.X, pady=(0, 5))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="╔═══════════════════════════════════════════════════════════════════════════════╗\n"
                 "║           CCLI - Custom Command Line Interface                                ║\n"
                 "╚═══════════════════════════════════════════════════════════════════════════════╝",
            bg='#1E1E1E',
            fg=self.info_color,
            font=('Consolas', 9),
            justify=tk.LEFT
        )
        title_label.pack(pady=5)
        
        # Output text area
        self.output_text = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            bg=self.bg_color,
            fg=self.fg_color,
            insertbackground=self.fg_color,
            font=('Consolas', 10),
            relief=tk.FLAT,
            borderwidth=0
        )
        self.output_text.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        # Configure tags for colored output
        self.output_text.tag_config('prompt', foreground=self.prompt_color, font=('Consolas', 10, 'bold'))
        self.output_text.tag_config('error', foreground=self.error_color)
        self.output_text.tag_config('success', foreground=self.success_color)
        self.output_text.tag_config('info', foreground=self.info_color)
        self.output_text.tag_config('directory', foreground=self.dir_color)
        self.output_text.tag_config('output', foreground=self.fg_color)
        
        # Input frame
        input_frame = tk.Frame(main_frame, bg=self.bg_color)
        input_frame.pack(fill=tk.X)
        
        # Prompt label
        self.prompt_label = tk.Label(
            input_frame,
            text="CCLI>",
            bg=self.bg_color,
            fg=self.prompt_color,
            font=('Consolas', 10, 'bold')
        )
        self.prompt_label.pack(side=tk.LEFT, padx=(0, 5))
        
        # Input entry
        self.input_entry = tk.Entry(
            input_frame,
            bg='#1E1E1E',
            fg=self.fg_color,
            insertbackground=self.fg_color,
            font=('Consolas', 10),
            relief=tk.FLAT,
            borderwidth=2
        )
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.input_entry.focus()
        
        # Bind events
        self.input_entry.bind('<Return>', self.handle_command)
        self.input_entry.bind('<Up>', self.history_up)
        self.input_entry.bind('<Down>', self.history_down)
        
        # Bind close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def display_welcome(self):
        """Display welcome message"""
        welcome = """Welcome to CCLI - Custom Command Line Interface

Type 'help' for available commands or 'exit' to quit.

"""
        self.display_output(welcome, 'info')
    
    def display_output(self, text, tag='output'):
        """Display text in the output area with specified tag"""
        self.output_text.insert(tk.END, text, tag)
        self.output_text.see(tk.END)
    
    def handle_command(self, event):
        """Handle command execution"""
        command = self.input_entry.get().strip()
        self.input_entry.delete(0, tk.END)
        
        if not command:
            return
        
        # Display command with prompt
        self.display_output("CCLI> ", 'prompt')
        self.display_output(command + '\n', 'output')
        
        # Handle exit
        if command.lower() == 'exit':
            self.on_closing()
            return
        
        # Handle clear
        if command.lower() in ['clear', 'cls']:
            self.output_text.delete(1.0, tk.END)
            self.display_welcome()
            return
        
        # Handle last command
        if command.lower() == 'last':
            last_cmd = self.executor.commands.last([])
            if last_cmd:
                command = last_cmd
        
        # Add to history
        self.env.add_to_history(command)
        self.history_index = len(self.env.command_history)
        
        # Execute command
        result = self.executor.execute(command)
        
        # Handle special results
        if result == 'CLEAR':
            self.output_text.delete(1.0, tk.END)
            self.display_welcome()
    
    def history_up(self, event):
        """Navigate up in command history"""
        if self.history_index > 0:
            self.history_index -= 1
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, self.env.command_history[self.history_index])
    
    def history_down(self, event):
        """Navigate down in command history"""
        if self.history_index < len(self.env.command_history) - 1:
            self.history_index += 1
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, self.env.command_history[self.history_index])
        else:
            self.history_index = len(self.env.command_history)
            self.input_entry.delete(0, tk.END)
    
    def on_closing(self):
        """Handle window closing"""
        self.root.destroy()