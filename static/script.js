// ==========================================
// TripMate AI & EcoVoyage - Client Controller
// ==========================================

let currentThreadId = localStorage.getItem("travel_thread_id") || null;
let latestAnswerMarkdown = "";
let stepperInterval = null;

// Configure Markdown parser
if (typeof marked !== "undefined") {
    marked.setOptions({
        gfm: true,
        breaks: true
    });
}

// ------------------------------------------
// Quick Prompt Handlers & Session Reset
// ------------------------------------------

function setPrompt(text) {
    const input = document.getElementById("userInput");
    if (!input) return;
    input.value = text;
    input.focus();
}

function startNewTrip() {
    localStorage.removeItem("travel_thread_id");
    currentThreadId = null;

    const input = document.getElementById("userInput");
    if (input) input.value = "";

    const resultSection = document.getElementById("resultSection");
    if (resultSection) resultSection.classList.add("hidden");

    resetStepperUI();
    hideError();
}

// ------------------------------------------
// UI Loading, Steppers & Status
// ------------------------------------------

function setLoading(isLoading) {
    const sendBtn = document.getElementById("sendBtn");
    const btnText = document.getElementById("btnText");
    const btnLoader = document.getElementById("btnLoader");

    if (!sendBtn) return;
    sendBtn.disabled = isLoading;

    if (isLoading) {
        if (btnText) btnText.classList.add("hidden");
        if (btnLoader) btnLoader.classList.remove("hidden");
        startStepperAnimation();
    } else {
        if (btnText) btnText.classList.remove("hidden");
        if (btnLoader) btnLoader.classList.add("hidden");
        stopStepperAnimation();
    }
}

const agentStepIds = ["step-flight", "step-hotel", "step-eco", "step-route"];

function resetStepperUI() {
    agentStepIds.forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            el.classList.remove("active", "completed");
        }
    });
}

function startStepperAnimation() {
    resetStepperUI();
    let currentStep = 0;

    const activate = (idx) => {
        agentStepIds.forEach((id, i) => {
            const el = document.getElementById(id);
            if (!el) return;
            if (i < idx) {
                el.classList.remove("active");
                el.classList.add("completed");
            } else if (i === idx) {
                el.classList.add("active");
                el.classList.remove("completed");
            } else {
                el.classList.remove("active", "completed");
            }
        });
    };

    activate(0);
    stepperInterval = setInterval(() => {
        currentStep++;
        if (currentStep < agentStepIds.length) {
            activate(currentStep);
        } else {
            clearInterval(stepperInterval);
        }
    }, 2800);
}

function stopStepperAnimation() {
    if (stepperInterval) {
        clearInterval(stepperInterval);
        stepperInterval = null;
    }
    // Mark all steps complete on response finish
    agentStepIds.forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            el.classList.remove("active");
            el.classList.add("completed");
        }
    });
}

// ------------------------------------------
// Error Messaging
// ------------------------------------------

function showError(message) {
    const errorBox = document.getElementById("errorBox");
    if (!errorBox) return;
    errorBox.textContent = message;
    errorBox.classList.remove("hidden");
}

function hideError() {
    const errorBox = document.getElementById("errorBox");
    if (!errorBox) return;
    errorBox.classList.add("hidden");
    errorBox.textContent = "";
}

// ------------------------------------------
// Render Response
// ------------------------------------------

function showResult(answer, threadId) {
    latestAnswerMarkdown = answer;

    const resultSection = document.getElementById("resultSection");
    const resultBox = document.getElementById("resultBox");
    const threadInfo = document.getElementById("threadInfo");

    if (typeof marked !== "undefined") {
        resultBox.innerHTML = marked.parse(answer);
    } else {
        resultBox.innerText = answer;
    }

    if (threadInfo) {
        threadInfo.textContent = `Thread ID: ${threadId || "active"}`;
    }

    if (resultSection) {
        resultSection.classList.remove("hidden");
        resultSection.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
    }
}

// ------------------------------------------
// API Call Orchestration
// ------------------------------------------

async function sendMessage() {
    hideError();

    const input = document.getElementById("userInput");
    if (!input) return;

    const message = input.value.trim();
    if (!message) {
        showError("Please enter your travel request first.");
        return;
    }

    setLoading(true);

    try {
        const response = await fetch("/api/travel", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message,
                thread_id: currentThreadId
            })
        });

        const data = await response.json();

        if (!response.ok || !data.success) {
            throw new Error(data.error || data.detail || "Failed to process travel plan.");
        }

        currentThreadId = data.thread_id;
        localStorage.setItem("travel_thread_id", currentThreadId);

        showResult(data.answer, data.thread_id);

    } catch (error) {
        showError(error.message || "Could not connect to backend server.");
    } finally {
        setLoading(false);
    }
}

// ------------------------------------------
// Action Buttons: Copy & PDF Download
// ------------------------------------------

function copyResult() {
    const resultBox = document.getElementById("resultBox");
    if (!resultBox) return;

    const text = resultBox.innerText;
    if (!text) {
        showError("No content to copy.");
        return;
    }

    navigator.clipboard.writeText(text)
        .then(() => {
            const copyBtn = document.querySelector(".copy-btn");
            if (!copyBtn) return;
            const oldText = copyBtn.textContent;

            copyBtn.textContent = "✓ Copied!";
            setTimeout(() => {
                copyBtn.textContent = oldText;
            }, 1500);
        })
        .catch(() => {
            showError("Could not copy result.");
        });
}

function downloadPDF() {
    const pdfContent = document.getElementById("pdfContent");

    if (!latestAnswerMarkdown || !pdfContent) {
        showError("No travel plan available to download.");
        return;
    }

    const downloadBtn = document.querySelector(".download-btn");
    const oldText = downloadBtn ? downloadBtn.textContent : "Download PDF";

    if (downloadBtn) {
        downloadBtn.textContent = "Preparing PDF...";
        downloadBtn.disabled = true;
    }

    const options = {
        margin: [0.4, 0.4, 0.4, 0.4],
        filename: `TripMate_Plan_${new Date().toISOString().slice(0, 10)}.pdf`,
        image: {
            type: "jpeg",
            quality: 0.98
        },
        html2canvas: {
            scale: 2,
            useCORS: true,
            backgroundColor: "#ffffff"
        },
        jsPDF: {
            unit: "in",
            format: "a4",
            orientation: "portrait"
        },
        pagebreak: {
            mode: ["avoid-all", "css", "legacy"]
        }
    };

    if (typeof html2pdf !== "undefined") {
        html2pdf()
            .set(options)
            .from(pdfContent)
            .save()
            .then(() => {
                if (downloadBtn) {
                    downloadBtn.textContent = oldText;
                    downloadBtn.disabled = false;
                }
            })
            .catch(() => {
                if (downloadBtn) {
                    downloadBtn.textContent = oldText;
                    downloadBtn.disabled = false;
                }
                showError("Could not download PDF.");
            });
    } else {
        window.print();
        if (downloadBtn) {
            downloadBtn.textContent = oldText;
            downloadBtn.disabled = false;
        }
    }
}

// ------------------------------------------
// Keyboard Shortcuts
// ------------------------------------------

document.addEventListener("keydown", function(event) {
    if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
        sendMessage();
    }
});