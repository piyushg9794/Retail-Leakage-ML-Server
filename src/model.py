from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ExpSineSquared, RationalQuadratic, Matern
from sklearn.model_selection import RandomizedSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import datetime as dt


rf = RandomForestRegressor()
rf_param = {'bootstrap': [True, False],
 'max_depth': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
 'max_features': ['auto', 'sqrt'],
 'min_samples_leaf': [1, 2, 4],
 'min_samples_split': [2, 5, 10],
 'n_estimators': [200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000]
 }

smooth_kernel = RBF(length_scale=1.0, length_scale_bounds=(1e-1, 10.0))
local_periodic_kernel = ExpSineSquared()*smooth_kernel
irregular_kernel = RationalQuadratic(length_scale=1.0, alpha=0.1)
kernel = (smooth_kernel + local_periodic_kernel + irregular_kernel)
fin_model = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=10, copy_X_train=False)

class CustomModel(BaseEstimator, TransformerMixin):
    def __init__(self):
        super().__init__()

    def fit(self, x, y):
        self.rscv = RandomizedSearchCV(rf, rf_param , cv=5, refit=True)
        self.fx_train = x.drop(columns=['Dist', 'Month', 'Crisis'])
        self.rscv.fit(self.fx_train, y)

        return self

    def transform(self, x, y=None):
        fx_preds= self.rscv.predict(self.fx_train)
        x = pd.DataFrame(data={'Date': self.fx_train.index,'Dist_repr': fx_preds,})
        x['Date']=x['Date'].map(dt.datetime.toordinal)

        return x

pipe = Pipeline([
            ('RF_Model', CustomModel()),
            ('Scaler', StandardScaler()),
            ('GPR_Model', fin_model)
            ])

