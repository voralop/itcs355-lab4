import os
import joblib
from sklearn.ensemble import RandomForestClassifier

def train():
    # สร้างข้อมูลจำลองสำหรับสร้างไฟล์โมเดล
    X = [[100], [500], [1200], [3000]]
    y = [0, 0, 1, 1]
    
    model = RandomForestClassifier(n_estimators=10, random_state=42)
    model.fit(X, y)
    
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/model_v1.pkl")
    print("Successfully generated models/model_v1.pkl")

if __name__ == "__main__":
    train()