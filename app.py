from flask import Flask,render_template,request,redirect
import smtplib

app=Flask(__name__)

#route() decorators
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/About.html')
def about():
    return render_template('About.html')

@app.route('/Menu.html')
def menu():
    return render_template('Menu.html')

@app.route('/Contact.html')
def contact():
    return render_template('Contact.html')

@app.route('/Mail.html')
def mail():
    return render_template('Mail.html')

@app.route('/send_email/',methods=['POST'])
def send():
    #Getting form data from the web form
    name=request.form['name']
    email=request.form['email']
    subject=request.form['subject']
    message=request.form['message']

    #Open and read a text file with gmail username and assigning the value to a gmail_sender variable
    with open('username.txt','r') as f:
        gmail_sender = f.read()
    f.close()
    #Open and read a text file with gmail password and assigning the value to a gmail_passwd variable
    with open('password.txt','r') as f:
        gmail_passwd = f.read()
    f.close()

    #sending email using smtplib
    TO = gmail_sender
    SUBJECT = subject
    TEXT = 'This is message from %s\n\n' % email +message+'\n\n'+name

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_sender, gmail_passwd)

    BODY = '\r\n'.join(['To: %s' % TO,
                        'From: %s' % gmail_sender,
                        'Subject: %s' % SUBJECT,
                        '', TEXT])
    try:
        server.sendmail(gmail_sender, [TO], BODY)
    except:
        print('error sending mail')
    
    server.quit()
    #Notification of email sending
    return redirect('/Mail.html')

if __name__=='__main__':
    app.run(debug=True)
