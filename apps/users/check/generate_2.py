from .second import get_each_path, get_allfile, get_cos, get_win

def gen_2(path,path_to_save):
    fpath = get_each_path(path)
    file1, file2 = get_allfile(fpath)
    sim_cos = get_cos(file1)
    sim_win = get_win(file2)
    n = len(file1)
    for i in range(n):
        for j in range(i + 1, n):
            sim_tot = (3 * sim_cos[i][j] + 1 * sim_win[i][j]) / 4
            f = open(path_to_save+ '\\' + '%s.txt' % (str(i + 1) + '_' + str(j + 1)), 'a+')
            f.write(str(sim_tot) + ' ')
            f.close()