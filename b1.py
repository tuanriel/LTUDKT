import pandas as pd
#b.Lưu dữ liệu từ các sheet vào các DataFrame df_Ha_Noi, df_Da_Nang, df_TP_HCM và hiển thị nội dung các DataFrame 
df_Ha_Noi = pd.read_excel('weather_data.xlsx', sheet_name='HaNoi')
df_Da_Nang = pd.read_excel('weather_data.xlsx', sheet_name='DaNang')
df_TP_HCM = pd.read_excel('weather_data.xlsx', sheet_name='TP_HCM')

print(df_Ha_Noi)
print(df_Da_Nang)
print(df_TP_HCM)

#c. Tạo ra 1 DataFrame mới (df_tong_hop) tổng hợp đầy đủ thông tin gồm các cột:
df_Ha_Noi['Thanh_pho'] = 'HaNoi'
df_TP_HCM['Thanh_pho'] = 'HoChiMinh'
df_Da_Nang['Thanh_pho'] = 'DaNang'

# Tính toán các cột mới
for df in [df_Ha_Noi, df_TP_HCM, df_Da_Nang]:
    df['Nhiet_do_trung_binh (oC)'] = (df['Nhiet_do_cao_nhat (oC)'] + df['Nhiet_do_thap_nhat(oC)']) / 2
    df['Chi_so_cam_giac_nong'] = df['Nhiet_do_trung_binh (oC)'] + 0.1 * df['Do_am(%)']
    df['Tinh_trang_thoi_tiet'] = df['Luong_mua(mm)'].apply(lambda x: 'Mưa' if x > 0 else 'Khô ráo')

# Ghép các DataFrame lại thành df_tong_hop
df_tong_hop = pd.concat([df_Ha_Noi[['Thanh_pho', 'Ngay', 'Nhiet_do_cao_nhat (oC)', 'Nhiet_do_thap_nhat(oC)', 'Nhiet_do_trung_binh (oC)', 'Chi_so_cam_giac_nong', 'Do_am(%)', 'Toc_do_gio (km/h)', 'Luong_mua(mm)', 'Chi_so_UV', 'Tinh_trang_thoi_tiet']],
               df_TP_HCM[['Thanh_pho', 'Ngay', 'Nhiet_do_cao_nhat (oC)', 'Nhiet_do_thap_nhat(oC)', 'Nhiet_do_trung_binh (oC)', 'Chi_so_cam_giac_nong', 'Do_am(%)', 'Toc_do_gio (km/h)', 'Luong_mua(mm)', 'Chi_so_UV', 'Tinh_trang_thoi_tiet']],
               df_Da_Nang[['Thanh_pho', 'Ngay', 'Nhiet_do_cao_nhat (oC)', 'Nhiet_do_thap_nhat(oC)', 'Nhiet_do_trung_binh (oC)', 'Chi_so_cam_giac_nong', 'Do_am(%)', 'Toc_do_gio (km/h)', 'Luong_mua(mm)', 'Chi_so_UV', 'Tinh_trang_thoi_tiet']]], ignore_index=True)
# Hiển thị DataFrame tổng hợp
df_tong_hop['Ngay'] = pd.to_datetime(df_tong_hop['Ngay']).dt.strftime('%m/%d/%y')
print(df_tong_hop) 

print(type(df_tong_hop))
#Vẽ biểu đồ scatter thể hiện mối quan hệ giữa nhiệt độ trung bình và Tình trạng thời tiết.
import matplotlib.pyplot as plt

# Giả sử df_tong_hop đã có cột 'Nhiet_do_trung_binh (oC)' và 'Tinh_trang_thoi_tiet'

# Tạo cột tương ứng cho Tình trạng thời tiết, chuyển 'Khô ráo' thành 0 và 'Mưa' thành 1 để vẽ
df_tong_hop['Tinh_trang_thoi_tiet_num'] = df_tong_hop['Tinh_trang_thoi_tiet'].apply(lambda x: 1 if x == 'Mưa' else 0)

#e. Lọc dữ liệu:
# Lọc và tạo DataFrame mới df_loc_du_lieu cho các ngày có nhiệt độ cao > 35 độ
df_loc_du_lieu_high_temp = df_tong_hop[df_tong_hop['Nhiet_do_cao_nhat (oC)'] > 35]

# Lọc và tạo DataFrame mới df_loc_du_lieu cho các ngày có lượng mưa > 10mm
df_loc_du_lieu_high_rain = df_tong_hop[df_tong_hop['Luong_mua(mm)'] > 10]

print(df_loc_du_lieu_high_temp)
print(df_loc_du_lieu_high_rain)

# Vẽ biểu đồ scatter thể hiện mối quan hệ giữa nhiệt độ trung bình và Tình trạng thời tiết.
plt.figure(figsize=(10, 6))
plt.scatter(df_tong_hop['Nhiet_do_trung_binh (oC)'], df_tong_hop['Tinh_trang_thoi_tiet_num'], alpha=0.7)

# Đặt tiêu đề và nhãn cho các trục
plt.title('Mối quan hệ giữa nhiệt độ trung bình và tình trạng thời tiết')
plt.xlabel('Nhiệt độ trung bình (°C)')
plt.ylabel('Tình trạng thời tiết (0: Khô ráo, 1: Mưa)')

# Hiển thị biểu đồ
plt.show()

# Vẽ biểu đồ cột so sánh tổng lượng mưa giữa 3 thành phố.
total_rain_by_city = df_tong_hop.groupby('Thanh_pho')['Luong_mua(mm)'].sum()

# Vẽ biểu đồ cột so sánh tổng lượng mưa giữa 3 thành phố
plt.figure(figsize=(10, 6))
total_rain_by_city.plot(kind='bar', color=['blue', 'orange', 'green'])

# Đặt tiêu đề và nhãn cho các trục
plt.title('So sánh tổng lượng mưa giữa 3 thành phố')
plt.xlabel('Thành phố')
plt.ylabel('Tổng lượng mưa (mm)')

plt.show()


#g. Xuất dữ liệu: 
with pd.ExcelWriter('weather_analysis.xlsx', engine='openpyxl') as writer:
    df_tong_hop.to_excel(writer, sheet_name='DataFrame Tong Hop', index=False)
    df_TP_HCM.to_excel(writer, sheet_name='TP_HCM', index=False)
    df_loc_du_lieu_high_temp.to_excel(writer, sheet_name='Các ngày nóng cao', index=False)
    df_loc_du_lieu_high_rain.to_excel(writer, sheet_name='Các ngày mưa nhieu', index=False)
