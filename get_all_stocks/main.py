import requests
import json
import pandas as pd

# 获取token
res_jqdata_token = requests.post("https://dataapi.joinquant.com/apis", data=json.dumps({
    "method": "get_token",
    "mob": "XXXXXXXXXXX",  # mob是申请JQData时所填写的手机号
    "pwd": "XXXXXX",  # Password为聚宽官网登录密码，新申请用户默认为手机号后6位
}))
token = res_jqdata_token.text

# 获取股票相关信息
res_jqdata_stocks = requests.post("https://dataapi.joinquant.com/apis", data=json.dumps({
     "method": "get_all_securities",
      "token": token,
     "code": "stock",
        "date": "2019-01-15"
     }))
 # 信息处理
stocks = res_jqdata_stocks.text.split('\n')
name, display_name, code = [], [], []
for i, stock in enumerate(stocks):
    if i >= 1:
        info = stock.split(',')
        name.append(info[2])
        display_name.append(info[1])
        code.append(info[0])

output = pd.DataFrame(data={"code": code, "name": name, "display_name": display_name})

# Use pandas to write the comma-separated output file
output.to_csv("../data/stocks.csv", index=False, quoting=3)
