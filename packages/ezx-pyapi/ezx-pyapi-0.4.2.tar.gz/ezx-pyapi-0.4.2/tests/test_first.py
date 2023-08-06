'''
Created on Sep 28, 2021

@author: Sgoldberg
'''
import unittest
import io

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testThisWorks(self):
        self.assertTrue(True, "should be true")

    def testStringBuffer(self):
        buffer = io.StringIO()
        buffer.write("Hello ")
        buffer.write("World")
        s = buffer.getvalue()
        self.assertEqual("Hello World", s, "got it")
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testThisWorks']
    unittest.main()