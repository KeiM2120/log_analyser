
# 方針: 正規表現を用いてパターンマッチングで必要な情報を取得していく
# pipにて外部ライブラリ dateutilを利用

import re
import collections
from dateutil.parser import parse 

REMOTE_HOST = r"(\d+)\.(\d+)\.(\d+)\.(\d+)"
TIME_STAMP = r"\[(.*)\]"

## このpythonファイルは、logファイルと同一階層においてあることを想定している。

## 問1 リモートホストとアクセス日時を抽出、アクセス時の時間で分類

read_data= open("access.log", "r")
data_lines= read_data.readlines()

# [リモートホスト, 時間]の配列に整形
acc_logs= []
for data in data_lines:
    host= re.match(REMOTE_HOST, data).group()
    time= parse(re.search(TIME_STAMP, data).group(), fuzzy=True)
    acc_logs.append([host,time])

# 0時から23時の間で分類
time_per_acc= [[]  for i in range(24)]
for log in acc_logs:
    h= log[1].hour
    time_per_acc[h].append(log[0])

# collections.Counterでホスト名あたりのアクセス数を算出、一度配列に変換してからアクセス数で降順ソート、出力
for i in range(24):
    print("HOUR:"+ str(i))
    cnt= collections.Counter(time_per_acc[i])
    acc_per_host=[]
    for j in cnt:
        acc_per_host.append([j,cnt[j]])
    acc_per_host = sorted(acc_per_host, key=lambda h: h[1], reverse=True)
    for k in acc_per_host:
        print("Remote host: "+ k[0]+ "  Access time: "+ str(k[1]))
    print("")


