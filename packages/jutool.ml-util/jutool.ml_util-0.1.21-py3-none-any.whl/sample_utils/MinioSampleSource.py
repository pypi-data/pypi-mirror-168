import io

from sample_utils.NLSampleSource import LocalDisk_NLSampleSource
from code_utils.log import log_error, log
import os, progressbar
from minio import Minio


class MinioSampleSource(LocalDisk_NLSampleSource):
    def __init__(self, folder_path, endpoint, access_key, secret_key, bucket_name):
        super().__init__(folder_path)
        self._folder_path = folder_path
        self._endpoint = endpoint
        self._access_key = access_key
        self._secret_key = secret_key
        self._bucket_name = bucket_name
        self._minio_client = None

    def _join(self, *args):
        args_list = [item for item in args]
        return "/".join(args_list)

    def _get_minio_client(self):
        if self._minio_client is None:
            self._minio_client = Minio(self._endpoint, self._access_key, self._secret_key, secure=False)
            if not self._minio_client.bucket_exists(self._bucket_name):
                log_error("此bucket不存在")
        return self._minio_client

    def _download_if_not_exsited(self, name: str):
        if super().has_set(name):
            return
        client = self._get_minio_client()
        all_sets = {obj.object_name.strip('/') for obj in client.list_objects(self._bucket_name)}
        if name in all_sets:
            log(f"Download the set {name} ...")
            os.mkdir(os.path.join(self.base_folder, name))
            all_set_files = list(client.list_objects(self._bucket_name, prefix=f"{name}/"))
            for remote_f in progressbar.progressbar(all_set_files):
                file_name = os.path.split(remote_f.object_name)[-1]
                client.fget_object(self._bucket_name, remote_f.object_name,
                                   os.path.join(self.base_folder, name, file_name))
        else:
            log_error("没有此set")

    def _object_exsited(self, name):
        try:
            client = self._get_minio_client()
            client.stat_object(self._bucket_name, name)
            return True
        except:
            return False

    def update(self, set_name=None):
        super().flush()
        client = self._get_minio_client()
        if set_name is not None:
            local_sets = [set_name]
        else:
            local_sets = super().get_dir_list()

        # comput count
        totle_count = 0
        for set in local_sets:
            for file in [f for f in os.listdir(os.path.join(self._folder_path, set)) if not f.startswith('.')]:
                totle_count += 1

        pb = progressbar.ProgressBar(0, max_value=totle_count, redirect_stdout=True)
        for set in local_sets:
            log(f"Upload set '{set}' \n")
            for file in [f for f in os.listdir(os.path.join(self._folder_path, set)) if not f.startswith('.')]:
                f_l_path = os.path.join(self._folder_path, set, file)
                o_path = self._join(set, file)
                if not self._object_exsited(o_path):
                    client.fput_object(self._bucket_name, o_path, f_l_path)
                else:
                    remote_data = client.get_object(self._bucket_name, o_path, 0, 160).data
                    remote_info = client.stat_object(self._bucket_name, o_path)
                    with open(f_l_path, 'rb') as f_obj:
                        fobj_data = f_obj.read(160)
                    local_size = os.path.getsize(f_l_path)
                    if (remote_data != fobj_data) and (remote_info.size == local_size):
                        client.fput_object(self._bucket_name, o_path, f_l_path)

                pb.update(pb.value + 1)

    def create_new_set(self, name: str, description: str, tags: [str], keys: [str], base_set="",
                       base_set_process="") -> bool:
        if self.has_set(name):
            log_error("已存在同名的set")
        return super().create_new_set(name, description, tags, keys, base_set=base_set,
                                      base_set_process=base_set_process)

    def has_set(self, name: str) -> bool:
        if super().has_set(name):
            return True
        client = self._get_minio_client()
        all_sets = {obj.object_name: obj.is_dir for obj in client.list_objects(self._bucket_name)}
        if name in all_sets:
            return True
        return False

    def add_row(self, name: str, data) -> bool:
        self._download_if_not_exsited(name)
        return super().add_row(name, data)

    def get_metadata_keys(self, name: str) -> {}:
        self._download_if_not_exsited(name)
        return super().get_metadata_keys(name)

    def iter_data(self, name: str):
        self._download_if_not_exsited(name)
        return super().iter_data(name)

    def get_remote_dir_list(self) -> {}:
        client = self._get_minio_client()
        sets = [obj.object_name.strip('/') for obj in client.list_objects(self._bucket_name)]
        sets_infos = {}
        start_seek = self.int_size * 5 + self.pointer_size + self.header_node_size
        for p_set in sets:
            with io.BytesIO() as ib:
                o_path = f"{p_set}/{p_set}.dlib"
                remote_data = client.get_object(self._bucket_name, o_path, 0, start_seek).data
                ib.write(remote_data)
                ib.seek(0)
                file_index, append_seek, data_start_seek, count, filecount, current_count = self._read_base_header(
                    ib)
                node = self._read_node(ib)
                sets_infos[p_set] = {
                    'meta': node,
                    'count': count,
                    'filecount': filecount
                }
        return sets_infos
