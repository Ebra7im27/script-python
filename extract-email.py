import pandas as pd
import re
import math

# تحديد المسار الكامل لملف Excel
file_path = r"D:\portfolio\emails.xlsx"

# قراءة كل الشيتات من ملف Excel
df = pd.read_excel(file_path, sheet_name=None)

# دمج كل النصوص من جميع الشيتات
all_text = ""
for sheet_name, sheet_data in df.items():
    all_text += " ".join(sheet_data.astype(str).fillna("").values.flatten())

# استخراج الإيميلات باستخدام regex
emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', all_text)

# إزالة التكرارات وترتيب الإيميلات
unique_emails = sorted(set(emails))

# تقسيم الإيميلات إلى دفعات (كل دفعة فيها 500 إيميل)
batch_size = 500
total_batches = math.ceil(len(unique_emails) / batch_size)

for i in range(total_batches):
    start_index = i * batch_size
    end_index = start_index + batch_size
    batch_emails = unique_emails[start_index:end_index]

    file_name = f"emails_batch_{i+1}.txt"
    with open(file_name, "w", encoding="utf-8") as f:
        for email in batch_emails:
            f.write(email + "\n")

print(f"✅ Successfully extracted {len(unique_emails)} emails into {total_batches} files.")