VENV = .venv

install: Install activity dependencies using pip, uv, pipx, or any other package manager
of your choice.
• run: Execute the main script of your activity (e.g., via Python interpreter).
• debug: Run the main script in debug mode using Python’s built-in debugger (e.g., pdb).
• clean: Remove temporary files or caches (e.g., __pycache__, .mypy_cache) to keep
the activity environment clean
 lint: flake8 . and mypy . --warn-return-any --warn-unused-ignores
--ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
Run with: make lint.
• lint-strict (optional): flake8 . and mypy . --strict
Run with: make lint-strict
