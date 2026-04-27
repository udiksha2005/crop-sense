# crop-sense
To help farmers quickly identify crop leaf diseases using an image and get instant treatment recommendations, reducing crop loss and improving yield.
User uploads a crop leaf image.
Backend sends the image to HuggingFace AI model.
AI identifies the disease + confidence score.
Backend maps the disease to the correct solution.
Result (disease + treatment) is shown to the user.

# Tech Stack
- Frontend: HTML, CSS, JavaScript
- Backend: python
- Machine Learning: Hugging Face Inference API (model serving)
- Database: SQLite

# Features
- Confidence scoring
- Disease → solution mapping
- Prediction history logging
- REST API architecture

# Future Improvements
- Custom-trained ML model
- Cloud deployment
- Dockerization
- Improved model calibration
- Frontend UI enhancement

