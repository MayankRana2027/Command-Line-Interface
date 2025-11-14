"""
Environment management for CCLI
Handles variables, command history, and aliases
"""

import os

class CCLIEnvironment:
    """Manages the shell environment state"""
    
    def __init__(self):
        self.variables = {
            'PATH': '/usr/local/bin:/usr/bin:/bin',
        }
        self.current_dir = os.getcwd()
        self.command_history = []
        self.aliases = {}
    
    def set_variable(self, name, value):
        """Set an environment variable"""
        self.variables[name] = value
    
    def get_variable(self, name):
        """Get an environment variable value"""
        return self.variables.get(name, '')
    
    def add_to_history(self, command):
        """Add a command to history"""
        self.command_history.append(command)
    
    def get_last_command(self):
        """Get the last executed command"""
        return self.command_history[-1] if self.command_history else ''
    
    def set_alias(self, name, command):
        """Create a command alias"""
        self.aliases[name] = command
    
    def get_alias(self, name):
        """Get a command alias"""
        return self.aliases.get(name)