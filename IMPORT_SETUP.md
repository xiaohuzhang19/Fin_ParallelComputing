# Universal Import Setup for All Notebooks

Add this code block to the **first cell** of any notebook in this project:

```python
import sys
from pathlib import Path

# Universal path setup - works from any directory
notebook_dir = Path.cwd()

# Find project root (Fin_ParallelComputing directory)
if (notebook_dir / 'src').exists():
    project_root = notebook_dir
elif notebook_dir.name == 'src':
    project_root = notebook_dir.parent
elif (notebook_dir.parent / 'src').exists():
    project_root = notebook_dir.parent
else:
    project_root = notebook_dir

# Add paths for both import styles
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

src_dir = project_root / 'src'
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))
```

After adding this setup, you can use **either** import style:

**Style 1 (from parent directory):**
```python
from src.models.mc import hybridMonteCarlo
from src.models.pso import PSO_Numpy
```

**Style 2 (from src directory):**
```python
from models.mc import hybridMonteCarlo
from models.pso import PSO_Numpy
```

Both will work with this setup!
