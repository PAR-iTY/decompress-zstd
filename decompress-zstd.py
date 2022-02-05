#! /usr/bin/env python3

#==========================================================================================#

import io
import tarfile
from pathlib import PurePosixPath

import zstandard as zstd
import fire

#==========================================================================================#


def init(in_file="./test/gcc.tar.zst", out_file="./test/gcc.tar", mode="stream"):
    # CLI args default to test gcc file if unspecified

    # define out_file using in_file
    out_file = PurePosixPath(in_file).parents[0] / PurePosixPath(in_file).stem

    # instantiate zstd decompressor
    dctx = zstd.ZstdDecompressor()

    # map stream / sync / tar-wrapper functions
    funcs = {
        'stream': decompress_zstd_stream,
        'sync': decompress_zstd_sync,
        'tar': decompress_zstd_sync_tar_wrap
    }

    # run the specified or default function
    funcs[mode](in_file, out_file, dctx)

#==========================================================================================#

# copies decompressed zstd stream to new file in chunks - works on any file size


def decompress_zstd_stream(in_file, out_file, decompressor):

    with open(in_file, 'rb') as input, open(out_file, 'wb') as output:

        print(
            f"stream copying {PurePosixPath(in_file).suffix[1:]} data to {PurePosixPath(out_file).suffix[1:]} file..")

        decompressor.copy_stream(input, output)

        print('..done')


#==========================================================================================#

# write tar bytes directly to new file - eliminates tarfile library approach
# will choke on large files due to reading whole file into memory up front


def decompress_zstd_sync(in_file, out_file, decompressor):

    with zstd.open(in_file, mode='rb', dctx=decompressor) as input, open(out_file, mode='wb') as output:

        print(
            f"decompressing {PurePosixPath(in_file).suffix[1:]} file into bytes..")

        # read all byte data from zstd decompressor
        data = input.read()

        print(
            f"writing {str(len(data))} bytes to {PurePosixPath(out_file).suffix[1:]} file..")

        # write all decompressed byte data to out file
        output.write(data)

        print('..done')


#==========================================================================================#

# if the data within zstd is not tar, unpack zstd data into a newly created tar file

# this approach uses tarfile library to write an in-memory tarfile to disk
# ensures headers and data make sense etc but is unnecessary for GCC use-case


def decompress_zstd_sync_tar_wrap(in_file, out_file, decompressor):

    with zstd.open(in_file, mode='rb', dctx=decompressor) as input, tarfile.open(name=out_file, mode='w') as output:

        print(
            f"opening {PurePosixPath(in_file).suffix[1:]} file for decompression..")
        # read data from decompressor
        data = input.read()

        # get decompressed data as a byte-stream
        # (tarfile's preference for writing in-memory tar data to file)
        # from: https://bugs.python.org/issue22208
        # this link also suggests learning about gettarinfo() usage
        io_bytes = io.BytesIO(initial_bytes=data)

        # print(f"input byte-stream: {io_bytes}")

        # create a TarInfo file to tell tarfile how to use the byte-stream
        # out_file is pathlib object, tarfile needs a string for name
        tar_info = tarfile.TarInfo(name=f"{out_file}")
        # [IMPORTANT] it is crucial to give a size to get a correct header
        tar_info.size = len(data)

        print(
            f"writing {str(tar_info.size)} bytes to {PurePosixPath(out_file).suffix[1:]} file..")

        # add tar file metadata and byte-stream objects and write to ouput
        output.addfile(tar_info, fileobj=io_bytes)

        print('..done')


#==========================================================================================#


if __name__ == '__main__':
    fire.Fire(init)

#==========================================================================================#

# import tokenize
# import shutil

# add encodings:
# tar    MIME type='application/x-tar'
# zstd   MIME type='application/zstd'

# encoding hack: add encoding='cp437'
# from: https://stackoverflow.com/a/58771838

# catch-all windows encoding='cp437'
# zst opened in text mode: <_io.TextIOWrapper encoding='cp1252'>

# diff approach solve windows cp1252 issues by:
# encoding='ascii', errors='surrogateescape'
# errors='backslashreplace' is even more tolerant

# shutil approach didnt work, needs diff string/byte encoding
# shutil.unpack_archive(data, './shutil-out/')

# try auto-detect
# with tokenize.open(in_file) as t:
#     print(t)

# with open(in_file, 'rb') as f:
#     tokens = tokenize.tokenize(f.readline)
#     for token in tokens:
#         print(token)

#==========================================================================================#
