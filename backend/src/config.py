EXCLUDED_DIRS = {
    'node_modules', 'venv', '.venv', 'env', '.env', '.git', '__pycache__',
    'build', 'dist', '.idea', '.vscode'
}

# List of file extensions to exclude
EXCLUDED_EXTENSIONS = {
    # Binary files
    '.pyc', '.pyo', '.pyd', '.obj', '.exe', '.dll', '.so', '.dylib',
    # Image files
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.ico',
    # Audio/Video files
    '.mp3', '.mp4', '.avi', '.mov',
    # Archive files
    '.zip', '.tar', '.gz', '.rar',
    # Database files
    '.db', '.sqlite', '.sqlite3',
    # Other non-text files
    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
    # Large data files
    '.csv', '.json', '.xml',
    # Configuration files
    '.gitignore'
}

INCLUDED_LANGUAGE_WITH_EXTENSION = {
    "cpp",
    "go",
    "java",
    "kotlin",
    "js",
    "ts",
    "php",
    "proto",
    "python",
    "rst",
    "ruby",
    "rust",
    "scala",
    "swift",
    "markdown",
    "latex",
    "html",
    "sol",
    "csharp",
    "cobol",
    "c",
    "lua",
    "perl",
    "haskell"
}

OTHER_ALLOWED_CONFIG_EXT = {
    "yaml", "yml", "json", "toml", "ini",
    "cfg", "conf", "properties", "env"
}
