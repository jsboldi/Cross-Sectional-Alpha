
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import lightgbm as lgb
import matplotlib
from sklearn import model_selection
import sklearn
import math

# initialize training panel

rtn_df = pd.read_parquet("../data/return5day.parquet",engine = "pyarrow")
vol_df = pd.read_parquet("../data/volatility.parquet", engine = "pyarrow")
mom_df = pd.read_parquet("../data/63daymomentum.parquet",engine = "pyarrow")
prices = pd.read_parquet("../data/data.parquet",engine = "pyarrow")
fwd_5d = np.log(prices.shift(-5)/prices)



rtn_df = rtn_df.stack().rename("ret_5d")
vol_df = vol_df.stack().rename("vol_20d")
mom_df = mom_df.stack().rename("mom_63d")
fwd_5d = fwd_5d.stack().rename("fwd_ret_5d")


training_panel = pd.concat([rtn_df,vol_df,mom_df,fwd_5d],axis= 1)
training_panel = training_panel.dropna()




unique_dates = training_panel.index.get_level_values("Date").unique().sort_values()

split_idx = int(len(unique_dates) * 0.75)
train_dates = unique_dates[:split_idx]
valid_dates = unique_dates[split_idx:]

train_panel = training_panel.loc[training_panel.index.get_level_values("Date").isin(train_dates)]
valid_panel = training_panel.loc[training_panel.index.get_level_values("Date").isin(valid_dates)]

X_train = train_panel[["ret_5d", "vol_20d", "mom_63d"]]
Y_train = train_panel["fwd_ret_5d"]

X_valid = valid_panel[["ret_5d", "vol_20d", "mom_63d"]]
Y_valid = valid_panel["fwd_ret_5d"]



modelv1 = lgb.LGBMRegressor(num_leaves= 31, learning_rate= 0.05, n_estimators = 20)
modelv1.fit(X_train,Y_train,eval_set= [(X_valid,Y_valid)])






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



valid_panel = valid_panel.copy()

valid_panel['score'] = y_predict

valid_panel['rank'] = valid_panel.groupby("Date")['score'].rank(method = "min",ascending  = 0 )

# cross-sectional percentile rank by date
valid_panel["score_pct"] = valid_panel.groupby(level="Date")["score"].rank(pct=True)

# signal: +1 long, -1 short, 0 neutral
valid_panel["signal"] = 0
valid_panel.loc[valid_panel["score_pct"] >= 0.90, "signal"] = 1
valid_panel.loc[valid_panel["score_pct"] <= 0.10, "signal"] = -1


# count number of longs and shorts per date
long_count = valid_panel.groupby(level="Date")["signal"].apply(lambda x: (x == 1).sum())
short_count = valid_panel.groupby(level="Date")["signal"].apply(lambda x: (x == -1).sum())

# map counts back to rows
valid_panel["n_longs"] = valid_panel.index.get_level_values("Date").map(long_count)
valid_panel["n_shorts"] = valid_panel.index.get_level_values("Date").map(short_count)

# equal weights
valid_panel["weight"] = 0.0
valid_panel.loc[valid_panel["signal"] == 1, "weight"] = 1.0 / valid_panel.loc[valid_panel["signal"] == 1, "n_longs"]
valid_panel.loc[valid_panel["signal"] == -1, "weight"] = -1.0 / valid_panel.loc[valid_panel["signal"] == -1, "n_shorts"]


valid_panel["weighted_return"] = valid_panel["weight"] * valid_panel["fwd_ret_5d"]

portfolio_returns = valid_panel.groupby(level="Date")["weighted_return"].sum()
print(portfolio_returns.head())


cumulative_log_return = portfolio_returns.cumsum()
equity_curve = np.exp(cumulative_log_return)

print(equity_curve.tail())


equity_curve.plot()
plt.title("Strategy Equity Curve")
plt.show()


print(valid_panel)

valid_panel.to_parquet("valid_panel.parquet")

print(valid_panel.head())



rebalance_dates = unique_dates[::5]

bt_panel = valid_panel.loc[
    valid_panel.index.get_level_values("Date").isin(rebalance_dates)
].copy()

bt_panel["pred"] = modelv1.predict(bt_panel[["ret_5d", "vol_20d", "mom_63d"]])

bt_panel["rank"] = bt_panel.groupby("Date")["pred"].rank(pct=True)

bt_panel["signal"] = 0
bt_panel.loc[bt_panel["rank"] >= 0.9, "signal"] = 1
bt_panel.loc[bt_panel["rank"] <= 0.1, "signal"] = -1

bt_panel["strategy_ret"] = bt_panel["signal"] * bt_panel["fwd_ret_5d"]

period_returns = bt_panel.groupby("Date")["strategy_ret"].mean()

equity_curve2 = np.exp(period_returns.cumsum())
equity_curve2.plot()
plt.title("Strategy Equity Curve 2")
plt.show()
print(bt_panel)