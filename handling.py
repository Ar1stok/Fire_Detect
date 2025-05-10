import cv2
import os

class Handling:
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
        self.label = "Fire"

        if not os.path.exists(frames_path):
            os.makedirs(frames_path)
    
    def to_frames(self, video_name: str):
        cap = cv2.VideoCapture(os.path.join(self.video_path, video_name))
        
        if not cap.isOpened():
            raise IOError(f"Cannot open video file {self.video_path}")
        
        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break  # No more frames

            # Construct filename for the frame
            frame_filename = os.path.join(self.frames_path, f"frame_{frame_count:05d}.{self.img_format}")

            # Save frame as image
            cv2.imwrite(frame_filename, frame)
            frame_count += 1

        cap.release()
        print(f"Extracted {frame_count} frames to folder '{self.frames_path}'")
        return frame_count

    def crop(self, img_name: str, x1, y1, w, h):
        img = cv2.imread(os.path.join(self.frames_path, img_name))

        # Crop image
        cropped_image = img[y1 - (h / 2):y1 + (h / 2), x1 - (w / 2):x1 + (w / 2)]
        return cropped_image
    
    def vizualize(self, img_name: str, x1, y1, w, h):
        img = cv2.imread(os.path.join(self.frames_path, img_name))
        cv2.rectangle(img, (int(x1), int(y1)), (int(x1 + w), int(y1 + h)), (0, 0, 255), 2)

        # Calculate the dimensions of the label text
        (label_width, label_height), _ = cv2.getTextSize(self.label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)

        # Calculate the position of the label text
        label_x = x1
        label_y = y1 - 10 if y1 - 10 > label_height else y1 + 10

         # Draw a filled rectangle as the background for the label text
        cv2.rectangle(img, (int(label_x), int(label_y - label_height)),
                      (int(label_x + label_width), int(label_y + label_height)),
                      (0, 0, 255), cv2.FILLED,)

        # Draw the label text on the image
        cv2.putText(img, self.label, (int(label_x), int(label_y)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        
