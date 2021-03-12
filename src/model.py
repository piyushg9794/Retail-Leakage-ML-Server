from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ExpSineSquared, RationalQuadratic, Matern
from sklearn.model_selection import RandomizedSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
import pandas as pd


rf = RandomForestRegressor()
rf_param = [{'bootstrap': [True, False],
 'max_depth': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, None],
 'max_features': ['auto', 'sqrt'],
 'min_samples_leaf': [1, 2, 4],
 'min_samples_split': [2, 5, 10],
 'n_estimators': [200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000]
 }]

smooth_kernel = RBF()
local_periodic_kernel = ExpSineSquared()*RBF()
irregular_kernel = RationalQuadratic()
kernel = (smooth_kernel + local_periodic_kernel + irregular_kernel)
fin_model = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=10, copy_X_train=False)

def fn(x,y):
    rscv = RandomizedSearchCV(rf, cv=5, param_grid=rf_param , refit=True)
    fx_train = x.drop(columns=['Dist', 'Month', 'Crisis'])
    rscv.fit(fx_train, y)
    fx_preds= rscv.predict(fx_train)
    gpr_x_train = pd.DataFrame(data={'Date': x.index,'Dist_repr': fx_preds,})

    return gpr_x_train, y

pipe = Pipeline([
            ('RF_Model', fn()),
            ('Scaler', StandardScaler()),
            ('GPR_Model', fin_model())
            ])


# https://www.kaggle.com/metadist/work-like-a-pro-with-pipelines-and-feature-unions
# hyperparameter tuning of kernel, rf paramgrid
