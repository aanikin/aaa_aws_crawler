import unittest

testmodules = ['Test_Audit', 'Test_ClientProvider', 'Test_IAM']

if __name__ == '__main__':
    suite = unittest.TestSuite()

    for tm in testmodules:
        suite.addTest(unittest.defaultTestLoader.loadTestsFromName(tm))

    unittest.TextTestRunner().run(suite)
