const tabs = document.querySelectorAll(".nav-button");
var activeTab = "";
const typeOptions = document.getElementById("type-options");
const URLOptions = document.getElementById("url-options");
const subTypes = typeOptions.querySelectorAll(".box-button");
var activeType = "";
const URLTypes = URLOptions.querySelectorAll(".box-button");
var activeURL = "";
const searchbar = document.querySelector(".searchbar");
const searchForm = document.getElementById("search-form");
const sbText = document.getElementById("sb-text");
const typeText = document.getElementById("type-text");
const searchBtn = document.getElementById("search-btn");
const homeTab = document.getElementById("Home");
const submissionsTab = document.getElementById("Submissions");
const indexTabs = [homeTab];

function check_tabs () {
    tabs.forEach((tab) => {
        if (tab.value != activeTab) {
            tab.disabled = false;
        }
        if (activeTab == "Home") {
            homeTab.style.display = "block";
        } else {
            homeTab.style.display = "none";
        }
    });
}

function set_active_tab () {
    tabs.forEach((tab) => {
        if (tab.disabled == true) {
            activeTab = tab.value;
        }
    });
}

tabs.forEach((tab) => {
    tab.addEventListener("mouseup", () => {
        tab.disabled = true;
        activeTab = tab.value;
        check_tabs();
    });
});

function check_types () {
    subTypes.forEach((st) => {
        if (st.value != activeType) {
            st.disabled = false;
        }
        if (st.value == "URL") {
            if (st.disabled == true) {
                URLOptions.style.display = "block";
            } else if (st.disabled == false) {
                URLOptions.style.display = "none";
            }
        }
    });
}

function check_urls () {
    URLTypes.forEach((ut) => {
        if (ut.value != activeURL) {
            ut.disabled = false;
        }
    });
}

subTypes.forEach((st) => {
    st.addEventListener("mouseup", () => {
        st.disabled = true;
        activeType = st.value;
        typeText.value = activeType;
        check_types();
        if (activeType == "URL") {
            searchbar.placeholder = "Enter " + activeType + " here...";
        } else {
            searchbar.placeholder = "Search " + activeType.toLocaleLowerCase() + " here...";
        }
    });
});

URLTypes.forEach((ut) => {
    ut.addEventListener("mouseup", () => {
        ut.disabled = true;
        activeURL = ut.value;
        check_urls();
    });
});

function execute_search () {
    let searchText = searchbar.value;
    sbText.value = searchText;
    if (searchText.length > 1) {
        searchForm.submit();
    } else {
        //do nothing 
    }
}

searchbar.addEventListener("keydown", (event) => {
    if (event.key == "Enter") {
        execute_search()
    }
});

searchBtn.addEventListener("mouseup", () => {execute_search()});