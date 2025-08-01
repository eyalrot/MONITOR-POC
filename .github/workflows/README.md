# GitHub Actions Workflows

This directory contains CI/CD workflows for the LLM Server Monitoring System.

## Planned Workflows

### ci.yaml
Continuous Integration workflow that will:
- Run Python linting (ruff)
- Run Python formatting checks (black)
- Execute unit tests
- Validate Docker Compose configurations
- Check for security vulnerabilities

### build-images.yaml
Docker image building workflow that will:
- Build all exporter images
- Push images to container registry
- Tag images with version numbers
- Update deployment configurations

### release.yaml
Release automation workflow that will:
- Create GitHub releases
- Generate changelog
- Build and publish Docker images
- Update documentation

## Implementation Notes

These workflows will be implemented in future stories as part of the CI/CD epic.

For now, developers should run tests and linting locally using:
- `make test` - Run all tests
- `make validate` - Validate configurations
- `ruff check .` - Run linting
- `black --check .` - Check formatting