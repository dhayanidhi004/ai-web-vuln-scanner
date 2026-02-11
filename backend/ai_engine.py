def ai_analyze(findings):
    """
    AI layer that converts raw scan findings into
    human-readable vulnerability reports with prevention guidance.
    Uses OWASP Top 10 mapping with severity-based intelligence.
    """

    # Safety check
    if not findings or not isinstance(findings, list):
        return {"total": 0, "results": []}

    data = []

    # ================= OWASP KNOWLEDGE BASE =================
    owasp_map = {
        "SQL Injection": {
            "prevention": "Use parameterized queries (prepared statements), ORM frameworks, and strict server-side input validation.",
            "reference": "OWASP A03:2021 – Injection"
        },
        "Cross Site Scripting (XSS)": {
            "prevention": "Escape and encode user input, enforce Content Security Policy (CSP), and avoid unsafe DOM manipulation.",
            "reference": "OWASP A03:2021 – Injection"
        },
        "Security Misconfiguration": {
            "prevention": "Disable directory listing, remove default credentials, configure security headers, and keep software updated.",
            "reference": "OWASP A05:2021 – Security Misconfiguration"
        },
        "Cross Site Request Forgery (CSRF)": {
            "prevention": "Use CSRF tokens, same-site cookies, validate request origin, and enforce proper authorization checks.",
            "reference": "OWASP A01:2021 – Broken Access Control"
        },
        "Broken Authentication": {
            "prevention": "Implement strong password policies, multi-factor authentication, session expiration, and secure cookie flags.",
            "reference": "OWASP A07:2021 – Identification and Authentication Failures"
        },
        "Broken Access Control": {
            "prevention": "Enforce server-side authorization, restrict access to admin endpoints, and apply least-privilege principles.",
            "reference": "OWASP A01:2021 – Broken Access Control"
        },
        "Sensitive Data Exposure": {
            "prevention": "Enforce HTTPS, enable HSTS, encrypt sensitive data, and avoid transmitting secrets in plain text.",
            "reference": "OWASP A02:2021 – Cryptographic Failures"
        },
        "Clickjacking": {
            "prevention": "Set X-Frame-Options or Content Security Policy frame-ancestors directive.",
            "reference": "OWASP A05:2021 – Security Misconfiguration"
        }
    }

    # ================= SEVERITY SCORES (OPTIONAL) =================
    severity_score = {
        "Critical": 9.5,
        "High": 7.5,
        "Medium": 5.0,
        "Low": 2.5
    }

    # ================= PROCESS FINDINGS =================
    for item in findings:
        try:
            vuln, severity, attack = item
        except ValueError:
            # Skip malformed entries
            continue

        # Normalize severity
        severity = severity.capitalize()
        if severity not in severity_score:
            severity = "Low"

        # Default AI recommendation
        fix = "Follow standard OWASP security best practices."
        ref = "OWASP Top 10"

        # OWASP-specific recommendation
        if vuln in owasp_map:
            fix = owasp_map[vuln]["prevention"]
            ref = owasp_map[vuln]["reference"]

        # Severity-based AI enhancement
        if severity == "Critical":
            fix += " Immediate remediation is strongly recommended to prevent system compromise."
        elif severity == "High":
            fix += " Should be fixed as soon as possible to reduce attack surface."
        elif severity == "Medium":
            fix += " Recommended to fix during the next development cycle."
        else:
            fix += " Monitor the issue and improve security posture over time."

        data.append({
            "vulnerability": vuln,
            "severity": severity,
            "attack": attack,
            "prevention": fix,
            "owasp_reference": ref,
            "score": severity_score.get(severity, 0)  # Optional CVSS-like score
        })

    return {
        "total": len(data),
        "results": data
    }
