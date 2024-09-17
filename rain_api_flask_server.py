from flask import Flask, jsonify
import json
import subprocess
import os

app = Flask(__name__)

# Bash 스크립트를 실행하고 JSON 파일을 최신화하는 함수
def update_json_file(scripts):
    try:
        # Bash 스크립트를 실행
        subprocess.run(["bash", scripts], check=True)

        # JSON 파일이 생성되었는지 확인
        if os.path.exists('/home/ubuntu/rain_api/json/filtered_coordinates.json'):
            with open('/home/ubuntu/rain_api/json/filtered_coordinates.json', 'r') as json_file:
                data = json.load(json_file)
            return data
        else:
            return {"error": "JSON 파일을 찾을 수 없습니다."}
    except subprocess.CalledProcessError as e:
        return {"error": f"스크립트 실행 중 오류 발생: {str(e)}"}

# weather-api 엔드포인트
@app.route('/rain', methods=['GET'])
def get_weather_data():
    # 스크립트를 실행하고 JSON 파일을 업데이트
    scripts = "/home/ubuntu/rain_api/codes/rain_data_update.sh"
    print("Request rain api")
    data = update_json_file(scripts)
    return build_actual_response(jsonify(data))

# weather-api 엔드포인트
@app.route('/rain/test', methods=['GET'])
def get_weather_data_test():
    # 스크립트를 실행하고 JSON 파일을 업데이트
    scripts = "/home/ubuntu/rain_api/codes/rain_data_update_test.sh"
    print("Request rain api test")
    data = update_json_file(scripts)
    return build_actual_response(jsonify(data))

@app.route('/health-check', methods=['GET'])
def health_check():
    return build_actual_response(jsonify(True))

def build_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == '__main__':
    # 서버 실행
    app.run(host='0.0.0.0', port=51822)
