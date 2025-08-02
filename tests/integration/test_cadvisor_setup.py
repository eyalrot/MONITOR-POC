"""Integration tests for cAdvisor setup."""

from pathlib import Path

import pytest
import requests
import yaml


class TestCAdvisorSetup:
    """Test suite for cAdvisor configuration and deployment."""

    CADVISOR_URL = "http://localhost:8080"
    PROMETHEUS_URL = "http://localhost:23001"

    def test_cadvisor_health_endpoint(self):
        """Test that cAdvisor health endpoint responds correctly."""
        response = requests.get(f"{self.CADVISOR_URL}/healthz", timeout=5)
        assert response.status_code == 200
        assert response.text.strip() == "ok"

    def test_cadvisor_metrics_endpoint(self):
        """Test that cAdvisor metrics endpoint is accessible."""
        response = requests.get(f"{self.CADVISOR_URL}/metrics", timeout=10)
        assert response.status_code == 200

        # Check for key cAdvisor metrics
        metrics_text = response.text
        assert "container_cpu_usage_seconds_total" in metrics_text
        assert "container_memory_usage_bytes" in metrics_text
        assert "container_network_receive_bytes_total" in metrics_text
        assert "container_fs_usage_bytes" in metrics_text

    def test_prometheus_scraping_cadvisor(self):
        """Test that Prometheus is successfully scraping cAdvisor."""
        # Check targets endpoint
        response = requests.get(f"{self.PROMETHEUS_URL}/api/v1/targets", timeout=5)
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "success"

        # Find cAdvisor target
        cadvisor_target = None
        for target in data["data"]["activeTargets"]:
            if target.get("labels", {}).get("job") == "cadvisor":
                cadvisor_target = target
                break

        assert cadvisor_target is not None, "cAdvisor target not found in Prometheus"
        assert cadvisor_target["health"] == "up", "cAdvisor target is not healthy"

    def test_container_metrics_available(self):
        """Test that container metrics are available in Prometheus."""
        # Query for container memory usage
        query = "container_memory_usage_bytes"
        response = requests.get(
            f"{self.PROMETHEUS_URL}/api/v1/query",
            params={"query": query},
            timeout=5,
        )
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "success"
        assert len(data["data"]["result"]) > 0, "No container metrics found"

    def test_container_labels_present(self):
        """Test that container metrics have proper labels."""
        # Query for a specific container metric with labels
        query = 'container_memory_usage_bytes{name!=""}'
        response = requests.get(
            f"{self.PROMETHEUS_URL}/api/v1/query", params={"query": query}, timeout=5
        )
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "success"

        # Check that metrics have expected labels
        if len(data["data"]["result"]) > 0:
            first_metric = data["data"]["result"][0]["metric"]
            # Standard labels that should be present
            assert "name" in first_metric
            assert "instance" in first_metric
            assert "job" in first_metric

    def test_prometheus_config_has_cadvisor(self):
        """Test that Prometheus configuration includes cAdvisor job."""
        # Read the prometheus config file
        config_path = (
            Path(__file__).parent.parent.parent
            / "config"
            / "prometheus"
            / "prometheus.yml"
        )
        with open(config_path) as f:
            config = yaml.safe_load(f)

        # Find cAdvisor job
        cadvisor_job = None
        for job in config["scrape_configs"]:
            if job["job_name"] == "cadvisor":
                cadvisor_job = job
                break

        assert cadvisor_job is not None, "cAdvisor job not found in Prometheus config"

        # Check job configuration
        assert len(cadvisor_job["static_configs"]) > 0
        targets = cadvisor_job["static_configs"][0]["targets"]
        assert "cadvisor:8080" in targets

        # Check metric relabeling is configured
        assert "metric_relabel_configs" in cadvisor_job

    def test_cadvisor_container_api(self):
        """Test cAdvisor container API endpoint."""
        # Test the container API endpoint
        response = requests.get(f"{self.CADVISOR_URL}/api/v1.3/containers", timeout=5)
        assert response.status_code == 200

        # Response should be JSON
        data = response.json()
        assert isinstance(data, list), "Container API should return a list"

    def test_metric_cardinality_control(self):
        """Test that high-cardinality metrics are dropped as configured."""
        # Query for metrics that should be dropped
        dropped_metrics = [
            "container_network_tcp_usage_total",
            "container_network_udp_usage_total",
            "container_tasks_state",
            "container_cpu_load_average_10s",
        ]

        for metric in dropped_metrics:
            response = requests.get(
                f"{self.PROMETHEUS_URL}/api/v1/query",
                params={"query": metric},
                timeout=5,
            )
            assert response.status_code == 200

            data = response.json()
            assert data["status"] == "success"
            # These metrics should have been dropped by relabeling
            assert (
                len(data["data"]["result"]) == 0
            ), f"High-cardinality metric {metric} should be dropped"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
