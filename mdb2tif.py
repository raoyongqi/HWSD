import pymdb
from PIL import Image
from io import BytesIO

# 打开 MDB 文件
mdb_file = 'your_database.mdb'
mdb = pymdb.open(mdb_file)

# 选择要读取的表和字段
table_name = 'your_table'
image_field = 'your_image_field'

# 查询数据
query = f"SELECT {image_field} FROM {table_name}"
records = mdb.execute(query)

for i, record in enumerate(records):
    # 提取图像数据
    image_data = record[0]  # 假设图像数据在第一个字段
    
    # 将二进制数据转换为图像
    image = Image.open(BytesIO(image_data))
    
    # 保存为 TIFF 文件
    image_file_name = f'image_{i}.tif'
    image.save(image_file_name)

    print(f'Saved image to {image_file_name}')
