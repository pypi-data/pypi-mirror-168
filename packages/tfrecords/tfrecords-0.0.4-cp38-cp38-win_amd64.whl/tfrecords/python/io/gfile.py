# @Time    : 2022/9/21 19:48
# @Author  : tk
# @FileName: gfile.py

from tfrecords.python.io.file_io import copy_v2 as copy
from tfrecords.python.io.file_io import create_dir_v2 as mkdir
from tfrecords.python.io.file_io import delete_file_v2 as remove
from tfrecords.python.io.file_io import delete_recursively_v2 as rmtree
from tfrecords.python.io.file_io import file_exists_v2 as exists
from tfrecords.python.io.file_io import get_matching_files_v2 as glob
from tfrecords.python.io.file_io import get_registered_schemes
from tfrecords.python.io.file_io import is_directory_v2 as isdir
from tfrecords.python.io.file_io import join
from tfrecords.python.io.file_io import list_directory_v2 as listdir
from tfrecords.python.io.file_io import recursive_create_dir_v2 as makedirs
from tfrecords.python.io.file_io import rename_v2 as rename
from tfrecords.python.io.file_io import stat_v2 as stat
from tfrecords.python.io.file_io import walk_v2 as walk
