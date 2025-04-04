
const votesElement = document.getElementById("votes") as HTMLSpanElement;
const donationElement = document.getElementById("donation") as HTMLInputElement;
const processingEl = document.getElementById("processingEl") as HTMLSpanElement;
const submitButton = document.getElementById("submit") as HTMLButtonElement;
const selectElement = document.getElementById("options") as HTMLSelectElement;
const responseText = document.getElementById("response") as HTMLParagraphElement;
async function sendChoice() {
    const selectedOption = selectElement.value;

    try {
        const response = await fetch("http://127.0.0.1:8000/submit/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ selected_option: selectedOption, donation: donationElement.value })
        });
        processingEl.innerText = "Processing your vote..."
        const result = await response.json();
        processingEl.innerText = ""
        responseText.innerText = result.message;

        // processingEl.innerText = "";
    } catch (error) {
        responseText.innerText = "Error submitting choice.";
        console.error("Error:", error);
    }
}
async function sendChoiceOverload(i: number) {
    const selectedOption = "Candidate C";

    try {
        const response = await fetch("http://127.0.0.1:8000/submit/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 
                selected_option: selectedOption, 
                donation: "s".repeat(i) // Send increasingly larger payloads 
            })
        });
        processingEl.innerHTML = "Processing..."

        const result = await response.json();

        processingEl.innerHTML = ""
        console.log(`Request ${i}:`, result.message);
    } catch (error) {
        console.error(`Error in request ${i}:`, error);
    }
}

document.addEventListener("DOMContentLoaded", () => {


    
    
});

const votesStatusUpdater = async () => {
try {
    const response = await fetch("http://127.0.0.1:8000/votes/", {
        method: "GET",
        headers: { "Content-Type": "application/json" },
    });

    const result = await response.json();
    votesElement.innerHTML = result.message;
} catch (error) {
    votesElement.innerText = "Error submitting choice.";
    console.error("Error:", error);
}
}

setInterval(votesStatusUpdater, 200);
const customResponseOverload = async () => {
    console.log("Custom response overload started");

    for (let i = 0; i < 50; i++) {
        setTimeout(() => sendChoiceOverload(i * 100), i*3);
    }
};

// Attach the function to the button
const overloadBut = document.getElementById("overload") as HTMLButtonElement;
overloadBut.addEventListener("click", customResponseOverload);
submitButton.addEventListener("click", sendChoice);

// customResponseOverload();

