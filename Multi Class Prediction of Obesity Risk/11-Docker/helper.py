import lightgbm as lgb
import pickle

# Replace 'model_path' with the actual path to your model file
# load model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)
    print("Model loaded successfully")
