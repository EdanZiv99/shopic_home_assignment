import sys
from pathlib import Path

# Add the project root (parent of 'tests/') to sys.path so 'pages/' is importable
sys.path.append(str(Path(__file__).resolve().parent.parent))
