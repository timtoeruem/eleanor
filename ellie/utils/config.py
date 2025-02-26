import json
from pathlib import Path

class ConfigManager():
    """Class to manage configuration files using JSON format. """
    def __init__(self, config_file="main_config.json"):
        self.config_file = config_file
    
    def load_config(self):
        """Load configuration from a JSON file and stores it as a object """
        # Check if the file exists
        if not Path(self.config_file).exists():
            raise FileNotFoundError(f"Configuration file {self.config_file} not found.") # Raise an error if the file does not exist
        # Open the file and load the configuration
        with open(self.config_file, 'r') as file:
            self.config = json.load(file)

        # Return the loaded configuration
        return self.config
        
    
    def save_config(self, config_dict):
        with open(self.config_file, 'w') as file:
            json.dump(config_dict, file)

# example usage that will be called if this file is called directly
if __name__ == "__main__":
    config_manager = ConfigManager("config.json")
    config = config_manager.load_config()
    print(config)
    config_manager.save_config({"key": "value"})  # save new configuration
    print("Configuration saved.")  # print confirmation message

