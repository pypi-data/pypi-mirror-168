import jqdatasdk as jq
import sys
from ..util.util import *
from ..util.date_worker import *

jq_fut_trade_days_cache = '/jq_data/fut_trade_days.npy'
jq_trade_days_cache = '/jq_data/trade_days.npy'
jq_futures_dominant_dir = '/jq_data/futures_dominant/'
jq_min_data_dir = '/jq_data/min/'
jq_cache_path = '/jq_data/cache/'
jq_futuresinfo_path = '/jq_data/futures_info.csv'
jq_con_path = '/jq_data/con.npy'
jq_con_map_path = '/jq_data/con_map.npy'
jq_issuedate_path = '/jq_data/issue_date.npy'
jq_startdate_path = '/jq_data/start_date.npy'
jq_enddate_path = '/jq_data/end_date.npy'
jq_daily_data_dir = '/jq_data/daily/'

ex_map = {'IC':'CFEX', 'IF': 'CFFX', 'IH':'CFFX', 'T':'CFFX', 'TF':'CFFX'}
account = [('18321785803','54hxy..'), ('15618384622','WMY69hxy'), ('18015166683', 'WMY69hxy'), ('15504544018', 'WMY69hxy'), ('13208419201', 'WMY69hxy')]
#account = [('15618384622','WMY69hxy')]
account = [('18321785803','54hxy..')]
for i, acc in enumerate(account):
  if i > 0: jq.logout()
  jq.auth(acc[0], acc[1])
  spare = jq.get_query_count()['spare']
  RedPrint(acc[0], 'spare =', spare, color='green')
  if jq.get_query_count()['spare'] > 100000: RedPrint('Using Account', acc[0], color='green'); break

def refresh_all_trade_days(path=jq_trade_days_cache):
  today = QDate(diff=-1)
  a = [td for td in jq.get_all_trade_days() if td < today]
  np.save(path, a)
  install_dirs()
  return a

def get_cache_fut_trade_days(ticker, edur=30):
  dates = np.load(jq_fut_trade_days_cache, allow_pickle=True).tolist()
  return dates[GetCon(ticker)]

def get_cache_trade_days(cache_file=jq_trade_days_cache, edur=30):
  dates = np.load(cache_file, allow_pickle=True)
  if dt.datetime.fromisoformat(QDate()) - dt.datetime.fromisoformat(max(dates)) > dt.timedelta(edur):
    RedPrint('cached trade days is expired more than', edur, 'days')
  return [str(date) for date in dates]

def AddEx(ticker):
  Assert(ticker in ex_map, 'invalid ticker, cant find exchange')
  return ticker + '.' + ex_map[ticker]

def get_min_data_by_ticker(ticker):
  if '.' not in ticker: ticker = AddEx(ticker)
  return jq.get_bars(ticker, 1000000, unit='1m',fields=['date','open','high','low','close', 'volume', 'money', 'open_interest'], end_dt=QDate(diff=-1))

def cache_dominant_one(ticker, date):
  return date, jq.get_dominant_future(ticker, date)

@timer
def cache_dominant_info(ticker, path = jq_futures_dominant_dir):
  count = jq.get_query_count()['spare']
  ticker = GetCon(ticker)
  install(path)
  m = {}
  if os.path.exists(path+ticker+'_dominant.npy'):  m = np.load(path+ticker+'_dominant.npy', allow_pickle=True).tolist()
  trade_days = get_cache_fut_trade_days(ticker)
  days = [t for t in reversed(trade_days) if t not in m]
  #RedPrint('[UpdateDominant] days are:', days)
  #print('keys()', m.keys())
  #print('days', trade_days)
  #res = MPRun(cache_dominant_one, [[ticker, i] for i in days])
  #new_m = {r[0]: r[1] for r in res if r[1] != ''}
  new_m = {}
  for i, d in enumerate(days):
    #print(ticker, d)
    con = jq.get_dominant_future(ticker, d)
    #print(con)
    if con != '': new_m[d] = con
    if i % 1000 == 999: RedPrint('cache_dominant_info Finished[%d/%d]'%(i, len(days)))
  print('updated map:', new_m)
  m.update(new_m)
  np.save(path+ticker+'_dominant.npy', m)
  lcount = jq.get_query_count()['spare']
  RedPrint('cache', ticker, 'dominant finished, cost count =', count-lcount, 'left =', lcount, color='purple')

def install(path):
  os.system('install -d ' + path)

@timer
def install_dirs(prefix=jq_min_data_dir, path=jq_trade_days_cache):
  days = np.load(path, allow_pickle=True)
  paths = [[prefix + d] for d in days]
  MPRun(install, paths)

