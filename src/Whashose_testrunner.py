#/usr/bin/env python
'''
Created on 26 Dec 2013

@author: kevin
'''
import unittest

if __name__ == "__main__":
    result = unittest.TestResult()
    loader = unittest.TestLoader()
    
    t = loader.discover('.', pattern='*_test.py')
    t.run(result)
    
    if result.wasSuccessful():
        print("Successfull testrun.")
        print("\tran: \t", result.testsRun, "tests successfully")
        exit(0)
    else:
        print("Testrun failed:")
        print("\tran: \t\t", result.testsRun)
        print("\terrors: \t", len(result.errors))
        print("\tfailures: \t", len(result.failures))
        
        if len(result.errors) > 0:
            print("Detailed information on errors:")
            for err in result.errors:
                test, trace = err
                print("\nError: ", test)
                print(trace)
        
        if len(result.failures) > 0:
            print("Detailed information on failures:")
            for fail in result.failures:
                test, trace = fail
                print("\nFailure: ", test)
                print(trace)
                        
        exit(1)