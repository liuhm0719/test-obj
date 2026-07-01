import os
import subprocess
import time

import httpx
import pytest

PORT = "8987"
BASE_URL = f"http://127.0.0.1:{PORT}"


@pytest.fixture()
def dev_server():
    env = os.environ.copy()
    env.update({"APP_ENV": "dev", "APP_HOST": "127.0.0.1", "APP_PORT": PORT})

    proc = subprocess.Popen(
        ["bash", "run.sh"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    time.sleep(3)
    yield proc
    proc.terminate()
    proc.wait(timeout=5)


def test_dev_startup(dev_server):
    resp = httpx.get(f"{BASE_URL}/health", timeout=5)
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"


def test_swagger_ui(dev_server):
    resp = httpx.get(f"{BASE_URL}/docs", timeout=5)
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]
