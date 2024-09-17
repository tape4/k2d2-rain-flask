import pandas as pd
import numpy as np
from scipy.interpolate import griddata

# CSV 파일에서 잘라낸 데이터를 불러옵니다.
clipped_df = pd.read_csv('/home/ubuntu/rain_api/csv_files/clipped_output_data.csv', header=None)

# 잘라낸 데이터의 모양을 기준으로 x, y 좌표를 생성합니다.
x = np.arange(0, clipped_df.shape[1])
y = np.arange(0, clipped_df.shape[0])
xv, yv = np.meshgrid(x, y)

# 잘라낸 데이터의 값을 가져옵니다.
values = clipped_df.values

# 100미터 간격으로 보간할 새로운 x, y 좌표를 생성합니다 (간격을 0.5로 설정).
x_new = np.arange(0, clipped_df.shape[1] - 1, 0.25)
y_new = np.arange(0, clipped_df.shape[0] - 1, 0.25)
xv_new, yv_new = np.meshgrid(x_new, y_new)

# 큐빅 보간을 수행합니다.
interpolated_data_250m = griddata((xv.ravel(), yv.ravel()), values.ravel(), (xv_new, yv_new), method='cubic')

# 보간된 데이터에서 음수 값을 0으로 대체합니다.
interpolated_data_250m[interpolated_data_250m < 0] = 0

# 보간된 데이터를 DataFrame으로 변환합니다.
interpolated_df_250m = pd.DataFrame(interpolated_data_250m)

# 소수점 4자리로 반올림합니다.
interpolated_df_250m = interpolated_df_250m.round(4)

# 보간된 데이터를 CSV 파일로 저장합니다.
interpolated_csv_filename_250m = '/home/ubuntu/rain_api/csv_files/interpolated_output_data_250m.csv'
interpolated_df_250m.to_csv(interpolated_csv_filename_250m, index=False, header=False, float_format='%.3f')

print(f"250미터 간격으로 보간된 데이터가 '{interpolated_csv_filename_250m}'에 저장되었습니다.")

# 보간된 데이터에서 중심값 12345.000의 위치(행과 열)를 찾습니다.
# row, col = np.where(interpolated_data_250m == 12345.000)
# ## 중심값 12345.000의 행: [290], 열: [200]


row_index = 116
col_index = 80

# value_at_coordinates = interpolated_df_250m.iloc[row_index, col_index]

# print(f"({row_index}, {col_index}) 위치의 값: {value_at_coordinates}")

# 중심값의 행과 열을 출력합니다.
# print(f"중심값 12345.000의 행: {row}, 열: {col}")
