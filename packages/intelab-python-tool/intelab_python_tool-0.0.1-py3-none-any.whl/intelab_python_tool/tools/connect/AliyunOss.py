
import os
import oss2


class ALiYunOss:

    def __init__(self, oss_config: dict):
        """
        初始化配置并建立连接
        使用方式如下：

        from intelab_python_tool.tools.connect.AliyunOss import ALiYunOss as oss

        oss.upload_file()
        oss.isurl()
        oss.download_file()
        oss.batch_delete_files()

        :param oss_config:
        """
        self.config = oss_config
        self.region = self.config.get('region', 'hangzhou')
        self.local_endpoint = self.config.get('endpoint', f'https://oss-cn-{self.region}.aliyuncs.com')
        self.bucket = oss2.Bucket(oss2.Auth(self.config['access_key_id'], self.config['access_key_secret']),
                                  self.local_endpoint, self.config['bucket_name'])

    def upload_file(self, origin_file, local_file) -> any:
        """
        上传文件至oss
        :param origin_file:
        :param local_file:
        :return:
        """
        url_base = self.config.get('internal',
                                   f'https://{self.config["bucket_name"]}.oss-cn-{self.region}.aliyuncs.com/')
        result = self.bucket.put_object_from_file(origin_file, local_file)

        if result.status == 200:
            origin_file_url = os.path.join(url_base, origin_file)
        else:
            origin_file_url = ''
        return origin_file_url

    def isurl(self, origin_file):
        """
        check 文件是否存在oss中
        :param origin_file:
        :return:
        """
        file_url = self.bucket.sign_url('GET', origin_file, 10)
        return True if file_url else None

    def download_file(self, origin_file, local_file):
        """
        下载阿里云文件至本地
        :param local_file:
        :param origin_file:
        :return:
        """
        if origin_file.startswith('http://') or origin_file.startswith('https://'):
            origin_file = origin_file.split('/', 3)[-1]

        self.bucket.get_object_to_file(origin_file, local_file)
        return local_file

    def batch_delete_files(self, files_list):
        """单个或批量删除云端文件"""
        bucket_files = []
        for origin_file in files_list:
            if origin_file.startswith('http://') or origin_file.startswith('https://'):
                bucket_files.append(origin_file.split('/', 3)[-1])
            else:
                bucket_files.append(origin_file)

        result = self.bucket.batch_delete_objects(bucket_files)
        return result.deleted_keys
