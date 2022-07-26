import re
from .first import get_each_path

def gen_345678(path,path_to_save):
    fpath=get_each_path(path)
    allfile = []
    n = len(fpath)
    d3 = []
    d4 = []
    d5 = []
    d6 = []
    d7 = []
    d8 = []
    for i in range(n):
        tt = []
        lines = open(fpath[i], encoding='utf-8').read().strip().split('\n')
        d3.append(len(lines))
        q5 = 0
        q6 = 0
        co = 0
        q8 = 0
        for l in lines:
            up = len(l)
            for i in range(up):
                if l[i] == ' ':
                    co = co + 1
                else:
                    break
            ll = l.replace(" ", "")
            if len(ll) > 1 and ll[0] == '/' and ll[1] == '/': continue
            q6 = q6 + len(re.findall('for', ll))
            q6 = q6 + len(re.findall('while', ll))
            q8 = q8 + len(re.findall('if', ll))
            q8 = q8 + len(re.findall('else', ll))
            pos = ll.find('//')
            if pos != -1:
                ll = ll[0:pos]
                q5 = q5 + 1
            if len(ll): tt.append(ll.lower())
        q4 = abs(len(lines) - q5)
        d4.append(q4)
        d5.append(q5)
        d6.append(q6)
        d7.append(co / (len(lines) + 1e-5))
        d8.append(q8)
        allfile.append(tt)
    for i in range(n):
        for j in range(i + 1, n):
            f = open(path_to_save+ '\\' + '%s.txt' % (str(i + 1) + '_' + str(j + 1)), 'a+')
            f1 = d3[i]
            f2 = d3[j]
            if f1 > f2: f1, f2 = f2, f1
            sim = f1 / (f2 + 1e-5)
            f.write(str(sim) + ' ')

            f1 = d4[i]
            f2 = d4[j]
            if f1 > f2: f1, f2 = f2, f1
            sim = f1 / (f2 + 1e-5)
            f.write(str(sim) + ' ')

            f1 = d5[i]
            f2 = d5[j]
            if f1 > f2: f1, f2 = f2, f1
            sim = f1 / (f2 + 1e-5)
            f.write(str(sim) + ' ')

            f1 = d6[i]
            f2 = d6[j]
            if f1 > f2: f1, f2 = f2, f1
            sim = f1 / (f2 + 1e-5)
            f.write(str(sim) + ' ')

            f1 = d7[i]
            f2 = d7[j]
            if f1 > f2: f1, f2 = f2, f1
            sim = f1 / (f2 + 1e-5)
            f.write(str(sim) + ' ')

            f1 = d8[i]
            f2 = d8[j]
            if f1 > f2: f1, f2 = f2, f1
            sim = f1 / (f2 + 1e-5)
            f.write(str(sim) + ' ')
            f.close()
