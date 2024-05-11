import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def lambda_handler(event, context):
    sqs_message = json.loads(event['Records'][0]['body'])

    email_destinatario = sqs_message['emailDestinatario']
    assunto = sqs_message['assunto']
    corpo_email = sqs_message['corpoEmail']

    # Foi usado o BREVO para usar STMP no envio de emails transacionais
    smtp_server = 'smtp-relay.brevo.com'
    smtp_port = 587
    smtp_username = '749fbb001@smtp-brevo.com'
    smtp_password = '364578vjnNUsqRFQ'

    msg = MIMEMultipart()
    msg['From'] = 'techchallenge.fase4@gmail.com'
    msg['To'] = email_destinatario
    msg['Subject'] = assunto
    msg.attach(MIMEText(corpo_email, 'html'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        print("E-mail enviado com sucesso. Dados enviados: " + json.dumps(sqs_message))
    except Exception as e:
        print("Erro ao enviar e-mail:", str(e))