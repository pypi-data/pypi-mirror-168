# LOFO
Leave One Feature Out (**LOFO**) is on of the most powerful techniques for feature selection. 

This repository contains the implementation of **LOFO** in Python and can be used with any model of the followings:
1. Any Scikit-Learn model.
2. Any TensorFlow/Keras model.
3. LightGBM.
4. CatBoost.
5. XGBoost.

# Usage
- Install the package:
```
pip install feature-selection-lofo
```

- Import lofo
```
from feature_selection_lofo import lofo
```

```
lofo.LOFO(X, Y, 
          model, 
          cv, 
          metric, 
          direction, 
          fit_params=None, 
          predict_type='predict', 
          return_bad_feats=False, 
          groups=None,
          is_keras_model=False)
```

|Args||
|---|---|
|X| Pandas DataFrame, input features to the model (predictors).|
|Y| array_like, target/label feature.|
|model| object, the model class (e.g. sklearn.linear_model.LinearRegression()).|
|cv| object, sklearn cross validatoin object (e.g. sklearn.model_selection.KFold(n_splits=5, shuffle=True, random_state=0)).|
|metric| object, metric to use during search (e.g. sklearn.metrics.roc_auc_score).|
|direction| string, direction of optimization ('max' or 'min').|
|fit_params| string, parameters to use for fitting (e.g. "{'X': x_train, 'y': y_train}") . Defaults to "{'X': x_train, 'y': y_train}".|
|predict_type| string, ('predict' or 'predict_proba'). Defaults to 'predict'.|
|return_bad_feats| boolean, whether to return a list of bad features. Defaults to False.|
|groups| array_like, used with StratifiedGroupKFold. Defaults to None.|
|is_keras_model| boolean, whether the model passed is Keras model. Defaults to False.|

|Returns|
|---|
|A Pandas DataFrame with harmful features removed.|
|If return_bad_feats is set to True, it returns a list of the harmful features.|

- Import the needed libraries for your model, cross-validation, etc
### Scikit-Learn Model Example
```
import warnings
import numpy as np
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
```
- Define the paramters
```
# shutdown warning messages
warnings.filterwarnings('ignore')

X = train_df.iloc[:, :-1]
Y = train_df.iloc[:, -1]
model = LogisticRegression()
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
metric = roc_auc_score
direction = 'max'
fit_params = "{'X': x_train, 'y': y_train}"
predict_type = 'predict_proba'
return_bad_feats = True
groups = None
is_keras_model = False
```

- Define the LOFO object and call it
```
lofo_object = lofo.LOFO(X, Y, model, cv, metric, direction, fit_params, 
                        predict_type, return_bad_feats, groups, is_keras_model)

clean_X, bad_feats = lofo_object()
```
clean_X: is the dataset containing the useful features only.

bad_feats: are the harmful or useless features.

### LightGBM Model Example
```
import warnings
import numpy as np
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold
import lightgbm as lgbm
```

- Define the paramters
```
# shutdown warning messages
warnings.filterwarnings('ignore')

X = train_df.iloc[:, :-1]
Y = train_df.iloc[:, -1]
model= lgbm.LGBMClassifier(
                       objective='binary',
                       metric='auc',
                       subsample=0.7,
                       learning_rate=0.03,
                       n_estimators=100,
                       n_jobs=-1)
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
metric = roc_auc_score
direction = 'max'
fit_params = "{'X': x_train, 'y': y_train, 'eval_set': [(x_valid,y_valid)], 'verbose': 0}"
predict_type = 'predict_proba'
return_bad_feats = True
groups = None
is_keras_model = False
```

- Define the LOFO object and call it
```
lofo_object = lofo.LOFO(X, Y, model, cv, metric, direction, fit_params, 
                        predict_type, return_bad_feats, groups, is_keras_model)
clean_X, bad_feats = lofo_object()
```

### TensorFlow/Keras Model Example
```
import warnings
import numpy as np
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold
import tensorflow as tf
from tensorflow.keras import layers
```
- Construct the model
```
def nn_model():
    inputs = layers.Input(shape=X.shape[-1],)
    x = layers.Dense(256, activation='relu')(inputs)
    x = layers.Dense(64, activation='relu')(x)
    output = layers.Dense(1, activation='sigmoid')(x)
    
    model = tf.keras.Model(inputs=inputs, outputs=output)
    model.compile(loss='binary_crossentropy',
              optimizer='adam',)
    
    return model
```

- Define the paramters
```
# shutdown warning messages
warnings.filterwarnings('ignore')

X = train_df.iloc[:, :-1]
Y = train_df.iloc[:, -1]

tf.keras.backend.clear_session()
model = nn_model()

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
metric = roc_auc_score
direction = 'max'
fit_params = "{'x': x_train, 'y': y_train, 'validation_data': (x_valid, y_valid), 'epochs': 10, 'batch_size': 256, 'verbose': 0}"
predict_type = 'predict'
return_bad_feats = True
groups = None
is_keras_model = True
```

- Define the LOFO object and call it
```
lofo_object = lofo.LOFO(X, Y, model, cv, metric, direction, fit_params, 
                        predict_type, return_bad_feats, groups, is_keras_model)

clean_X, bad_feats = lofo_object()
```
