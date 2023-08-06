import abc, io, shutil
import os, pickle
from code_util.log import log_error


class NLSampleSourceBase(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create_new_set(self, name: str, description: str, tags: [str], keys: [str], base_set="",
                       base_set_process="") -> bool:
        pass

    @abc.abstractmethod
    def has_set(self, name: str) -> bool:
        pass

    @abc.abstractmethod
    def add_row(self, name: str, data: []) -> bool:
        pass

    @abc.abstractmethod
    def get_metadata_keys(self, name: str) -> {}:
        pass

    @abc.abstractmethod
    def get_dir_list(self) -> {}:
        pass

    @abc.abstractmethod
    def iter_data(self, name: str):
        pass

    @abc.abstractmethod
    def iter_pointer(self, name: str):
        pass

    @abc.abstractmethod
    def delete_set(self, name: str):
        pass

    @abc.abstractmethod
    def load_pointer_data(self, name: str, pointer):
        pass

    @abc.abstractmethod
    def get_set_count(self, name: str):
        pass

    @abc.abstractmethod
    def add_attachment(self, set_name: str, key, data):
        pass

    @abc.abstractmethod
    def read_attachment(self, set_name: str):
        pass

    def arrange_dir_list(self, dir_list: {}):
        new_dic = {}
        files_order_list = sorted([k for k in dir_list.keys()], key=lambda item: len(item.split('_')))
        key_pointers = {}
        for set_key in files_order_list:
            if dir_list[set_key]['meta']['base_set'] == "":
                new_dic[set_key] = {
                    'meta': dir_list[set_key]['meta'],
                    'children': {},
                    'count': dir_list[set_key]['count']
                }
                key_pointers[set_key] = new_dic[set_key]
            else:
                base_set_name = dir_list[set_key]['meta']['base_set']
                key_pointers[base_set_name]['children'][set_key] = {
                    'meta': dir_list[set_key]['meta'],
                    'children': {},
                    'count': dir_list[set_key]['count']
                }
                key_pointers[set_key] = key_pointers[base_set_name]['children'][set_key]

        if print:
            def printsub(level: int, name, item):
                blank_str = ""
                for _ in range(level):
                    blank_str += "\t"
                print(f"{blank_str} - {name}({item['count']}): {item['meta']['des']}")
                for sub_item in item['children'].keys():
                    printsub(level + 1, sub_item, item['children'][sub_item])

            for key in new_dic.keys():
                printsub(0, key, new_dic[key])

        return new_dic


class LocalDisk_NLSampleSource(NLSampleSourceBase):
    """
    Save on a Folder.
    File Format:
    """

    def get_dir_list(self) -> {}:
        sets = [file for file in os.listdir(self.base_folder) if not file.startswith('.')]
        sets_infos = {}
        for p_set in sets:
            base_f = self._try_get_file_obj(p_set)
            file_index, append_seek, data_start_seek, count, filecount, current_count = self._read_base_header(base_f)
            node = self._read_node(base_f)
            sets_infos[p_set] = {
                'meta': node,
                'count': count,
                'filecount': filecount
            }
        return sets_infos

    def __init__(self, folder_path):
        self.base_folder = folder_path
        self.int_size = 8
        self.shortint_size = 4
        self.pointer_size = self.int_size + self.shortint_size
        self.header_node_size = 5 * 1024
        self.file_size = 1024 * 1024 * 100
        self.file_pool = {}

        self.base_seek_dic = {
            'file_index': 0,
            'append_seek': self.int_size,
            'data_start_seek': self.int_size + self.pointer_size,
            'data_count': self.int_size * 2 + self.pointer_size,
            'file_count': self.int_size * 3 + self.pointer_size,
            'current_file_count': self.int_size * 4 + self.pointer_size,
        }

        self.linked_seek_dic = {
            'file_index': 0,
            'current_file_count': self.int_size,
            'data_start_seek': self.int_size * 2,
        }

    def _try_get_file_obj(self, name: str, file_index=0):
        set_name = name
        if file_index != 0:
            name = f"{name}__{file_index}"
        if name not in self.file_pool:
            self.file_pool[name] = open(os.path.join(self.base_folder, set_name, f"{name}.dlib"), 'rb+')

        return self.file_pool[name]

    def __del__(self):
        for name in self.file_pool.keys():
            self.file_pool[name].close()

    def flush(self):
        for name in self.file_pool.keys():
            self.file_pool[name].flush()

    def _read_int(self, f) -> int:
        return int.from_bytes(f.read(self.int_size), "big", signed=False)

    def _write_int(self, f, int_value: int):
        f.write(int_value.to_bytes(self.int_size, "big", signed=False))

    def _add_int_plusone(self, f, seekp):
        f.seek(seekp)
        v = self._read_int(f)
        v += 1
        f.seek(seekp)
        self._write_int(f, v)

    def _read_shortint(self, f) -> int:
        return int.from_bytes(f.read(self.shortint_size), "big", signed=False)

    def _write_shortint(self, f, int_value: int):
        f.write(int_value.to_bytes(self.shortint_size, "big", signed=False))

    def _read_pointer(self, f) -> (int, int):
        p = self._read_shortint(f)
        s = self._read_int(f)
        return (p, s)

    def _write_pointer(self, f, page: int, seek: int):
        self._write_shortint(f, page)
        self._write_int(f, seek)

    def _read_node(self, f):
        f_len = self._read_int(f)
        act_len = self._read_int(f)
        with io.BytesIO() as bf:
            bf.write(f.read(act_len))
            bf.seek(0)
            return pickle.load(bf)

    def _seek_to_node(self, f):
        o_loc = f.tell()
        f_len = self._read_int(f)
        act_len = self._read_int(f)
        c_loc = f.tell()
        f.seek(c_loc + act_len)
        return o_loc

    def _write_node(self, f, node, size=None):
        """
        Node format:  plan_size(int),Act_size(int), data
        :param f:
        :param node:
        :param size:
        :return:
        """
        with io.BytesIO() as bf:
            pickle.dump(node, bf)
            act_len = bf.tell()
            if size and act_len > size:
                log_error("超过Node限制")
            f_len = act_len if size is None else size
            bf.seek(0)
            self._write_int(f, f_len)
            self._write_int(f, act_len)
            f.write(bf.read(act_len))

    def _read_base_header(self, f):
        f.seek(0)
        file_index = self._read_int(f)
        append_seek = self._read_pointer(f)
        data_start_seek = self._read_int(f)
        count = self._read_int(f)
        file_count = self._read_int(f)
        current_file_count = self._read_int(f)
        # node = self._read_node(f)
        return file_index, append_seek, data_start_seek, count, file_count, current_file_count

    def _read_linked_header(self, f):
        f.seek(0)
        file_index = self._read_int(f)
        current_count = self._read_int(f)
        data_start_seek = self._read_int(f)

        return file_index, current_count, data_start_seek

    def load_pointer_data(self, name: str, pointer):
        file_index, start_seek_location = pointer
        c_f = self._try_get_file_obj(name, file_index)
        c_f.seek(start_seek_location)
        return self._read_node(c_f)

    def create_new_set(self, name: str, description: str, tags: [str], keys: [str],
                       base_set="", base_set_process="") -> bool:
        """
        header format:  file_index(int): 文件序号
                        append_seek(pointer): 添加新数据指针
                        data_start_seek(int): 本文件中数据的开始位置
                        data_count(int): 数据的个数
                        file_count(int): 文件链个数
                        current_file_count(int): 当前数据数量
                        header_node: 数据
        :param name:
        :param description:
        :param tags:
        :param label_keys:
        :return:
        """
        if '_' in name:
            log_error("set名中不能包含符号 '_' ")

        if base_set != "":
            name = f"{base_set}_{name}"

        os.mkdir(os.path.join(self.base_folder, name))
        with open(os.path.join(self.base_folder, name, f"{name}.dlib"), 'wb') as f:
            header = {
                'name': name,
                'des': description,
                'tags': tags,
                'label_keys': keys,
                'base_set': base_set,
                'base_set_process': base_set_process
            }
            self._write_int(f, 0)  # file_index
            start_seek = self.int_size * 5 + self.pointer_size + self.header_node_size
            self._write_pointer(f, 0, start_seek)  # append_seek
            self._write_int(f, start_seek)  # data_start_seek
            self._write_int(f, 0)  # data_count
            self._write_int(f, 1)  # file_count
            self._write_int(f, 0)  # current_file_count
            self._write_node(f, header, self.header_node_size)

        return True

    def has_set(self, name: str) -> bool:
        if os.path.exists(os.path.join(self.base_folder, name, f"{name}.dlib")):
            return True
        return False

    def add_row(self, name: str, data: []) -> bool:
        base_f = self._try_get_file_obj(name)
        file_index, append_seek, data_start_seek, count, filecount, current_count = self._read_base_header(base_f)

        f = self._try_get_file_obj(name, append_seek[0])

        f.seek(append_seek[1])
        self._write_node(f, data)
        new_append_seek = f.tell()
        new_append_page = append_seek[0]

        if new_append_seek > self.file_size:
            new_append_page += 1
            with open(os.path.join(self.base_folder, name, f"{name}__{new_append_page}.dlib"), 'wb') as f_new:
                self._write_int(f_new, new_append_page)
                self._write_int(f_new, 0)
                self._write_int(f_new, 3 * self.int_size)
                new_append_seek = f_new.tell()
            self._add_int_plusone(base_f, self.base_seek_dic['file_count'])  # file_count

        base_f.seek(self.base_seek_dic['append_seek'])
        self._write_pointer(base_f, new_append_page, new_append_seek)  # append_seek

        self._add_int_plusone(base_f, self.base_seek_dic['data_count'])  # data_count

        # updata current file count
        if append_seek[0] == 0:
            self._add_int_plusone(f, self.base_seek_dic['current_file_count'])
        else:
            self._add_int_plusone(f, self.linked_seek_dic['current_file_count'])

        return True

    def iter_data(self, name: str):
        base_f = self._try_get_file_obj(name)
        file_index, append_seek, data_start_seek, count, filecount, current_count = self._read_base_header(base_f)

        for file_index in range(filecount):
            c_f = self._try_get_file_obj(name, file_index)
            if file_index == 0:
                c_f.seek(self.base_seek_dic['current_file_count'])
            else:
                c_f.seek(self.linked_seek_dic['current_file_count'])
            count = self._read_int(c_f)

            if file_index == 0:
                c_f.seek(self.base_seek_dic['data_start_seek'])
            else:
                c_f.seek(self.linked_seek_dic['data_start_seek'])
            start_seek_location = self._read_int(c_f)
            c_f.seek(start_seek_location)
            for f_count in range(count):
                yield self._read_node(c_f)

    def iter_pointer(self, name: str):
        base_f = self._try_get_file_obj(name)
        file_index, append_seek, data_start_seek, count, filecount, current_count = self._read_base_header(base_f)

        for file_index in range(filecount):
            c_f = self._try_get_file_obj(name, file_index)
            if file_index == 0:
                c_f.seek(self.base_seek_dic['current_file_count'])
            else:
                c_f.seek(self.linked_seek_dic['current_file_count'])
            count = self._read_int(c_f)

            if file_index == 0:
                c_f.seek(self.base_seek_dic['data_start_seek'])
            else:
                c_f.seek(self.linked_seek_dic['data_start_seek'])
            start_seek_location = self._read_int(c_f)
            c_f.seek(start_seek_location)
            for f_count in range(count):
                yield file_index, self._seek_to_node(c_f)

    def get_set_count(self, name: str):
        base_f = self._try_get_file_obj(name)
        file_index, append_seek, data_start_seek, count, filecount, current_count = self._read_base_header(base_f)
        return count

    def get_metadata_keys(self, name: str) -> {}:
        base_f = self._try_get_file_obj(name)
        file_index, append_seek, data_start_seek, count, filecount, current_count = self._read_base_header(base_f)
        return self._read_node(base_f)

    def print_set_info(self, name: str):
        base_f = self._try_get_file_obj(name)
        v_count = 0
        file_index, append_seek, data_start_seek, count, filecount, current_count = self._read_base_header(base_f)
        print("*************************************************************** ")
        print(f"file_index(int):{file_index} \t append_seek:{append_seek[0]},{append_seek[1]} ")
        print(f"data_start_seek(int):{data_start_seek} \t count(int):{count} ")
        print(f"filecount(int):{filecount} \t current_count(int):{current_count} ")
        v_count += current_count
        for index in range(1, filecount):
            cn_f = self._try_get_file_obj(name, index)
            file_index, current_count, start_append_seek = self._read_linked_header(cn_f)
            v_count += current_count
            print("———————————————————————————————————————————————————————————————— ")
            print(
                f"file_index(int):{file_index} \t current_count:{current_count},start_append_seek : {start_append_seek} ")
        if v_count != count:
            print(f'Count_ERROR:{count}->{v_count}')
        print("*************************************************************** ")

    def delete_set(self, name: str):
        for kname in self.file_pool.keys():
            self.file_pool[kname].close()
        self.file_pool = {}
        shutil.rmtree(os.path.join(self.base_folder, name))

    def add_attachment(self, set_name: str, key, data):
        if not self.has_set(set_name):
            log_error("没有此set")

        attachment_file_path = os.path.join(self.base_folder, set_name, f"{set_name}.attch")
        if not os.path.exists(attachment_file_path):
            with open(attachment_file_path, 'wb') as f:
                self._write_int(f, 0)
                self._write_int(f, self.int_size * 2)

        with open(attachment_file_path, 'rb+') as f:
            count = self._read_int(f)
            start_loc = self._read_int(f)
            f.seek(start_loc)
            self._write_node(f, {'key': key, 'data': data})
            next_start = f.tell()
            f.seek(0)
            self._write_int(f, count + 1)
            self._write_int(f, next_start)

    def read_attachment(self, set_name: str):
        attachment_file_path = os.path.join(self.base_folder, set_name, f"{set_name}.attch")
        if not os.path.exists(attachment_file_path):
            log_error("此set没有附件")

        attach_dic = []
        with open(attachment_file_path, 'rb+') as f:
            count = self._read_int(f)
            start_loc = self._read_int(f)
            for _ in range(count):
                attach_dic.append(self._read_node(f))

        return attach_dic
