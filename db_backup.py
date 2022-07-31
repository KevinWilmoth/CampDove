import transaction_table
import json
import tab_table

if __name__ == '__main__':
    allTransactions   = transaction_table.get_all_items()
    allTabs           = tab_table.get_all_tabs()
    json_transactions = json.dumps(allTransactions, indent=4)
    json_tabs         = json.dumps(allTabs, indent=4)

    with open("db_backup/transactions.json", "w") as outfile:
        outfile.write(json_transactions)
    with open("db_backup/tabs.json", "w") as outfile:
        outfile.write(json_tabs)

    exit(0)