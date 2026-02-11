// ================= AUTH CHECK =================
async function checkLogin() {
    try {
        const res = await fetch(`/health`, {
            credentials: "include"
        });

        if (!res.ok) {
            window.location.href = "login.html";
        }
    } catch (err) {
        window.location.href = "login.html";
    }
}

// Run auth check on page load
checkLogin();


// ================= MAIN SCAN FUNCTION =================
async function scan() {
    const urlInput = document.getElementById("url");
    const url = urlInput.value.trim();

    if (!url) {
        alert("Please enter a website URL");
        return;
    }

    // ================= RESET UI =================
    document.getElementById("cards").innerHTML = "";
    document.getElementById("summary").innerHTML = `
        <h2 style="text-align:center; color:#00ffe0; width:100%">
            🔍 Initializing AI Scan for:<br>${url}
        </h2>
    `;

    try {
        // ================= BACKEND CALL =================
        const res = await fetch(
            `/scan?url=${encodeURIComponent(url)}`,
            {
                method: "GET",
                credentials: "include"
            }
        );

        // Unauthorized → redirect to login
        if (res.status === 401) {
            window.location.href = "login.html";
            return;
        }

        if (!res.ok) {
            throw new Error(`HTTP Error ${res.status}`);
        }

        const data = await res.json();
        console.log("SCAN RESPONSE:", data);

        // ================= BACKEND ERROR =================
        if (data.error) {
            document.getElementById("summary").innerHTML = `
                <h2 style="color:#ff6b6b; text-align:center; width:100%">
                    ❌ Error: ${data.error}
                </h2>
            `;
            return;
        }

        // ================= NO RESULTS =================
        if (!data.results || data.results.length === 0) {
            document.getElementById("summary").innerHTML = `
                <h2 style="color:#00ff88; text-align:center; width:100%">
                    ✅ No vulnerabilities detected
                </h2>
            `;
            return;
        }

        // ================= SUMMARY COUNTS =================
        let counts = { Critical: 0, High: 0, Medium: 0, Low: 0 };

        data.results.forEach(v => {
            if (counts[v.severity] !== undefined) {
                counts[v.severity]++;
            }
        });

        document.getElementById("summary").innerHTML = `
            <div class="summary-box critical">Critical<span>${counts.Critical}</span></div>
            <div class="summary-box high">High<span>${counts.High}</span></div>
            <div class="summary-box medium">Medium<span>${counts.Medium}</span></div>
            <div class="summary-box low">Low<span>${counts.Low}</span></div>
            <div class="summary-box green">Total<span>${data.total}</span></div>
        `;

        // ================= VULNERABILITY CARDS =================
        let html = "";
        data.results.forEach(v => {
            html += `
                <div class="card ${v.severity}">
                    <h3>${v.vulnerability}</h3>
                    <p><b>Severity:</b> ${v.severity}</p>
                    <p><b>Attack Vector:</b> ${v.attack}</p>
                    <p style="color:#00ffe0">
                        <b>AI Suggestion:</b> ${v.prevention}
                    </p>
                </div>
            `;
        });

        document.getElementById("cards").innerHTML = html;

        // ================= CHARTS =================
        if (typeof drawCharts === "function") {
            drawCharts(data.results);
        }

    } catch (error) {
        console.error("SCAN FAILED:", error);
        document.getElementById("summary").innerHTML = `
            <h2 style="color:#ff4b2b; text-align:center; width:100%">
                ❌ Scan Failed. Backend not reachable.
            </h2>
        `;
    }
}


// ================= PDF DOWNLOAD =================
document.querySelector(".pdf")?.addEventListener("click", () => {
    const url = document.getElementById("url").value.trim();

    if (!url) {
        alert("Please scan a website first");
        return;
    }

    window.location.href =
        `/pdf?url=${encodeURIComponent(url)}`;
});


// ================= LOGOUT =================
function logout() {
    fetch(`/logout`, {
        credentials: "include"
    }).then(() => {
        window.location.href = "login.html";
    });
}
