
def mail_from_yahoo(from_email_address, 
                    to_email_address, 
                    Subject, 
                    content, 
                    footer, passcode):
    try:
        conn = smtplib.SMTP_SSL('smtp.mail.yahoo.com', 465)

        conn.ehlo()

        conn.login(from_email_address, passcode)

        conn.sendmail(from_email_address, to_email_address, Subject+content+footer)

        conn.quit()
        print('successful')

    except:
        print('failed')
