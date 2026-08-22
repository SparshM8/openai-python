import os
import subprocess
import sys
from pathlib import Path

def test_pydantic_defer_build_env_var():
    """Verify that OPENAI_PYDANTIC_DEFER_BUILD controls Pydantic model building."""
    repo_root = Path(__file__).parent.parent
    src_path = repo_root / "src"
    
    # Test with OPENAI_PYDANTIC_DEFER_BUILD=false
    code = """
import os
os.environ["OPENAI_PYDANTIC_DEFER_BUILD"] = "false"
import openai._models
from pydantic import BaseModel
print(openai._models.BaseModel.model_config.get("defer_build"))
"""
    result = subprocess.run(
        [sys.executable, "-c", code],
        env={**os.environ, "PYTHONPATH": str(src_path)},
        capture_output=True,
        text=True
    )
    assert result.stdout.strip() == "False"

    # Test with OPENAI_PYDANTIC_DEFER_BUILD=true
    code = """
import os
os.environ["OPENAI_PYDANTIC_DEFER_BUILD"] = "true"
import openai._models
print(openai._models.BaseModel.model_config.get("defer_build"))
"""
    result = subprocess.run(
        [sys.executable, "-c", code],
        env={**os.environ, "PYTHONPATH": str(src_path)},
        capture_output=True,
        text=True
    )
    assert result.stdout.strip() == "True"

if __name__ == "__main__":
    try:
        test_pydantic_defer_build_env_var()
        print("Test PASSED")
    except AssertionError as e:
        print(f"Test FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
