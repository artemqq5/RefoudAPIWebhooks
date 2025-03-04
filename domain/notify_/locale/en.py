messages_en = {

    ################ CLOSE ACCOUNT ################
    "REFUND-ADMIN": '''🔖 2\\2 Refund for account <b>{account_email}</b> | <b>{team_name}</b>!
    ━━━━━━━━━━━━━━━━
    MCC: <b>{mcc_name}</b>
    Сustomer ID: <code>{customer_id}</code>
    
    Account spend: <b>{spend}</b>
    Refund amount: <b>{refund_value}</b>
    Refund commission: <b>{commission}</b>''',

    "REFUND-CLIENT": '''✅ Refund for account <b>{account_email}</b> completed!
    ━━━━━━━━━━━━━━━━
    MCC: <b>{mcc_name}</b>
    Сustomer ID: <code>{customer_id}</code>
    
    Refund amount: <b>{refund_value}</b>
    Refund commission: <b>{commission}</b>''',

    ################ CREATE ACCOUNT ################
    "VERIFICATED-ACCOUNT-ADMIN": ''' 🟢 2\\2 Account <b>{account_email}</b> created with balance <b>{amount}$</b>!
    ━━━━━━━━━━━━━━━━━━━━
    ✅ Verification confirmed!
    ━━━━━━━━━━━━━━━━━━━━━━
    MCC: <b>{mcc_name}</b>
    Сustomer ID: <code>{customer_id}</code>
    Team: <b>{team_name}</b>''',

    "VERIFICATED-ACCOUNT-CLIENT": ''' ✅ Verification confirmed! <b>{account_email}</b> with balance <b>{amount}$</b>!
    MCC: <b>{mcc_name}</b>
    Сustomer ID: <code>{customer_id}</code>''',

    ################ CREATE BUDGET ################
    "CREATE-BUDGET-ADMIN": '''🏦 Account budget has been created! <b>{account_email}</b>!
    ━━━━━━━━━━━━━━━━
    <b>{amount}</b>
    ━━━━━━━━━━━━━━━━
    MCC: <b>{mcc_name}</b>
    Customer ID: <code>{customer_id}</code>
    Team: <b>{team_name}</b>''',

    "CREATE-BUDGET-CLIENT": '''🏦 Account budget has been created! <b>{account_email}</b>!
    ━━━━━━━━━━━━━━━━━
    <b>{amount}</b>
    ━━━━━━━━━━━━━━━━━
    MCC: <b>{mcc_name}</b>
    Сustomer ID: <code>{customer_id}</code>''',

    ############### INVITE ##################
    "SEND-INVITE-ADMIN": '''📩 Account invitation sent! <b>{account_email}</b>!
    ━━━━━━━━━━━━━━━━━━━━
    MCC: <b>{mcc_name}</b>
    Сustomer ID: <code>{customer_id}</code>
    Team: <b>{team_name}</b>''',

    "SEND-INVITE-CLIENT": '''📩 Account invitation sent! <b>{account_email}</b>!
    ━━━━━━━━━━━━━━━━
    MCC: <b>{mcc_name}</b>
    Customer ID: <code>{customer_id}</code>''',
}
