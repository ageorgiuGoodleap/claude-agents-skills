# Python Best Practices Stack

## 1. Style and Documentation

### PEP 8 - Style Guide
* Follow PEP 8 for consistent, readable formatting
* Maximum line length: 88 characters (Black default) or 79 (PEP 8 strict)
* 4 spaces for indentation (never tabs)
* 2 blank lines between top-level definitions
* 1 blank line between method definitions
* Imports grouped: standard library, third-party, local (alphabetically sorted within groups)
* Reference: https://peps.python.org/pep-0008/

### PEP 257 - Docstring Conventions
* Use triple double-quotes for all docstrings: `"""Docstring"""`
* One-line docstrings: `"""Do X and return Y."""` (period at end, imperative mood)
* Multi-line docstrings: summary line, blank line, detailed description
* Document all public modules, functions, classes, and methods
* Reference: https://peps.python.org/pep-0257/

## 2. Types and Correctness

### Type Hints (PEP 484)
* Use type hints at public boundaries and complex logic
* Always annotate function signatures: `def func(x: int, y: str) -> bool:`
* Use `Optional[T]` for values that can be None
* Use `Union[A, B]` for multiple possible types
* Use `list[str]`, `dict[str, int]` (Python 3.9+) or `List[str]`, `Dict[str, int]` (3.8)
* Use Protocol for structural subtyping
* Reference: https://peps.python.org/pep-0484/

### Static Type Checking with mypy
* Run mypy to catch type errors before runtime: `mypy src/`
* Enable strict mode for new projects: `mypy --strict src/`
* Configure in `pyproject.toml`:
  ```toml
  [tool.mypy]
  python_version = "3.11"
  warn_return_any = true
  warn_unused_configs = true
  disallow_untyped_defs = true
  ```
* Reference: https://www.mypy-lang.org/

## 3. Formatting and Linting

### Black - Autoformatter
* Use Black to eliminate formatting debates
* Run: `black .`
* Configure in `pyproject.toml`:
  ```toml
  [tool.black]
  line-length = 88
  target-version = ['py311']
  ```
* Reference: https://github.com/psf/black

### Ruff - Fast Linter
* Ruff replaces Flake8, isort, pydocstyle, pyupgrade, and more
* Run: `ruff check .` (linting) and `ruff format .` (formatting)
* Configure in `pyproject.toml`:
  ```toml
  [tool.ruff]
  line-length = 88
  target-version = "py311"

  [tool.ruff.lint]
  select = ["E", "F", "I", "N", "UP", "S", "B", "A", "C4", "DTZ", "T10", "DJ", "EM", "G", "PIE", "T20", "Q"]
  ignore = ["E501"]  # Black handles line length
  ```
* Reference: https://docs.astral.sh/ruff/

## 4. Testing

### pytest - Testing Framework
* Use pytest for readable, scalable tests
* Run: `pytest` or `pytest tests/` or `pytest -v` (verbose)
* Name test files: `test_*.py` or `*_test.py`
* Name test functions: `test_*`
* Use fixtures for setup/teardown
* Use parametrize for multiple test cases: `@pytest.mark.parametrize("input,expected", [...])`
* Configure in `pyproject.toml`:
  ```toml
  [tool.pytest.ini_options]
  testpaths = ["tests"]
  python_files = ["test_*.py"]
  python_functions = ["test_*"]
  addopts = "-ra -q --strict-markers"
  ```
* Reference: https://docs.pytest.org/

### Coverage
* Measure test coverage: `pytest --cov=src --cov-report=term-missing`
* Aim for >80% coverage on critical paths
* Configure in `pyproject.toml`:
  ```toml
  [tool.coverage.run]
  source = ["src"]
  omit = ["*/tests/*", "*/test_*.py"]

  [tool.coverage.report]
  exclude_lines = ["pragma: no cover", "def __repr__", "raise AssertionError", "raise NotImplementedError", "if __name__ == .__main__.:"]
  ```

## 5. Project Configuration

