# -*- coding: utf-8 -*-
"""
Uvicorn configuration for development.
This file is used to configure reload exclusions and other settings.
"""

# Directories and patterns to exclude from reload watching
reload_excludes = [
    ".venv/*",
    "venv/*",
    "*.pyc",
    "__pycache__/*",
    "gen2kgbot/*",
    ".git/*",
    "*.log",
    "data/*",
    "tests/*",
]

# Directories to include for reload watching
reload_includes = [
    "*.py",
]
