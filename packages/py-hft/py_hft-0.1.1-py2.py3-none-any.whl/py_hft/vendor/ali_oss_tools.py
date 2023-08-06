import oss2
from oss2.models import (RestoreJobParameters, RestoreConfiguration, RESTORE_TIER_EXPEDITED,  RESTORE_TIER_STANDARD, RESTORE_TIER_BULK)
import sys
from ..util.util import *
from ..util.date_worker import *

def UploadFromDisk(path='D:/data/', topic=['stock', 'futures']):
  global_start = time.time()
  print('start', path, topic)
  a = AliOSS()
  remote_paths = ['market_data/binary/%s/%s' %(t, f.split('/')[-1]) for t in topic for f in os.listdir(path+t) if '.gz' in f]
  local_paths = [path+t+'/'+f for t in topic for f in os.listdir(path+t) if '.gz' in f]
  MPRun(a.Upload, [[r, l, i, len(local_paths), False] for i, (r, l) in enumerate(zip(remote_paths, local_paths))], ret=False)
  print('global %s cost %.2f'%(path, time.time() - global_start))

def UploadBinaryFutures(path = '/today/', diff=0):
  global_start = time.time()
  date = QDate(diff=diff)
  a = AliOSS()
  local_paths = ['/running/%s/future%s.dat.gz'%(date, date)] #[path + f for f in os.listdir(path) if 'dat.gz' in f]
  remote_paths = ['market_data/binary/futures/%s' %(f.split('/')[-1]) for f in local_paths]
  MPRun(a.UploadAndDelete, [[r, l, i, len(local_paths), False] for i, (r, l) in enumerate(zip(remote_paths, local_paths))], ret=False)
  print('global %s cost %.2f'%(path, time.time() - global_start))

def UploadNewFutures(path = '/live_mmm/', diff=0):
  global_start = time.time()
  date = QDate(diff=diff, split_c='')
  a = AliOSS()
  local_paths = ['/live_mmm/futures.%s.dat.gz'%(date), '/live_mmm/futures_night.%s.dat.gz'%(date)] #[path + f for f in os.listdir(path) if 'dat.gz' in f]
  remote_paths = ['market_data/new/futures/%s' %(f.split('/')[-1]) for f in local_paths]
  MPRun(a.Upload, [[r, l, i, len(local_paths), False] for i, (r, l) in enumerate(zip(remote_paths, local_paths))], ret=False)
  print('global %s cost %.2f'%(path, time.time() - global_start))

def UploadTick(path='/running/csv/', diff=0):
  global_start = time.time()
  date = QDate(diff=diff)
  a = AliOSS()
  for t in ['csv', 'pickle']:
    local_paths = [path+date+'/'+f for f in os.listdir(path+date+'/') if '%s.gz'%(t) in f]
    remote_paths = ['market_data/tick/gz/%s/%s/%s' %(t, date, f.split('/')[-1]) for f in local_paths]
    MPRun(a.UploadAndDelete, [[r, l, i, len(local_paths), False] for i, (r, l) in enumerate(zip(remote_paths, local_paths))], ret=False)

def UploadBinaryStock(path = '/root/huatai/build/', diff=0):
  global_start = time.time()
  date = QDate(diff=diff)
  a = AliOSS()
  local_paths = [path + f for f in os.listdir(path) if 'dat.gz' in f and 'stocktick' in f]
  remote_paths = ['market_data/binary/stock/%s' %(f.split('/')[-1]) for f in local_paths]
  MPRun(a.UploadAndDelete, [[r, l, i, len(local_paths), False] for i, (r, l) in enumerate(zip(remote_paths, local_paths))], ret=False)
  print('global %s cost %.2f'%(path, time.time() - global_start))

def DataUpload(diff=-1):
  #UploadTick(diff=-1)
  #UploadBinaryFutures(diff=diff)
  #UploadBinaryStock(diff=diff)
  UploadNewFutures(diff=diff)

