####################################################################################################
# 
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
# 
####################################################################################################

####################################################################################################

import unittest

####################################################################################################

from PyGeoPortail.Tools.RevisionVersion import RevisionVersion
            
####################################################################################################

class TestRevisionVersion(unittest.TestCase):

    ##############################################

    def __init__(self, method_name):

        super(TestRevisionVersion, self).__init__(method_name)

    ##############################################
        
    def test(self):

        v0_str = 'v3.2.1'
        v0_tuple = (3, 2, 1)

        self.assertEqual(RevisionVersion(v0_str), RevisionVersion(v0_tuple))
        self.assertEqual(str(RevisionVersion(v0_str)), v0_str)

        self.assertTrue(RevisionVersion('v3.2.1') > RevisionVersion('v2.3.2'))
        self.assertTrue(RevisionVersion('v3.2.1') > RevisionVersion('v3.1.2'))
        self.assertTrue(RevisionVersion('v3.2.1') > RevisionVersion('v3.2.0'))

        self.assertTrue(RevisionVersion('v3.2.1') >= RevisionVersion('v2.3.2'))
        self.assertTrue(RevisionVersion('v3.2.1') >= RevisionVersion('v3.2.1'))
        self.assertTrue(RevisionVersion('v3.2.1') >= RevisionVersion('v3.1.2'))
        self.assertTrue(RevisionVersion('v3.2.1') >= RevisionVersion('v3.2.0'))
        self.assertFalse(RevisionVersion('v3.2.0') >= RevisionVersion('v3.2.1'))
        self.assertFalse(RevisionVersion('v3.2.1') >= RevisionVersion('v3.3.0'))

        self.assertTrue(RevisionVersion('v2.3.2') < RevisionVersion('v3.2.1'))
        self.assertTrue(RevisionVersion('v3.1.2') < RevisionVersion('v3.2.1'))
        self.assertTrue(RevisionVersion('v3.2.0') < RevisionVersion('v3.2.1'))

        self.assertTrue(RevisionVersion('v2.3.2') <= RevisionVersion('v3.2.1'))
        self.assertTrue(RevisionVersion('v3.2.1') <= RevisionVersion('v3.2.1'))
        self.assertTrue(RevisionVersion('v3.1.2') <= RevisionVersion('v3.2.1'))
        self.assertTrue(RevisionVersion('v3.2.0') <= RevisionVersion('v3.2.1'))
        self.assertFalse(RevisionVersion('v3.2.1') <= RevisionVersion('v3.2.0'))

####################################################################################################

if __name__ == '__main__':

    unittest.main()

####################################################################################################
#
# End
#
####################################################################################################
