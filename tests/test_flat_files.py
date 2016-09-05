import unittest

from nxtool.log_providers import flat_file
from nxtool.whitelists_generators import cookies, images_1002


class TestParseLog(unittest.TestCase):
    def test_show_stats(self):
        parser = flat_file.FlatFile()
        parser.get_statistics()

    def test_generate_whitelist_cookies(self):
        parser = flat_file.FlatFile('./tests/data/cookies.txt')
        parser.get_relevant_ids = lambda x:  [42000227]
        self.assertEqual(cookies.generate_whitelist(parser, []), [{'wl': [42000227], 'mz':['$HEADERS_VAR:cookie'], 'msg': 'Cookies'}])
        self.assertEqual(cookies.generate_whitelist(parser, [{'wl': [42000227]}]), [])

    def test_generate_whitelist_images(self):
        parser = flat_file.FlatFile('./tests/data/images_1002.txt')
        self.assertEqual(
            images_1002.generate_whitelist(parser, []),
            [{'mz': ['$URL_X:^/phpMyAdmin-2.8.2/scripts/setup.php|URL'], 'wl': [1002], 'msg': 'Images size (0x)'}]
        )
        self.assertEqual(images_1002.generate_whitelist(parser, [{'wl': [1002]}]), [])


class TestFiltering(unittest.TestCase):
    def test_filter_str(self):
        parser = flat_file.FlatFile('./tests/data/cookies.txt')
        self.assertEquals([i for i in parser.get_results()][0], {'block': '0',
           'cscore0': '$UWA', 'id0': '42000227', 'ip': 'X.X.X.X', 'learning': '0', 'score0': '8',
           'server': 'Y.Y.Y.Y', 'total_blocked': '204', 'total_processed': '472',
           'uri': '/phpMyAdmin-2.8.2/scripts/setup.php', 'var_name0': 'cookie', 'vers': '0.52', 'zone0': 'HEADERS'}
        )

    def test_filter_list(self):
        parser = flat_file.FlatFile('./tests/data/cookies.txt')
        parser.add_filters({'ip': ['X.X.X.X', 'A.A.A.A']})
        self.assertEquals([i for i in parser.get_results()], [{'block': '0',
           'cscore0': '$UWA', 'id0': '42000227', 'ip': 'X.X.X.X', 'learning': '0', 'score0': '8',
           'server': 'Y.Y.Y.Y', 'total_blocked': '204', 'total_processed': '472',
           'uri': '/phpMyAdmin-2.8.2/scripts/setup.php', 'var_name0': 'cookie', 'vers': '0.52', 'zone0': 'HEADERS'}])

        parser = flat_file.FlatFile('./tests/data/cookies.txt')
        parser.add_filters({'ip': ['A.A.A.A']})
        self.assertEquals([i for i in parser.get_results()], [])

        parser = flat_file.FlatFile('./tests/data/cookies.txt')
        parser.add_filters({'ip': ['X.X.X.X']}, negative=True)
        self.assertEquals([i for i in parser.get_results()], [])