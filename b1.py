import pandas as pd
#b.Lưu dữ liệu từ các sheet vào các DataFrame df_Ha_Noi, df_Da_Nang, df_TP_HCM và hiển thị nội dung các DataFrame 
df_Ha_Noi = pd.read_excel('weather_data.xlsx', sheet_name='HaNoi')
df_Da_Nang = pd.read_excel('weather_data.xlsx', sheet_name='DaNang')
df_TP_HCM = pd.read_excel('weather_data.xlsx', sheet_name='TP_HCM')

print(df_Ha_Noi)
print(df_Da_Nang)
print(df_TP_HCM)
print(df_Ha_Noi.columns)

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
df_tong_hop = [df_Ha_Noi[['Thanh_pho', 'Ngay', 'Nhiet_do_cao_nhat (oC)', 'Nhiet_do_thap_nhat(oC)', 'Nhiet_do_trung_binh (oC)', 'Chi_so_cam_giac_nong', 'Do_am(%)', 'Toc_do_gio (km/h)', 'Luong_mua(mm)', 'Chi_so_UV', 'Tinh_trang_thoi_tiet']],
               df_TP_HCM[['Thanh_pho', 'Ngay', 'Nhiet_do_cao_nhat (oC)', 'Nhiet_do_thap_nhat(oC)', 'Nhiet_do_trung_binh (oC)', 'Chi_so_cam_giac_nong', 'Do_am(%)', 'Toc_do_gio (km/h)', 'Luong_mua(mm)', 'Chi_so_UV', 'Tinh_trang_thoi_tiet']],
               df_Da_Nang[['Thanh_pho', 'Ngay', 'Nhiet_do_cao_nhat (oC)', 'Nhiet_do_thap_nhat(oC)', 'Nhiet_do_trung_binh (oC)', 'Chi_so_cam_giac_nong', 'Do_am(%)', 'Toc_do_gio (km/h)', 'Luong_mua(mm)', 'Chi_so_UV', 'Tinh_trang_thoi_tiet']]]
# Hiển thị DataFrame tổng hợp
print(df_tong_hop) 


#Vẽ biểu đồ scatter thể hiện mối quan hệ giữa nhiệt độ trung bình và Tình trạng thời tiết.
import matplotlib.pyplot as plt

# Giả sử df_tong_hop đã có cột 'Nhiet_do_trung_binh (oC)' và 'Tinh_trang_thoi_tiet'

# Tạo cột tương ứng cho Tình trạng thời tiết, chuyển 'Khô ráo' thành 0 và 'Mưa' thành 1 để vẽ
df_tong_hop['Tinh_trang_thoi_tiet_num'] = df_tong_hop['Tinh_trang_thoi_tiet'].apply(lambda x: 1 if x == 'Mưa' else 0)

# Vẽ biểu đồ scatter
plt.figure(figsize=(10, 6))
plt.scatter(df_tong_hop['Nhiet_do_trung_binh (oC)'], df_tong_hop['Tinh_trang_thoi_tiet_num'], alpha=0.7)

# Đặt tiêu đề và nhãn cho các trục
plt.title('Mối quan hệ giữa nhiệt độ trung bình và tình trạng thời tiết')
plt.xlabel('Nhiệt độ trung bình (°C)')
plt.ylabel('Tình trạng thời tiết (0: Khô ráo, 1: Mưa)')

# Hiển thị biểu đồ
plt.show()