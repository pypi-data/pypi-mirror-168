import shutil
import unittest
import pyutils.fsext as fs
import os


class TestFsext(unittest.TestCase):
    def test_to_base64(self):
        cwd = os.getcwd()
        if not cwd.endswith('tests'):
            os.chdir('tests')
        self.assertEqual(fs.to_base64('abs'), '')
        self.assertNotEqual(fs.to_base64('./data/to_base64.png'), '')
        output_dir = './output'
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        os.makedirs(output_dir)
        output_file = os.path.join(output_dir, 'to_base64')
        content = fs.to_base64('./data/to_base64.png', output_file)
        with open(output_file, 'r+', encoding='utf-8') as f:
            self.assertEqual(f.readline(), content)

    def test_convert_encoding(self):
        test_root_dir = os.path.dirname(__file__)
        with open(os.path.join(test_root_dir, 'data/test_convert_encoding'), 'rb') as f:
            test_convert_encoding = f.read()
        gbk_encoding_source_path = os.path.join(test_root_dir, "data/gbk_encoding")
        test_gbk_encoding_path = os.path.join(os.path.dirname(gbk_encoding_source_path), 'test_gbk_encoding')
        shutil.copyfile(gbk_encoding_source_path, test_gbk_encoding_path)
        with open(test_gbk_encoding_path, 'rb') as f:
            gbk_encoding = f.read()
        self.assertNotEqual(gbk_encoding, test_convert_encoding)
        fs.convert_encoding(test_gbk_encoding_path)
        with open(test_gbk_encoding_path, 'rb') as f:
            gbk_encoding = f.read()
        self.assertEqual(gbk_encoding, test_convert_encoding)
