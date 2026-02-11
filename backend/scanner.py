import requests
from urllib.parse import urljoin

# Reusable request headers
HEADERS = {
    "User-Agent": "AI-Web-Vulnerability-Scanner/1.0"
}

def scan_site(url):
    """
    Performs passive vulnerability checks based on OWASP Top 10.
    Safe scanning only — no exploitation, no payload injection.
    """

    results = []
    seen = set()  # prevent duplicate findings

    def add_finding(vuln, severity, attack):
        key = (vuln, severity, attack)
        if key not in seen:
            seen.add(key)
            results.append(key)

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=6,
            allow_redirects=True
        )

        headers = {k.lower(): v for k, v in response.headers.items()}
        body = response.text.lower()

        # ================= SECURITY HEADERS =================
        if "content-security-policy" not in headers:
            add_finding(
                "Cross Site Scripting (XSS)",
                "High",
                "Malicious script injection and session hijacking"
            )

        if "x-frame-options" not in headers:
            add_finding(
                "Clickjacking",
                "Medium",
                "UI redress attack using iframes"
            )

        if "x-content-type-options" not in headers:
            add_finding(
                "Security Misconfiguration",
                "Medium",
                "MIME-type sniffing attacks"
            )

        if "strict-transport-security" not in headers:
            add_finding(
                "Sensitive Data Exposure",
                "High",
                "Man-in-the-middle (MITM) attack"
            )

        # ================= HTTPS CHECK =================
        if not url.startswith("https://"):
            add_finding(
                "Sensitive Data Exposure",
                "High",
                "Unencrypted HTTP communication"
            )

        # ================= SQL INJECTION INDICATORS =================
        sql_errors = [
            "you have an error in your sql syntax",
            "warning: mysql",
            "unclosed quotation mark",
            "quoted string not properly terminated",
            "sqlstate",
            "ora-"
        ]

        for error in sql_errors:
            if error in body:
                add_finding(
                    "SQL Injection",
                    "Critical",
                    "Database extraction or manipulation"
                )
                break

        # ================= ADMIN / SENSITIVE PATH EXPOSURE =================
        admin_paths = [
            "/admin",
            "/administrator",
            "/login",
            "/dashboard",
            "/admin/login"
        ]

        for path in admin_paths:
            admin_url = urljoin(url, path)
            try:
                r = requests.get(
                    admin_url,
                    headers=HEADERS,
                    timeout=4
                )
                if r.status_code == 200:
                    add_finding(
                        "Broken Access Control",
                        "Medium",
                        f"Exposed endpoint: {path}"
                    )
                    break
            except requests.RequestException:
                continue

        # ================= CSRF INDICATORS =================
        if "csrf" not in body and "token" not in body:
            add_finding(
                "Cross Site Request Forgery (CSRF)",
                "Medium",
                "Unauthorized request execution"
            )

        # ================= DIRECTORY LISTING =================
        if "index of /" in body:
            add_finding(
                "Security Misconfiguration",
                "High",
                "Directory listing enabled"
            )

    except requests.RequestException as e:
        add_finding(
            "Scan Error",
            "Low",
            f"Connection issue: {str(e)}"
        )

    except Exception as e:
        add_finding(
            "Scan Error",
            "Low",
            str(e)
        )

    return results