class AliOSS:
  def __init__(self, user='nick', bucket_name='market-data-cache'):
    self.bucket = AliOSS.Bucket(user=user, bucket_name=bucket_name)
    self.FILESIZETHR = 10000  # threashold: 10M, less than thr will be override

  @staticmethod
  def Auth(user='nick'):
    return oss2.Auth('LTAI4G719wvoqK4VgmgwzWc4', '8WzJh9KFAUHFarMWjhyiG3wIbp3kSd')
  
  @staticmethod
  def Bucket(user='nick', bucket_name='market-data-cache', endpoint='oss-accelerate.aliyuncs.com'):
    return oss2.Bucket(AliOSS.Auth(user), 'http://oss-cn-shanghai.aliyuncs.com', bucket_name)
    #return oss2.Bucket(AliOSS.Auth(user), endpoint, bucket_name)
  
  def Upload(self, remote, local, i=-1, j=-1, override=True):
    file_start = time.time()
    headers = dict()
    if self.CheckExisted(remote) == True and self.GetSize(remote) > self.FILESIZETHR and override == False:
      print('remote %s existed and size good, ignored')
      return
    print('start upload', remote)
    result = self.bucket.put_object_from_file(remote, local, headers=headers)
    self.Res(result)
    print(local, 'uploaded as', remote, 'cost', time.time()-file_start, '[%d/%d]'%(i, j))#, end='/r')

  def UploadAndDelete(self, remote, local, i=-1, j=-1, override=True):
    if not os.path.exists(local):
      RedPrint('local file missing', local)
      return
    RedPrint('remote:', self.GetSize(remote), 'local:', os.path.getsize(local))
    self.Upload(remote, local, i, j, override)
    if self.GetSize(remote) == os.path.getsize(local):
      RedPrint('rm %s' %(local))
      os.system('rm %s' %(local))

  def __delete(self, prefix):
    for obj in oss2.ObjectIterator(self.bucket, prefix=prefix):
      res = self.bucket.delete_object(obj.key)
      self.Res(res)
  
  def Res(self, result):
    print('http status:', result.status, 'request_id:', result.request_id) #, 'ETag:',result.etag, 'date:', result.headers['date'])

  def ManualDelete(self, prefix):
    command = input('Confirmed deleted[%s]?' % (self.ListFiles(prefix)))
    if command != 'yes':
      RedPrint('Delete Cancelled')
      return
    self.__delete(prefix)
  
  def GetSize(self, prefix=''):
    return sum([obj.size for obj in oss2.ObjectIterator(self.bucket, prefix=prefix) if obj.key[-1] != '/'])
  
  def ListFiles(self, prefix=''):
    return [obj.key for obj in oss2.ObjectIterator(self.bucket, prefix=prefix) if obj.key[-1] != '/']

  def ListDirs(self, prefix=''):
    return [obj.key for obj in oss2.ObjectIterator(self.bucket, prefix=prefix) if obj.key[-1] == '/']
    
  def CheckExisted(self, remote_file):
    return self.bucket.object_exists(remote_file)

  def Restore(self, remote_file):
    if isinstance(remote_file, str):
      self.bucket.restore_object(remote_file)
    elif isinstance(remote_file, list):
      for rf in remote_file:
        self.bucket.restore_object(rf)
    else:
      RedPrint('Restore failed')
      sys.exit(1)

  def Download(self, remote, local, i=-1, j=-1, override=True):
    file_start = time.time()
    if override == False and os.path.getsize(local) > self.FILESIZETHR:
      print('local %s existed and size good, ignored'%(local))
      return
    meta = self.bucket.head_object(remote)
    #job_parameters = RestoreJobParameters(RESTORE_TIER_EXPEDITED)
    #restore_config= RestoreConfiguration(days=7, job_parameters=job_parameters)
    if meta.resp.headers['x-oss-storage-class'] == oss2.BUCKET_STORAGE_CLASS_ARCHIVE:
      RedPrint('start defreeze')
      if 'x-oss-storage' not in meta.resp.headers:
          #for _ in range(7):
            try:
              RedPrint('defreeze')#, _)#, end='/r')
              self.bucket.restore_object(remote)#, input=restore_config)
            except oss2.exceptions.RestoreAlreadyInProgress:
              RedPrint('Restoring..., waiting...', color='green')
              time.sleep(1)
      while True:
        meta = self.bucket.head_object(remote)
        print((meta.__dict__))
        if meta.resp.headers['x-oss-restore'] == 'ongoing-request="true"':
          RedPrint(remote, 'defreezing...', color='green')
          time.sleep(5)
        else:
          RedPrint('end defreeze')
          break
    result = self.bucket.get_object_to_file(remote, local) # , headers=headers)
    self.Res(result)
    print(local, 'downloaded as', remote, 'cost', time.time()-file_start, '[%d/%d]'%(i, j))#, end='/r')
  
if __name__ == '__main__':
  #Upload('market_data/test/zeromq-4.1.2.tar.gz', '/home/xhuang/zeromq-4.1.2.tar.gz', override=False)
  a = AliOSS()
  #print(a.ListDirs('market_data'))
  fs = (a.ListFiles())
  fs = filter(lambda x: 'futures' in x and x >= 'market_data/binary/futures/future2020-10-09.dat.gz' and 'future_' not in x and x < 'market_data/binary/futures/future2021-03-24.dat.gz', fs)
  fs = list(fs)
  for f in fs:
    of = '/binary_data/raw/ali/'+f.split('/')[-1]
    if os.path.exists(of): continue
    a.Download(f, of)
  #a.ManualDelete(prefix='')
  #a.UploadAndDelete('market_data/binary/futures/future2020-10-23.dat.gz', '/today/future2020-10-23.dat.gz')
  #a.Restore('market_data/binary/futures/future2020-10-23.dat.gz')
  #a.Download('market_data/binary/stock/stocktick2020-05-12.dat.gz', 'stocktick2020-05-12.dat.gz')
