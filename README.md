# crop-sense
To help farmers quickly identify crop leaf diseases using an image and get instant treatment recommendations, reducing crop loss and improving yield.
User uploads a crop leaf image.
Backend sends the image to HuggingFace AI model.
AI identifies the disease + confidence score.
Backend maps the disease to the correct solution.
Result (disease + treatment) is shown to the user.
