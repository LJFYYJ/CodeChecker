from django.conf import settings
from .models import CheckInfo, CheckResult, CheckInfoFile
from .check import first, second, pre_third, third, generate_html
import os
import datetime
import zipfile
import rarfile
import tarfile


class CheckCode:

    def __init__(self, username, rar_name):
        self.username = username
        self.rar_name = rar_name
        self.root_path = ''
        self.suffix = ['.cpp', '.c', '.txt']
        self.check_info = CheckInfo()
        self.check_info.username = username
        self.short_name = {}

    # 将解压后特定代码文件提取到查重文件夹下，删除空目录
    def listDir(self, root, add_name):
        dirpath = os.path.join(self.root_path, 'check_info')
        for file in os.listdir(root):
            path = os.path.join(root, file)
            if os.path.isfile(path):
                # 只处理特定几种类型的文件
                if os.path.splitext(file)[1] in self.suffix:
                    copy_file_path = os.path.join(dirpath, add_name + file)
                    self.short_name[copy_file_path.split('\\')[-1]] = path.split('\\')[-1]
                    open(copy_file_path, 'wb').write(open(path, 'rb').read())
                os.remove(path)
            elif os.path.isdir(path):
                self.listDir(path, add_name + path.split('\\')[-1] + '_')
        if os.path.exists(root):
            os.removedirs(root)

    # 解压压缩包以及提取文件
    def checkcode_init(self):
        # 创建本次查重文件夹
        time = str(datetime.datetime.now()).split('.')[0].replace(':', '-')
        self.root_path = '%s\%s\%s\%s' % (settings.MEDIA_ROOT, self.username, 'check', time)
        self.check_info.check_time = time
        self.check_info.save()
        # 将查重文件信息写入CheckInfoFile
        for file in self.rar_name:
            checkinfofile = CheckInfoFile()
            checkinfofile.check_id = self.check_info.id
            checkinfofile.filename = file
            checkinfofile.save()
        # 建立三个文件夹，分别存储 源文件 第三级预处理文件 html文件
        info_path = os.path.join(self.root_path, 'check_info')
        if not os.path.exists(info_path):
            os.makedirs(info_path)
        if not os.path.exists(os.path.join(self.root_path, 'check_medium')):
            os.makedirs(os.path.join(self.root_path, 'check_medium'))
        if not os.path.exists(os.path.join(self.root_path, 'check_result')):
            os.makedirs(os.path.join(self.root_path, 'check_result'))
        # 将所有文件全部复制到该文件夹下
        path = '%s\%s\%s' % (settings.MEDIA_ROOT, self.username, 'upload_file')
        for file in self.rar_name:
            file_old_path = os.path.join(path, file)
            file_new_path = os.path.join(info_path, file)
            open(file_new_path, 'wb').write(open(file_old_path, 'rb').read())
        # 将该文件夹下的所有压缩包解压，目前主要支持zip、rar格式
        for file in os.listdir(info_path):
            file_path = os.path.join(info_path, file)
            new_path = os.path.join(info_path, os.path.splitext(file)[0])
            # 如果是zip格式
            if os.path.splitext(file)[1] == '.zip':
                os.makedirs(new_path)
                zip_files = zipfile.ZipFile(file_path, 'r')
                for zip_file in zip_files.namelist():
                    zip_files.extract(zip_file, new_path)
                zip_files.close()
                os.remove(file_path)
            # 如果是rar格式
            if os.path.splitext(file)[1] == '.rar':
                os.makedirs(new_path)
                rar_files = rarfile.RarFile(file_path, 'r')
                for rar_file in rar_files.namelist():
                    rar_files.extract(rar_file, new_path)
                rar_files.close()
                os.remove(file_path)
            # 如果是tar格式
            # 问题：tar解压后中文文件名乱码
            if os.path.splitext(file)[1] == '.tar':
                os.makedirs(new_path)
                tar_files = tarfile.open(file_path, 'r')
                for tar_file in tar_files.getnames():
                    tar_files.extract(tar_file, new_path)
                tar_files.close()
                os.remove(file_path)
            # 如果是gz格式
            if os.path.splitext(file)[1] == '.gz':
                new_path = os.path.splitext(new_path)[0]
                os.makedirs(new_path)
                tar_files = tarfile.open(file_path, 'r:gz')
                for tar_file in tar_files.getnames():
                    tar_files.extract(tar_file, new_path)
                tar_files.close()
                os.remove(file_path)
        # 将解压后所有代码文件提取到查重文件夹下
        for file in os.listdir(info_path):
            file_path = os.path.join(info_path, file)
            if os.path.isdir(file_path):
                self.listDir(file_path, add_name=file + '_')


    def check(self):
        self.checkcode_init()
        info_path = os.path.join(self.root_path, 'check_info')
        save_path = os.path.join(self.root_path, 'check_medium')
        save_html_path = os.path.join(self.root_path, 'check_result')
        # 第一级查重
        first.get_first_result(info_path, self.check_info.id, save_html_path)
        print('first success')
        # 第二级查重
        second.get_second_result(info_path, self.check_info.id)
        print('second success')
        # 生成第三级查重向量
        pre_third.generate_vector(info_path, save_path)
        print('pre_third success')
        # 进行第三级查重
        result = third.nn(save_path + '\\final_vector.txt')
        print('third success')
        check_results = CheckResult.objects.filter(check_id=self.check_info.id)
        if len(check_results) != len(result):
            return
        for i in range(len(result)):
            check_results[i].sim3 = result[i]*100
            check_results[i].filename1 = self.short_name[check_results[i].file1]
            check_results[i].filename2 = self.short_name[check_results[i].file2]
            check_results[i].save()


