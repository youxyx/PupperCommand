#!/usr/bin/env sh
# PupperCommand 全新安装脚本 - 适配 BlueZ原生PS3蓝牙手柄
# 无旧驱动，纯全新配置

# 定位脚本所在目录
FOLDER=$(dirname $(realpath "$0"))
cd "$FOLDER"

echo "============================================="
echo "  PupperCommand PS3蓝牙手柄 全新安装"
echo "============================================="

# 1. 更新软件源
echo "[1/3] 更新软件源..."
sudo apt update

# 2. 安装手柄依赖（pygame：读取原生PS3手柄）
echo "[2/3] 安装依赖库..."
sudo apt install -y python3-pip python3-pygame
sudo pip3 install pygame

# 3. 配置硬件权限（手柄+蓝牙，必须！）
echo "[3/3] 配置权限并注册服务..."
sudo usermod -aG input pi
sudo usermod -aG bluetooth pi

# 注册系统服务 + 开机自启
sudo ln -sf "$FOLDER/joystick.service" /lib/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable joystick

echo "============================================="
echo "  安装完成！"
echo "  请重启树莓派生效权限：sudo reboot"
echo "  重启后按手柄PS键，自动连接使用"
echo "============================================="
