# Contributing

Pull requests are welcome! 🎉

## Guidelines

### One Change Per PR
Keep pull requests focused on a single feature, bug fix, or improvement. This makes review easier and helps maintain project quality.

### Quality Standards
- **Tests required** - Maintain test coverage standards
- **All tests must pass** - Including existing test suite
- **Follow style conventions** - Use pytest and pytest-mock for testing
- **Respect coverage requirements** - Currently set at 99.5%

### Dependencies Policy
This is a minimal wrapper around `uv run`. Be very thoughtful about proposing new dependencies:

- Currently only `rich` is required (and we might remove it)
- New dependencies need strong justification
- Consider if functionality can be achieved with standard library
- Avoid adding heavy dependencies for minor features

### AI Assistance
AI assistance is welcome alongside manual contributions! This project was largely AI-assisted (using [Zed](https://zed.dev/) with [Claude Sonnet 3.5](https://www.anthropic.com/claude) and [Gemini Flash 2.0](https://deepmind.google/technologies/gemini/flash/)), but all contributions must meet quality standards regardless of how they were created.

## Development Setup

Clone and set up the development environment:

```bash
git clone <repository-url>
cd autopep723
uv sync
```

## Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage report
uv run pytest --cov=autopep723

# Quick test run
uv run pytest -q

# Run specific test file
uv run pytest tests/test_autopep723.py
```

## Code Style

The project uses Ruff for linting and formatting:

```bash
# Check code style
uv run ruff check

# Auto-fix issues
uv run ruff check --fix

# Format code
uv run ruff format
```

## Making Changes

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature-name`
3. **Make** your changes
4. **Add** tests for new functionality
5. **Run** the test suite: `uv run pytest`
6. **Check** code style: `uv run ruff check`
7. **Commit** with a clear message
8. **Push** and create a pull request

## Testing Guidelines

- Use `pytest` for test framework
- Use `pytest-mock` for mocking
- Test both success and failure cases
- Include edge cases in tests
- Maintain high test coverage

Example test structure:

```python
def test_feature_success(mocker):
    # Arrange
    mock_dependency = mocker.patch('module.dependency')
    
    # Act
    result = function_under_test()
    
    # Assert
    assert result == expected_value
    mock_dependency.assert_called_once()
```

## Documentation

Update documentation when making changes:

- Update README.md for user-facing changes
- Add examples to docs/examples.md if relevant
- Update API documentation for interface changes
- Build docs locally: `make docs`

## Code of Conduct

We follow a zero-tolerance policy for harassment of any kind. Be respectful and inclusive in all interactions.

## Other Ways to Contribute

### Review Pull Requests
Reviewing PRs is a valuable way to contribute! Look for open pull requests and provide constructive feedback on code quality, testing, and documentation.

## Questions?

Feel free to open an issue for questions about contributing or to discuss potential changes before implementing them.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.