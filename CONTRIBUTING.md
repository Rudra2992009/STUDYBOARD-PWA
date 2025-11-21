# Contributing to STUDYBOARD PWA

Thank you for your interest in contributing to STUDYBOARD! This document provides guidelines for contributing to the project.

## Code of Conduct

By participating in this project, you agree to:
- Be respectful and inclusive
- Focus on educational purposes only
- Follow ethical AI guidelines
- Respect intellectual property rights

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/Rudra2992009/STUDYBOARD-PWA/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version, GPU)
   - Error logs/screenshots

### Suggesting Features

1. Open a new issue with `[Feature Request]` prefix
2. Describe the feature and its benefits
3. Provide use cases
4. Consider implementation complexity

### Pull Requests

1. **Fork the repository**
```bash
git clone https://github.com/YOUR_USERNAME/STUDYBOARD-PWA.git
```

2. **Create a feature branch**
```bash
git checkout -b feature/your-feature-name
```

3. **Make your changes**
   - Follow code style guidelines
   - Add tests if applicable
   - Update documentation

4. **Test your changes**
```bash
cd backend
pytest tests/
```

5. **Commit with clear messages**
```bash
git commit -m "Add: Feature description"
```

6. **Push to your fork**
```bash
git push origin feature/your-feature-name
```

7. **Open a Pull Request**
   - Reference related issues
   - Describe changes made
   - Add screenshots if UI changes

## Development Setup

```bash
# Clone and setup
git clone https://github.com/Rudra2992009/STUDYBOARD-PWA.git
cd STUDYBOARD-PWA
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
cd backend
pip install -r requirements.txt
pip install pytest flake8 black
```

## Code Style

### Python
- Follow PEP 8
- Use type hints
- Maximum line length: 127 characters
- Use Black for formatting

```bash
black backend/
flake8 backend/
```

### JavaScript
- Use ES6+ syntax
- Consistent indentation (2 spaces)
- Semicolons required
- Descriptive variable names

### C++
- Follow C++17 standard
- Use smart pointers
- RAII principles
- Document public APIs

## Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v --cov
```

### Frontend Tests
```javascript
// Use browser console for manual testing
// Automated tests coming soon
```

## Documentation

- Update README.md for major changes
- Add inline comments for complex logic
- Update API documentation
- Include examples

## Commit Message Format

```
Type: Brief description

Detailed explanation if needed

Fixes #issue_number
```

**Types**:
- `Add`: New feature
- `Fix`: Bug fix
- `Update`: Modify existing feature
- `Remove`: Delete code/files
- `Docs`: Documentation only
- `Style`: Formatting changes
- `Refactor`: Code restructuring
- `Test`: Add/update tests
- `Chore`: Maintenance tasks

## Areas for Contribution

### High Priority
- [ ] Add unit tests for model_loader.py
- [ ] Implement offline model caching
- [ ] Add support for Hindi language
- [ ] Optimize image generation speed
- [ ] Mobile app (React Native)

### Medium Priority
- [ ] Add quiz generation feature
- [ ] Implement user progress tracking
- [ ] Voice input/output support
- [ ] More subject coverage
- [ ] Better error handling

### Low Priority
- [ ] Dark mode theme
- [ ] Custom model fine-tuning guide
- [ ] Performance benchmarks
- [ ] Video tutorials

## Questions?

Feel free to:
- Open a discussion on GitHub
- Email: rudra160113.work@gmail.com
- Check existing issues/PRs

---

**Thank you for contributing to education! 🎓**