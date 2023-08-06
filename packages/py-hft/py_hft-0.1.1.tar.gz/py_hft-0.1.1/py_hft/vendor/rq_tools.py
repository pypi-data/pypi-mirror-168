import rqdatac as rq
import sys
from ..util.date_worker import *

rq_trade_date_path = '/rq_data/trade_date.npy'
rq_con_path = '/rq_data/con.npy'
rq_ticker_path = '/rq_data/ticker.npy'
rq_min_cache_path = '/rq_data/min_cache/'
rq_daily_cache_path = '/rq_data/daily_cache/'

def login():
  rq.init('18321785803', '584hxy..')

login()

def cache_trade_dates():
  np.save(rq_trade_date_path, [date.isoformat() for date in rq.get_trading_dates('20050101', end_date=QDate(diff=-1), market='cn')])

def cache_con():
  df = rq.all_instruments(type='Future', market='cn')
  df = df[df['listed_date'] < QDate()]
  np.save(rq_con_path, list(set(df['underlying_symbol'])))
  np.save(rq_ticker_path, list(set(df['order_book_id'])))
  
def get_cache_trade_date():
  return np.load(rq_trade_date_path).tolist()

def get_cache_ticker():
  return np.load(rq_ticker_path).tolist()

def get_cache_con():
  return np.load(rq_con_path).tolist()

@timer
def cache_data(freq='1d'):
  tickers = get_cache_ticker()
  date = QDate(diff=-1)
  for i, t in enumerate(tickers):
    file_path = '%s/cache_%s.csv.gz'%(rq_min_cache_path if freq == '1m' else rq_daily_cache_path, t)
    if os.path.exists(file_path):
      print(file_path, 'existed, passed')
      continue
    df = rq.get_price(t, start_date='2005-01-01', end_date=date, frequency=freq, fields=None, adjust_type='pre', skip_suspended =False, market='cn', expect_df=False)
    if not isinstance(df, pd.DataFrame) or len(df) == 0:
      p(t, 'wrong', df)
      continue
    df.to_csv(file_path)
    if i % 50 == 49:
      RedPrint('finished[%d/%d]' %(i, len(tickers)))

if __name__ == '__main__':
  cache_data('1m')
