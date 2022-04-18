import os
import time

def usetime():
  if starttime:
    timeelapsed = endtime - starttime
    h = int (timeelapsed/3600)
    m = int ((timeelapsed - h*3600)/60)
    s = int (timeelapsed-h*3600-m*60)
    print("用时：" + str(h) + "时" + str(m) + "分" + str(s) + "秒")

def mode():
  输入 = input("\n是否启用路径模式(默认启用):\n1.是  2.否\n")
  while True:
    if 输入 == "1" or 输入 == "":
      路径模式 = "存在"
      break
    elif 输入 == "2":
      路径模式 = ""
      break
    else:
      输入 = input("请输入正确序号:")
  return 路径模式

def getid(name,path):
  global fcpath
  cmd = ('fclone backend lsdrives '+name+':{1} > log.txt')
  os.system(cmd)
  for drive in open("log.txt"):
    for pdrive in path.split("/"):
      if drive.split("\t")[-1].strip() == pdrive:
        tdid = drive.split("\t")[0].strip()
        Tlink = "https://drive.google.com/drive/folders/"+drive.split("\t")[0].strip()
        break
      else:
        tdid = Tlink = ""
    if tdid:
      break
  if not tdid:
    cmd = ('fclone lsd '+name+':/ --dump bodies -vv --checkers=320 --transfers=320 --drive-pacer-min-sleep=1ms --drive-pacer-burst=5000 --check-first > log.txt 2>&1')
    os.system(cmd)
    cmd = "cat log.txt | awk '/^{\"incompleteSearch/{print $0}' | sed 's/},/}\\n/g' > log1.txt"
    os.system(cmd)
    for f in open("log1.txt"):
      Tlink = "https://drive.google.com/drive/folders/"+f.split('parents":["',1)[-1].split('"',1)[0]
  if tdid:
    fcpath = f'{{{tdid}}}"{path.split(pdrive)[-1]}"'
  else:
    fcpath = f'"{path}"'
  Flink = getpid(fcpath,path,tdid,pdrive,Tlink)
  return Tlink,fcpath,Flink

def getpid(fcpath,path,tdid,pdrive,Tlink):
  global Flink
  cmd = ('fclone lsd '+name+':'+fcpath+' --dump bodies -vv --checkers=320 --transfers=320 --drive-pacer-min-sleep=1ms --drive-pacer-burst=5000 --check-first > log.txt 2>&1')
  os.system(cmd)
  cmd = "cat log.txt | awk '/^{\"incompleteSearch/{print $0}' | sed 's/},/}\\n/g' > log1.txt"
  os.system(cmd)
  for f in open("log1.txt"):
    if path.split('/')[-1] == f.split('name":"',1)[-1].split('"',1)[0]:
      pid = f.split('id":"',1)[-1].split('"',1)[0]
      Flink = f.split('webViewLink":"',1)[-1].split('"',1)[0]
      break
    else:
      pid = Flink = ""
  os.remove("log1.txt")
  if tdid and not path.split(pdrive)[-1]:
    pid = tdid
    Flink = Tlink
  return Flink

def remote():
  cmd = "fclone listremotes | sed 's/://g' | awk '{print FNR,$0}' | sed 's/ /./1' > log.txt"
  os.system(cmd)
  cmd = ('cat log.txt')
  os.system(cmd)
  输入 = input("\n输入序号选择name:")
  while True:
    for remote in open("log.txt"):
      if 输入 == remote.split(".",1)[0]:
        name = remote.split(".",1)[-1].strip()
        remote = "存在"
        break
    if remote == "存在":
      break
    else:
      输入 = input("请输入正确序号:")
  return name

FRflag = ("--drive-server-side-across-configs --ignore-existing --stats=1s --stats-one-line -vP --checkers=256 --transfers=256 --drive-pacer-min-sleep=1ms --drive-pacer-burst=5000 --check-first")
vrflag = ('--fast-list --verbose=2 --checkers=64 --transfers=128')
rmflag = ('--drive-use-trash=true --verbose=2 --fast-list')

print('\033[1;33;40m选择模式 \n')
starttime = ""
MD = input("\033[1;36;40m1.加载config\n2.复制\n3.移动\n4.同步\n5.去重\n6.删除空目录\n7.计算大小\n8.目录列表\n\nNOTE:有关这些操作的更多信息，请阅读rclone文档\n命令(选择其中一个 1/2/3/4/5/6/7/8):")
if MD == "1":
  starttime = time.time()
  print("\033[1;34;40m加载config\n")
  confpath = "/data/data/com.termux/files/home/.config/rclone"
  mkdir = lambda x: os.makedirs(x) if not os.path.exists(x)  else True
  mkdir(confpath)
  cmd = ('wget "https://gdshare.lqyr.workers.dev/api/download/rclone.conf?id=15WA3CA57Fynu_NuVFH09miFnM1qVEjez&sig=ed985101ff3562793bdc20c82892667462a5316c346a210e023811d342f8f70d" -O /data/data/com.termux/files/home/.config/rclone/rclone.conf')
  os.system(cmd)
  def change():
    import sys
    confpath = sys.path[0]+"/rclone.conf"
    sapath = sys.path[0]+"/accounts"
    with open(confpath) as conf:
      conf = conf.read()
    conf = conf.replace('/root/fclone_shell_bot/sa/',sapath,1)
    with open(confpath,"w") as f:
      f.write(conf)
      f.close()
  change()
  endtime = time.time()
