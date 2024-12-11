import cv2
import numpy as np
import os

# 设置视频的宽度、高度和帧率
width = 640
height = 480
fps = 30

# 计算 7 分钟的帧数（7 分钟 * 60 秒/分钟 * 30 帧/秒）
frames = 7 * 60 * fps

# 注意这里修改了文件的保存路径
output_path = r'D:\py-workspace\autotradestocksys\test\black_video.mp4'

# 检查文件是否存在
if os.path.exists(output_path):
    print(f"文件 {output_path} 已存在，将覆盖原文件。")

# 创建一个 VideoWriter 对象，指定输出文件名、编解码器、帧率和视频尺寸
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

# 创建一个全黑的帧
black_frame = np.zeros((height, width, 3), dtype=np.uint8)

# 写入指定时长的黑色帧
for i in range(frames):
    out.write(black_frame)

# 释放资源
out.release()

# 输出生成成功的通知
print("生成成功")