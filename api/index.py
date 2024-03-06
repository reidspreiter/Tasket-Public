from flask import Flask, url_for, render_template, request, redirect, jsonify, session
from firebase_admin import credentials, db, initialize_app
from _utils.keycodes import get_unit_numbers, get_keycodes
from _utils.delunits import DelUnits
from _utils.make_map import make_map
from _utils.sort_to_walk import sort_to_walk
from _utils.transfer_form import create_transfer_form
from _utils.email import send_email
from _utils.utilities import sort_utilities
import base64

# Verify database credentials
cred = credentials.Certificate("serviceAccountKey.json")

# Initialize realtime database
initialize_app(cred, {
    "databaseURL": "URL"
})

# Create Flask app
app = Flask(__name__)

# Home Page
@app.route("/")
def home():
    return render_template("home.html")

# Task page with key list form
@app.route("/key_list")
def key_list():
    return render_template("key_list.html")

# Get and return key list
@app.route("/get_key_list", methods=["POST"])
def get_key_list():
    try:
        units = request.args.get("units")
        buildings = request.args.get("buildings")
        email_reciever = request.args.get("reciever")
        pull_in_order = False if request.args.get("PIO") == "false" else True

        unit_numbers = get_unit_numbers(units, buildings)
        codes = get_keycodes(unit_numbers, pull_in_order)

        if codes == "":
            return jsonify({"warn": "No valid units entered"})
        
        if email_reciever != "":
            subject = "Key List Result"
            body = f"Here are your keycodes:\n\n{codes}\n\nHave a great day!"
            send_email(subject, body, email_reciever)
        return jsonify({"message": codes})
    except Exception:
        return jsonify({"error": "Failed to pull keys"})

# Task page with delinquency form
@app.route("/delinquency")
def delinquency():
    return render_template("delinquency.html")

# Create delinquency files, store in database, and return number of files
@app.route("/get_delinquency", methods=["POST"])
def get_delinquency():
    try:
        property_name = request.args.get("prop")
        curr_date = request.args.get("curr")
        due_date = request.args.get("due")
        delinquency = request.args.get("del")

        if delinquency[0:len(property_name)] != property_name:
            return jsonify({"warn": "Invalid delinquency info"})
        
        delinquent_units = DelUnits()
        pdfs = delinquent_units.get_delinquency(delinquency, property_name, curr_date, due_date)

        for pdf in pdfs:
            pdf["content"] = base64.b64encode(pdf["content"]).decode("utf-8")

        ref = db.reference("/documents")
        ref.child("blobs").set(pdfs)
        return jsonify({"message": len(pdfs)})
    except Exception:
        return jsonify({"error": "NTV generation failure"})
    
# Return a specific document stored in the database
@app.route("/get_files", methods=["POST"])
def get_files():
    try:
        page = int(request.args.get("page"))
        ref = db.reference("/documents")
        documents = ref.child("blobs").get()
        return jsonify({"message": documents[page]})
    except Exception:
        return jsonify({"error": f"Page {page} retrieval failure"})
    
# Remove files from database once retrieved
@app.route("/clean", methods=["GET", "POST"])
def clean():
    try:
        ref = db.reference("/documents")
        ref.child("blobs").delete()
        return jsonify({"message": "success"})
    except Exception:
        return jsonify({"error": "File deletion failure"})

# Task page with transfer form form
@app.route("/transfer_form")
def transfer_form():
    return render_template("transfer_form.html")

# Get and return transfer form
@app.route("/get_transfer_form", methods=["POST"])
def get_transfer_form():
    try:
        name = request.args.get("name")
        unit = request.args.get("unit")
        move_out = request.args.get("moveout")
        fee = f"${request.args.get('fee')}"
        res_num = request.args.get("resnum")

        transfer_form = create_transfer_form(name, unit, move_out, fee, res_num)
        transfer_form["content"] = base64.b64encode(transfer_form["content"]).decode("utf-8")

        return jsonify({"message": transfer_form})
    except Exception:
        return jsonify({"error": "Transfer form failure"})

# Task page with property walk form
@app.route("/property_walk")
def property_walk():
    return render_template("property_walk.html")

# Get and return property walk form
@app.route("/get_property_walk", methods=["POST"])
def get_property_walk():
    try:
        units = request.args.get("units")
        buildings = request.args.get("buildings")
        add_keys = False if request.args.get("addKeys") == "false" else True
        pull_in_order = False if request.args.get("PIO") == "false" else True

        unit_numbers = get_unit_numbers(units, buildings)
        if unit_numbers == []:
            return jsonify({"warn": "No valid units entered"})
        
        unit_numbers = sort_to_walk(unit_numbers)
        codes = get_keycodes(unit_numbers, pull_in_order) if add_keys else None
        property_walk = make_map(unit_numbers, codes)
        property_walk["content"] = base64.b64encode(property_walk["content"]).decode("utf-8")

        return jsonify({"message": property_walk})
    except Exception:
        return jsonify({"error": "Property walk failure"})

# Task page with utilities form
@app.route("/utilities")
def utilities():
    return render_template("utilities.html")

# Task to allocate utility data to spreadsheet
@app.route("/allocate_utilities", methods = ["POST"])
def allocate_utilities():
    try:
        invoice = request.args.get("csv")
        accounts = request.args.get("act")
        if invoice[:4] != '"Due' or not accounts[0].isnumeric():
            return jsonify({"warn": "Invalid invoice or account info"})
        
        sorted_balances, errors = sort_utilities(invoice, accounts)
        print(sorted_balances)
        return jsonify({"message": str(sorted_balances), "errors": str(errors)})
    except Exception:
        return jsonify({"error": "Utility allocation failure"})

if __name__ == "__main__":
    app.run(debug=True)