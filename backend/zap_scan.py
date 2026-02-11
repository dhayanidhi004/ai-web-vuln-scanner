import requests
import time

# ================= ZAP CONFIG =================
ZAP_API = "http://localhost:8080"
API_KEY = ""  # Optional: set if ZAP API key is enabled
TIMEOUT = 5


def zap_scan(url):
    """
    Triggers OWASP ZAP Active Scan and checks scan status.
    Safe integration layer (no direct exploit handling here).
    """

    try:
        # ----------------- START ACTIVE SCAN -----------------
        start_resp = requests.get(
            f"{ZAP_API}/JSON/ascan/action/scan/",
            params={
                "url": url,
                "recurse": True,
                "inScopeOnly": False,
                "apikey": API_KEY
            },
            timeout=TIMEOUT
        )

        if start_resp.status_code != 200:
            return {
                "status": "error",
                "message": "Unable to connect to ZAP API"
            }

        scan_id = start_resp.json().get("scan")

        if not scan_id:
            return {
                "status": "error",
                "message": "Failed to start ZAP scan"
            }

        # ----------------- POLL STATUS -----------------
        for _ in range(5):  # short polling (demo-friendly)
            status_resp = requests.get(
                f"{ZAP_API}/JSON/ascan/view/status/",
                params={
                    "scanId": scan_id,
                    "apikey": API_KEY
                },
                timeout=TIMEOUT
            )

            status_data = status_resp.json()
            progress = status_data.get("status", "0")

            if progress == "100":
                return {
                    "status": "completed",
                    "message": "OWASP ZAP Active Scan completed",
                    "scan_id": scan_id
                }

            time.sleep(2)

        return {
            "status": "running",
            "message": "OWASP ZAP Scan is still running",
            "scan_id": scan_id
        }

    except requests.exceptions.ConnectionError:
        return {
            "status": "error",
            "message": "OWASP ZAP is not running on localhost:8080"
        }

    except requests.exceptions.Timeout:
        return {
            "status": "error",
            "message": "ZAP API request timed out"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"ZAP Error: {str(e)}"
        }
