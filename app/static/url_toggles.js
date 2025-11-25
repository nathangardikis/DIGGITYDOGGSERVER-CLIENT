
const formatToggle1 = document.getElementById("format-toggle-1");
const formatToggle2 = document.getElementById("format-toggle-2");
const formatToggle3 = document.getElementById("format-toggle-3");
const apiToggle = document.getElementById("api-toggle");
const apiSelection = apiToggle.querySelector(".selection");
const searchbar = document.getElementById("searchbar");

const dzBtn = document.getElementById("dz-btn");
const spBtn = document.getElementById("sp-btn");
const ytBtn = document.getElementById("yt-btn");

formatToggle2.style.display = "none";
formatToggle3.style.display = "none";

const ytOptionsContainer = document.getElementById("youtube-options-container");

ytBtn.addEventListener("mouseup", () => {
    formatToggle2.style.display = "none";
    formatToggle3.style.display = "none";
    formatToggle1.style.display = "inline-block";
    ytOptionsContainer.style.display = "block";
    searchbar.placeholder = "Enter " + ytBtn.innerHTML.toLowerCase() + " URL here...";
});

dzBtn.addEventListener("mouseup", () => {
    formatToggle1.style.display = "none";
    formatToggle3.style.display = "none";
    formatToggle2.style.display = "inline-block";
    ytOptionsContainer.style.display = "none";
    searchbar.placeholder = "Enter " + dzBtn.innerHTML.toLowerCase() + " URL here...";
});

spBtn.addEventListener("mouseup", () => {
    formatToggle1.style.display = "none";
    formatToggle2.style.display = "none";
    formatToggle3.style.display = "inline-block";
    ytOptionsContainer.style.display = "none";
    searchbar.placeholder = "Enter " + spBtn.innerHTML.toLowerCase() + " URL here...";
});

