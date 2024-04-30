import os
import json

class Config:
    def __init__(self) -> None:
        if self.find_config() is None:
            if self.find_config(True) is not None:
                with open(self.find_config(True), "r") as file:
                    with open(self.find_config(True).replace(".example", ""), "w") as new_file:
                        new_file.write(file.read())
            
            raise FileNotFoundError("Config file not found, if the config.example.json file exists, it has been copied to config.json, please fill out the config.json file with the correct values")
        
        self.data_path = self.find_config().removesuffix("config.json")
        
        with open(self.find_config(), "r") as file:
            self.data = json.load(file)
            
    def find_config(self, example: bool = False) -> str:
        """
        Finds the config file in the current directory

        Args:
            example (bool, optional): Whether to find the example config file. Defaults to False.

        Returns:
            str: The path to the config file
        """
        
        search = "config.example.json" if example else "config.json"
        
        for dirpath, dirnames, filenames in os.walk("."):
            if search in filenames:
                return os.path.join(dirpath, search)
            
        return None
            
    def get(self, key: str) -> str:
        """
        Gets the key from the config

        Args:
            key (str): The key to get from the config

        Returns:
            str: The value of the key
        """
        
        return self.data[key]

    def set(self, key: str, value: str) -> None:
        """
        Sets the key in the config

        Args:
            key (str): The key to set in the config
            value (str): The value to set for the key
        """
        
        self.data = {**self.data, key: value}
        
        with open("config.json", "w") as file:
            json.dump(self.data, file, indent=4)
            
config = Config()