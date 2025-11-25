const tabs = document.querySelectorAll(".tab");
const emails = document.querySelectorAll(".email");
const settingsForm = document.getElementById("settings-form");

const requestSwitch = document.getElementById("allow-requests-switch");
const bitrateSwitch = document.getElementById("allow-bitrate-switch");
const accountSwitch = document.getElementById("allow-account-switch");
const blacklistSwitch = document.getElementById("enable-blacklist-switch");
const whitelistSwitch = document.getElementById("enable-whitelist-switch");
const showRequestSwitch = document.getElementById("show-requests-switch");




const generalSwitches = [
    requestSwitch,
    bitrateSwitch,
    accountSwitch,
    blacklistSwitch,
    whitelistSwitch,
    showRequestSwitch
];

var requestSwitchStatus;
var bitrateSwitchStatus;
var accountSwitchStatus;
var blacklistSwitchStatus;
var whitelistSwitchStatus;
var showRequestSwitchStatus;
var users = [];
var usernames = [];
var generalData = {};

var adminStatus = [];
var adminSwitchStatus;
var settingSwitchStatus;

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
        if (t.value == "General") {
            t.disabled = true;
        }
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

function on_switch (s) {
    s.style.backgroundColor = "rgb(49, 121, 66)"; 
    s.style.textIndent = "1.4rem";
}

function off_switch (s) {
    s.style.backgroundColor = "rgb(21, 24, 21)";
    s.style.textIndent = "0rem";
}

function toggle_switch (s) {
    var switchStatus;
    if (s.style.textIndent == "0rem") {
        on_switch(s);
        switchStatus = true;
    } else {
        off_switch(s);
        switchStatus = false;
    }
    return switchStatus;
}

function check_general_settings() {
    generalSwitches.forEach((gs) => {
        if (gs.style.textIndent == "0rem") {
            generalData[gs.name] = false;
        } else {
            generalData[gs.name] = true;
        }
    });
    console.log(generalData);
}

function apply_general_settings() {
    $.ajax ({
        url: 'http://127.0.0.1:5000/auth/apply-general',
        contentType: 'application/json',
        type: 'POST',
        data: JSON.stringify(generalData),
        success: function (response) {
            console.log(response);
        },
        error: function(response) {
            console.log(response);
        }
    });
}

function apply_admin_switch(status, username) {
    users.forEach((user) => {
        if (user.username == username) {
            user.admin = status;
        }
    })
}

function apply_setting_switch(status, username) {
    users.forEach((user) => {
        if (user.username == username) {
            user.allow_settings = status;
        }
    })
}

function get_users() {
    $.ajax ({
        url: 'http://127.0.0.1:5000/auth/apply-user',
        type: 'GET',
        contentType: 'application/json',
        dataType: 'json',
        success: function (response) {
            response.forEach((r) => {
                users.push(r);
            });
            users.forEach((user) => {
                usernames.push(user.username);
            });
        },
        error: function (response) {
            console.log(response);
        }
    })
}

function get_username_from_email(email) {
    var endpoint = "http:127.0.0.1:5000/get-user-from-email/" + email;
    $.ajax ({
        url: endpoint,
        type: 'GET',
        success: function(response) {
            return response;
        },
        error: function () {
            return error;
        }
    });
}

function get_emails () {
    var email_list = [];
    emails.forEach((e) => {
        email_list.push(e.innerHTML);
    });
    return email_list;
}

function apply_user_settings() {
    $.ajax ({
        url: 'http://127.0.0.1:5000/auth/apply-user',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(users),
        success: function(response) {
            console.log(response);
        },
        error: function(response) {
            console.log(response);
        }
    });
}


get_users();

check_general_settings();


document.getElementById("General").addEventListener("click", (event) => {
    if (event.target.id == "allow-requests-switch") {
        requestSwitchStatus = toggle_switch(requestSwitch);
        generalData["allow_requests"] = requestSwitchStatus;
        apply_general_settings();
    } else if (event.target.id == "allow-bitrate-switch") {
        bitrateSwitchStatus = toggle_switch(bitrateSwitch);
        generalData["allow_bitrate"] = bitrateSwitchStatus;
        apply_general_settings();
    } else if (event.target.id == "allow-account-switch") {
        accountSwitchStatus = toggle_switch(accountSwitch);
        generalData["allow_new_accounts"] = accountSwitchStatus;
        apply_general_settings();
    } else if (event.target.id == "enable-blacklist-switch") {
        blacklistSwitchStatus = toggle_switch(blacklistSwitch);
        generalData["enable_blacklist"] = blacklistSwitchStatus;
        apply_general_settings();
    } else if (event.target.id == "enable-whitelist-switch") {
        whitelistSwitchStatus = toggle_switch(whitelistSwitch);
        generalData["enable_whitelist"] = whitelistSwitchStatus;
        apply_general_settings();
    } else if (event.target.id == "show-requests-switch") {
        showRequestSwitchStatus = toggle_switch(showRequestSwitch);
        generalData["show_requests"] = showRequestSwitchStatus;
        apply_general_settings();
    }
});

document.getElementById("Users").addEventListener("click", (event) => {
    usernames.forEach((user) => {
        var adminSwitchId = user + "-admin-switch";
        var adminSwitch = document.getElementById(adminSwitchId);

        var settingSwitchId = user + "-allow-settings-switch";
        var settingSwitch = document.getElementById(settingSwitchId);
        if (event.target.id == adminSwitchId) {
            adminSwitchStatus = toggle_switch(adminSwitch);
            apply_admin_switch(adminSwitchStatus, user);
            apply_user_settings();
        } else if (event.target.id == settingSwitchId) {
            settingSwitchStatus = toggle_switch(settingSwitch);
            apply_setting_switch(settingSwitchStatus, user);
            apply_user_settings();
        }
    });
});