### pyproject.toml
* Centralize all tool configuration in `pyproject.toml`
* Used by: pip, build, setuptools, black, ruff, mypy, pytest, coverage
* Example structure:
  ```toml
  [project]
  name = "my-package"
  version = "0.1.0"
  description = "A brief description"
  requires-python = ">=3.11"
  dependencies = ["requests>=2.28.0"]

  [project.optional-dependencies]
  dev = ["pytest>=7.0", "black>=23.0", "ruff>=0.1.0", "mypy>=1.0"]

  [build-system]
  requires = ["setuptools>=68.0"]
  build-backend = "setuptools.build_meta"
  ```
* Reference: https://packaging.python.org/en/latest/guides/writing-pyproject-toml/

## 6. Concrete Python Rules That Keep Code Clean

### Exception Handling
* Prefer explicit exceptions over sentinel return values (no `-1` or `None` for errors)
* Do not catch broad exceptions unless you rethrow or add context:
  ```python
  # Bad
  try:
      do_something()
  except Exception:
      pass

  # Good
  try:
      do_something()
  except ValueError as e:
      logger.error(f"Invalid input: {e}")
      raise
  ```
* Use custom exceptions for domain errors: `class InvalidUserError(Exception): ...`

### I/O at the Edges
* Keep core logic pure and deterministic
* Push I/O (file, network, database) to the edges
* Pass data in, return data out:
  ```python
  # Good - pure function
  def calculate_total(items: list[Item]) -> Decimal:
      return sum(item.price for item in items)

  # Bad - I/O mixed with logic
  def calculate_total(db_connection) -> Decimal:
      items = db_connection.query("SELECT * FROM items")
      return sum(item.price for item in items)
  ```

### Avoid Global State
* Pass dependencies explicitly via function parameters or class constructors
* Use dependency injection instead of global singletons:
  ```python
  # Good
  def process_order(order: Order, db: Database, mailer: EmailService) -> None:
      db.save(order)
      mailer.send_confirmation(order.customer)

  # Bad
  def process_order(order: Order) -> None:
      DATABASE.save(order)  # Global dependency
      MAILER.send_confirmation(order.customer)  # Global dependency
  ```

### Dataclasses for Plain Data
* Use `@dataclass` for simple data containers
* Automatic `__init__`, `__repr__`, `__eq__`
* Add `frozen=True` for immutability
  ```python
  from dataclasses import dataclass

  @dataclass(frozen=True)
  class User:
      id: int
      name: str
      email: str
  ```

### Small Public APIs
* Keep module public APIs small and focused
* Hide internals behind underscore names: `_internal_helper()`
* Use `__all__` to explicitly define public API:
  ```python
  # mymodule.py
  __all__ = ["PublicClass", "public_function"]

  class PublicClass: ...
  def public_function(): ...
  def _internal_helper(): ...  # Not exported
  ```

### Single Responsibility
* Functions and classes should do one thing
* If a function name contains "and", it likely does too much
* Keep functions under 20-30 lines when possible
* Extract complex conditionals into named functions:
  ```python
  # Good
  def is_eligible_for_discount(user: User) -> bool:
      return user.is_premium and user.orders_count > 10

  if is_eligible_for_discount(user):
      apply_discount()

  # Bad
  if user.is_premium and user.orders_count > 10:
      apply_discount()  # What does this condition mean?
  ```

### Composition Over Inheritance
* Prefer composition unless inheritance truly models the domain
* Use protocols for duck typing instead of deep inheritance hierarchies
* Favor small, focused classes with clear responsibilities

### Type Boundaries
* Validate untrusted inputs at boundaries
* Convert to typed domain objects early
* Fail fast with clear error messages:
  ```python
  def create_user(data: dict) -> User:
      # Validate at boundary
      if "email" not in data or "@" not in data["email"]:
          raise ValueError("Invalid email format")

      # Convert to typed object
      return User(
          id=int(data["id"]),
          name=str(data["name"]),
          email=str(data["email"])
      )
  ```
