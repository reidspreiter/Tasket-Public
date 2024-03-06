// Gets delinquency documents
async function get_delinquency() {
    add_loader();
    const property = document.getElementById("property").value;
    const currDate = reformat_date(document.getElementById("post-date").value);
    const dueDate = reformat_date(document.getElementById("due-date").value);
    const del = document.getElementById("del").value;

    try {
        const response = await fetch(`/get_delinquency?prop=${encodeURIComponent(property)}&curr=${encodeURIComponent(currDate)}&due=${encodeURIComponent(dueDate)}&del=${encodeURIComponent(del)}`, {
            method: "POST"
        });
        const data = await response.json();
        
        if (!data.hasOwnProperty("message")) {
            throw new CustomError(data);
        } 
        const numPages = data["message"];
        let files = [];
        for (let i = 0; i < numPages; i++) {
            files.push(collect_files(i));
        }
        let results = await Promise.all(files);
        clear_files();
        download_zip(results);

    } catch (error) {
        handle_error(error);
    }
}

// Collects a specific file from the database
async function collect_files(page) {
    const response = await fetch(`/get_files?page=${encodeURIComponent(page)}`, {
        method: "POST"
    });
    const data = await response.json();
    if (!data.hasOwnProperty("message")) {
        throw new CustomError(data);
    }
    return data["message"];
}

// Clears files from database
async function clear_files() {
    const response = await fetch('/clean');
    const data = await response.json();
    if (!data.hasOwnProperty("message")) {
        throw new CustomError(data);
    }
}

// Creates and downloads a zip file
function download_zip(files) {
    let zip = new JSZip();
    let zipFiles = [];
    for (let file of files) {
        const binaryString = atob(file["content"]);
        const bytes = new Uint8Array(binaryString.length);
        for (let i = 0; i < binaryString.length; i++) {
            bytes[i] = binaryString.charCodeAt(i);
        }
        zipFiles.push({name: file["title"], content: bytes});
    }
    zipFiles.map((value) => zip.file(value.name, value.content));

    zipTitle = `${get_todays_date()}DEL.zip`;
    zip.generateAsync({ type: "blob" })
    .then((content) => {
        let link = document.createElement('a');
        link.href = URL.createObjectURL(content);
        link.download = zipTitle;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });
    banner("success", `Downloading ${zipTitle}`);
}

/*
 * Key List Task Function
 */
async function get_key_list() {
    add_loader();
    const units = document.getElementById("units").value;
    const checkboxes = document.getElementsByName("building");
    const pullInOrder = document.getElementById("pull-in-order").checked;
    const reciever = document.getElementById("email-address").value;
    let buildings = "";

    for (let checkbox of checkboxes) {
        if (checkbox.checked) {
            buildings += checkbox.value + " ";
        }
    }
    try {
        const response = await fetch(`/get_key_list?units=${encodeURIComponent(units)}&buildings=${encodeURIComponent(buildings)}&reciever=${encodeURIComponent(reciever)}&PIO=${encodeURIComponent(pullInOrder)}`, {
            method: "POST"
        });
        const data = await response.json();

        if (!data.hasOwnProperty("message")) {
            throw new CustomError(data);
        }
        const keycodes = data["message"];
        banner("success", "Keys pulled");
        expanded_results(keycodes);
    } catch(error) {
        handle_error(error);
    }
}

// Gets and downloads a property walk map
async function get_property_walk() {
    add_loader();
    const units = document.getElementById("units").value;
    const checkboxes = document.getElementsByName("building");
    const addKeys = document.getElementById("add-keys").checked;
    const pullInOrder = document.getElementById("pull-in-order").checked;
    let buildings = [];

    for (let checkbox of checkboxes) {
        if (checkbox.checked) {
            buildings += checkbox.value + " ";
        }
    }

    try {
        const response = await fetch(`/get_property_walk?units=${encodeURIComponent(units)}&buildings=${encodeURIComponent(buildings)}&addKeys=${encodeURIComponent(addKeys)}&PIO=${encodeURIComponent(pullInOrder)}`, {
            method: "POST"
        });
        const data = await response.json();

        if (!data.hasOwnProperty("message")) {
            throw new CustomError(data);
        }
        let mapFile = data["message"];
        download_file(mapFile);
    } catch(error) {
        handle_error(error);
    }
}

// Populates and downloads a transfer form
async function get_transfer_form() {
    add_loader();
    const name = document.getElementById("res-name").value;
    const unit = document.getElementById("unit-number").value;
    const moveOut = reformat_date(document.getElementById("move-out").value);
    const fee = document.getElementById("fee").value;
    const resNum = document.getElementById("res-num").value;

    try {
        const response = await fetch(`/get_transfer_form?name=${encodeURIComponent(name)}&unit=${encodeURIComponent(unit)}&moveout=${encodeURIComponent(moveOut)}&fee=${encodeURIComponent(fee)}&resnum=${encodeURIComponent(resNum)}`, {
            method: "POST"
        });
        const data = await response.json();

        if (!data.hasOwnProperty("message")) {
            throw new CustomError(data);
        }
        const transferForm = data["message"];
        download_file(transferForm);
    } catch(error) {
        handle_error(error);
    }
}

// Function to decode and download file
function download_file(file) {
    let content = file["content"];
    const binaryString = atob(content);
    const bytes = new Uint8Array(binaryString.length);
    for (let i = 0; i < binaryString.length; i++) {
        bytes[i] = binaryString.charCodeAt(i);
    }
    const blob = new Blob([bytes], { type: "application/octet-stream"});

    let link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = file["title"];

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    banner("success", `Downloading ${file["title"]}`);
}

// Allocates a utility spreadsheet
async function allocate_utilities() {
    add_loader();
    const invoice = document.getElementById("invoice").value;
    const accounts = document.getElementById("accounts").value;
    
    try {
        const response = await fetch(`/allocate_utilities?csv=${encodeURIComponent(invoice)}&act=${encodeURIComponent(accounts)}`, {
            method: "POST"
        });
        const data = await response.json();
        if (!data.hasOwnProperty("message")) {
            throw new CustomError(data);
        }
        const balances = data["message"];
        const errors = data["errors"];
        banner("success", "Utilities allocated successfully");
        expanded_results(balances, errors);
    } catch(error) {
        handle_error(error);
    }
}