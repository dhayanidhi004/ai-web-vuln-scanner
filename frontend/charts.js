// ================= CHART CONFIG =================
let pieChart = null;
let barChart = null;

// ================= DRAW CHARTS =================
function drawCharts(data) {

    // Safety: handle empty or invalid data
    if (!Array.isArray(data) || data.length === 0) {
        console.warn("No data provided to drawCharts()");
        return;
    }

    // Severity counters
    let counts = {
        Critical: 0,
        High: 0,
        Medium: 0,
        Low: 0
    };

    data.forEach(v => {
        if (v && counts[v.severity] !== undefined) {
            counts[v.severity]++;
        }
    });

    // Get canvas elements safely
    const pieCanvas = document.getElementById("pie");
    const barCanvas = document.getElementById("bar");

    if (!pieCanvas || !barCanvas) {
        console.error("Chart canvas not found");
        return;
    }

    // Destroy old charts (important to avoid overlap)
    if (pieChart) {
        pieChart.destroy();
        pieChart = null;
    }
    if (barChart) {
        barChart.destroy();
        barChart = null;
    }

    // ================= PIE CHART =================
    pieChart = new Chart(pieCanvas.getContext("2d"), {
        type: "pie",
        data: {
            labels: Object.keys(counts),
            datasets: [
                {
                    data: Object.values(counts),
                    backgroundColor: [
                        "#ff003c", // Critical
                        "#ff8c00", // High
                        "#ffd700", // Medium
                        "#00ff9d"  // Low
                    ],
                    borderWidth: 0
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: {
                        color: "#ffffff",
                        font: {
                            size: 12
                        }
                    }
                },
                tooltip: {
                    enabled: true
                }
            }
        }
    });

    // ================= BAR CHART =================
    barChart = new Chart(barCanvas.getContext("2d"), {
        type: "bar",
        data: {
            labels: Object.keys(counts),
            datasets: [
                {
                    label: "Detected Vulnerabilities",
                    data: Object.values(counts),
                    backgroundColor: "#00ffe0",
                    borderRadius: 6
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: "#ffffff"
                    },
                    grid: {
                        color: "rgba(255,255,255,0.1)"
                    }
                },
                x: {
                    ticks: {
                        color: "#ffffff"
                    },
                    grid: {
                        display: false
                    }
                }
            },
            plugins: {
                legend: {
                    labels: {
                        color: "#ffffff"
                    }
                },
                tooltip: {
                    enabled: true
                }
            }
        }
    });
}
