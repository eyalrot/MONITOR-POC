"""Integration tests for Loki setup."""

import time
from pathlib import Path

import pytest
import requests
import yaml


class TestLokiSetup:
    """Test suite for Loki configuration and deployment."""

    LOKI_URL = "http://localhost:23002"
    LOKI_INTERNAL_URL = "http://localhost:3100"

    @classmethod
    def setup_class(cls):
        """Set up test class with proper paths."""
        # Get the project root directory
        cls.project_root = Path(__file__).parent.parent.parent
        cls.config_path = cls.project_root / "config" / "loki" / "loki-config.yml"

    def test_loki_config_syntax(self):
        """Test that loki-config.yml has valid syntax."""
        with open(self.config_path) as f:
            config = yaml.safe_load(f)
        
        # Verify required sections exist
        assert "auth_enabled" in config
        assert config["auth_enabled"] is False
        
        assert "server" in config
        assert config["server"]["http_listen_port"] == 3100
        
        assert "schema_config" in config
        assert config["schema_config"]["configs"][0]["schema"] == "v13"
        assert config["schema_config"]["configs"][0]["store"] == "tsdb"
        
        assert "limits_config" in config
        assert config["limits_config"]["retention_period"] == "744h"
        
        assert "compactor" in config
        assert config["compactor"]["retention_enabled"] is True
    
    def test_loki_readiness_endpoint(self):
        """Test that Loki readiness endpoint responds correctly."""
        max_retries = 10
        retry_delay = 3
        
        for attempt in range(max_retries):
            try:
                response = requests.get(f"{self.LOKI_URL}/ready", timeout=5)
                if response.status_code == 200:
                    assert response.text.strip() == "ready"
                    return
            except requests.exceptions.RequestException:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                else:
                    raise
        
        pytest.fail("Loki readiness endpoint did not become ready")
    
    def test_loki_metrics_endpoint(self):
        """Test that Loki metrics endpoint is accessible."""
        response = requests.get(f"{self.LOKI_URL}/metrics", timeout=10)
        assert response.status_code == 200
        
        # Check for some expected metrics
        metrics_text = response.text
        assert "loki_build_info" in metrics_text
        assert "go_info" in metrics_text
        assert "loki_ingester_memory_chunks" in metrics_text
    
    def test_loki_log_ingestion_readiness(self):
        """Test that Loki is ready to receive logs."""
        # Test the push endpoint exists (even if we don't push logs yet)
        response = requests.get(f"{self.LOKI_URL}/loki/api/v1/push", timeout=5)
        # GET on push endpoint should return 405 Method Not Allowed
        assert response.status_code == 405
    
    def test_loki_retention_configuration(self):
        """Test that retention is properly configured."""
        response = requests.get(f"{self.LOKI_URL}/config", timeout=5)
        
        if response.status_code == 200:
            config = response.json()
            # Check retention settings
            assert config.get("limits_config", {}).get("retention_period") == "744h0m0s"
            assert config.get("compactor", {}).get("retention_enabled") is True
    
    def test_loki_storage_schema(self):
        """Test that storage schema is correctly configured for TSDB."""
        response = requests.get(f"{self.LOKI_URL}/config", timeout=5)
        
        if response.status_code == 200:
            config = response.json()
            schema_configs = config.get("schema_config", {}).get("configs", [])
            assert len(schema_configs) > 0
            
            latest_schema = schema_configs[-1]
            assert latest_schema.get("store") == "tsdb"
            assert latest_schema.get("schema") == "v13"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])