from flask import Flask, request, render_template
import pandas as pd
import smtplib
from email.message import EmailMessage
app = Flask(__name__)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        df = pd.read_csv(request.files.get('file'))
        usr_email=request.form['email']
        usr_pwd=request.form['password']
        

        df.columns=df.columns.str.lower()

        names_list=df['name'].values.tolist()
        mail_list=df['mail'].values.tolist()
        subject_list=df['subject'].values.tolist()
        m_essage_list=df['message'].values.tolist()
        
        for(a,b,c,d) in zip(names_list,mail_list,subject_list,m_essage_list):
          msg= EmailMessage()
          msg['From']=usr_email
          msg['To']=b
          msg['Subject']=c
          msg.set_content(d)


        with smtplib.SMTP('smtp.gmail.com',587) as smtp:
         smtp.ehlo()
         smtp.starttls()
         smtp.ehlo()

         smtp.login(usr_email,usr_pwd)
         smtp.send_message(msg)

        return render_template('main.html',result='Mails successfully sent!')
    
    
    return render_template('main.html')

if __name__ == '__main__':
  app.run(debug=True)
