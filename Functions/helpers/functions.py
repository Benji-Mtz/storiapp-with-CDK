from email.message import EmailMessage
import smtplib
import csv
import io

calendar = {
    '1': "Januray",
    '2': "Febrary",
    '3': "March",
    '4': "April",
    '5': "May",
    '6': "June",
    '7': "July",
    '8': "August",
    '9': "September",
    '10': "October",
    '11': "November",
    '12': "December"
}


def reading_csv(data):
    diccionary_aux = {}
    count = 0

    reader = csv.reader(io.StringIO(data))
    for row in reader:
        if count == 0:
            for col in row:
                diccionary_aux[col] = []
                # print(col)
            count = count + 1
            return diccionary_aux


def reading_dict(data, keys_dict):
    reader = csv.DictReader(io.StringIO(data))
    for row in reader:
        for llave in row:
            keys_dict[llave].append(row[llave])
    return keys_dict


def total_balance(general_dict):

    for llave in general_dict:
        if 'Transaction' in llave:
            tb = sum([float(value) for value in general_dict[llave]])
            return tb
        else:
            pass


def transactions_for_month(general_dict):
    dates = {}
    for llave in general_dict:
        if 'Date' in llave:
            dates = general_dict[llave]
        else:
            pass

    register_dates = {}
    default_day = 1

    for date in dates:
        month_int, _ = date.split('/')
        month_str = calendar[month_int]

        if month_str in register_dates:
            register_dates[month_str] = register_dates[month_str] + 1
        else:
            register_dates[month_str] = default_day

    return register_dates


def average_amount(general_dict):
    for llave in general_dict:
        if 'Transaction' in llave:
            liststr_to_float = [float(value) for value in general_dict[llave]]
            debit = sum(
                [negative for negative in liststr_to_float if negative < 0]) / 2
            credit = sum(
                [positive for positive in liststr_to_float if positive >= 0]) / 2

            return debit, credit
        else:
            pass


def send_email(data, sender_email,  receiver_email, token):
    msg = EmailMessage()
    msg['Subject'] = 'Reporte de transaciones'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    concat_transactions = ''
    counter = 1

    for tx in data['transactions']:
        if counter == len(data['transactions']):
            concat_transactions += f"<li>Number of transactions in { tx }: <b>{data['transactions'][tx]}</b></li>"
        else:
            concat_transactions += f"<li>Number of transactions in { tx }: <b>{data['transactions'][tx]}</b></li>" + "\n"
            counter = counter + 1

    msg.set_content(f'''
    <!DOCTYPE html>
    <html>
        <body>
            <div style="background-color:#DAF7A6;padding:10px 20px;">
                <h1 style="font-family:Georgia, 'Times New Roman', Times, serif; color:#0572b0; text-align:center;">Stori Report</h1>
            </div>
            <br />
            <div style="padding:20px 0px">
                <div style="height: 500px;width:400px">
                    <img src="https://blog.storicard.com/wp-content/uploads/2019/07/Stori-horizontal-11.jpg" style="height: 300px; text-align:center;">
                    <div style="text-align:justify;">
                        <h2>This was the behavior of your account.</h2>
                        <p style="font-size: 1.5em;">
                            <ul>
                                <li>Total balance is:&nbsp;<b>{ data['total_balance'] }</b></li>
                                {concat_transactions}
                                <li>Average debit amount:&nbsp;<b>{ data['avg_debit'] }</b></li>
                                <li>Average credit amount:&nbsp;<b>{ data['avg_credit'] }</b></li>
                            </ul>
                        </p>
                        <a href="#">Leer más</a>
                    </div>
                </div>
            </div>
        </body>
    </html>
    ''', subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_email, token)
        smtp.send_message(msg)