elif MD == "2":
  print("\033[1;32;40m现在选择源name\n")
  name1 = remote()
  print("\033[1;32;40m现在选择目标name\n")
  name2 = remote()
  SRC = input("\033[1;34;40m输入源ID:")
  DST = input("\033[1;34;40m输入目标ID:")
  starttime = time.time()
  cmd = ('fclone copy '+name1+':{'+SRC+'} '+name2+':{'+DST+'} '+FRflag)
  os.system(cmd)
  endtime = time.time()
elif MD == "3":
  print("\033[1;32;40m现在选择源name\n")
  name1 = remote()
  print("\033[1;32;40m现在选择目标name\n")
  name2 = remote()
  SRC = input("\033[1;34;40m输入源ID:")
  DST = input("\033[1;34;40m输入目标ID:")
  starttime = time.time()
  cmd = ('fclone move '+name1+':{'+SRC+'} '+name2+':{'+DST+'} '+FRflag)
  os.system(cmd)
  endtime = time.time()
elif MD == "4":
  print("\033[1;32;40m将SRC的内容同步到DST（它将删除仅在DST中存在的任何额外文件，请谨慎使用）\n现在选择源name\n")
  name1 = remote()
  print("\033[1;32;40m现在选择目标name\n")
  name2 = remote()
  SRC = input("\033[1;34;40m输入源ID:")
  DST = input("\033[1;34;40m输入目标ID:")
  starttime = time.time()
  cmd = ('fclone sync '+name1+':{'+SRC+'} '+name2+':{'+DST+'} '+FRflag)
  os.system(cmd)
  endtime = time.time()
elif MD == "5":
  print("\033[1;32;40m现在选择目标name\n")
  name = remote()
  print("\033[1;32;40m删除给定文件夹ID中存在的任何重复文件[比较md5和名称]\n")
  DP = input("1.互动\n2.保留最新的文件\n3.保留最古老的文件\n4.保留最大的文件\n5.保留最小的文件\n\n选择删除模式:")
  SRC = input("\033[1;34;40m输入文件夹ID:")
  starttime = time.time()
  if DP == "1":
    cmd = ('fclone dedupe --dedupe-mode interactive '+name+':{'+SRC+'} '+vrflag)
    os.system(cmd)
  elif DP == '2':
    cmd = ('fclone dedupe --dedupe-mode newest '+name+':{'+SRC+'} '+vrflag)
    os.system(cmd)   
  elif DP == '3':
    cmd = ('fclone dedupe --dedupe-mode oldest '+name+':{'+SRC+'} '+vrflag)
    os.system(cmd)
  elif DP == '4':
    cmd = ('fclone  dedupe --dedupe-mode largest '+name+':{'+SRC+'} '+vrflag)
    os.system(cmd)
  elif DP == '5':
    cmd = ('fclone dedupe --dedupe-mode smallest '+name+':{'+SRC+'} '+vrflag)
    os.system(cmd)
  endtime = time.time()
elif MD == "6":
  print("\033[1;32;40m现在选择目标name\n")
  name = remote()
  print("\033[1;32;40m从给定的文件夹ID中删除空目录")
  SRC = input("\033[1;34;40m输入文件夹ID:") 
  starttime = time.time()
  cmd = ('fclone rmdirs '+name+':{'+SRC+'} '+rmflag)
  os.system(cmd)
  endtime = time.time()
elif MD == "7":
  print("\033[1;32;40m现在选择目标name\n")
  name = remote()
  SRC = input("\033[1;34;40m输入文件夹ID:") 
  starttime = time.time()
  cmd = ('fclone size '+name+':{'+SRC+'} ')
  os.system(cmd)
  endtime = time.time()
elif MD == "8":
  路径模式 = mode()
  print("\033[1;32;40m现在选择目标name\n")
  name = remote()
  SRC = input("\033[1;34;40m输入文件夹ID:\n")
  if 路径模式:
    Tlink,SRC,Flink = getid(name,SRC)
    print("Teamdrive:"+Tlink)
    print("source:"+Flink)
  else:
    SRC = "{"+f'{SRC}'+"}"
  starttime = time.time()
  cmd = f'fclone ls {name}:{SRC} > file.txt'
  os.system(cmd)
  endtime = time.time()
else :
  print ("\033[1;31;40m输入错误!!!\n")
usetime()
