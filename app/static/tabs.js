const tabs = document.querySelectorAll(".tab");

function pass () {};

function clear_tabs () {
    tabs.forEach((t) => {
        t.disabled = false;
    });
}

function clear_views () {
    tabs.forEach((t) => {
        try {
            let view = document.getElementById(t.value);
            view.style.visibility = "hidden";
        } catch {
            pass();
        }
    });
}

function show_tab (tab) {
    let view = document.getElementById(tab.value);
    view.style.visibility = "visible";
}

function check_tabs () {
    tabs.forEach((t) => {
        if (t.disabled == true) {
            show_tab(t);
        }
    });
}

tabs.forEach((tab) => {
    tab.addEventListener("mouseup", () => {
        clear_tabs();
        clear_views();
        tab.disabled = true;
        show_tab(tab);
    });
});

check_tabs();
