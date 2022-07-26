from .first import get_each_path

KEY=['int','float','double','long long','void','bool','unsigned','short','short int','unsigned int','long long int',
     'unsigned long long','char']

def gen_910(path,path_to_save):
    fpath=get_each_path(path)
    d9 = []
    d8 = []
    n = len(fpath)
    for i in range(n):
        q9 = 0
        q8 = 0
        lines = open(fpath[i], encoding='utf-8').read().strip().split('\n')
        for l in lines:
            ll = l.replace(" ", "").lower()
            if len(ll) > 1 and ll[0] == '/' and ll[1] == '/': continue
            pos = ll.find('//')
            if pos != -1: ll = ll[0:pos]
            if len(ll) < 2: continue
            for i in KEY:
                pp = ll.find(i)
                if pp != -1:
                    pp = pp + len(i)
                    if pp + 2 < len(ll) and ll[pp + 1] == '(' and ll[pp + 2] == ')':
                        q9 = q9 + 1
                    else:
                        q8 = q8 + 1
                        for j in range(pp, len(ll)):
                            if ll[j] == ',':
                                q8 = q8 + 1
                            elif ll[j] == ';':
                                break
        d9.append(q9)
        d8.append(q8)
    for i in range(n):
        for j in range(i + 1, n):
            f = open(path_to_save + '\\'+ '%s.txt' % (str(i + 1) + '_' + str(j + 1)), 'a+')
            f1 = d8[i]
            f2 = d8[j]
            if f1 > f2: f1, f2 = f2, f1
            sim = f1 / (f2 + 1e-5)
            f.write(str(sim) + ' ')
            f1 = d9[i]
            f2 = d9[j]
            if f1 > f2: f1, f2 = f2, f1
            sim = f1 / (f2 + 1e-5)
            f.write(str(sim) + ' ')
            f.close()