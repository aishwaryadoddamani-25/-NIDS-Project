NIDS ANDROID PROJECT - READ THIS FIRST

This package preserves your actual scikit-learn IsolationForest model in a Python backend.
The Android APK is a small WebView app that opens the hosted NIDS dashboard.

IMPORTANT LIMITATION
- The machine-learning model runs on the hosted Python service, not inside the APK.
- The APK needs an internet connection and a deployed backend URL.
- This is the smallest practical path for someone with only an Android phone.
- A fully offline APK containing scikit-learn is much harder because its compiled dependencies need Android-compatible builds.

WHAT IS INCLUDED
1. backend/app.py       Python Flask dashboard + original IsolationForest logic
2. backend/requirements.txt
3. android/             minimal Android WebView project
4. .github/workflows/build-apk.yml  cloud APK build workflow

WHAT MUST STILL HAPPEN
A. Host the backend online (for example, using Replit). The backend folder is self-contained.
B. Copy the resulting public HTTPS URL into:
   android/app/src/main/java/com/example/nids/MainActivity.java
   Replace https://YOUR-NIDS-BACKEND-URL with your real URL.
C. Put the project in a GitHub repository and run the "Build Android APK" workflow.
D. Download app-debug.apk from the workflow's Artifacts section.

No APK is prebuilt in this ZIP. Building requires an online hosting service for the model and a cloud build run for Android.

The sample dataset contains 10 fixed records. The dashboard does NOT capture or monitor live phone network traffic.