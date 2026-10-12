const documentInput = document.getElementById("documentInput");
const chooseButton = document.getElementById("chooseButton");
const uploadArea = document.getElementById("uploadArea");
const analyzeButton = document.getElementById("analyzeButton");
const fileName = document.getElementById("fileName");

const loadingSection = document.getElementById("loadingSection");
const resultSection = document.getElementById("resultSection");
const errorSection = document.getElementById("errorSection");

const status = document.getElementById("status");
const trustScore = document.getElementById("trustScore");
const reasons = document.getElementById("reasons");
const aiSummary = document.getElementById("aiSummary");
const errorMessage = document.getElementById("errorMessage");

const newAnalysisButton = document.getElementById("newAnalysisButton");
const retryButton = document.getElementById("retryButton");

let selectedFile = null;


// ============================================
// CHOOSE FILE
// ============================================

chooseButton.addEventListener("click", function (event) {
    event.stopPropagation();
    documentInput.click();
});


// ============================================
// UPLOAD AREA CLICK
// ============================================

uploadArea.addEventListener("click", function (event) {
    if (
        event.target !== chooseButton &&
        !chooseButton.contains(event.target)
    ) {
        documentInput.click();
    }
});


// ============================================
// FILE SELECTION
// ============================================

documentInput.addEventListener("change", function () {

    if (this.files && this.files.length > 0) {

        selectedFile = this.files[0];

        fileName.textContent = selectedFile.name;

        analyzeButton.disabled = false;

        console.log("Selected file:", selectedFile.name);
    }
});


// ============================================
// ANALYZE DOCUMENT
// ============================================

analyzeButton.addEventListener("click", async function (event) {

    event.preventDefault();

    if (!selectedFile) {
        showError("Please select a document first.");
        return;
    }

    analyzeButton.disabled = true;

    showLoading();

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/upload",
            {
                method: "POST",
                body: formData
            }
        );

        if (!response.ok) {

            const errorText = await response.text();

            throw new Error(
                "Server error: " +
                response.status +
                " " +
                errorText
            );
        }

        const data = await response.json();

        console.log("Backend response:", data);

        displayResult(data);

    } catch (error) {

        console.error("Analysis error:", error);

        showError(error.message);

    } finally {

        analyzeButton.disabled = false;
    }
});


// ============================================
// DISPLAY ACTUAL BACKEND RESULT
// ============================================

function displayResult(data) {

    loadingSection.style.display = "none";
    errorSection.style.display = "none";
    resultSection.style.display = "block";

    const reportData = data.report || data;

    // FINAL VERDICT FROM BACKEND

    status.textContent =
        reportData.status || "Manual Review Required";


    // SCORE FROM BACKEND

    const score = reportData.trust_score;

    trustScore.textContent =
        score !== null && score !== undefined
            ? score
            : "N/A";


    // FINDINGS FROM BACKEND

    reasons.innerHTML = "";

    const findings = Array.isArray(reportData.reasons)
        ? reportData.reasons
        : [];

    if (findings.length > 0) {

        findings.forEach(function (finding) {

            const li = document.createElement("li");

            li.textContent = finding;

            reasons.appendChild(li);
        });

    } else {

        const li = document.createElement("li");

        li.textContent =
            "No structured findings were returned by the backend.";

        reasons.appendChild(li);
    }


    // AI FORENSIC REPORT FROM BACKEND

    aiSummary.textContent =
        reportData.ai_summary ||
        reportData.final_report ||
        "No AI forensic report was returned.";

}


// ============================================
// SHOW LOADING
// ============================================

function showLoading() {

    resultSection.style.display = "none";
    errorSection.style.display = "none";
    loadingSection.style.display = "block";

}


// ============================================
// SHOW ERROR
// ============================================

function showError(message) {

    loadingSection.style.display = "none";
    resultSection.style.display = "none";
    errorSection.style.display = "block";

    errorMessage.textContent = message;

}


// ============================================
// ANALYZE ANOTHER DOCUMENT
// ============================================

newAnalysisButton.addEventListener("click", function () {
    resetPage();
});


// ============================================
// RETRY
// ============================================

retryButton.addEventListener("click", function () {
    resetPage();
});


// ============================================
// RESET PAGE
// ============================================

function resetPage() {

    selectedFile = null;

    documentInput.value = "";

    fileName.textContent = "No file selected";

    analyzeButton.disabled = true;

    resultSection.style.display = "none";
    loadingSection.style.display = "none";
    errorSection.style.display = "none";

}