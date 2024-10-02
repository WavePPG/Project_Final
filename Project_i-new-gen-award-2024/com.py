from flask import Flask, render_template, request
import json

app = Flask(__name__)

# ตัวแปรเพื่อเก็บค่าทิศทาง
direction_data = {'direction': None}

# กำหนด route สำหรับหน้าแรก
@app.route('/')
def home():
    return render_template('index.html', direction=direction_data['direction'])

# กำหนด route สำหรับการส่งข้อมูล
@app.route('/send', methods=['POST'])
def send():
    direction = request.form.get('direction')
    direction_data['direction'] = direction
    return 'Direction set to ' + direction

# กำหนด route สำหรับดึงข้อมูล
@app.route('/get_direction', methods=['GET'])
def get_direction():
    return json.dumps(direction_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
