import sys
from pathlib import Path

from streamlit.web import cli as streamlit_cli


def main() -> None:
    app_path = Path(__file__).with_name("cli.py").resolve()
    sys.argv = ["streamlit", "run", str(app_path), *sys.argv[1:]]
    streamlit_cli.main()
