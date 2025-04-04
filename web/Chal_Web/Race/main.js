"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
const votesElement = document.getElementById("votes");
const donationElement = document.getElementById("donation");
const processingEl = document.getElementById("processingEl");
const submitButton = document.getElementById("submit");
const selectElement = document.getElementById("options");
const responseText = document.getElementById("response");
function sendChoice() {
    return __awaiter(this, void 0, void 0, function* () {
        const selectedOption = selectElement.value;
        try {
            const response = yield fetch("http://127.0.0.1:8000/submit/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ selected_option: selectedOption, donation: donationElement.value })
            });
            processingEl.innerText = "Processing your vote...";
            const result = yield response.json();
            processingEl.innerText = "";
            responseText.innerText = result.message;
            // processingEl.innerText = "";
        }
        catch (error) {
            responseText.innerText = "Error submitting choice.";
            console.error("Error:", error);
        }
    });
}
function sendChoiceOverload(i) {
    return __awaiter(this, void 0, void 0, function* () {
        const selectedOption = "Candidate C";
        try {
            const response = yield fetch("http://127.0.0.1:8000/submit/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    selected_option: selectedOption,
                    donation: "s".repeat(i) // Send increasingly larger payloads 
                })
            });
            processingEl.innerHTML = "Processing...";
            const result = yield response.json();
            processingEl.innerHTML = "";
            console.log(`Request ${i}:`, result.message);
        }
        catch (error) {
            console.error(`Error in request ${i}:`, error);
        }
    });
}
document.addEventListener("DOMContentLoaded", () => {
});
const votesStatusUpdater = () => __awaiter(void 0, void 0, void 0, function* () {
    try {
        const response = yield fetch("http://127.0.0.1:8000/votes/", {
            method: "GET",
            headers: { "Content-Type": "application/json" },
        });
        const result = yield response.json();
        votesElement.innerHTML = result.message;
    }
    catch (error) {
        votesElement.innerText = "Error submitting choice.";
        console.error("Error:", error);
    }
});
setInterval(votesStatusUpdater, 200);
const customResponseOverload = () => __awaiter(void 0, void 0, void 0, function* () {
    console.log("Custom response overload started");
    for (let i = 0; i < 50; i++) {
        setTimeout(() => sendChoiceOverload(i * 100), i * 3);
    }
});
// Attach the function to the button
const overloadBut = document.getElementById("overload");
overloadBut.addEventListener("click", customResponseOverload);
submitButton.addEventListener("click", sendChoice);
// customResponseOverload();
