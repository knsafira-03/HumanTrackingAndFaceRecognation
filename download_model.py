from ultralytics import YOLO
import shutil
import os

print("Downloading YOLOv8n...")

# otomatis download ke folder kerja jika belum ada
model = YOLO("yolov8n.pt")

# pindahkan ke folder models/yolo
os.makedirs("models/yolo", exist_ok=True)

shutil.move("yolov8n.pt", "models/yolo/yolov8n.pt")

print("Model berhasil disimpan di models/yolo/")