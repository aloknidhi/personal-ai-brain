import requests

BASE = "http://localhost:8000"
passed = 0
failed = 0

def t(name, method, path, data=None, headers=None, params=None, expect=200):
    global passed, failed
    try:
        if method == "GET":
            r = requests.get(BASE + path, headers=headers, params=params)
        elif method == "POST":
            r = requests.post(BASE + path, json=data, headers=headers, params=params)
        elif method == "PATCH":
            r = requests.patch(BASE + path, json=data, headers=headers, params=params)
        elif method == "DELETE":
            r = requests.delete(BASE + path, headers=headers)
        ok = r.status_code == expect
        print(f"{'PASS' if ok else 'FAIL'}: {name} ({r.status_code})")
        if ok:
            passed += 1
        else:
            failed += 1
        return r
    except Exception as e:
        print(f"ERROR: {name} - {e}")
        failed += 1
        return None

print("=== HEALTH ===")
t("GET /health", "GET", "/health")
t("GET /", "GET", "/")

print("=== AUTH ===")
t("POST /auth/register", "POST", "/api/v1/auth/register",
   {"email": "bugtest@example.com", "password": "test123", "full_name": "Bug Test"})
t("POST /auth/register dup", "POST", "/api/v1/auth/register",
   {"email": "bugtest@example.com", "password": "test123"}, expect=400)
t("POST /auth/login", "POST", "/api/v1/auth/login",
   {"email": "bugtest@example.com", "password": "test123"})
t("POST /auth/login wrong", "POST", "/api/v1/auth/login",
   {"email": "bugtest@example.com", "password": "wrong"}, expect=401)

r = requests.post(BASE + "/api/v1/auth/login",
                  json={"email": "bugtest@example.com", "password": "test123"})
token = r.json().get("access_token") if r.status_code == 200 else None
h = {"Authorization": f"Bearer {token}"} if token else {}
print(f"Token: {'YES' if token else 'NO'}")

if token:
    t("GET /auth/me", "GET", "/api/v1/auth/me", headers=h)
    t("POST /auth/logout", "POST", "/api/v1/auth/logout", headers=h)
    t("POST /auth/login again", "POST", "/api/v1/auth/login",
      {"email": "bugtest@example.com", "password": "test123"})
    token2 = requests.post(BASE + "/api/v1/auth/login",
                           json={"email": "bugtest@example.com", "password": "test123"}).json().get("access_token")
    h2 = {"Authorization": f"Bearer {token2}"}

print("=== SOURCES ===")
if token2:
    t("POST /sources chatgpt", "POST", "/api/v1/sources/", {"source_type": "chatgpt"}, headers=h2)
    t("POST /sources github", "POST", "/api/v1/sources/", {"source_type": "github"}, headers=h2)
    t("GET /sources", "GET", "/api/v1/sources/", headers=h2)

r = requests.get(BASE + "/api/v1/sources/", headers=h2)
srcs = r.json() if r.status_code == 200 else []
sid = srcs[0]["id"] if srcs else None

if token2 and sid:
    t("POST /sources/{id}/sync", "POST", f"/api/v1/imports/sources/{sid}/sync", headers=h2)
    t("GET /sources/{id}/conversations", "GET", f"/api/v1/imports/sources/{sid}/conversations", headers=h2)
    t("DELETE /sources/{id}", "DELETE", f"/api/v1/sources/{sid}", headers=h2)

print("=== KNOWLEDGE ===")
if token2:
    t("POST /knowledge/subjects", "POST", "/api/v1/knowledge/subjects", {"name": "C++"}, headers=h2)
    t("POST /knowledge/subjects", "POST", "/api/v1/knowledge/subjects", {"name": "Java"}, headers=h2)
    t("GET /knowledge/subjects", "GET", "/api/v1/knowledge/subjects", headers=h2)

r = requests.get(BASE + "/api/v1/knowledge/subjects", headers=h2)
subs = r.json() if r.status_code == 200 else []
subid = subs[0]["id"] if subs else None

if token2 and subid:
    t("POST /knowledge/topics", "POST", "/api/v1/knowledge/topics",
      {"name": "Inheritance", "subject_id": subid}, headers=h2)
    t("POST /knowledge/topics bad subject", "POST", "/api/v1/knowledge/topics",
      {"name": "Orphan", "subject_id": "nope"}, headers=h2, expect=404)
    t("GET /knowledge/topics", "GET", "/api/v1/knowledge/topics", headers=h2)

if token2:
    t("GET /knowledge/", "GET", "/api/v1/knowledge/", headers=h2)

print("=== CONVERSATIONS ===")
if token2:
    t("GET /conversations/", "GET", "/api/v1/conversations/", headers=h2)

print("=== ANALYSIS ===")
if token2:
    t("POST /analysis/preview", "POST", "/api/v1/analysis/preview",
      {"analysis_type": "topic_extraction"}, headers=h2)
    t("POST /analysis/analyze-selected empty", "POST", "/api/v1/analysis/analyze-selected", [], headers=h2)
    t("POST /analysis/analyze-selected bad id", "POST", "/api/v1/analysis/analyze-selected",
      ["nope"], headers=h2, expect=404)
    t("GET /analysis/", "GET", "/api/v1/analysis/", headers=h2)

print("=== STUDY PLANNER ===")
if token2:
    t("POST /plans/generate", "POST", "/api/v1/plans/generate", {"title": "C++ OOP"}, headers=h2)
    t("POST /plans/generate-detailed", "POST", "/api/v1/plans/generate-detailed", None,
      headers=h2, params=[("title", "JS"), ("goal", "learn"), ("topics", "React"),
                          ("daily_hours", "2"), ("days", "7")])
    t("GET /plans/", "GET", "/api/v1/plans/", headers=h2)

r = requests.get(BASE + "/api/v1/plans/", headers=h2)
plans = r.json() if r.status_code == 200 else []
pid = plans[0]["id"] if plans else None

if token2 and pid:
    t("GET /plans/{id}", "GET", f"/api/v1/plans/{pid}", headers=h2)
    t("POST /plans/{id}/tasks", "POST", f"/api/v1/plans/{pid}/tasks",
      {"title": "Study", "status": "upcoming"}, headers=h2)

r = requests.get(BASE + f"/api/v1/plans/{pid}", headers=h2) if pid else None
tasks = r.json().get("tasks", []) if r and r.status_code == 200 else []
tid = tasks[0]["id"] if tasks else None

if token2 and tid:
    t("PATCH /plans/tasks/{id}", "PATCH", f"/api/v1/plans/tasks/{tid}",
      None, headers=h2, params={"status": "completed"})

print("=== ACTIVITIES ===")
if token2:
    t("POST /activities/start", "POST", "/api/v1/activities/start",
      {"title": "Study Session"}, headers=h2)
    t("POST /activities/start with task", "POST", "/api/v1/activities/start",
      {"title": "Java", "task_id": tid or "dummy"}, headers=h2)
    t("GET /activities/", "GET", "/api/v1/activities/", headers=h2)

if token2:
    r = requests.get(BASE + "/api/v1/activities/", headers=h2)
    acts = r.json() if r.status_code == 200 else []
    aid = acts[0]["id"] if acts else None
    if aid:
        t("POST /activities/{id}/stop", "POST", f"/api/v1/activities/{aid}/stop", headers=h2)

print(f"\n=== RESULTS: {passed} passed, {failed} failed out of {passed + failed} ===")
