import re


SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+")
ISO8601_UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}")


def test_health_status_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_health_version_semver(client):
    response = client.get("/health")
    version = response.json()["version"]
    assert version and SEMVER_RE.match(version)


def test_health_timestamp_iso8601(client):
    response = client.get("/health")
    timestamp = response.json()["timestamp"]
    assert timestamp and ISO8601_UTC_RE.match(timestamp)


def test_health_no_auth_required(client):
    response = client.get("/health")
    assert response.status_code == 200


def test_health_content_type_json(client):
    response = client.get("/health")
    assert "application/json" in response.headers["content-type"]
