from fire_detector_YOLO import FireDetector_YOLO
from fire_detector_ResNet50 import FireDetector_ResNet50
from croper import crop_image_by_bbox
import cv2
import numpy as np
from typing import List, Tuple, Union, Optional
from PIL import Image
import os

class CombinedFireDetector:
    def __init__(self, yolo_model_path: str, resnet_model_path: str, debug_dir: Optional[str] = None):
        """
        Инициализация комбинированного детектора огня
        
        Args:
            yolo_model_path: путь к модели YOLO (.onnx)
            resnet_model_path: путь к модели ResNet (.pth)
            debug_dir: директория для сохранения debug изображений (None - отключено)
        """
        self.yolo_detector = FireDetector_YOLO(yolo_model_path)
        self.resnet_detector = FireDetector_ResNet50(resnet_model_path)
        self.debug_dir = debug_dir
        self.last_crops = []  # Сохраняем последние кропы для отладки
        
        if debug_dir is not None:
            os.makedirs(debug_dir, exist_ok=True)
    
    def detect_fire(self, image: Union[str, np.ndarray]) -> str:
        """
        Комбинированная детекция огня
        
        Args:
            image: путь к изображению или numpy array (BGR)
            
        Returns:
            "FIRE" если огонь обнаружен, иначе "NO_YOLO" или "NO_RESNET"
        """
        self.last_crops = []  # Очищаем предыдущие кропы
        
        # Загрузка изображения если передан путь
        if isinstance(image, str):
            img = cv2.imread(image)
            if img is None:
                raise FileNotFoundError(f"Не удалось загрузить изображение: {image}")
        else:
            img = image.copy()
        
        # Детекция YOLO
        fire_boxes = self.yolo_detector.detect_fire(img)
        
        # Если YOLO не нашла огонь
        if not fire_boxes:
            return "NO_YOLO"
        
        # Проверка каждого обнаруженного региона с помощью ResNet
        for i, (x, y, w, h) in enumerate(fire_boxes):
            # Обрезка изображения
            cropped_img = crop_image_by_bbox(img, (x, y, w, h))
            self.last_crops.append(cropped_img)

            # Сохранение для отладки
            if self.debug_dir is not None:
                crop_path = os.path.join(self.debug_dir, f"crop_{i}.jpg")
                cv2.imwrite(crop_path, cropped_img)
            
            # Конвертация в PIL Image (ожидаемый ResNet формат)
            pil_img = Image.fromarray(cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB))
            
            # Проверка ResNet
            class_name, confidence = self.resnet_detector.predict(pil_img)
            
            if class_name == "Fire" and confidence > 0.2:
                return "FIRE"
        
        return "NO_RESNET"

    def visualize_detections(self, image: np.ndarray) -> np.ndarray:
        """
        Визуализация обнаруженных регионов огня
        
        Args:
            image: входное изображение (BGR)
            
        Returns:
            изображение с отрисованными bounding boxes
        """
        img = image.copy()
        fire_boxes = self.yolo_detector.detect_fire(img)
        
        for i, (x, y, w, h) in enumerate(fire_boxes, 1):
            # Отрисовка прямоугольника
            cv2.rectangle(img, (int(x), int(y)), (int(w), int(h)), (0, 0, 255), 2)
            
            # Проверка ResNet для подписи
            cropped_img = crop_image_by_bbox(img, (x, y, w, h))
            pil_img = Image.fromarray(cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB))
            class_name, confidence = self.resnet_detector.predict(pil_img)
            
            label = f"{class_name} {i}: {confidence:.2f}"
            cv2.putText(img, label, (int(x), int(y)-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        
        return img
    
    def show_last_crops(self):
        """Отображает последние кропнутые изображения (для отладки)"""
        for i, crop in enumerate(self.last_crops):
            cv2.imshow(f"Crop {i}", crop)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    import os
    
    # Инициализация детектора с debug директорией
    detector = CombinedFireDetector(
        yolo_model_path="onnx/fire_yolov8.onnx",
        resnet_model_path="onnx/ResNet50.pth",
        debug_dir="debug_crops"  # Сохраняем кропы в эту папку
    )
    
    # Путь к изображению
    image_path = os.path.join(os.path.dirname(__file__), "frames/obj_2032754221/frame_0050.png")
    
    # Загрузка изображения
    try:
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Не удалось загрузить изображение: {image_path}")
        
        # Детекция огня
        result = detector.detect_fire(image)
        print(f"Результат детекции: {result}")
        
        # Визуализация
        if result.startswith("NO"):
            print("Огонь не обнаружен")
        else:
            print("Обнаружен огонь!")
        
        # Показать оригинал с детекциями
        visualized_img = detector.visualize_detections(image)
        cv2.imshow("Original with detections", visualized_img)
        
        # Показать кропнутые изображения (для отладки)
        detector.show_last_crops()
        
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    except Exception as e:
        print(f"Ошибка: {str(e)}")