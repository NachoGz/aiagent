# AI Agent

A simple CLI tool that provides an AI coding agent powered by Google's Gemini AI. The agent can interact with your codebase by reading files, writing code, and executing Python scripts to help debug issues and implement features.

## Features

- **File Operations**: List directories, read file contents, and write/modify files
- **Code Execution**: Run Python scripts with optional arguments
- **Bug Fixing**: Automatically investigate and fix code issues
- **Security**: Sandboxed file operations restricted to a working directory

## Installation

1. Clone the repository:
```bash
git clone https://github.com/NachoGz/aiagent.git
cd aiagent
```

2. Create a virtual environment at the top level of your project directory
```bash
uv venv
```

3. Activate the virtual environment:
```bash
source .venv/bin/activate
```

4. Install dependencies using uv:
```bash
uv pip install .
```

5. Set up your Gemini API key:
```bash
# Create a .env file
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

## Usage

### Basic Usage

```bash
uv run main.py "<your prompt>"
```

### Verbose Mode

Use the `-v` flag to see detailed information about function calls and token usage:

## How It Works

The AI agent operates within a sandboxed environment (set in `functions/config.py`) and can perform these operations:

1. **get_files_info**: List files and directories with sizes
2. **get_file_content**: Read the contents of files
3. **write_file**: Create or modify files
4. **run_python_file**: Execute Python scripts with optional arguments

## Configuration

### Working Directory
By default, the agent operates in the `./calculator` directory. You can change this in `functions/config.py`:

```python
CWD = "./your-project-directory"
```

### File Size Limits
Large files are automatically truncated to prevent token limit issues:

```python
MAX_CHARS = 10000  # Maximum characters per file
```

### Execution Timeout
Python script execution has a safety timeout:

```python
TIMEOUT = 30  # seconds
```

## Security Features

- **Path Traversal Protection**: All file operations are restricted to the working directory
- **File Type Validation**: Only Python files can be executed
- **Execution Timeout**: Scripts are automatically terminated after the timeout period
- **Read-Only Truncation**: Large files are truncated in memory without modifying originals

## Requirements
- Python 3.9+
- Google Gemini API key
- uv package manager

## Dependencies

- `google-genai==1.12.1`: Official Google Gemini AI client
- `python-dotenv==1.1.0`: Environment variable management
