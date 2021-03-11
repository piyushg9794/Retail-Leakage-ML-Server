from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ExpSineSquared, RationalQuadratic, Matern
from sklearn.model_selection import RandomizedSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
import pandas as pd


rf = RandomForestRegressor()
rf_param = []

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
