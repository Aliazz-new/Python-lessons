
# ====== KONFIGURACJA ======
try:
    from local_config import EMAIL, API_TOKEN, DOMAIN, JQL
except ImportError:
    EMAIL = "aliazz@wp.pl"
    API_TOKEN = "<YOUR_API_TOKEN>"
    DOMAIN = "aliazz"  # bez .atlassian.net
    JQL = "project = 'Test Scrum'"

def get_all_issues(domain, email, api_token, jql):
    import requests
    from requests.auth import HTTPBasicAuth

    url = f"https://{domain}.atlassian.net/rest/api/3/search/jql"

    auth = HTTPBasicAuth(email, api_token)

    headers = {
        "Accept": "application/json"
    }

    start_at = 0
    max_results = 50
    all_issues = []

    while True:
        params = {
            "jql": jql,
            "startAt": start_at,
            "maxResults": max_results,
            "fields": ["summary", "issuetype"]
        }

        response = requests.get(url, headers=headers, auth=auth, params=params)

        #if response.status_code != 200:
         #   print("Błąd:", response.text)
          #  break

        data = response.json()

        issues = data.get("issues") or data.get("values") or []
        total = data.get("total", 0)

        print(f"Pobrano {len(issues)} issue (startAt={start_at})")

        for issue in issues:
            key = issue.get("key") or issue.get("id")
            fields = issue.get("fields", {})
            summary = fields.get("summary")
            issuetype = fields.get("issuetype", {}).get("name")

            all_issues.append({
                "key": key,
                "summary": summary,
                "issuetype": issuetype
            })

        start_at += max_results

        if start_at >= total:
            break

    return all_issues

issues = get_all_issues(DOMAIN, EMAIL, API_TOKEN, JQL)

print(f"\nŁącznie pobrano: {len(issues)} issue")

for issue in issues:
    print(issue["key"], "→", issue["summary"])
