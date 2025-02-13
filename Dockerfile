# Use Python as the base image
FROM python:3.9-slim

# Set the environment variables
ENV PYTHONPATH=/app
ENV DISPLAY=:99

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    xvfb \
    libgl1-mesa-glx \
    libxkbcommon-x11-0 \
    libxcb-xinerama0

# Copy the application files
COPY src/ ./src/
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the necessary ports
EXPOSE 8080

# Command to run the application
CMD ["xvfb-run", "python", "./src/main.py"]
# 使用官方的 Python 3.9 轻量级镜像
FROM python:3.9-slim

# 更新系统包
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    xvfb \
    x11-utils \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 拷贝源代码
COPY src/ ./src/

# 安装所有依赖项
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 暴露应用程序使用到的端口
EXPOSE 8080

# 设置显示环境变量
ENV DISPLAY=:0

# 定义启动命令
CMD ["python", "-m", "src.main"]
