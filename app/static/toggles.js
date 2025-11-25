
const toggles = document.querySelectorAll(".toggle");
const body = document.querySelector("body");
const allItems = document.querySelectorAll(".drop-item");
const allSelections = document.querySelectorAll(".selection");
const containers = document.querySelectorAll(".options-container-1");

toggles.forEach((toggle) => {
    const selection = toggle.querySelector(".selection");
    const data = toggle.querySelector(".data");
    const items = toggle.querySelectorAll(".drop-item");
    const tg = toggle.querySelector(".tg");

    selection.addEventListener("mouseup", () => {
        items.forEach((item) => {
            if (item.style.display == "block") {
                item.style.display = "none";
                selection.style.borderBottomRightRadius = "0.5rem";
                selection.style.borderBottomLeftRadius = "0.5rem";
                tg.style.transform = "rotate(0deg)";
            } else {
                if (selection.innerHTML != item.innerHTML) {
                    item.style.display = "block";
                    selection.style.borderBottomRightRadius = "0rem";
                    selection.style.borderBottomLeftRadius = "0rem";
                    tg.style.transform = "rotate(-90deg)";
                }
            }
        });
    });

    body.addEventListener("mouseup", (event) => {
        if (event.target != selection) {
            items.forEach((i) => {
                i.style.display = "none";
            });
            selection.style.borderBottomRightRadius = "0.5rem";
            selection.style.borderBottomLeftRadius = "0.5rem";
            tg.style.transform = "rotate(0deg)";
        }
    });

    items.forEach((item) => {
        item.addEventListener("mouseup", () => {
            selection.innerHTML = item.innerHTML;
            items.forEach((i) => {
                i.style.display = "none";
            });
            data.value = item.innerHTML;
            selection.style.borderRadius = "0.5rem";
            tg.style.transform = "rotate(0deg)";
        });
    });
});
