import pandas as pd
import numpy as np
import requests
import json
import base64
import zlib
from datetime import datetime, timedelta
from scipy.interpolate import griddata


print("기상청 API 시작")
# 공공데이터포털에서 받은 인증키를 입력하세요
service_key = "인증키"

# API 요청 URL
url = "http://apis.data.go.kr/1360000/RadarObsInfoService/getLocalRadarRn"

# 현재 시간의 30분 전을 구합니다.
current_time = datetime.now()
time_30_minutes_ago = current_time - timedelta(minutes=30)
formatted_time = time_30_minutes_ago.strftime('%Y%m%d%H%M')
print(f"Requesting data for time: {formatted_time}")

# 요청에 필요한 파라미터 설정
params = {
    "ServiceKey": service_key,
    "pageNo": 1,
    "numOfRows": 10,
    "dataType": "JSON",
    "dateTime": formatted_time,
    "qcType": "OQC",
    "siteCd": "KWK",
    "dataTypeCd": "RN"
}

# GET 요청 보내기 (쿼리 파라미터 포함)
response = requests.get(url, params=params)

# 응답 데이터 출력
data = response.json()


# 압축 데이터를 디코딩 및 압축 해제
base64_encoded_data = data['response']['body']['items']['item'][0]['cappiCompressData']
siteLat = data['response']['body']['items']['item'][0]['siteLat']
siteLon = data['response']['body']['items']['item'][0]['siteLon']
compressed_data = base64.b64decode(base64_encoded_data)
decompressed_data = zlib.decompress(compressed_data, zlib.MAX_WBITS)

# CSV 파일로 저장
csv_filename = '/home/ubuntu/rain_api/csv_files/output_data.csv'
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    file.write(decompressed_data.decode('utf-8'))

print("기상청 API 완료")

print("서울 크기로 짜르기 시작")
# CSV 파일 읽기
df = pd.read_csv(csv_filename, header=None)

# -9999 값을 0으로 변경
df.replace(-9999, 0, inplace=True)

# 중심값에 '****' 추가
# center_index = (240, 240)
# df.iloc[center_index] = 10

# 업데이트된 데이터를 다시 CSV 파일에 저장
# df.to_csv(csv_filename, index=False, header=False)
# print(f"중심값이 수정된 CSV 파일은 '{csv_filename}'에 저장되었습니다.")

# 잘라야 하는 인덱스 정의
west_index = 261
east_index = 220
north_index = 241
south_index = 211

# 데이터를 잘라내기 (DataFrame의 행, 열은 북, 남, 서, 동 순서)
clipped_df = df.iloc[south_index:north_index+1, east_index:west_index+1]

clipped_df_csv_filename = '/home/ubuntu/rain_api/csv_files/clipped_output_data.csv'
clipped_df.to_csv(clipped_df_csv_filename, index=False, header=False, float_format='%.4f')
print(f"잘라낸 데이터가 '{clipped_df_csv_filename}'에 저장되었습니다.")
print("서울 크기로 짜르기 완료")

# print("보간 시작")
# # 보간을 위해 x, y 좌표 생성
# x = np.arange(0, clipped_df.shape[1])
# y = np.arange(0, clipped_df.shape[0])
# xv, yv = np.meshgrid(x, y)

# # 데이터 값
# values = clipped_df.values

# # 보간할 새로운 x, y 좌표 생성 (0.5 간격으로)
# x_new = np.arange(0, clipped_df.shape[1] - 1, 0.5)
# y_new = np.arange(0, clipped_df.shape[0] - 1, 0.5)
# xv_new, yv_new = np.meshgrid(x_new, y_new)

# # 큐빅 스플라인 보간 수행
# interpolated_data = griddata((xv.ravel(), yv.ravel()), values.ravel(), (xv_new, yv_new), method='cubic')

# # 보간된 데이터에서 음수 값을 0으로 대체
# interpolated_data[interpolated_data < 0] = 0

# # 보간된 데이터를 DataFrame으로 변환
# interpolated_df = pd.DataFrame(interpolated_data)

# # 소수점 4자리로 반올림
# interpolated_df = interpolated_df.round(4)

# # 보간된 데이터를 새로운 CSV 파일로 저장 (소수점 4자리)
# interpolated_csv_filename = '/home/ubuntu/rain_api/csv_files/interpolated_output_data_cubic.csv'
# interpolated_df.to_csv(interpolated_csv_filename, index=False, header=False, float_format='%.3f')

# # 자르기 후의 중심 좌표
# clipped_center = (240 - south_index, 240 - east_index)

# # 보간 후의 중심 좌표 (보간 간격이 0.5로 두 배가 됨)
# interpolated_center = (clipped_center[0] * 2, clipped_center[1] * 2)
# print("보간 종료")

# print(f"자른 후 중심 좌표: {clipped_center}")
# print(f"보간 후 중심 좌표: {interpolated_center}")
# print(siteLat, siteLon)
# print(f"큐빅 스플라인 보간을 사용하여 보간된 데이터는 '{interpolated_csv_filename}'에 소수점 4자리로 저장되었습니다.")
