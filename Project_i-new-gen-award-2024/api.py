# Ceate ENV 
# pip install flask


from flask import Flask

app = Flask(__name__)

# กำหนด route สำหรับหน้าแรก
@app.route('/')
def home():
    return "Welcome to "

# กำหนด route สำหรับหน้าเกี่ยวกับ
@app.route('/about')
def about():
    return "This is the About Page."

if __name__ == '__main__':
    # รันเซิร์ฟเวอร์บน IP 10.80.94.190 ที่พอร์ต 5000
    app.run(host='10.80.94.190', port=5000, debug=True)

# host='10.80.94.190' host ของเครื่อง
# copy past ไปอีกเครื่อง http://10.80.94.190:5000  
# connect wifi เดียวกัน