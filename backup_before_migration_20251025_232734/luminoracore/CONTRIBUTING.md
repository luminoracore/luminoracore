# Contributing to LuminoraCore

Thank you for your interest in contributing to LuminoraCore! This document provides guidelines and information for contributors.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct. Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for details.

## How to Contribute

### Reporting Bugs

1. Check existing issues to avoid duplicates
2. Use the bug report template
3. Include:
   - Clear description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, LuminoraCore version)
   - Error logs or screenshots

### Suggesting Features

1. Check existing feature requests
2. Use the feature request template
3. Include:
   - Clear description of the feature
   - Use case and motivation
   - Implementation ideas (if any)
   - Additional context

### Submitting Personalities

1. Use the personality submission template
2. Ensure your personality:
   - Follows the JSON schema
   - Passes validation
   - Includes realistic examples
   - Has appropriate safety guards
   - Is well-documented

## Development Setup

### Prerequisites

- Python 3.8+
- Git
- pip

### Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/luminoracore.git
   cd luminoracore
   ```

3. Install in development mode:
   ```bash
   pip install -e ".[dev]"
   ```

4. Run tests to ensure everything works:
   ```bash
   pytest tests/ -v
   ```

### Development Workflow

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes
3. Run tests and linting:
   ```bash
   pytest tests/ -v
   flake8 luminoracore/ tests/ examples/
   mypy luminoracore/
   ```

4. Commit your changes:
   ```bash
   git commit -m "Add your feature description"
   ```

5. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

6. Create a Pull Request

## Code Style

### Python Code

- Follow PEP 8
- Use type hints
- Write docstrings for all public functions
- Keep functions focused and small
- Use meaningful variable names

### Example:

```python
def compile_personality(personality: Personality, provider: LLMProvider) -> CompilationResult:
    """
    Compile a personality for a specific LLM provider.
    
    Args:
        personality: The personality to compile
        provider: Target LLM provider
        
    Returns:
        CompilationResult with compiled prompt
        
    Raises:
        PersonalityError: If compilation fails
    """
    # Implementation here
```

### JSON Files

- Use 2-space indentation
- Sort keys logically
- Include comments where helpful
- Validate against schema

### Documentation

- Use Markdown for documentation
- Include code examples
- Keep language clear and concise
- Update docs when adding features

## Testing

### Writing Tests

- Write tests for all new functionality
- Use descriptive test names
- Test both success and failure cases
- Aim for high coverage

### Test Structure

```python
class TestYourFeature:
    """Test cases for your feature."""
    
    def test_success_case(self):
        """Test successful operation."""
        # Arrange
        # Act
        # Assert
        
    def test_failure_case(self):
        """Test failure handling."""
        # Arrange
        # Act
        # Assert
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=luminoracore --cov-report=html

# Run specific test file
pytest tests/test_your_feature.py -v

# Run specific test
pytest tests/test_your_feature.py::TestYourFeature::test_specific_case -v
```

## Pull Request Process

### Before Submitting

1. Ensure all tests pass
2. Run linting and fix issues
3. Update documentation if needed
4. Add tests for new functionality
5. Validate all personalities pass validation

### PR Description

Include:
- Description of changes
- Type of change (bug fix, feature, etc.)
- Testing performed
- Screenshots if applicable
- Breaking changes (if any)

### Review Process

1. Automated checks must pass
2. At least one maintainer review required
3. Address feedback promptly
4. Keep PR focused and small when possible

## Personality Guidelines

### Creating New Personalities

1. **Follow the Schema**: Ensure all required fields are present
2. **Be Original**: Create unique, interesting personalities
3. **Include Examples**: Provide realistic sample interactions
4. **Set Safety Guards**: Include appropriate content filters
5. **Test Thoroughly**: Validate and test your personality

### Personality Quality Checklist

- [ ] All required fields present
- [ ] Validates against schema
- [ ] Realistic examples included
- [ ] Appropriate behavioral rules
- [ ] Safety guards in place
- [ ] Clear and engaging description
- [ ] Proper tags and metadata

### Example Personality Structure

```json
{
  "persona": {
    "name": "Your Personality Name",
    "version": "1.0.0",
    "description": "Clear description of what makes this personality unique",
    "author": "Your Name",
    "tags": ["relevant", "tags"],
    "language": "en",
    "compatibility": ["openai", "anthropic"]
  },
  "core_traits": {
    "archetype": "scientist",
    "temperament": "calm",
    "communication_style": "formal"
  },
  "linguistic_profile": {
    "tone": ["professional", "friendly"],
    "syntax": "varied",
    "vocabulary": ["characteristic", "words", "phrases"]
  },
  "behavioral_rules": [
    "Clear behavioral guideline 1",
    "Clear behavioral guideline 2",
    "Clear behavioral guideline 3"
  ]
}
```

## Documentation

### Updating Documentation

- Update relevant docs when adding features
- Include code examples
- Keep language clear and accessible
- Test all code examples

### Documentation Structure

- `README.md` - Project overview and quick start
- `docs/getting_started.md` - Detailed setup guide
- `docs/personality_format.md` - Schema documentation
- `docs/api_reference.md` - Complete API reference
- `docs/best_practices.md` - Guidelines and tips

## Release Process

### Versioning

We use semantic versioning (MAJOR.MINOR.PATCH):
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes (backward compatible)

### Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] Version bumped
- [ ] CHANGELOG.md updated
- [ ] Tag created
- [ ] PyPI release

## Community

### Getting Help

- 💬 [Discord](https://discord.gg/luminoracore) - Real-time chat
- 🐛 [GitHub Issues](https://github.com/luminoracore/luminoracore/issues) - Bug reports
- 💡 [GitHub Discussions](https://github.com/luminoracore/luminoracore/discussions) - Ideas and questions
- 📧 team@luminoracore.dev - Direct contact

### Recognition

Contributors are recognized in:
- README.md contributors section
- Release notes
- Annual contributor highlights

## License

By contributing to LuminoraCore, you agree that your contributions will be licensed under the MIT License.

## Questions?

If you have questions about contributing, please:
1. Check existing documentation
2. Search existing issues
3. Ask in Discord
4. Create a new issue

Thank you for contributing to LuminoraCore! 🎭✨
