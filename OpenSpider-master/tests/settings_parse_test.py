__author__ = 'zhangxa'


import unittest

import configparser

class SettingsTest(unittest.TestCase):
    def test_parse_config(self):
        config = configparser.ConfigParser()
        config.read('./settings.cfg')
        settings = {}
        driver_settings = {}
        settings['driver'] = config['QUEUE_DRIVER']['driver']
        driver_settings['host'] = config['DRIVER_SETTINGS']['host']
        driver_settings['port'] = config['DRIVER_SETTINGS']['port']
        driver_settings['db'] = int(config['DRIVER_SETTINGS']['db'])
        settings['driver_settings'] = driver_settings
        self.assertEqual(settings['driver'],'redis')
        self.assertEqual(settings['driver_settings']['host'],'localhost')
        self.assertEqual(settings['driver_settings']['port'],'6379')
        self.assertEqual(settings['driver_settings']['db'],1)

if __name__ == "__main__":
    unittest.main(warnings='ignore')

