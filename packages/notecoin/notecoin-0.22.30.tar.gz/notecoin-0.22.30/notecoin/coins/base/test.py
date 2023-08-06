import dask.dataframe as dd

path = '/home/bingtao/workspace/tmp/notecoin/binance/trade-daily-detail/binance-trade-daily-detail-20220909.csv'
# nohup /home/bingtao/opt/anaconda3/bin/python /home/bingtao/workspace/notechats/notecoin/notecoin/coins/base/cron.py >>/notechats/notecoin/logs/notecoin-$(date +%Y-%m-%d).log 2>&1 &
df = dd.read_csv(path)

df.to_csv("/home/bingtao/workspace/tmp/my_hi-*.csv.gz", index=False, compression="gzip")
print(2)
