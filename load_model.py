import pickle
import numpy as np
import pandas as pd

with open('model.pkl', 'rb') as f:
  reg_model = pickle.load(f)

row = np.array([407.65, 50.07, 91.33, 53.93, 34.34, 19.08])
feature_names = ['r', 's', 't', 'u', 'v', 'w']

X_new = pd.DataFrame([row], columns=feature_names)
pred = reg_model.predict(X_new)
print(pred)
