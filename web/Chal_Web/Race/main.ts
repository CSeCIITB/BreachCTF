
const votesElement = document.getElementById("votes") as HTMLSpanElement;
const donationElement = document.getElementById("donation") as HTMLInputElement;

document.addEventListener("DOMContentLoaded", () => {
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

            const result = await response.json();
            responseText.innerText = result.message;
        } catch (error) {
            responseText.innerText = "Error submitting choice.";
            console.error("Error:", error);
        }
    }

    submitButton.addEventListener("click", sendChoice);
});

const votesStatusUpdater = async () => {
try {
    const response = await fetch("http://127.0.0.1:8000/votes/", {
        method: "GET",
        headers: { "Content-Type": "application/json" },
        // body: JSON.stringify({ selected_option: selectedOption })
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

    async function sendChoice(i: number) {
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

            const result = await response.json();
            console.log(`Request ${i}:`, result.message);
        } catch (error) {
            console.error(`Error in request ${i}:`, error);
        }
    }

    // Fire many requests with slight delays to increase the chance of a race condition
    for (let i = 0; i < 100; i++) {
        setTimeout(() => sendChoice(i * 100), Math.random() * 200);
    }
};

// Attach the function to the button
const overloadBut = document.getElementById("overload") as HTMLButtonElement;
overloadBut.addEventListener("click", customResponseOverload);

// customResponseOverload();

