import geopandas as gpd
from shapely.geometry import Point
import pandas as pd
import math
import os
import json
import psycopg2

# PostgreSQL 연결 설정
db_config = {
    'dbname': 'gisdb',
    'user': 'k2d2',
    'password': 'k2d2password',
    'host': '61.252.59.19',
    'port': '5432'
}

# 중심 인덱스와 중심 좌표 설정
center_index = (116, 80)
central_lat = 37.444168
central_lon = 126.963333

# 각 셀의 좌표를 계산하는 함수 (500m 간격)
def index_to_coordinates(row_idx, col_idx, central_lat, central_lon, lat_step_m=250, lon_step_m=250):
    # 위도 변화: 1도당 약 111.32km
    lat_change_per_meter = 1 / 111320  # 위도 1미터당 변화량
    lat = central_lat + (center_index[0] - row_idx) * lat_step_m * lat_change_per_meter  # 북쪽으로 갈수록 위도 증가

    # 경도 변화: 위도에 따라 경도당 거리가 달라짐
    lon_change_per_meter = 1 / (111320 * math.cos(math.radians(central_lat)))  # 경도 1미터당 변화량
    lon = central_lon + (col_idx - center_index[1]) * lon_step_m * lon_change_per_meter  # 동쪽으로 갈수록 경도 증가

    return lat, lon

# PostGIS와 연결
conn = psycopg2.connect(**db_config)
cursor = conn.cursor()

# 좌표가 다각형 내에 포함되는지 확인하는 함수
def is_point_in_polygon(lon, lat):
    query = f"""
    SELECT CASE 
        WHEN EXISTS (
            SELECT 1
            FROM totalgis AS polygon
            WHERE ST_Contains(polygon.geometry, ST_SetSRID(ST_Point({lon}, {lat}), 4326))
        ) THEN true
        ELSE false
    END AS is_point_in_any_polygon;
    """
    cursor.execute(query)
    result = cursor.fetchone()[0]
    return result

# CSV 파일 읽기
df = pd.read_csv('/home/ubuntu/rain_api/csv_files/test_data_all_points_250m.csv', header=None)

# 포인트 목록을 저장할 리스트
points = []
coordinates = []
count = 0
# 값이 95 이상인 셀의 좌표와 값을 찾고, 다각형에 포함되는지 확인
for row_idx in range(df.shape[0]):
    for col_idx in range(df.shape[1]):
        value = df.iat[row_idx, col_idx]
        lat, lon = index_to_coordinates(row_idx, col_idx, central_lat, central_lon)
        if is_point_in_polygon(lon, lat):  # 좌표가 다각형에 포함되는지 확인
            # 포인트 생성
            count+=1
            coordinates.append({"row": row_idx, "col": col_idx})

print(count)
result_json = json.dumps(coordinates, indent=4)

# JSON 파일로 저장
with open('/home/ubuntu/rain_api/json/gis_points_coordinates.json', 'w') as json_file:
    json_file.write(result_json)

print("gis_points_coordinates JSON with values saved to 'gis_points_coordinates.json'")

# PostGIS 연결 닫기
cursor.close()
conn.close()