import os
from math import *
from ..models import CheckResult

OP=['+','-','*','/','=','%',':','?','&','^','!','|','>','<',',','.',',',';','~','#',
    '+=','-=','*=','/=','&&','!=','%=','>>','<<','==','||','++','--','->','&=','|=','^=','**','>=','<=','//']

def get_each_path(path):
    fname = os.listdir(path)
    fpath=[]
    for name in fname:
        tmp = path + '\\' + name
        fpath.append(tmp)
    return fpath

def get_allfile(fpath):
    allfile = []
    ALLFILE = []
    n = len(fpath)
    for i in range(n):
        TT = ""
        tt = []
        t1 = set('')
        t2 = set('')
        t3 = t4 = t5 = 0
        lines = open(fpath[i], encoding='utf-8').read().strip().split('\n')
        for l in lines:
            ll = l.replace(" ", "").lower()
            if len(ll) > 1 and ll[0] == '/' and ll[1] == '/': continue
            pos = ll.find('//')
            if pos != -1: ll = ll[0:pos]
            if len(ll) < 2: continue
            TT += ll
            t5 += 1
            llen = len(ll)
            po = 0
            for x in range(llen - 1):
                if x > 0 and ll[x - 1] in OP: continue
                if ll[x:x + 2] in OP:
                    t1.add(ll[x:x + 2])
                    t2.add(ll[po:x])
                    po = x + 2
                    t3 += 1
                    t4 += 1
                elif ll[x] in OP:
                    t1.add(ll[x])
                    t2.add(ll[po:x])
                    po = x + 1
                    t3 += 1
                    t4 += 1
            t4 += 1
            t2.add(ll[po:])
        if '' in t2: t2.remove('')
        tt.append(len(t1))
        tt.append(len(t2))
        tt.append(t3)
        tt.append(t4)
        tt.append(t5)
        allfile.append(tt)
        ALLFILE.append(TT)
    return allfile,ALLFILE

def get_cos(allfile):
    n=len(allfile)
    sim_cos = [[0] * (n + 1) for o in range(n + 1)]
    for i in range(n):
        for j in range(i + 1, n):
            f1 = allfile[i]
            f2 = allfile[j]
            s1 = s2 = s3 = 0
            for x in range(len(f1)):
                s1 += f1[x] * f2[x]
                s2 += f1[x] ** 2
                s3 += f2[x] ** 2
            sim_cos[i][j] = s1 / sqrt(s2 + 1e-3) / sqrt(s3 + 1e-3)
    return sim_cos

def cal_hash(str,base,k):
    hash=[]
    tmp=0
    n=len(str)
    mod=1000*1000*1000+7
    for i in range(k):
        if i<n:
            tmp+=ord(str[i])*(base**(k-1-i))
    tmp%=mod
    hash.append(tmp)
    for i in range(k,n):
        tmp=((tmp-ord(str[i-k])*(base**(k-1)))*base+ord(str[i]))%mod
        tmp+=mod
        tmp%=mod
        hash.append(tmp)
    return hash
def winnow(hash,t,k):
    d=t-k+1
    fingerprint={}
    n=len(hash)
    for i in range(n-d+1):
        tmp=hash[i:i+d]
        mi=tmp[0]
        mi_x=0
        for j in range(d):
            if tmp[j]<=mi:
                mi=tmp[j]
                mi_x=j
        if (i+mi_x) not in fingerprint.keys():
            fingerprint[i+mi_x]=mi
    return fingerprint
def cal_dp(a,b):
    n1=len(a)
    n2=len(b)
    s1=[]
    s2=[]
    for i in a.values(): s1.append(i)
    for i in b.values(): s2.append(i)
    dp=[[0]*(n2+1) for o in range(n1+1)]
    for q in range(n1):
        for w in range(n2):
            dp[q+1][w+1] = (dp[q][w]+1) if s1[q] == s2[w] else (max(dp[q][w+1],dp[q+1][w]))
    sim_win=dp[n1][n2]/(min(n1,n2)+1e-3)
    return sim_win

def get_win(ALLFILE):
    n=len(ALLFILE)
    t = 7
    k = 3
    base = 233
    sim_win = [[0] * (n + 1) for o in range(n + 1)]
    for i in range(n):
        for j in range(i + 1, n):
            f1 = ALLFILE[i]
            f2 = ALLFILE[j]
            sim_win[i][j] = cal_dp(winnow(cal_hash(f1, base, k), t, k), winnow(cal_hash(f2, base, k), t, k))
    return sim_win

def get_second_result(path, id):
    fpath=get_each_path(path)
    file1,file2=get_allfile(fpath)
    sim_cos=get_cos(file1)
    sim_win=get_win(file2)
    n=len(file1)
    for i in range(n):
        for j in range(i+1,n):
            sim_tot = (3 * sim_cos[i][j] + 1 * sim_win[i][j]) / 4 * 100
            check = CheckResult.objects.get(check_id=id, file1=fpath[i].split('\\')[-1], file2=fpath[j].split('\\')[-1])
            check.sim2 = sim_tot
            check.save()

