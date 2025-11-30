const typeToggle = document.getElementById("type-toggle");
const dropItems = typeToggle.querySelectorAll(".drop-item");
const searchbar = document.getElementById("searchbar");
const searchForm = document.getElementById("search-form");
const searchBtn = searchForm.querySelector(".search-btn");
const sec = document.getElementById("sec");
const dismissButton = document.getElementById("dismiss-button");

function execute_search () {
    let searchText = searchbar.value;
    if (searchText.length > 0) {
        searchForm.submit();
    } else {
        sec.style.visibility = "visible";
        searchbar.style.outline = "3px solid red";
        sec.style.marginTop = "-3rem";
        sec.style.opacity = "100";
    }
}

function dismiss_search_error () {
    searchbar.style.outline = "none";
    sec.style.marginTop = "0rem";
    sec.style.opacity = "0";
    sec.style.visibility = "hidden";
}

searchbar.addEventListener("mouseup", dismiss_search_error);
dismissButton.addEventListener("mouseup", dismiss_search_error);

searchBtn.addEventListener("mouseup", execute_search);

searchbar.addEventListener("keydown", (event) => {
    if (event.key == "Enter") {
        execute_search()
    }
});

dropItems.forEach((dropItem) => {
    dropItem.addEventListener("mouseup", () => {
        searchbar.placeholder = "Search " + dropItem.innerHTML.toLowerCase() + "...";
    });
});

const homeBtn = document.getElementById("home");
homeBtn.disabled = true;