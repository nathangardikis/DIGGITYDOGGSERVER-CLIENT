const verifyButton = document.getElementById("verify-button");
const retryButton = document.getElementById("retry-btn");
const emailEntry = document.getElementById("email-entry");
const emailData = document.getElementById("email-data");

const emailCard1 = document.getElementById("email-card-1");
const emailCard2 = document.getElementById("email-card-2");
const registerCard = document.getElementById("register-card");

const url = "http://127.0.0.1:5000/auth/verify/";

function verifyEmail () {
    $.ajax ({
        url: url + emailEntry.value,
        type: 'GET',
        data: null,
        success: function (response) {
            if (response == "found") {
                emailCard1.style.display = "none";
                emailCard2.style.display = "none";
                registerCard.style.display = "block";
                emailData.value = emailEntry.value;
            } else if (response == "missing") {
                emailCard1.style.display = "none";
                emailCard2.style.display = "block";
                registerCard.style.display = "none";
            } else if (response == "active") {
                emailCard1.style.display = "none";
                emailCard2.style.display = "block";
                registerCard.style.display = "none";
            }
        },
        error: function () {
            console.log("error");
        }
    });
}



verifyButton.addEventListener("mouseup", () => {
    verifyEmail();
});

retryButton.addEventListener("mouseup", () => {
    emailCard1.style.display = "block";
    emailCard2.style.display = "none";
    registerCard.style.display = "none";
    emailEntry.value = "";
});

emailEntry.addEventListener("keydown", (event) => {
    if (event.key == "Enter") {
        verifyEmail();
    }
});