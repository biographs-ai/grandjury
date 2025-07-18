# Version Management Guide

This guide explains how to handle version updates for the grandjury package.

## 🔄 Automated Release Workflow (Recommended)

### Setup (One-time)

1. **Add PyPI API Token to GitHub Secrets**
   - Go to your GitHub repository settings
   - Navigate to "Secrets and variables" → "Actions"
   - Add new secret: `PYPI_API_TOKEN`
   - Value: Your PyPI API token (same one you used for manual upload)

2. **Workflow is Ready**
   - GitHub Actions workflow is in `.github/workflows/publish.yml`
   - Automatically runs tests on Python 3.8-3.12
   - Publishes to PyPI on tags/releases

### Release Process

#### Option A: Using the Bump Script (Easiest)
```bash
# Patch release (1.0.0 → 1.0.1)
python scripts/bump_version.py patch

# Minor release (1.0.1 → 1.1.0)  
python scripts/bump_version.py minor

# Major release (1.1.0 → 2.0.0)
python scripts/bump_version.py major

# Push to trigger release
git push origin main --tags
```

#### Option B: Manual Process
```bash
# 1. Update version in pyproject.toml
# version = "1.0.1"

# 2. Commit and tag
git add pyproject.toml
git commit -m "Bump version to 1.0.1"
git tag -a v1.0.1 -m "Release version 1.0.1"

# 3. Push to trigger release
git push origin main --tags
```

#### Option C: GitHub Release (Web Interface)
1. Go to your GitHub repository
2. Click "Releases" → "Create a new release"
3. Create tag: `v1.0.1` 
4. Set title: `Release 1.0.1`
5. Add release notes
6. Publish release

### What Happens Automatically

1. **GitHub Actions triggers** on tag push or release
2. **Tests run** on multiple Python versions
3. **Package builds** automatically
4. **Validates** with twine check
5. **Publishes to PyPI** if all tests pass
6. **Users can install** the new version immediately

## 📦 Manual Release Workflow

If you prefer manual control:

```bash
# 1. Update version in pyproject.toml
# 2. Build and test
python scripts/build_with_uv.py

# 3. Upload to PyPI
uv run twine upload dist/*
```

## 🏷️ Version Numbering

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR** (2.0.0): Breaking changes
- **MINOR** (1.1.0): New features, backward compatible
- **PATCH** (1.0.1): Bug fixes, backward compatible

### Examples:
- Bug fix: `1.0.0` → `1.0.1`
- New endpoint: `1.0.1` → `1.1.0`
- API breaking change: `1.1.0` → `2.0.0`

## 🔍 Monitoring Releases

- **PyPI page**: https://pypi.org/project/grandjury/
- **GitHub Actions**: Check workflow runs
- **Download stats**: Available on PyPI
- **Issues**: Monitor GitHub issues for problems

## 🛠️ Troubleshooting

### Failed GitHub Actions
- Check the Actions tab in your repository
- Common issues: missing secrets, test failures
- Re-run failed workflows after fixing

### Failed PyPI Upload
- Verify PyPI API token in GitHub secrets
- Check if version already exists on PyPI
- Ensure all tests pass

### Version Conflicts
- Each version can only be uploaded once
- If you need to fix a release, bump to next patch version
- Cannot delete/replace versions on PyPI

## 🎯 Best Practices

1. **Always test** before releasing
2. **Use semantic versioning** consistently  
3. **Write release notes** for users
4. **Monitor** for issues after release
5. **Keep dependencies** up to date
