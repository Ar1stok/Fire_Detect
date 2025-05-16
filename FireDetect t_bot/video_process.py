from CombinedFD import CombinedFireDetector
import cv2
import os


class Processing:
    def __init__(self, video_path: str, frames_path: str, img_format='png'):
        """
        Initialize class for working with video and frames

        Args:
            video_path (str): Path to folder with video files
            frames_path (str): Path to folder for saving frames
            img_format (default: .png): choose your image format (.png or .jpg)
        """
        self.video_path = video_path
        self.frames_path = frames_path
        self.img_format = img_format

        self.detector = CombinedFireDetector(
            yolo_model_path="onnx/fire_yolov8.onnx",
            resnet_model_path="onnx/ResNet50.pth",
            debug_dir="debug_crops"
        )

        if not os.path.exists(frames_path):
            os.makedirs(frames_path)
    
    def duration(self, video_name: str):
        cap = cv2.VideoCapture(os.path.join(self.video_path, video_name))
        
        if not cap.isOpened():
            raise IOError(f"Cannot open video file {self.video_path}")

        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        # Получаем частоту кадров (fps)
        fps = cap.get(cv2.CAP_PROP_FPS)
        # Вычисляем длину видео в секундах
        duration = frame_count / fps if fps > 0 else 0

        return duration


    def detection(self, video_name: str):
        cap = cv2.VideoCapture(os.path.join(self.video_path, video_name))
        
        if not cap.isOpened():
            raise IOError(f"Cannot open video file {self.video_path}")
        
        video_folder_name = os.path.splitext(video_name)[0]
        id_frame_path = os.path.join(self.frames_path, video_folder_name) 
        os.makedirs(id_frame_path, exist_ok=True)

        fire_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break  # No more frames

            # Construct filename for the frame
            frame_filename = os.path.join(id_frame_path, f"frame_{fire_count:04d}.{self.img_format}")

            result = self.detector.detect_fire(frame)
            print(result)
            
            if not result.startswith("NO"):
                # Save frame as images
                cv2.imwrite(frame_filename, frame)
                fire_count += 1

        cap.release()
        return fire_count