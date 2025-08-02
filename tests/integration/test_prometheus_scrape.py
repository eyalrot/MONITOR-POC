"""Integration tests for Prometheus configuration and scraping"""

from pathlib import Path

import pytest
import requests
import yaml


class TestPrometheusConfiguration:
    """Test Prometheus configuration and deployment"""

    @pytest.fixture
    def prometheus_config_path(self):
        """Get path to prometheus.yml"""
        return Path(__file__).parent.parent.parent / "config/prometheus/prometheus.yml"

    @pytest.fixture
    def prometheus_base_url(self):
        """Prometheus API base URL"""
        return "http://localhost:23001"

    def test_prometheus_config_syntax(self, prometheus_config_path):
        """Test that prometheus.yml has valid syntax"""
        assert prometheus_config_path.exists(), f"Config file not found: {prometheus_config_path}"

        # Load and parse YAML
        with open(prometheus_config_path) as f:
            config = yaml.safe_load(f)

        # Verify required sections exist
        assert "global" in config, "Missing 'global' section in config"
        assert "scrape_configs" in config, "Missing 'scrape_configs' section in config"

        # Verify global settings
        global_config = config["global"]
        assert global_config.get("scrape_interval") == "30s", "Scrape interval should be 30s"
        assert (
            global_config.get("evaluation_interval") == "30s"
        ), "Evaluation interval should be 30s"

    def test_scrape_interval_configuration(self, prometheus_config_path):
        """Test that scrape intervals are properly configured"""
        with open(prometheus_config_path) as f:
            config = yaml.safe_load(f)

        # Check global scrape interval
        assert config["global"]["scrape_interval"] == "30s"

        # Verify all job configs respect the interval
        for job in config["scrape_configs"]:
            job_interval = job.get("scrape_interval")
            if job_interval:
                # If job has custom interval, it should be >= 30s
                interval_seconds = self._parse_duration(job_interval)
                assert interval_seconds >= 30, f"Job {job["job_name"]} has interval < 30s"

    def test_prometheus_self_scraping(self, prometheus_base_url):
        """Test that Prometheus can scrape its own metrics"""
        # Check if Prometheus is healthy
        health_response = requests.get(f"{prometheus_base_url}/-/healthy")
        assert health_response.status_code == 200
        assert "Healthy" in health_response.text

        # Check targets endpoint
        targets_response = requests.get(f"{prometheus_base_url}/api/v1/targets")
        assert targets_response.status_code == 200

        targets_data = targets_response.json()
        assert targets_data["status"] == "success"

        # Find prometheus job in active targets
        prometheus_targets = [
            target
            for target in targets_data["data"]["activeTargets"]
            if target["labels"]["job"] == "prometheus"
        ]

        assert len(prometheus_targets) > 0, "Prometheus self-monitoring target not found"

        # Verify target is up
        for target in prometheus_targets:
            assert target["health"] == "up", "Prometheus target is not healthy"

    def test_retention_configuration(self, prometheus_base_url):
        """Test that retention is properly configured"""
        # Query Prometheus flags to verify retention
        flags_response = requests.get(f"{prometheus_base_url}/api/v1/status/flags")
        assert flags_response.status_code == 200

        flags_data = flags_response.json()
        assert flags_data["status"] == "success"

        # Check retention time flag
        retention_flag = flags_data["data"].get("storage.tsdb.retention.time")
        assert retention_flag == "30d", f"Expected 30d retention, got {retention_flag}"

    def test_prometheus_ready_endpoint(self, prometheus_base_url):
        """Test Prometheus readiness endpoint"""
        ready_response = requests.get(f"{prometheus_base_url}/-/ready")
        assert ready_response.status_code == 200
        assert "ready" in ready_response.text.lower()

    def test_prometheus_metrics_endpoint(self, prometheus_base_url):
        """Test that Prometheus exposes its own metrics"""
        metrics_response = requests.get(f"{prometheus_base_url}/metrics")
        assert metrics_response.status_code == 200

        # Check for some key Prometheus metrics
        metrics_text = metrics_response.text
        assert "prometheus_build_info" in metrics_text
        assert "prometheus_tsdb_head_samples_appended_total" in metrics_text
        assert "go_memstats_alloc_bytes" in metrics_text

    @staticmethod
    def _parse_duration(duration_str):
        """Parse Prometheus duration string to seconds"""
        if duration_str.endswith("s"):
            return int(duration_str[:-1])
        elif duration_str.endswith("m"):
            return int(duration_str[:-1]) * 60
        elif duration_str.endswith("h"):
            return int(duration_str[:-1]) * 3600
        elif duration_str.endswith("d"):
            return int(duration_str[:-1]) * 86400
        else:
            raise ValueError(f"Unknown duration format: {duration_str}")
