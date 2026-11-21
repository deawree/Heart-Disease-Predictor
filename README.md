# 🫀 Heart Disease Risk Check

A Streamlit app that estimates heart disease risk from 11 clinical inputs using a trained Logistic Regression model, then gives simple, plain-language advice.

🔗 **Live demo:** [https://heart-disease-predictor-npgcnsvlz5bfenicxrrraa.streamlit.app/](https://heart-disease-predictor-npgcnsvlz5bfenicxrrraa.streamlit.app/)

> **Disclaimer:** For learning only. This is not a medical diagnosis. Please see a doctor for any health concern.

## Features

- Easy input form (age, blood pressure, cholesterol, ECG, and more)
- Predict button with a colour-coded risk result (low, moderate, high)
- Plain-language advice and an emergency warning box
- Example profiles, reset button, and a downloadable summary

## Project structure

```
Heart Disease Predictor/
├── MODEL/
│   └── Heart_Disease.ipynb         # Model training notebook
├── app.py                          # Streamlit app
├── Logistic Regression_heart.pkl   # Trained model
├── scaler.pkl                      # Fitted StandardScaler
├── columns.pkl                     # Training feature columns
└── requirements.txt                # Dependencies
```

## Tech stack

Python, Streamlit, scikit-learn, pandas, joblib

## Author

**Deawree Sayanton** · [GitHub]https://github.com/deawree 
