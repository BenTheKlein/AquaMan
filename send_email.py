import smtplib
from email.mime.text import MIMEText

sender_email = "winery.solo@gmail.com"
sender_password = "ססס"
recipient_email = "benk1510@gmail.com"
subject = "AQUA NOTIFICATION IMPORTANT!!"
body = """
<html>
  <body>
    <p>This is an <b>HTML</b> email sent from Python using the Gmail SMTP server.</p>
  </body>
</html>
"""
html_message = MIMEText(body, 'html')
html_message['Subject'] = subject
html_message['From'] = sender_email
html_message['To'] = recipient_email
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login(sender_email, sender_password)
server.sendmail(sender_email, recipient_email, html_message.as_string())
server.quit()