class CheckDownload:


    def __init__(self):
        self.checkresults = []

    def download(self, infoid, username, checkresults):
        # 将所有需要的文件提取出来
        check_info = CheckInfo.objects.get(id=infoid)
        base_path = '%s\%s\%s\%s' % (settings.MEDIA_ROOT, username, 'check', check_info.check_time)
        new_path = '%s\%s' % (base_path, 'final_result')
        info_path = '%s\%s' % (base_path, 'check_info')
        result_path = '%s\%s' % (base_path, 'check_result')
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        j = 0
        for checkresult in checkresults:
            j = j + 1
            fileold1 = os.path.join(info_path, checkresult.file1)
            fileold2 = os.path.join(info_path, checkresult.file2)
            filenew1 = os.path.join(new_path, str(j) + '_' + checkresult.filename1)
            filenew2 = os.path.join(new_path, str(j) + '_' + checkresult.filename2)
            filehtml1 = '%s\%s' % (result_path, checkresult.file1.split('.')[0] + '_' + checkresult.file2.split('.')[0] + '__1.html')
            filehtml2 = '%s\%s' % (result_path, checkresult.file1.split('.')[0] + '_' + checkresult.file2.split('.')[0] + '__2.html')
            sim = str('%.1f' % checkresult.sim3)
            savename = str(j) + '__' + checkresult.filename1.split('.')[0] + '_' + checkresult.filename2.split('.')[0] + '.html'
            savename_path = os.path.join(new_path, savename)
            generate_html.generate_html(checkresult.filename1, sim, checkresult.filename2, open(filehtml1, 'r').read(), open(filehtml2, 'r').read(), savename_path)
            open(filenew1, 'w').write(open(fileold1, 'r').read())
            open(filenew2, 'w').write(open(fileold2, 'r').read())
        zipname = check_info.check_time + '.zip'
        zippath = os.path.join(base_path, zipname)
        zipp = zipfile.ZipFile(zippath, 'w', zipfile.ZIP_DEFLATED)
        files = os.listdir(new_path)
        for file in files:
            filepath = os.path.join(new_path, file)
            zipp.write(filepath, file)
        zipp.close()









