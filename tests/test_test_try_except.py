import unittest
import helper

class TestTryExceptStepByStep(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": "import numpy as np",
            "DC_SOLUTION": '''
try:
    x = max([1, 2, 'a'])
except TypeError as e:
    x = 'typeerror'
except ValueError:
    x = 'valueerror'
except (ZeroDivisionError, IOError) as e:
    x = e
except :
    x = 'someerror'
else :
    passed = True
finally:
    print('done')
            ''',
            "DC_SCT": '''
import collections
handlers = collections.OrderedDict()
handlers['TypeError'] = lambda: test_object_after_expression('x')
handlers['ValueError'] = lambda: test_object_after_expression('x')
handlers['ZeroDivisionError'] = lambda: test_object_after_expression('x', context_vals = ['anerror'])
handlers['IOError'] = lambda: test_object_after_expression('x', context_vals = ['anerror'])
handlers['all'] = lambda: test_object_after_expression('x')
test_try_except(index = 1,
                body = lambda: test_function("max"),
                handlers = handlers,
                orelse = lambda: test_object_after_expression('passed'),
                finalbody = lambda: test_function('print'))
            '''
        }

        self.SCT_NO_LAM = helper.remove_lambdas(self.data['DC_SCT'])

    def test_fail_01(self):
        self.data["DC_CODE"] = ""
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "The system wants to check the first try-except block but hasn't found it.")

    def test_fail_02(self):
        self.data["DC_CODE"] = '''
try:
    x = max([1, 2, 'a'])
except TypeError as e:
    x = 'typeerrors'
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Check the first try-except block. Did you correctly specify the <code>TypeError</code> <code>except</code> block? Are you sure you assigned the correct value to <code>x</code>?")

    def test_fail_03(self):
        self.data["DC_CODE"] = '''
try:
    x = max([1, 2, 'a'])
except TypeError as e:
    x = 'typeerror'
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Have you included a <code>ValueError</code> <code>except</code> block in your first try-except block?")

    def test_fail_04(self):
        self.data["DC_CODE"] = '''
try:
    x = max([1, 2, 'a'])
except TypeError as e:
    x = 'typeerror'
except ValueError:
    x = 'valueerrors'
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Check the first try-except block. Did you correctly specify the <code>ValueError</code> <code>except</code> block? Are you sure you assigned the correct value to <code>x</code>?")

    def test_fail_05(self):
        self.data["DC_CODE"] = '''
try:
    x = max([1, 2, 'a'])
except TypeError as e:
    x = 'typeerror'
except ValueError:
    x = 'valueerror'
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Have you included a <code>ZeroDivisionError</code> <code>except</code> block in your first try-except block?")

    def test_fail_06(self):
        self.data["DC_CODE"] = '''
try:
    x = max([1, 2, 'a'])
except TypeError as e:
    x = 'typeerror'
except ValueError:
    x = 'valueerror'
except ZeroDivisionError as e:
    x = 'test'
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Check the first try-except block. Did you correctly specify the <code>ZeroDivisionError</code> <code>except</code> block? Are you sure you assigned the correct value to <code>x</code>?")

    def test_fail_07(self):
        self.data["DC_CODE"] = '''
try:
    x = max([1, 2, 'a'])
except TypeError as e:
    x = 'typeerror'
except ValueError:
    x = 'valueerror'
except ZeroDivisionError as e:
    x = e
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Have you included a <code>IOError</code> <code>except</code> block in your first try-except block?")

    def test_fail_08(self):
        self.data["DC_CODE"] = '''
try:
    x = max([1, 2, 'a'])
except TypeError as e:
    x = 'typeerror'
except ValueError:
    x = 'valueerror'
except (ZeroDivisionError, IOError) as e:
    x = 'test'
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Check the first try-except block. Did you correctly specify the <code>ZeroDivisionError</code> <code>except</code> block? Are you sure you assigned the correct value to <code>x</code>?")

    def test_fail_09(self):
        self.data["DC_CODE"] = '''
try:
    x = max([1, 2, 'a'])
except TypeError as e:
    x = 'typeerror'
except ValueError:
    x = 'valueerror'
except (ZeroDivisionError, IOError) as e:
    x = e
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Have you included a general <code>except</code> block in your first try-except block?")

    def test_fail_10(self):
        self.data["DC_CODE"] = '''
try:
    x = max([1, 2, 'a'])
except TypeError as e:
    x = 'typeerror'
except ValueError:
    x = 'valueerror'
except (ZeroDivisionError, IOError) as e:
    x = e
except :
    x = 'someerrors'
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Check the first try-except block. Did you correctly specify the general <code>except</code> block? Are you sure you assigned the correct value to <code>x</code>?")

    def test_fail_11(self):
        self.data["DC_CODE"] = '''
try:
    x = max([1, 2, 'a'])
except TypeError as e:
    x = 'typeerror'
except ValueError:
    x = 'valueerror'
except (ZeroDivisionError, IOError) as e:
    x = e
except :
    x = 'someerror'
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Have you included a <code>else</code> part in your first try-except block?")

    def test_fail_12(self):
        self.data["DC_CODE"] = '''
try:
    x = max([1, 2, 'a'])
except TypeError as e:
    x = 'typeerror'
except ValueError:
    x = 'valueerror'
except (ZeroDivisionError, IOError) as e:
    x = e
except :
    x = 'someerror'
else :
    passed = False
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Check the first try-except block. Did you correctly specify the <code>else</code> part? Are you sure you assigned the correct value to <code>passed</code>?")

    def test_fail_13(self):
        self.data["DC_CODE"] = '''
try:
    x = max([1, 2, 'a'])
except TypeError as e:
    x = 'typeerror'
except ValueError:
    x = 'valueerror'
except (ZeroDivisionError, IOError) as e:
    x = e
except :
    x = 'someerror'
else :
    passed = True
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Have you included a <code>finally</code> part in your first try-except block?")

    def test_fail_14(self):
        self.data["DC_CODE"] = '''
try:
    x = max([1, 2, 'a'])
except TypeError as e:
    x = 'typeerror'
except ValueError:
    x = 'valueerror'
except (ZeroDivisionError, IOError) as e:
    x = e
except :
    x = 'someerror'
else :
    passed = True
finally:
    print('donessss')
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

    def test_pass(self):
        self.data["DC_CODE"] = self.data["DC_SOLUTION"]
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_fail_01_no_lam(self):
        self.data["DC_SCT"] = self.SCT_NO_LAM
        self.test_fail_01()

    def test_fail_04_no_lam(self):
        self.data["DC_SCT"] = self.SCT_NO_LAM
        self.test_fail_04()

    def test_fail_14_no_lam(self):
        self.data["DC_SCT"] = self.SCT_NO_LAM
        self.test_fail_14()

    def test_pass_no_lam(self):
        self.data["DC_SCT"] = self.SCT_NO_LAM
        self.test_pass()

    def test_fail_01_exchain(self):
        self.data["DC_SCT"] = self.SCT_NO_LAM.replace('test_try_except', 'Ex().test_try_except')
        self.test_fail_01()

    def test_pass_exchain(self):
        self.data["DC_SCT"] = self.SCT_NO_LAM.replace('test_try_except', 'Ex().test_try_except')
        self.test_pass()



if __name__ == "__main__":
    unittest.main()
