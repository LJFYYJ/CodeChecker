from .first import get_each_path, get_allfile
from .generate_2 import gen_2
from .generate_345678 import gen_345678
from .generate_910 import gen_910
import random

def generate_vector(path,path_to_save):
    fpath = get_each_path(path)
    allfile = get_allfile(fpath)
    n = len(fpath)
    for i in range(n):
        for j in range(i + 1, n):
            f1 = allfile[i]
            f2 = allfile[j]
            f = open(path_to_save + '\\'+'%s.txt' % (str(i + 1) + '_' + str(j + 1)), 'w+')
            flag = [0] * (len(f2) + 1)
            sh = 0
            for s1 in f1:
                for r, s2 in enumerate(f2):
                    if flag[r] == 1: continue
                    n1 = len(s1)
                    n2 = len(s2)
                    dp = [[0] * (n2 + 1) for o in range(n1 + 1)]
                    for q in range(n1):
                        for w in range(n2):
                            dp[q + 1][w + 1] = (dp[q][w] + 1) if s1[q] == s2[w] else (max(dp[q][w + 1], dp[q + 1][w]))
                    if n1 + n2 > 0 and dp[n1][n2] * 2 / (n1 + n2) > 0.5:
                        flag[r] = 1
                        sh += 1
            sim = sh * 2 / (len(f1) + len(f2) + 1e-5)
            f.write(str(sim) + ' ')
            f.close()

    gen_2(path, path_to_save)
    gen_345678(path, path_to_save)
    gen_910(path, path_to_save)

    fpath = get_each_path(path_to_save)
    n = len(fpath)
    final_path=path_to_save+'\\'+'final_vector.txt'
    f = open(final_path, 'a+')
    for i in range(n):
        line = open(fpath[i], encoding='utf-8').read()
        # l=line.split()
        # sim=float(l[0])
        # sim+=random.random()/10
        # if sim>1: sim-=0.1
        f.write(line +'\n')
    f.close()