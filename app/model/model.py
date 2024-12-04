from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler
import joblib
import pandas as pd

DIABETES_MODEL = "./app/model/diabetes_model.h5"
HYPERTENSION_MODEL = "./app/model/hypertension_model.joblib"
OBESITY_MODEL = "./app/model/obesity_model.joblib"
DYSLIPIDEMI_MODEL = "./app/model/dyslipidemia_model.h5"

def model(input_data):
    input_df = pd.DataFrame([input_data])
    input_df_processed = pd.get_dummies(input_df, drop_first=True)
    scaler = StandardScaler()
    input_scaled = scaler.fit_transform(input_df_processed)
    input_array = input_df.values.reshape(1, -1)

    diabetes_probe = diabetes_model.predict(input_array) 
    dyslipidemi_probe = dyslipidemi_model.predict(input_scaled) 
    hypertension_probe = hypertension_model.predict_proba(input_df)
    obesity_probe = obesity_model.predict_proba(input_scaled)

    # 확률값 출력
    print("Diabetes Model Prediction (Probability):", diabetes_probe[0][0])
    print("Dyslipidemi Model Prediction (Probability):", dyslipidemi_probe[0][0])
    print("Hypertension Model Prediction (Probabilities):", hypertension_probe[0][1])
    print("Obesity Model Prediction (Probabilities):", obesity_probe[0][1])

    return {
        "당뇨": round(diabetes_probe[0][0] * 100, 2),
        "이상지질혈증": round(dyslipidemi_probe[0][0] * 100, 2),
        "고혈압": round(hypertension_probe[0][1] * 100, 2),
        "복부비만": round(obesity_probe[0][1] * 100, 2),
    }


def load_joblib_model(file_path):
    "obesity / hypertension"
    loaded_model = joblib.load(file_path)
    return loaded_model


def load_h5_model(model_path):
    "diabetes / dyslipidemia"
    loaded_model = load_model(model_path)
    return loaded_model


diabetes_model = load_h5_model(DIABETES_MODEL)
dyslipidemi_model = load_h5_model(DYSLIPIDEMI_MODEL)
hypertension_model = load_joblib_model(HYPERTENSION_MODEL)
obesity_model = load_joblib_model(OBESITY_MODEL)