def sort_utilities(invoice, accounts):
    invoice = invoice.split("\n")
    accounts = accounts.split("\n")
    errors = []

    for i, string in enumerate(invoice):
        if "#" in string:
            account_number = string[string.index("#") + 1:]
            balance = invoice[i+1].split("\t")[-1]
            balance = balance.replace("\"", "").replace(",", "")
            try:
                accounts[accounts.index(account_number)] = balance
            except ValueError:
                errors.append(account_number)

    accounts = "\n".join(accounts)
    errors = "\n".join(errors)
    return accounts, errors