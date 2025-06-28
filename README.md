# Arachnida

Arachnida is an advanced web data extraction tool suite for extracting images, emails, and phone numbers from websites. It supports recursive crawling, custom configurations, and a beautiful interactive terminal UI.

## Features
- Extract images, emails, and phone numbers from any website
- Recursive crawling with configurable depth
- Custom extraction options (choose what to extract)
- CLI and interactive menu modes
- Colorful, user-friendly terminal interface

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/aabderrafie/Arachnida.git
   cd Arachnida
   ```

2. **(Recommended) Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
   If you don't have `venv`, install it with:
   ```bash
   python3 -m pip install --user virtualenv
   python3 -m virtualenv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Interactive Mode (Recommended)
Run the main interface:
```bash
python3 main_interface.py
```
Follow the on-screen menu to select extraction options and configure settings.

### CLI Mode
You can also run Arachnida in CLI mode:
```bash
python3 main_interface.py --cli --url <URL> --type <images|emails|phones|all> [-r] [-l DEPTH] [-p OUTPUT_PATH]
```
- `--url`: Website URL to extract from
- `--type`: Extraction type (`images`, `emails`, `phones`, or `all`)
- `-r`: Enable recursive crawling
- `-l`: Maximum depth (default: 5)
- `-p`: Output directory (default: ./data/)

**Example:**
```bash
python3 main_interface.py --cli --url example.com --type all -r -l 3 -p ./output/
```

## Troubleshooting
If you encounter issues running the tool (e.g., missing modules), ensure you have activated your virtual environment and installed all dependencies. If problems persist, try recreating the environment:

```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## License
MIT

## Author
Created by abderrafie
