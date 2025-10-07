import numpy as np

# Simulate a trained model (replace with actual loading logic)
class DummyModel:
    def predict(self, X):
        # simple linear combination simulation
        return np.sum(X, axis=1) * 0.5 + 1

model = DummyModel()

def make_predictions(features_list):
    """Takes a list of dicts -> returns predictions"""
    X = np.array([[v for v in f.values()] for f in features_list])
    preds = model.predict(X)
    return preds.tolist()
