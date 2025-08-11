#!/usr/bin/env python3
import atexit
import json
import asyncio
import contextlib
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from pathlib import Path
import time
import uvicorn
import pyaudio
import os  # <-- ADDED
from datetime import datetime  # <-- ADDED
import urllib.request  # <-- ADDED

from motors_control import (
    forward,
    backward,
    strafe_left,
    strafe_right,
    rotate_left,
    rotate_right,
    stop,
    fire
)

# ====== PWM参数与舵机角度限制 ======
PWMCHIP = 2
PWM_YAW_IDX = 2   # 对应 GPIO18
PWM_PITCH_IDX = 3 # 对应 GPIO19
PERIOD_NS, PULSE_MIN, PULSE_MAX = 20_000_000, 1_000_000, 2_000_000
YAW_MIN, YAW_MAX, PITCH_MIN, PITCH_MAX = 20, 121, 50, 150
CONTROL_HZ, ALPHA, DEADBAND_DEG, MAX_STEP_DEG = 50, 0.25, 0.4, 3.0
BASE = Path(f"/sys/class/pwm/pwmchip{PWMCHIP}")
yaw_pwm = pitch_pwm = None
current_yaw = target_yaw = 90.0
current_pitch = target_pitch = 90.0
hold_flag = False
loop_task: asyncio.Task | None = None

# --- 音频播放配置 ---
p = None
stream = None
FORMAT, CHANNELS, RATE, CHUNK = pyaudio.paFloat32, 1, 44100, 1024

# --- START: ADDED SCREENSHOT CODE ---

# --- Configuration for screenshots ---
IMAGE_SAVE_PATH = "/home/han/tank/image"
MJPG_STREAMER_SNAPSHOT_URL = "http://localhost:8080/?action=snapshot"

def take_screenshot():
    """Fetches a snapshot from the local MJPEG-streamer and saves it."""
    try:
        # Generate a unique filename using the current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")[:-3]
        filename = f"{timestamp}.jpg"
        filepath = os.path.join(IMAGE_SAVE_PATH, filename)

        # Fetch the image data
        with urllib.request.urlopen(MJPG_STREAMER_SNAPSHOT_URL, timeout=2) as response:
            image_data = response.read()
        
        # Save the image file
        with open(filepath, 'wb') as f:
            f.write(image_data)
        
        print(f"✅ Screenshot saved: {filepath}")
        return {"status": "screenshot_ok", "filename": filename}
    except Exception as e:
        print(f"❌ Error taking screenshot: {e}")
        return {"status": "screenshot_error", "message": str(e)}

# --- END: ADDED SCREENSHOT CODE ---


# ========== PWM 控制相关函数 (无改动) ==========
def sysfs_write(path: Path, value):
    with open(path, "w") as f: f.write(f"{value}\n")
def export_channel(idx: int) -> Path:
    pwm_path = BASE / f"pwm{idx}";
    if not pwm_path.exists(): sysfs_write(BASE / "export", idx); time.sleep(0.1)
    return pwm_path
def setup_pwm(pwm_path: Path):
    sysfs_write(pwm_path / "enable", 0); sysfs_write(pwm_path / "period", PERIOD_NS);
    sysfs_write(pwm_path / "duty_cycle", PULSE_MIN); sysfs_write(pwm_path / "enable", 1)
def angle_to_pulse_ns(angle: float) -> int:
    return int(PULSE_MIN + (max(0, min(180, angle)) / 180.0) * (PULSE_MAX - PULSE_MIN))
def set_angle(pwm_path: Path, angle: float):
    sysfs_write(pwm_path / "duty_cycle", angle_to_pulse_ns(angle))
def cleanup_pwm(*pwm_paths):
    for p in pwm_paths:
        if p:
            try: sysfs_write(p / "enable", 0)
            except Exception: pass
def cleanup_audio():
    global p, stream;
    if stream and stream.is_active(): stream.stop_stream(); stream.close()
    if p: p.terminate()

# ========== FastAPI 应用 ==========
app = FastAPI()
def clamp(v, lo, hi): return max(lo, min(hi, v))

