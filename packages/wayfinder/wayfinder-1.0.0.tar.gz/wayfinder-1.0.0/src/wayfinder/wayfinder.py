#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 14:29:58 2022

@author: user
"""

import warnings
import json
import pathlib
from pathlib import Path
import os



routes = {}

def set_route(name, path):
    
    routes[name] = convert(path)


class PathFinder:

    def __init__(self, raise_errors=True):
        self.raise_errors = raise_errors

    def find_file(self, filename, waypoint=Path.cwd(), ext="", down_to=None):
        path = waypoint
        collection = [path for path in Path(path).glob(
            f'**/*{ext}') if filename in path.as_posix()]

        while path.name != down_to:
            if collection:
                break
            path = path.parent
            collection = [path for path in Path(path).glob(
                f'**/*{ext}') if filename in path.as_posix()]

        self.warning(collection, filename)

        return collection

    def find_folder(self, foldername, waypoint=Path.cwd(), down_to=None):

        path = waypoint
        collection = [path for path in Path(path).glob(
            '**/*') if foldername == path.name and path.is_dir()]

        while path.name != down_to:
            if collection:
                break
            path = path.parent
            collection = [path for path in Path(path).glob(
                '**/*') if foldername == path.name and path.is_dir()]

        # collection =  list(dict.fromkeys(collection)) #check to eliminate multiples of the same element
        self.warning(collection, foldername)

        return collection

    def warning(self, collection, item_name):

        if not collection and self.raise_errors:
            raise OSError(f"{item_name} not found.")

        elif not collection and not self.raise_errors:
            warnings.warn(f"{item_name} not found")

        if len(collection) > 1:
            warnings.warn(f"{len(collection)} items called {item_name} found.")



def convert(path):
    
    return Path(path) if isinstance(path, str) and Path(path).exists() else path


class Configure:

    def __init__(self, config_file=None, save_as=False):
        
        default = Path.cwd().joinpath("local_configuration.json")
        self.config_path = None
        self.PATHS = {"PATHS": {}, "WAYPOINTS": {}}
        self.PathFinder = PathFinder(raise_errors=False)
         
        if config_file: 
            config_path = convert(config_file)
            self.config_name = config_path.name
        
            if not config_path.exists(): 
        
                collection = self.PathFinder.find_file(self.config_name, down_to=None)
        
                if len(collection) > 1:
                    raise ValueError("Too many configuration files found.", 
                                 f"Check your folder tree for duplicates of {self.config_name}.")
                    config_path = collection[0]
                    
            self.load_configuration(config_path)

        for key, value in routes.items():
            self.set_waypoint(key, value)
        
        self.entries = [key for dic in self.PATHS.values() for key in dic.keys()]

        if save_as: self.save(default)
        
    def load_configuration(self, config_path):
        
        with config_path.open() as f:
            config = json.load(f)
            PROJECT_PATHS = {key: Path(path)
                     for key, path in config["PATHS"].items()}
            WAYPOINTS = {key: Path(path)
                     for key, path in config["WAYPOINTS"].items()}

        self.PATHS = {"PATHS": PROJECT_PATHS, "WAYPOINTS": WAYPOINTS}
        self.config = config_path
        
    def parse_waypoints(self,):
        
        self.home = Path(os.path.commonpath([*self.PATHS["WAYPOINTS"].values()]))
        
        for waypoint, path in self.PATHS["WAYPOINTS"].items(): setattr(self, waypoint, path)
            
        
    def set_waypoint(self, waypoint, path):
        
        if waypoint not in self.PATHS["WAYPOINTS"].keys():
            self.update(path, waypoint=Path.cwd(), down_to=Path.home().name, 
                                            update="waypoints", label=waypoint)
        
        self.parse_waypoints()
        
    def __call__(self, target, waypoint=None, down_to=None, update_file=True):

        waypoint = convert(waypoint)

        if not waypoint: waypoint = self.home
            
        if not down_to: down_to = waypoint.name
  
        if  waypoint.name not in self.entries and waypoint != self.home:
            print(f"Waypoint {waypoint.name} not found. Defaulting to {self.home}.")
            waypoint = self.home
        
        for key, value in self.PATHS["WAYPOINTS"].items():
            
            if target==value.name: 
                print(f"{target} is a WAYPOINT. No update necessary.")
                return value
        
        if target not in self.entries:
            self.update(target, waypoint, down_to, update="PATHS")
            if update_file: self.save()

        return self.PATHS["PATHS"][target]

    def update(self, folder, waypoint, down_to, update, label=None):

        folder = convert(folder)

        if not isinstance(folder, pathlib.PurePath):
            collection = self.PathFinder.find_folder(folder, waypoint=waypoint, down_to=down_to)

            if len(collection) > 1:
                raise ValueError("Configuration entries must be unique.", 
                                 "Found too many folders with the same name.")

            folder = collection[0]

        if isinstance(update, str): update = update.upper()

        self.PATHS[update or "PATHS"][label or folder.name] = folder
        self.entries = [key for dic in self.PATHS.values() for key in dic.keys()]

        print(f"configuration entry created for {folder}.")

    def save(self, config=None):

        config = config or self.config
        with open(config, "w") as f:

            FOLDERS_as_posix = {key: path.as_posix()
                                for key, path in self.PATHS["PATHS"].items()}
            WAYPOINTS_as_posix = {key: path.as_posix()
                                  for key, path in self.PATHS["WAYPOINTS"].items()}

            json.dump({"PATHS": FOLDERS_as_posix,
                      "WAYPOINTS": WAYPOINTS_as_posix}, f)
        
        self.config = config
        print("Configuration file updated successfully.")
