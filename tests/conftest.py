"""Shared test fixtures and configuration for all test suites."""

import os
import sys
from pathlib import Path

import pytest
import yaml

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture
def project_root():
    """Return the project root directory."""
    return PROJECT_ROOT


@pytest.fixture
def config_dir(project_root):
    """Return the configuration directory."""
    return project_root / "config"


@pytest.fixture
def prometheus_config_path(config_dir):
    """Return path to prometheus.yml."""
    return config_dir / "prometheus" / "prometheus.yml"


@pytest.fixture
def loki_config_path(config_dir):
    """Return path to loki-config.yml."""
    return config_dir / "loki" / "loki-config.yml"


@pytest.fixture
def docker_compose_path(project_root):
    """Return path to main docker-compose.yml."""
    return project_root / "docker" / "docker-compose.yml"


@pytest.fixture
def load_yaml():
    """Fixture to load YAML files."""
    def _load_yaml(file_path):
        with open(file_path) as f:
            return yaml.safe_load(f)
    return _load_yaml


@pytest.fixture
def mock_env(monkeypatch):
    """Fixture to mock environment variables."""
    def _mock_env(**kwargs):
        for key, value in kwargs.items():
            monkeypatch.setenv(key, str(value))
    return _mock_env


# Test environment configuration
@pytest.fixture(scope="session")
def test_env():
    """Return test environment configuration."""
    return {
        "prometheus_url": os.getenv("TEST_PROMETHEUS_URL", "http://localhost:23001"),
        "grafana_url": os.getenv("TEST_GRAFANA_URL", "http://localhost:23000"),
        "loki_url": os.getenv("TEST_LOKI_URL", "http://localhost:23002"),
        "timeout": int(os.getenv("TEST_TIMEOUT", "30")),
    }


# Markers for test categorization
def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "e2e: End-to-end tests")
    config.addinivalue_line("markers", "slow: Slow running tests")
    config.addinivalue_line("markers", "docker: Tests requiring Docker")


# Skip tests if Docker is not available
def pytest_collection_modifyitems(config, items):
    """Automatically skip Docker tests if Docker is not available."""
    try:
        import docker
        client = docker.from_env()
        client.ping()
        docker_available = True
    except Exception:
        docker_available = False

    skip_docker = pytest.mark.skip(reason="Docker not available")
    for item in items:
        if "docker" in item.keywords and not docker_available:
            item.add_marker(skip_docker)