@app.on_event("startup")
async def hw_init():
    global yaw_pwm, pitch_pwm, current_yaw, current_pitch, target_yaw, target_pitch, loop_task, p, stream
    yaw_pwm = export_channel(PWM_YAW_IDX); pitch_pwm = export_channel(PWM_PITCH_IDX)
    setup_pwm(yaw_pwm); setup_pwm(pitch_pwm)
    current_yaw = target_yaw = clamp(90, YAW_MIN, YAW_MAX)
    current_pitch = target_pitch = clamp(90, PITCH_MIN, PITCH_MAX)
    set_angle(yaw_pwm, current_yaw); set_angle(pitch_pwm, current_pitch)
    loop_task = asyncio.create_task(servo_loop())
    print("[startup] Hardware initialized & PWM loop started.")
    try:
        p = pyaudio.PyAudio(); stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)
        print("[startup] Audio stream opened successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to open audio stream: {e}"); p = stream = None
    
    # --- ADDED: Ensure the image save directory exists on startup ---
    os.makedirs(IMAGE_SAVE_PATH, exist_ok=True)
    print(f"[startup] Image save directory ensured at: {IMAGE_SAVE_PATH}")


@app.on_event("shutdown")
async def hw_close():
    global loop_task;
    if loop_task: loop_task.cancel()
    cleanup()
@atexit.register
def cleanup():
    cleanup_pwm(yaw_pwm, pitch_pwm)
    cleanup_audio()
    print("[cleanup] Resources cleaned up.")

@app.get("/health")
def health(): return JSONResponse({"ok": True})

async def servo_loop():
    global current_yaw, current_pitch, target_yaw, target_pitch, hold_flag
    dt = 1.0 / CONTROL_HZ
    while True:
        if not hold_flag:
            dyaw = clamp(target_yaw, YAW_MIN, YAW_MAX) - current_yaw
            dpitch = clamp(target_pitch, PITCH_MIN, PITCH_MAX) - current_pitch
            if abs(dyaw) > DEADBAND_DEG: current_yaw += clamp(dyaw * ALPHA, -MAX_STEP_DEG, MAX_STEP_DEG)
            if abs(dpitch) > DEADBAND_DEG: current_pitch += clamp(dpitch * ALPHA, -MAX_STEP_DEG, MAX_STEP_DEG)
        set_angle(yaw_pwm, current_yaw); set_angle(pitch_pwm, current_pitch)
        await asyncio.sleep(dt)

@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    global target_yaw, target_pitch, current_yaw, current_pitch, hold_flag, stream
    await websocket.accept()
    client = websocket.client; print(f"[ws] Client connected: {client.host}:{client.port}")
    try:
        while True:
            message = await websocket.receive()
            if 'text' in message:
                raw = message['text']
                try: data = json.loads(raw)
                except Exception: continue

                # --- ADDED: Handle screenshot command ---
                if data.get("action") == "screenshot":
                    result = take_screenshot()
                    await websocket.send_text(json.dumps(result))
                    continue  # Skip other processing for this message
                
                # --- Original control logic ---
                mode = data.get("mode")
                if mode in ["on", "off"]: hold_flag = False if mode == "on" else hold_flag
                key, state = data.get("key"), data.get("state")
                if key and state:
                    if state == "down":
                        if key == "w": forward()
                        elif key == "s": backward()
                        elif key == "a": rotate_left()
                        elif key == "d": rotate_right()
                        elif key == "q": strafe_left()
                        elif key == "e": strafe_right()
                        elif key == " ": fire()
                    else: stop()
                    continue
                yaw, pitch, hold = data.get("yaw"), data.get("pitch"), bool(data.get("hold", False))
                if yaw is not None and pitch is not None:
                    try:
                        target_yaw, target_pitch = float(yaw), float(pitch)
                        if hold:
                            current_yaw, current_pitch = target_yaw, target_pitch
                            hold_flag = True; set_angle(yaw_pwm, current_yaw); set_angle(pitch_pwm, current_pitch)
                        else: hold_flag = False
                    except ValueError: continue
                    await websocket.send_text(json.dumps({"ok": True, "yaw": round(current_yaw, 2), "pitch": round(current_pitch, 2)}))

            elif 'bytes' in message:
                if stream: stream.write(message['bytes'])
    except WebSocketDisconnect:
        print(f"[ws] Client disconnected: {client.host}:{client.port}")
    finally:
        stop()
        print(f"[ws] Connection closed. Motors stopped.")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, reload=False)