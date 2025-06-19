import os
import cv2
import pandas as pd

# Path to extracted dataset
DATASET_DIR = "train"

# Only include these 5 emotions
emotion_map = {
    "angry": 0,
    "happy": 1,
    "sad": 2,
    "surprise": 3,
    "neutral": 4
}

data = []

# Loop through only relevant folders
for emotion_name, label in emotion_map.items():
    folder_path = os.path.join(DATASET_DIR, emotion_name)
    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        continue
    for img_file in os.listdir(folder_path):
        img_path = os.path.join(folder_path, img_file)
        try:
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            img = cv2.resize(img, (48, 48))  # Ensure standard size
            pixels = img.flatten()
            row = [label] + pixels.tolist()
            data.append(row)
        except Exception as e:
            print(f"Skipped {img_path}: {e}")
            continue

# Save DataFrame
columns = ['emotion'] + [f'pixel{i}' for i in range(48 * 48)]
df = pd.DataFrame(data, columns=columns)
df.to_csv('fer2013_training_onehot.csv', index=False)

print(f"✅ Created fer2013_training_onehot.csv with {len(df)} rows.")
