// Ensure email address is entered if email option is selected
let emailCheckbox = document.getElementById("email");
if (emailCheckbox != null) {
    emailCheckbox.addEventListener("change", () => {
        emailInput = document.getElementById("email-address");
        if (emailCheckbox.checked) {
            emailInput.required = true;
            emailInput.style.opacity = 1;
            emailInput.style.cursor = "text";
        } else {
            emailInput.required = false;
            emailInput.style.opacity = 0;
            emailInput.style.cursor = "default";
        }
    });
}

// Ensure add-keys is checked if pull-in-order is checked
let pullInOrderCheckbox = document.getElementById("pull-in-order");
if (pullInOrderCheckbox != null) {
    pullInOrderCheckbox.addEventListener("change", function() {
        if (pullInOrderCheckbox.checked) {
            if (!document.getElementById("add-keys").checked) {
                document.getElementById("add-keys").checked = true;
            }
        }
    });
}

// Ensure pull-in-order is not checked if add-keys is not checked
let addKeysCheckBox = document.getElementById("add-keys");
if (addKeysCheckBox != null) {
    addKeysCheckBox.addEventListener("change", function() {
        if (!addKeysCheckBox.checked) {
            if (document.getElementById("pull-in-order").checked) {
                document.getElementById("pull-in-order").checked = false;
            }
        }
    });
}

// Get today's date
function get_todays_date() {

    const today = new Date();
    const year = today.getFullYear();
    let month = today.getMonth() + 1;
    let day = today.getDate();

    month = month < 10 ? `0${month}` : month;
    day = day < 10 ? `0${day}` : day;

    return `${year}-${month}-${day}`;
}

// Get delinquency due date (3 days after today)
function get_due_date() {

    const today = new Date();
    const year = today.getFullYear();
    let month = today.getMonth() + 1;
    let day = today.getDate();
    let dayOfWeek = today.getDay();

    if (dayOfWeek > 2 && dayOfWeek < 6) {
        day = day + 5;
    } else {
        day = day + 3;
    }

    month = month < 10 ? `0${month}` : month;
    day = day < 10 ? `0${day}` : day;

    return `${year}-${month}-${day}`;
}

// Set delinquency form's post-date and due-date by default
if (document.getElementById("post-date") !== null) {
    document.getElementById("post-date").value = get_todays_date();
    document.getElementById("due-date").value = get_due_date();
}

// Set transfer form's move-out date by default
if (document.getElementById("move-out") !== null) {
    document.getElementById("move-out").min = get_todays_date();
}

// Reformat a date from yyyy-mm-dd to mm/dd/yyyy
function reformat_date(date) {
    let [year, month, day] = date.split("-");
    return `${month}/${day}/${year}`;
}

//Error Handling

function CustomError(message) {
    this.message = message;
}

function handle_error(error) {
    if (error instanceof CustomError) {
        const message = error["message"];
        if (message.hasOwnProperty("warn")) {
            banner("warn", message["warn"]);
        } else {
            banner("error", message["error"]);
        }
    } else {
        console.error(error);
        banner("error", "Please try again");
    }
}

function banner(type, message) {
    const formats = {
        "success": {"color": "#009500", "note": "Success:"},
        "warn": {"color": "#E69600", "note": "Warning:"},
        "error": {"color": "#be0000", "note": "Error:"},
    };
    const color = formats[type]["color"];
    const note = formats[type]["note"];

    let banner = document.querySelector(".banner");
    banner.style.backgroundColor = color;
    banner.innerText = `${note} ${message}`;
    banner.style.transition = "0.1s ease-out";

    remove_loader();
    banner.style.opacity = 1;

    const milliseconds = 3000;
    setTimeout( () => {
        banner.style.transition = "1s ease-in";
        banner.style.opacity = 0;
    }, milliseconds);
}

function add_loader() {
    const loaderDiv = document.createElement("div");
    loaderDiv.className = "loader";
    const resultsDiv = document.querySelector(".results");
    const bannerDiv = resultsDiv.querySelector(".banner");
    resultsDiv.insertBefore(loaderDiv, bannerDiv);
    document.querySelector(".loader").style.opacity = 1;
}

function remove_loader() {
    const loader = document.querySelector(".results .loader");
    if (loader) {
        loader.parentNode.removeChild(loader);
    }
}

function expanded_results(content, errors = "") {
    let elementsToAppend = [
        ["p", "Results:"],
        ["textarea", content],
    ];
    if (errors != "") {
        elementsToAppend.push(["p", "Errors:"]);
        elementsToAppend.push(["textarea", errors]);
    }

    let results = document.querySelector(".expanded-results");
    while (results.firstChild) {
        results.removeChild(results.firstChild);
    }
    elementsToAppend.forEach((element) => {
        console.log(element);
        let newElement = document.createElement(element[0]);
        newElement.textContent = element[1];
        results.appendChild(newElement);
    });
    results.style.maxHeight = "300vh";
    results.style.padding = "10px";
    results.style.marginTop = "14px";

    let milliseconds = 500;
    setTimeout( () => {
        results.style.display = "auto";
        results.style.transition = "opacity 2s";
        results.style.opacity = 1;
    }, milliseconds);
}