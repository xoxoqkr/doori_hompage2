from flask import Flask, render_template_string, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 구글 시트 인증
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("your-service-account.json", scope)
client = gspread.authorize(creds)

# 구글시트 이름/ID로 열기
SHEET_NAME = "시트1"  # 시트 이름
SPREADSHEET_ID = "1u-4PL7HiBTU-k_3Bdxe4zBOUzjA4kHACQZXBSj9K8j4"  # URL 중간의 긴 ID
sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

app = Flask(__name__)

HTML = '''
<!doctype html>
<title>통지확인</title>
<h2>통지확인</h2>
<form method="POST">
  이름: <input name="name"><br>
  생년월일: <input name="birth"><br>
  전화번호: <input name="phone"><br>
  <button type="submit">검색</button>
</form>
{% if result %}
  <h3>검색 결과</h3>
  <b>{{result['이름']}} ({{result['생년월일']}})</b><br>
  <a href="{{result['통지서링크']}}" target="_blank">[통지서 바로가기]</a>
  {% if result['이미지링크'] %}
    <img src="{{result['이미지링크']}}" width=300>
  {% endif %}
{% elif result is not none %}
  <b>일치하는 정보가 없습니다.</b>
{% endif %}
'''

def search_notice(name, birth, phone):
    records = sheet.get_all_records()
    for row in records:
        if row['이름'] == name and str(row['생년월일']) == birth and str(row['전화번호']) == phone:
            return row
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        name = request.form['name'].strip()
        birth = request.form['birth'].strip()
        phone = request.form['phone'].strip()
        result = search_notice(name, birth, phone)
    return render_template_string(HTML, result=result)

if __name__ == '__main__':
    app.run(debug=True)
