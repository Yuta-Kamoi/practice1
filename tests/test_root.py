def test_root_redirects(client):
    resp = client.get("/", allow_redirects=False)
    assert resp.status_code in (301, 302, 307, 308)
    loc = resp.headers.get("location", "")
    assert loc.endswith("/static/index.html")
