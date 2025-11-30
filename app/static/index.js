const tabs = document.querySelectorAll("li");

function disable_tabs () {
    tabs.forEach((tab) => {
        tab.disabled = true;
    });
}

disable_tabs();