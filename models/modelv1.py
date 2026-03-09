
import matplotlib.pyplot
import pandas as pd
import numpy as np
import lightgbm as lgb
import matplotlib
from sklearn import model_selection
import sklearn
import math

# initialize training panel

rtn_df = pd.read_parquet("../data/return1day.parquet",engine = "pyarrow")
vol_df = pd.read_parquet("../data/volatility.parquet", engine = "pyarrow")
mom_df = pd.read_parquet("../data/63daymomentum.parquet",engine = "pyarrow")
prices = pd.read_parquet("../data/data.parquet",engine = "pyarrow")
fwd_5d = np.log(prices.shift(-5)/prices)


print("mom level0 unique sample:", mom_df.index.get_level_values(0)[:5].tolist())
print("run level0 unique sample:", rtn_df.index.get_level_values(0)[:5].tolist())

rtn_df = rtn_df.stack()
vol_df = vol_df.stack()
mom_df = mom_df.stack()
fwd_5d = fwd_5d.stack()


training_panel = pd.concat([rtn_df,vol_df,mom_df,fwd_5d],axis= 1)




print(training_panel.head())

training_panel = training_panel.dropna()


#X_train,X_valid,Y_train,Y_valid  = model_selection.train_test_split(training_panel.loc[:,['5dayReturn','63dayMomentum','20dayVolatility']],training_panel.loc[:,'5d_Fwdreturn'],test_size= 0.2, random_state= 42)

X_train,X_valid,Y_train,Y_valid  = model_selection.train_test_split(training_panel.iloc[:,0:3],training_panel.iloc[:,3],test_size= 0.25, random_state= 42)
print(X_train.info())



modelv1 = lgb.LGBMRegressor(num_leaves= 31, learning_rate= 0.05, n_estimators = 20)
modelv1.fit(X_train,Y_train,eval_set= (X_valid,Y_valid))






y_predict = modelv1.predict(X_valid)

from sklearn import metrics
import numpy as np
import pandas as pd

print("MAE:", metrics.mean_absolute_error(Y_valid, y_predict))
print("MSE:", metrics.mean_squared_error(Y_valid, y_predict))
print("RMSE:", np.sqrt(metrics.mean_squared_error(Y_valid, y_predict)))
print("R2:", metrics.r2_score(Y_valid, y_predict))

importance_df = pd.DataFrame({
    "feature": X_train.columns,
    "importance": modelv1.feature_importances_
}).sort_values("importance", ascending=False)

print(importance_df)