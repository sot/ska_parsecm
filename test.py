import os
import unittest
import ska_parsecm
import glob

SKA = os.environ['SKA']

class Tests(unittest.TestCase):
    def test_05_read_backstop(self):
        bs = ska_parsecm.read_backstop(f'{SKA}/data/mpcrit1/mplogs/2009/FEB0209/oflsa/CR032_1103.backstop')
        self.assertEqual(len(bs), 2090)
        self.assertEqual(bs[3]['params']['TLMSID'], 'AONMMODE')

    def test_10_read_2008_backstops(self):
        for bsfile in glob.glob(f'{SKA}/data/mpcrit1/mplogs/2008/*/ofls/*.backstop'):
            bs = ska_parsecm.read_backstop(bsfile)
            self.assertEqual(len(bs), len(open(bsfile).readlines()))

    def test_15_read_mm(self):
        mms = ska_parsecm.read_mm(f'{SKA}/data/mpcrit1/mplogs/2009/MAR0209/oflsc/mps/mm059_2310.sum')
        self.assertEqual(mms[0]['initial']['obsid'], 10870)

    def test_20_read_2008_mms(self):
        for mmfile in glob.glob(f'{SKA}/data/mpcrit1/mplogs/2008/*/ofls/mps/mm*.sum'):
            mms = ska_parsecm.read_mm(mmfile)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(Tests)
    unittest.TextTestRunner(verbosity=2).run(suite)
