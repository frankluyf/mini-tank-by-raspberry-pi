#!/bin/bash

DEVICE=${1:-/dev/video0}

# 检查设备是否存在
if [ ! -e "$DEVICE" ]; then
    echo "设备 $DEVICE 不存在"
    exit 1
fi

echo "📷 当前使用设备: $DEVICE"
echo "----------------------------"

# 显示支持的控制项
echo "🔍 可调节的摄像头参数如下："
v4l2-ctl -d "$DEVICE" --list-ctrls

# 可选：展示当前参数值
echo ""
echo "📋 当前参数值："
v4l2-ctl -d "$DEVICE" --all
