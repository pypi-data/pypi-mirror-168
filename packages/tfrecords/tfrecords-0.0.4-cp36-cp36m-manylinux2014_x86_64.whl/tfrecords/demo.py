# -*- coding: utf-8 -*-
# @Time    : 2022/9/8 15:49
import tfrecords

options = tfrecords.TFRecordOptions(compression_type=tfrecords.TFRecordCompressionType.NONE)
def test_write(filename, N=3, context='aaa'):
    with tfrecords.TFRecordWriter(filename, options=options) as file_writer:
        for _ in range(N):
            # x, y = np.random.random(), np.random.random()
            file_writer.write(context + '____' + str(_))

def test_record_iterator():
    example_paths = tfrecords.glob('d:/example.tfrecords*')
    for example_path in example_paths:
        iterator = tfrecords.tf_record_iterator(example_path, options=options)
        num = 0
        for iter in iterator:
            num += 1
            print(iter)


def test_random_reader():
    example_paths = tfrecords.glob('d:/example.tfrecords*')
    for example_path in example_paths:
        file_reader = tfrecords.tf_record_random_reader(example_path, options=options)
        last_pos = 0
        while True:
            try:
                x,pos = file_reader.read(last_pos)
                print(x)
                last_pos = pos
            except:
                break

test_write('d:/example.tfrecords0',3,'file0')
test_write('d:/example.tfrecords1',10,'file1')
test_write('d:/example.tfrecords2',12,'file2')


print('\ntest_record_iterator')
test_record_iterator()

print('\ntest_random_reader')
test_random_reader()