#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 11:27:51 2022

@author: user
"""

import tomlkit

toml_data = """
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
"""

print(tomlkit.dumps(tomlkit.loads(toml_data)))
