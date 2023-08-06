import re
from pathlib import Path

current_folder = Path(__file__).parent
README = re.sub('!\[Screenshot\]\(.*\)', '', (current_folder / "README.md").read_text())
print(README)


