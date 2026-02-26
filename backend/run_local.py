"""Development server runner."""

import sys
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "ecommerce.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
