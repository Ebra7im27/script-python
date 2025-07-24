import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# إعدادات البريد
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "" # استبدل هذا ببريدك الإلكتروني
SENDER_PASSWORD = "" # استبدل هذا بكلمة مرور بريدك الإلكتروني أو رمز التطبيق

CV_PATH = r"D:\portfolio\MY CV.pdf" # استبدل هذا بالمسار الصحيح لملف السيرة الذاتية

# تحميل الإيميلات من ملف
def read_emails_from_file(filename):
    with open(filename, "r") as file:
        return [line.strip() for line in file if line.strip()]

recipient_emails = read_emails_from_file(r"D:\portfolio\emails_batch_1.txt") # استبدل هذا بالمسار الصحيح لملف الإيميلات

# محتوى الرسالة
subject = "Application for Front-End Developer Role"

# قالب الرسالة
# يمكنك تخصيص هذا القالب حسب الحاجة
body_template = """
<div style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px; border-radius: 12px; border: 1px solid #ddd; max-width: 700px; margin: auto;">
    <h2 style="color: #333;">Dear {name},</h2>
    <p style="font-size: 16px; color: #555;">
        I hope this message finds you well. I am writing to express my interest in a full-time front-end development position within your organization.
    </p>
    <p style="font-size: 16px; color: #555;">
        I am currently a student at El-Sherif Higher Institute for Computer Science in Kafr El-Sheikh, Egypt. I have practical experience developing responsive, modern web interfaces using <strong>React.js</strong>, <strong>Next.js</strong>, <strong>HTML</strong>, <strong>CSS</strong>, and <strong>JavaScript</strong>. I also use modern tools like <strong>Tailwind CSS</strong> and <strong>Bootstrap</strong>.
    </p>
    <p style="font-size: 16px; color: #555;">
        I recently completed a professional front-end development track where I built several UI projects and gained experience working with real-world APIs and application data.
    </p>
    <p style="font-size: 16px; color: #555;">
        I'm eager to apply what I’ve learned in a real work environment, contribute to meaningful projects, and continue growing as a developer. My resume is attached for your consideration.
    </p>
    <hr style="margin: 20px 0; border: none; border-top: 1px solid #ccc;">
    <p style="font-size: 14px; color: #666;">
        📧 <strong>Email:</strong> ebrahimmohamed2325@gmail.com<br>
        📞 <strong>Phone:</strong> +201068054735<br>
        🔗 <strong>LinkedIn:</strong> <a href="https://www.linkedin.com/in/ebrahim-elngar-6860a2333" style="color: #4CAF50; text-decoration: none;">linkedin.com/in/ebrahim-elngar-6860a2333</a><br>
        💻 <strong>GitHub:</strong> <a href="https://github.com/Ebra7im27" style="color: #4CAF50; text-decoration: none;">github.com/Ebra7im27</a>
    </p>
    <p style="margin-top: 20px; color: #444;">
        Best regards,<br>
        <strong>Ebrahim Elngar</strong>
    </p>
</div>
"""

def send_email(recipient_list):
    sent_count = 0
    failed_count = 0

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        for recipient in recipient_list:
            try:
                name = recipient.split("@")[0].capitalize()

                msg = MIMEMultipart()
                msg['From'] = SENDER_EMAIL
                msg['To'] = recipient
                msg['Subject'] = subject

                body = body_template.format(name=name)
                msg.attach(MIMEText(body, 'html'))

                if os.path.exists(CV_PATH):
                    filename = os.path.basename(CV_PATH)
                    with open(CV_PATH, "rb") as attachment:
                        part = MIMEBase("application", "octet-stream")
                        part.set_payload(attachment.read())
                        encoders.encode_base64(part)
                        part.add_header("Content-Disposition", f"attachment; filename=\"{filename}\"")
                        msg.attach(part)
                else:
                    print(f"❌ CV not found: {CV_PATH}")
                    continue

                server.sendmail(SENDER_EMAIL, recipient, msg.as_string())
                sent_count += 1
                print(f"✅ Email sent to {recipient}")

            except Exception as e:
                failed_count += 1
                print(f"❌ Failed to send email to {recipient}")
                print(f"   📌 Reason: {e}\n")

        server.quit()
        print(f"\n📬 Summary\n✅ Sent: {sent_count}\n❌ Failed: {failed_count}")

    except Exception as global_error:
        print(f"❌ Error connecting to server: {global_error}")

# إرسال الإيميلات
send_email(recipient_emails)