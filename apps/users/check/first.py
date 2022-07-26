import os
from ..models import CheckResult


def get_each_path(path):
    fname = os.listdir(path)
    fpath=[]
    for name in fname:
        tmp = path + '\\' + name
        fpath.append(tmp)
    return fpath


def get_allfile(fpath):
    all=[]
    n=len(fpath)
    for i in range(n):
        tt = []
        lines = open(fpath[i], encoding='utf-8').read().strip().split('\n')
        for l in lines:
            ll = l.replace(" ", "")
            if len(ll) > 1 and ll[0] == '/' and ll[1] == '/': continue
            pos = ll.find('//')
            if pos != -1: ll = ll[0:pos]
            if len(ll): tt.append(ll.lower())
        all.append(tt)
    return all


def get_first_result(path, id, path_to_save_html_file):
    fpath = get_each_path(path)
    allfile = get_allfile(fpath)
    n = len(fpath)
    for i in range(n):
        for j in range(i + 1, n):
            f1 = allfile[i]
            f2 = allfile[j]
            flag = [0] * (len(f2) + 1)
            flag1 = [0] * (len(f1) + 1)
            sh = 0
            for r1,s1 in enumerate(f1):
                for r, s2 in enumerate(f2):
                    if flag[r] > 0 or flag1[r1] > 0: continue
                    n1 = len(s1)
                    n2 = len(s2)
                    dp = [[0] * (n2 + 1) for o in range(n1 + 1)]
                    for q in range(n1):
                        for w in range(n2):
                            dp[q + 1][w + 1] = (dp[q][w] + 1) if s1[q] == s2[w] else (max(dp[q][w + 1], dp[q + 1][w]))
                    if n1 + n2 > 0 and dp[n1][n2] * 2 / (n1 + n2) > 0.5:
                        tmp=dp[n1][n2]*2/(n1+n2+1e-6)*100
                        flag1[r1]=tmp;
                        flag[r] = tmp
                        sh += 1
            sim = sh * 2 / (len(f1) + len(f2) + 1e-5)*100
            fname = os.listdir(path)
            html1=open(path_to_save_html_file+'\\'+'%s.html'%(fname[i].split('.')[0] + '_' + fname[j].split('.')[0]+'__1'),'w+')
            html2=open(path_to_save_html_file+'\\'+'%s.html'%(fname[i].split('.')[0] + '_' + fname[j].split('.')[0]+'__2'),'w+')
            for r1,s1 in enumerate(f1):
                tt=""
                s1 = s1.replace('<', '&lt;')
                s1 = s1.replace('>', '&gt;')
                if s1 == '{' or s1 == '}' or s1 == '};':
                    tt = '<span style="background-color: write">' + s1 + '</span>'
                    html1.write(tt + '\n')
                    continue
                if flag1[r1]>85:
                    tt='<span style="background-color: red">'+s1+'</span>'
                elif flag1[r1]>70:
                    tt='<span style="background-color: yellow">'+s1+'</span>'
                elif flag1[r1]>55:
                    tt='<span style="background-color: greenyellow">'+s1+'</span>'
                else:
                    tt='<span style="background-color: write">'+s1+'</span>'
                html1.write(tt+'</br>'+'\n')
            for r,s1 in enumerate(f2):
                tt=""
                s1 = s1.replace('<', '&lt;')
                s1 = s1.replace('>', '&gt;')
                if s1 == '{' or s1 == '}' or s1 == '};':
                    tt = '<span style="background-color: write">' + s1 + '</span>'
                    html2.write(tt + '\n')
                    continue
                if flag[r]>85:
                    tt='<span style="background-color: red">'+s1+'</span>'
                elif flag[r]>70:
                    tt='<span style="background-color: yellow">'+s1+'</span>'
                elif flag[r]>55:
                    tt='<span style="background-color: greenyellow">'+s1+'</span>'
                else:
                    tt='<span style="background-color: white">'+s1+'</span>'
                html2.write(tt+'</br>'+'\n')
            html1.close()
            html2.close()
            check_result = CheckResult()
            check_result.check_id = id
            check_result.file1 = fpath[i].split('\\')[-1]
            check_result.file2 = fpath[j].split('\\')[-1]
            check_result.sim1 = sim
            check_result.save()