def cache_min_data_by_ticker(ticker, path=jq_min_data_dir, cache_path=jq_cache_path):
  RedPrint('cache_min_date_by_ticker handling', ticker, color='purple')
  count = jq.get_query_count()['spare']
  if os.path.exists('%s/%s.csv'%(cache_path, ticker)) and file_dur('%s/%s.csv'%(cache_path, ticker)) < 10:
    df = pd.read_csv('%s/%s.csv'%(cache_path, ticker))
  else:
    df = get_min_data_by_ticker(ticker)
    df.to_csv('%s/%s.csv'%(jq_cache_path, ticker), index=False)
  if 'Unnamed: 0' in df: del df['Unnamed: 0']
  df['d'] = [dt.datetime.fromisoformat(d).date().isoformat() for d in df['date']] if df['date'].dtype == object else [d.date().isoformat() for d in df['date']]
  df['dat'] = [dt.datetime.fromisoformat(d).date().isoformat() for d in df['date']] if df['date'].dtype == object else [d.date().isoformat() for d in df['date']]
  df['dat'] = [i.split('.')[0] for i in df['dat']]
  if not os.path.exists('%s/%s_dominant.npy'%(jq_futures_dominant_dir, GetCon(ticker))): cache_dominant_info(ticker=GetCon(ticker))
  if '9999' in ticker:
    dom = pd.Series(np.load('%s/%s_dominant.npy'%(jq_futures_dominant_dir, GetCon(ticker)), allow_pickle=True).tolist()).to_frame(name='real_ticker')
    df = df.merge(dom, left_on=['d'], right_index=True, how='left')
  else:
    df['real_ticker'] = ticker
  df['real_ticker'] = [i if isinstance(i, str) else '' for i in df['real_ticker']]
  try:
    RedPrint('real_ticker missing', set(df[~df['real_ticker'].str.contains(GetCon(ticker))]['d']))
  except AttributeError as e:
    print(e)
    return
  print(df)
  if len(df) == 0: return
  dates = set(df['dat'])
  for i in dates:
    os.system('install -d %s/%s/'%(path, i))
  df.groupby('d').apply(lambda x:x.to_csv('%s/%s/%s.csv'%(path, x['dat'].iloc[0], ticker)))
  lcount = jq.get_query_count()['spare']
  RedPrint('cache', ticker, 'finished, cost count =', count-lcount, 'left =', lcount, color='purple')

def GetFuturesInfo(fut_trade_path=jq_fut_trade_days_cache, info_path=jq_futuresinfo_path, con_path=jq_con_path, con_map_path=jq_con_map_path, issue_path=jq_issuedate_path, override=False):
  if not os.path.exists(info_path) or override:
    df = jq.get_all_securities(types=['futures'])
    df['ticker'] = df.index
    df.to_csv(info_path, index=False)
  else:
    df = pd.read_csv(info_path)
  #df['con'] = [GetCon(i) for i in df['name']]
  #con_list = set(df['con'])
  con_list = []
  con_map = {}
  tickers=set(df['ticker'])
  for t in tickers:
    con_list.append(GetCon(t))
    con_map[GetCon(t)] = t.split('.')[-1]
  np.save(con_path, con_list)
  np.save(con_map_path, con_map)
  issue_date, start_date, end_date = {}, {}, {}
  df['con'] = [GetCon(i) for i in df['name']]
  for con in con_list:
    date = str(df[df['con'] == con]['start_date'].min())
    issue_date[con] = date
  for t in tickers:
    date = str(df[df['ticker'] == t]['start_date'].min())
    start_date[t] = date
    date = str(df[df['ticker'] == t]['end_date'].max())
    end_date[t] = date
  np.save(issue_path, issue_date)
  np.save(jq_startdate_path, start_date)
  np.save(jq_enddate_path, end_date)
  all_days = np.load(jq_trade_days_cache, allow_pickle=True).tolist()
  fut_trade_days = {}
  #print(type(all_days[0]))
  for con in con_list:
    fut_trade_days[con] = [d for d in all_days if d >= issue_date[con]]
  np.save(fut_trade_path, fut_trade_days)
  #print(fut_trade_days)

def cache_dominant_all():
  df = pd.read_csv(jq_futuresinfo_path)
  tickers = list(set(df['ticker']))
  for i, t in enumerate(tickers):
    cache_dominant_info(t)
    if i % 30 == 29:
      RedPrint('cache_dominant_all finished[%d/%d]' %(i, len(tickers)))

def cache_min_all():
  df = pd.read_csv(jq_futuresinfo_path)
  tickers = list(set(df['ticker']))
  #print(tickers)
  #tickers = ['IH9999.CCFX', 'IF9999.CCFX', 'NI9999.XSGE', 'CU9999.XSGE', 'EB9999.XDCE', 'OI9999.XDCE']
  #MPRun(cache_min_data_by_ticker, [[t] for t in tickers])
  for t in tickers:
    cache_min_data_by_ticker(t)
    #cache_dominant_info(t)

def cache_daily_all():
  df = pd.read_csv(jq_futuresinfo_path)
  tickers = list(set(df['ticker']))
  start_date, end_date = np.load(jq_startdate_path, allow_pickle=True).tolist(), np.load(jq_enddate_path, allow_pickle=True).tolist()
  today = QDate(diff=-1)
  for i, t in enumerate(tickers):
    s, e = start_date[t], end_date[t]
    RedPrint('Handling', t, s, e, color='purple')
    out_path = '%s/%s.csv.gz'%(jq_daily_data_dir, t)
    if os.path.exists(out_path) and file_date(out_path) > e: continue
    df = jq.get_price(t, start_date=s, end_date=min(e, today), frequency='daily', fields=['open', 'close', 'high', 'low', 'volume', 'money', 'open_interest'])
    if '9999' in t:
      dom = pd.Series(np.load('%s/%s_dominant.npy'%(jq_futures_dominant_dir, GetCon(t)), allow_pickle=True).tolist()).to_frame(name='real_ticker')
      df = df.merge(dom, left_on=['d'], right_index=True, how='left')
    else:
      df['real_ticker'] = t
    df['t'] = [t.split('.')[0] for i in df['real_ticker']]
    df.to_csv(out_path)
    if np.isnan(df['open']).mean() > 0.1:  RedPrint('too much nan in', out_path, np.isnan(df['open']).mean());# sys.exit(1)
    if i % 100 == 99: RedPrint('Cache_daily_all finished[%d/%d]' %(i, len(tickers)))

if __name__ == '__main__':
  #refresh_all_trade_days()
  #print(get_cache_trade_days())
  #cache_min_data_by_ticker(ticker='IH2011.CCFX')
  #cache_dominant_info(ticker='IF')
  #GetFuturesInfo(override=False)
  cache_min_all()
  #cache_daily_all()
