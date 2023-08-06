import codecs
import ctypes
import fnmatch
import glob
import os
import shutil
import base64
import charade

import pyutils.shorthand as shd
import pyutils.simplelogger as logger
########################
########################
#    文件系统扩展方法    #
########################
########################


def detect_encoding(input):
    """
    猜测 bytes | str 的编码

    Args:
        input (str | bytes): 待猜测的内容
    """
    try:
        # check it in the charade list
        if isinstance(input, str):
            return charade.detect(input.encode())
        # detecting the string
        else:
            return charade.detect(input)
    # in case of error
    # encode with 'utf -8' encoding
    except UnicodeDecodeError:
        return charade.detect(input.encode('utf-8'))


def convert_encoding(file_path, target_encoding='utf-8'):
    """converting the target file encoding.

    Args:
        file_path (str): target file path
        target_encoding (str, optional): target encoding to convert. Defaults to 'utf-8'.
    """
    if not os.path.exists(file_path) or os.path.isdir(file_path):
        print(f"{file_path} isn't a valid path to specific file.")
        return
    try:
        with open(file_path, 'rb') as f_in:
            raw_content = f_in.read()
        detect_result = detect_encoding(raw_content)
        if detect_result['confidence'] < 0.9:
            logger.warning("detect_result confidence less than 0.9,"
                           f"You should confirm than transform encoding of the file {file_path} manually.")
            return
        if detect_result['encoding'] != target_encoding:
            logger.info(f'{file_path} processed with detect_result {detect_result}.')
            with codecs.open(file_path, 'r',
                             encoding=detect_result['encoding']) as f_in:
                content = f_in.read()
            with codecs.open(file_path, 'w', encoding=target_encoding) as f_out:
                f_out.write(content)
    except IOError as err:
        logger.error(f"I/O error: {err}")


def search(pattern: str, validator=None, params={}):
    """按指定路径模式搜索单路径，可以添加自定义验证函数来过滤匹配的路径

    Args:
        pattern (str): 路径匹配模式，在 windows 下会自动搜索所有盘符
        validator (function, optional): 自定义验证函数，回调参数为匹配的路径和 params. Defaults to None.
        params (dict, optional): 自定义验证函数的剩余回调参数. Defaults to {}.

    Returns:
        str | None: 搜索到的路径，未搜索到则返回 None
    """
    def glob_wrap(path):
        logger.info('=> Searching at {}'.format(path), False)
        result = glob.glob(path, recursive=True)
        if len(result) > 0:
            for find_path in result:
                if validator is None or validator(find_path, **params):
                    return find_path
    if shd.is_win():
        volumes = get_all_volumes_win()
        for volume in volumes:
            search_path = os.path.join(volume, pattern)
            result = glob_wrap(search_path)
            if result is not None:
                return result
    else:
        return glob_wrap(pattern)


def copy_files(target_path, src_file_list, logs=False):
    """复制并覆盖目标路径下所有同名内容，如果 src_file 是文件夹，使用 shutil.copytree 复制，否则使用 shutil.copy2

    Args:
        target_path (str): 目标路径
        src_file_list (list): 被复制的文件列表
    """
    for src_file in src_file_list:
        if os.path.exists(src_file):
            src_basename = os.path.basename(src_file)
            deploy_file_path = os.path.join(target_path, src_basename)
            deploy_dir = os.path.dirname(deploy_file_path)
            if not os.path.exists(deploy_dir):
                os.makedirs(deploy_dir)
                if logs:
                    logger.info('Makedirs => {}'.format(deploy_dir))
            if os.path.isfile(deploy_file_path):
                os.remove(deploy_file_path)
                if logs:
                    logger.info('Removed => {}'.format(deploy_file_path))
            if os.path.isfile(src_file):
                shutil.copy2(src_file, deploy_file_path)
            else:
                shutil.copytree(src_file, deploy_file_path)
            if logs:
                logger.info('Copy file from {} to => {}'.format(src_file, deploy_file_path))


def read_file(file, decode='utf-8'):
    if os.path.isfile(file):
        content = ''
        with open(file, 'rb') as fo:
            content = fo.read()
        content = content.decode(decode)
        return content
    else:
        logger.error('{} is not found or is not a file'.format(file))


def get_all_volumes_win():
    if shd.is_win():
        lp_buffer = ctypes.create_string_buffer(78)
        ctypes.windll.kernel32.GetLogicalDriveStringsA(
            ctypes.sizeof(lp_buffer), lp_buffer)
        all_volumes = lp_buffer.raw.split(b'\x00')
        legal_volumes = []
        for vol in all_volumes:
            s = str(vol, encoding='utf-8')
            if os.path.isdir(s):
                legal_volumes.append(s)
        return legal_volumes


def get_files(work_dir, include_patterns=None, ignore_patterns=None, follow_links=False, recursive=True, apply_ignore_when_conflick=True):
    """
    NOTE:这里的 patterns 用的是 UNIX 通配符，而非语言正则表达式
    TODO: replace with glob.glob
    """
    if os.path.isfile(work_dir):
        result = [work_dir]
    else:
        result = []
        walk_result = os.walk(work_dir, followlinks=follow_links)
        if not recursive:
            try:
                walk_result = [next(walk_result)]
            except Exception:
                walk_result = None
        if walk_result is not None:
            for dirpath, _, filenames in walk_result:
                for filename in filenames:
                    full_path = os.path.join(dirpath, filename)
                    valid = True
                    if ignore_patterns is not None:
                        for ignore_pattern in ignore_patterns:
                            match_result = fnmatch.fnmatch(full_path, ignore_pattern)
                            valid = valid and not match_result
                            if not valid:
                                break
                    if include_patterns is not None:
                        for include_pattern in include_patterns:
                            match_result = fnmatch.fnmatch(full_path, include_pattern)
                            if apply_ignore_when_conflick:
                                valid = match_result and valid
                            else:
                                valid = match_result or valid
                            if valid:
                                break
                    if valid:
                        result.append(full_path)
    return sorted(result)


def to_base64(src, tar=None):
    """将 src 路径指定文件转为 base64 并返回，如果提供了 tar 目标文件路径，则将返回值同时存储在 tar 目标文件

    Args:
        src (str): 源文件路径
        tar (str): 目标文件路径
    """
    if not os.path.isfile(src):
        logger.warning(f'{src} is not a file path.')
        return ''
    filename = os.path.split(src)[1]
    ext = os.path.splitext(src)[1][1:]
    with open(src, 'rb') as f_img:
        base64_out = base64.b64encode(f_img.read())
    content = f"{filename} = [img]:data:image/{ext};base64,{base64_out.decode('utf-8')}\n"
    if tar is not None:
        if os.path.exists(tar):
            logger.warning(f'{tar} is not a file or target file exist.')
            return content
        with open(tar, 'w+', encoding='utf-8') as f:
            f.write(content)
    return content
