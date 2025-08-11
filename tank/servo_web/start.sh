#!/bin/bash

# =================================================================
# 脚本名称: start.sh
# 脚本功能:
#   1. 启动摄像头内核模块。
#   2. 自动生成 web/ip.js。
#   3. 启动 Python HTTP 服务器 (8081) 和 MJPG Streamer (8080)。
#   4. 捕获 Ctrl+C，退出时停止所有服务并卸载摄像头模块。
# =================================================================

# 工作目录
BASE_DIR="/home/han/tank/servo_web"
WEB_DIR="/home/han/tank/servo_web"
MJPG_DIR="/home/han/tank/mjpg-streamer/mjpg-streamer-experimental"

# 确保脚本退出时能杀死所有子进程
trap 'trap - SIGTERM && kill 0' SIGINT SIGTERM EXIT

cleanup() {
    echo -e "\n\n捕获到退出信号，正在执行清理程序..."

    if [ ! -z "$PYTHON_PID" ] && kill -0 $PYTHON_PID 2>/dev/null; then
        echo "--> 停止 Python HTTP 服务器 (PID: $PYTHON_PID)..."
        kill $PYTHON_PID
    fi

    if [ ! -z "$MJPG_PID" ] && kill -0 $MJPG_PID 2>/dev/null; then
        echo "--> 停止 MJPG Streamer (PID: $MJPG_PID)..."
        kill $MJPG_PID
    fi

    sleep 1

    echo "--> 卸载摄像头内核模块..."
    sudo modprobe -r bcm2835-v4l2
    echo "清理完毕。"
    exit 0
}

trap cleanup SIGINT SIGTERM

# 1. 启动摄像头模块
echo "正在启动摄像头内核模块..."
sudo modprobe bcm2835-v4l2
if [ $? -ne 0 ]; then
    echo "错误：启动摄像头模块失败！"
    exit 1
fi
echo "摄像头模块已加载。"
echo "=========================================="

# 2. 获取当前 IP 并生成 ip.js
CURRENT_IP=$(hostname -I | awk '{print $1}')
echo "当前树莓派 IP: $CURRENT_IP"
echo "const RASPBERRY_IP='${CURRENT_IP}';" > "$WEB_DIR/ip.js"
echo "已生成 $WEB_DIR/ip.js"
echo "------------------------------------------"

# 3. 启动 Python HTTP 服务器
echo "正在启动 Python HTTP 服务器 (端口 8081)..."
(cd "$WEB_DIR" && python3 -m http.server 8081) &
PYTHON_PID=$!
echo "Python HTTP 服务器 PID: $PYTHON_PID"
echo "------------------------------------------"

# 4. 启动 MJPG Streamer
echo "正在启动 MJPG Streamer (端口 8080)..."
(cd "$MJPG_DIR" && ./mjpg_streamer \
  -i "./input_uvc.so -d /dev/video0 -r 1280x720 -f 30" \
  -o "./output_http.so -w ./www") &
MJPG_PID=$!
echo "MJPG Streamer PID: $MJPG_PID"
echo "=========================================="

# 5. 等待用户中断
echo "服务已启动："
echo "📹 视频流:     http://${CURRENT_IP}:8080/?action=stream"
echo "🌐 控制界面:   http://${CURRENT_IP}:8081"
echo "按下 Ctrl+C 停止所有服务并退出。"
wait
