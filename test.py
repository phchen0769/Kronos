import os

# 在加载模型前设置环境变量
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"  # 设置镜像源

import pandas as pd

from model import Kronos, KronosTokenizer, KronosPredictor

# 1. 加载模型和tokenizer
tokenizer = KronosTokenizer.from_pretrained("NeoQuasar/Kronos-Tokenizer-base")
model = Kronos.from_pretrained("NeoQuasar/Kronos-small")

# 2. 初始化预测器
# predictor = KronosPredictor(model, tokenizer, device="cuda:0", max_context=512)
predictor = KronosPredictor(model, tokenizer, device="cpu", max_context=512)

# 3. 加载数据
df = pd.read_csv("examples/data/XSHG_5min_600977.csv")
df["timestamps"] = pd.to_datetime(df["timestamps"])

# 4. 定义内容窗口和预测长度
lookback = 400
pred_len = 120

# 5. 初始化数据输入
x_df = df.loc[: lookback - 1, ["open", "high", "low", "close", "volume", "amount"]]
x_timestamp = df.loc[: lookback - 1, "timestamps"]
y_timestamp = df.loc[lookback : lookback + pred_len - 1, "timestamps"]

# 6. 生成预测
pred_df = predictor.predict(
    df=x_df,
    x_timestamp=x_timestamp,
    y_timestamp=y_timestamp,
    pred_len=pred_len,
    T=1.0,  # Temperature for sampling
    top_p=0.9,  # Nucleus sampling probability
    sample_count=1,  # Number of forecast paths to generate and average
)

print("Forecasted Data Head:")
print(pred_df.head())

# # 7. 批量预测
# df_list = [df1, df2, df3]  # List of DataFrames
# x_timestamp_list = [x_ts1, x_ts2, x_ts3]  # List of historical timestamps
# y_timestamp_list = [y_ts1, y_ts2, y_ts3]  # List of future timestamps

# # Generate batch predictions
# pred_df_list = predictor.predict_batch(
#     df_list=df_list,
#     x_timestamp_list=x_timestamp_list,
#     y_timestamp_list=y_timestamp_list,
#     pred_len=pred_len,
#     T=1.0,
#     top_p=0.9,
#     sample_count=1,
#     verbose=True
# )

# # pred_df_list contains prediction results in the same order as input
# for i, pred_df in enumerate(pred_df_list):
#     print(f"Predictions for series {i}:")
#     print(pred_df.head())