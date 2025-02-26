messages_uk = {
    ################ CLOSE ACCOUNT ################
    "REFUND-ADMIN": '''🔖 2\\2 Рефаунд акаунта <b>{account_email}</b> | <b>{team_name}</b>!
    ━━━━━━━━━━━━━━━━
    MCC: <b>{mcc_name}</b>
    Сustomer ID: <code>{customer_id}</<code>

    Спенд акаунта: <b>{spend}</b>
    Сума рефаунду: <b>{refund_value}</b>
    Комісія за рефаунд: <b>{commission}</b>''',

    "REFUND-CLIENT": '''✅ Рефаунд акаунта <b>{account_email}</b> завершено!
    ━━━━━━━━━━━━━━━━
    MCC: <b>{mcc_name}</b>
    Сustomer ID: <code>{customer_id}</<code>

    Сума рефаунду: <b>{refund_value}</b>
    Комісія за рефаунд: <b>{commission}</b>''',

    ############### CREATE ACCOUNT ################
    "VERIFICATED-ACCOUNT-ADMIN": '''🟢 2\\2 Створенно акаунт <b>{account_email}</b>!
    ━━━━━━━━━━━━━━━━
    ✅ Верефікацію підтверджено!
    ━━━━━━━━━━━━━━━━
    MCC: <b>{mcc_name}</b>
    Сustomer ID: <code>{customer_id}</<code>
    Команда: <b>{team_name}</b>''',

    "VERIFICATED-ACCOUNT-CLIENT": '''✅ Верефікацію підтверджено! <b>{account_email}</b>!
    MCC: <b>{mcc_name}</b>
    Сustomer ID: <code>{customer_id}</<code>''',

    ############### CREATE BUDGET ################
    "CREATE-BUDGET-ADMIN": '''🏦 Бюджет аккаунта створено! <b>{account_email}</b>!
    ━━━━━━━━━━━━━━━━
    <b>{amount}</b>
    ━━━━━━━━━━━━━━━━
    MCC: <b>{mcc_name}</b>
    Сustomer ID: <code>{customer_id}</<code>
    Команда: <b>{team_name}</b>''',

    "CREATE-BUDGET-CLIENT": '''🏦 Бюджет аккаунта створено! <b>{account_email}</b>!
    ━━━━━━━━━━━━━━━━
    <b>{amount}</b>
    ━━━━━━━━━━━━━━━━
    MCC: <b>{mcc_name}</b>
    Сustomer ID: <code>{customer_id}</code>''',

    ############### INVITE ################
    "SEND-INVITE-ADMIN": '''📩 Інвайт в акаунт відправлено! <b>{account_email}</b>!
    ━━━━━━━━━━━━━━━━
    MCC: <b>{mcc_name}</b>
    Сustomer ID: <code>{customer_id}</<code>
    Команда: <b>{team_name}</b>''',

    "SEND-INVITE-CLIENT": '''📩 Інвайт в акаунт відправлено! <b>{account_email}</b>!
    ━━━━━━━━━━━━━━━━
    MCC: <b>{mcc_name}</b>
    Сustomer ID: <code>{customer_id}</code>''',
}
