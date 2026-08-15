import cv2
from ultralytics import YOLO
import os
import matplotlib.pyplot as plt
import firebase_admin
from firebase_admin import credentials, storage, db

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FIREBASE_CREDENTIALS_PATH = os.environ.get(
    "FIREBASE_CREDENTIALS_PATH",
    os.path.join(BASE_DIR, "firebase-credentials.json"),
)
MODEL_PATH = os.path.join(BASE_DIR, "TrashDetection.pt")
SCREENSHOT_FOLDER = os.path.join(BASE_DIR, "screenshots")
STORAGE_BUCKET = os.environ.get("FIREBASE_STORAGE_BUCKET")
DATABASE_URL = os.environ.get("FIREBASE_DATABASE_URL")

if not os.path.exists(FIREBASE_CREDENTIALS_PATH):
    raise FileNotFoundError(
        f"Firebase credentials not found at {FIREBASE_CREDENTIALS_PATH}. "
        "Copy firebase-credentials.json.example to firebase-credentials.json "
        "and add your Firebase service account key."
    )

if not STORAGE_BUCKET or not DATABASE_URL:
    raise EnvironmentError(
        "Set FIREBASE_STORAGE_BUCKET and FIREBASE_DATABASE_URL environment variables. "
        "See .env.example for placeholder values."
    )

cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
firebase_admin.initialize_app(
    cred,
    {
        "storageBucket": STORAGE_BUCKET,
        "databaseURL": DATABASE_URL,
    },
)

model = YOLO(MODEL_PATH)

cap = cv2.VideoCapture(0)

os.makedirs(SCREENSHOT_FOLDER, exist_ok=True)

frame_counter = 1

frames_ref = db.reference("frames")
if not frames_ref.get():
    frames_ref.set({})

while cap.isOpened():
    ret, frame = cap.read()

    results = model(frame)

    if isinstance(results, list):
        for result in results:
            if result.boxes is not None:
                for box in result.boxes.xyxy:
                    print("Bounding Box:", box)
                    cv2.rectangle(
                        frame,
                        (int(box[0]), int(box[1])),
                        (int(box[2]), int(box[3])),
                        (0, 255, 0),
                        2,
                    )

        screenshot_filename = f"Figure_{frame_counter}.png"
        screenshot_path = os.path.join(SCREENSHOT_FOLDER, screenshot_filename)
        cv2.imwrite(screenshot_path, frame)

        if screenshot_path.endswith(".png"):
            bucket = storage.bucket()
            blob = bucket.blob(f"frames/{screenshot_filename}")
            blob.upload_from_filename(screenshot_path)

            storage_url = f"https://storage.googleapis.com/{bucket.name}/{blob.name}"

            sanitized_filename = screenshot_filename.replace(".", "").replace("#", "")

            metadata = {
                "bounding_boxes": [box.tolist() for box in result.boxes.xyxy],
                "storage_url": storage_url,
            }

            frames_ref.child(sanitized_filename).set(metadata)

            print(
                f"Uploaded {screenshot_filename} to Firebase Storage "
                "and added metadata to Realtime Database"
            )

        frame_counter += 1

    plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    plt.title("YOLOv8")
    plt.pause(0.001)
