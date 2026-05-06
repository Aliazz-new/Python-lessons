import requests
from requests.auth import HTTPBasicAuth


# ====== KONFIGURACJA ======
try:
    from local_config import EMAIL, API_TOKEN, DOMAIN, JQL
except ImportError:
    EMAIL = "aliazz@wp.pl"
    API_TOKEN = "<YOUR_API_TOKEN>"
    DOMAIN = "aliazz"  # bez .atlassian.net
    JQL = "project = 'Test Scrum'"



# ====== FUNKCJA ======
def get_issues(domain, email, api_token, jql):
    url = f"https://{domain}.atlassian.net/rest/api/3/search/jql"

    auth = HTTPBasicAuth(email, api_token)

    headers = {
        "Accept": "application/json"
    }

    params = {
        "jql": jql,
        "maxResults": 5,
        "fields": ["summary", "issuetype"]  # klucz może nie być potrzebny
    }

    response = requests.get(url, headers=headers, auth=auth, params=params)

    print("Status HTTP:", response.status_code)

    if response.status_code != 200:
        print("Błąd:", response.text)
        return []

    data = response.json()

    # Debug – zobacz strukturę:
    print("DEBUG KEYS:", data.keys())

    issues = data.get("issues") or data.get("values") or []

    result = []

    for issue in issues:
        print("DEBUG ISSUE:", issue)

        # czasem key jest na top-level
        key = issue.get("key")

        # jeśli nie ma key, spróbuj użyć id
        if not key:
            key = issue.get("id")

        fields = issue.get("fields", {})
        summary = fields.get("summary")

        issuetype = fields.get("issuetype", {}).get("name")

        result.append({
            "key": key,
            "summary": summary,
            "issuetype": issuetype
        })

    return result


# ====== MAIN ======
if __name__ == "__main__":
    issues = get_issues(DOMAIN, EMAIL, API_TOKEN, JQL)

    print("\nWYNIK:")
    for issue in issues:
        print(f"{issue['key']} → {issue['summary']} ({issue['issuetype']})")
