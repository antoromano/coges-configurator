import sys
from pathlib import Path

# Garantisce che 'app' sia importabile indipendentemente dalla cwd da cui
# viene lanciato pytest.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
