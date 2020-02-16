from .models import Directories
from shutil import copytree, ignore_patterns, rmtree
import os

import paramiko
from stat import S_ISDIR
from fnmatch import fnmatch


class TasksClass():

    def __init__(self):
        self.tmp_backup_folder = '/tmp/baackup'
        self.sftp = None
        self.directory = None

    def sftp_walk(self, remotepath):
        path = remotepath
        files = []
        folders = []
        for f in self.sftp.listdir_attr(remotepath):
            if S_ISDIR(f.st_mode):
                folders.append(f.filename)
            else:
                files.append(f.filename)
        if files:
            yield path, files
        for folder in folders:
            new_path = os.path.join(remotepath, folder)
            for x in self.sftp_walk(new_path):
                yield x

    def is_ignored(self, check_dir):
        ignore = False
        ignore_dirs = self.directory.exclude_dirs.split(',')
        for ignore_dir in ignore_dirs:
            if fnmatch(check_dir, ignore_dir):
                ignore = True
        return ignore

    def backup_ssh(self, backup_location):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.directory.remote_url,
                    username=self.directory.remote_user,
                    password=self.directory.remote_pass,
                    timeout=3)
        self.sftp = ssh.open_sftp()

        for path, files in self.sftp_walk(self.directory.path):
            folder = path.replace(self.directory.path, '').lstrip('/')
            local_dir = os.path.join(backup_location, folder)
            # print('->', backup_location, folder, local_dir)
            if not self.is_ignored(folder):
                # print('makedir:', local_dir)
                os.makedirs(local_dir)
                for file in files:
                    if not self.is_ignored(file):
                        remote = os.path.join(os.path.join(path, file))
                        local = os.path.join(local_dir, file)
                        # print('\t', remote, local, file)
                        self.sftp.get(remote, local)
        self.sftp.close()

    def backup_local(self, backup_location):
        ignore_dirs = self.directory.exclude_dirs.split(',')
        copytree(self.directory.path,
                 backup_location,
                 ignore=ignore_patterns(*ignore_dirs))

    def backup(self):
        if os.path.isdir(self.tmp_backup_folder):
            rmtree(self.tmp_backup_folder)
        # if os.path.exists(tmp_out_targz):
        #     os.remove(tmp_out_targz)
        # if os.path.exists(out_gpg):
        #     os.remove(out_gpg)
        os.makedirs(self.tmp_backup_folder)

        for self.directory in Directories.objects.all():
            if self.directory.exists():
                backup_location = os.path.join(
                    self.tmp_backup_folder, self.directory.name)
                if self.directory.location == 'local':
                    self.backup_local(backup_location)
                if self.directory.location == 'remote':
                    self.backup_ssh(backup_location)
                size, unit = self.get_size(backup_location)
                # logging.info('%s: %s %s' % (self.directory.name, size, unit))
                print('  %s: %s %s' % (self.directory.name, size, unit))
        size, unit = self.get_size(self.tmp_backup_folder)
        print('ALL: %s %s' % (size, unit))

    def get_size(self, path):
        size = sum([sum(map(lambda fname: os.path.getsize(os.path.join(
            directory, fname)), files)) for directory, folders, files in os.walk(path)])
        # 2**10 = 1024
        power = 2**10
        n = 0
        Dic_powerN = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
        while size > power:
            size /= power
            n += 1
        size = round(size, 2)
        return size, Dic_powerN[n] + 'B'
