from sample_utils.MinioSampleSource import MinioSampleSource
from sample_utils.samples_lib import NLSampleLib
from sample_utils.SampleSet import DirectSet
import time

mss = MinioSampleSource("/Users/jiangke/Downloads/buffer", "192.168.2.10:31001", "datareader", "uo6HuW37ArEYu9",
                        "samplestore")

samplelib = NLSampleLib(mss)


# samplelib.import_data("caipan@01", [{'a': [x, x + 1], 'b': "ddd"} for x in range(1000)])


def trans_fff(item):
    return item


#samplelib.transform_to_new_set("fenlei-01", "trans1", "sdfsdfasfd", None, trans_fff)

all_data=mss.get_dir_list()

time.time()
