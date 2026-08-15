# Trash Detection Event Action System (TDEAs)

A senior project that detects trash in real time using a custom YOLOv8 model, uploads detection screenshots to Firebase Storage, and displays results in a web dashboard.

## Project Structure

```
Senior Project/
├── HTML CODE TDEAs/          # Frontend dashboard (HTML/CSS)
│   ├── test.html
│   ├── style.css
│   └── firebase-config.example.js
└── SeniorProject2_TDEAs/     # Backend detection script (Python)
    ├── TDEAs.py
    ├── TrashDetection.pt     # Custom trained model
    ├── yolov8n.pt            # Base YOLOv8 model
    ├── screenshots/            # Local detection screenshots
    └── firebase-credentials.json.example
```

## Tech Stack

- **Python** — OpenCV, Ultralytics YOLOv8, Matplotlib
- **Firebase** — Realtime Database & Cloud Storage
- **Frontend** — HTML, CSS, Bootstrap, Firebase JS SDK

## Setup

### 1. Python environment

```bash
cd SeniorProject2_TDEAs
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 2. Firebase credentials

1. Go to [Firebase Console](https://console.firebase.google.com/) → Project Settings → Service Accounts.
2. Generate a new private key (JSON file).
3. Copy the example file and add your key:

```bash
copy firebase-credentials.json.example firebase-credentials.json
```

4. Replace the placeholder values in `firebase-credentials.json` with your downloaded key.

> **Important:** `firebase-credentials.json` is gitignored and must never be committed.

### 3. Configure environment variables

Copy the example file and fill in your Firebase project details:

```bash
copy .env.example .env
```

Set these values in `.env` (or as system environment variables):

| Variable | Example placeholder |
|----------|---------------------|
| `FIREBASE_STORAGE_BUCKET` | `your-project-id.appspot.com` |
| `FIREBASE_DATABASE_URL` | `https://your-project-id-default-rtdb.firebaseio.com` |
| `FIREBASE_CREDENTIALS_PATH` | `./firebase-credentials.json` |

### 4. Run the detection backend

```bash
python TDEAs.py
```

This opens your webcam, runs trash detection, saves screenshots locally, and uploads them to Firebase.

### 5. View the dashboard

1. Copy the frontend Firebase config:

```bash
cd ..\HTML CODE TDEAs
copy firebase-config.example.js firebase-config.js
```

2. Replace the placeholder values in `firebase-config.js` with your Firebase web app config from the Firebase Console.

3. Open `HTML CODE TDEAs/test.html` in a browser to see detected images from Firebase Realtime Database.

## Security Notes

- Never commit Firebase Admin SDK keys or `.env` files.
- If a service account key was ever shared publicly, revoke it in Firebase Console and generate a new one.
- Configure Firebase Security Rules to restrict database and storage access appropriately.

## License

Senior project — for academic and portfolio use.
