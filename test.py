import unittest
import Ska.ParseCM
import glob

class Tests(unittest.TestCase):
    def test_05_read_backstop(self):
        bs = Ska.ParseCM.read_backstop('/data/mpcrit1/mplogs/2009/FEB0209/oflsa/CR032_1103.backstop')
        self.assertEqual(len(bs), 2090)
        self.assertEqual(bs[3]['params']['TLMSID'], 'AONMMODE')

    def test_10_read_2008_backstops(self):
        for bsfile in glob.glob('/data/mpcrit1/mplogs/2008/*/ofls/*.backstop'):
            bs = Ska.ParseCM.read_backstop(bsfile)
            self.assertEqual(len(bs), len(open(bsfile).readlines()))

    def test_15_read_mm(self):
        mms = Ska.ParseCM.read_mm('/data/mpcrit1/mplogs/2009/MAR0209/oflsc/mps/mm059_2310.sum')
        self.assertEqual(mms[0]['initial']['obsid'], '10870')

    def test_20_read_2008_mms(self):
        for mmfile in glob.glob('/data/mpcrit1/mplogs/2008/*/ofls/mps/mm*.sum'):
            mms = Ska.ParseCM.read_mm(mmfile)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(Tests)
    unittest.TextTestRunner(verbosity=2).run(suite)
