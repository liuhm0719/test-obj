from app.main import app


def test_app_instance():
    assert app is not None
    assert app.title == "FastAPI Example"


def test_routes_not_empty():
    routes = app.routes
    assert len(routes) > 0


def test_health_route_registered():
    paths = [route.path for route in app.routes if hasattr(route, "path")]
    assert "/health" in paths
