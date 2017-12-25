import unittest
from account import Account
from accountTypes import AccountType

class TestAccount(unittest.TestCase):
    ''' A collection of unit tests for Account
    It is assumed that the standard test 
    instructor (Charlie, Danny) and student (Alice Bob)
    accounts exist
    '''
    
    def test_password_auth(self):
        self.testAcc = Account("user", "pass")
        self.assertTrue(self.testAcc.auth("pass"))
        
    def test_password_auth_fail(self):
        self.testAcc = Account("user", "pass")
        self.assertFalse(self.testAcc.auth("Not"))
        
    def test_password_auth_blank(self):
        self.testAcc = Account("user", "pass")
        self.assertFalse(self.testAcc.auth(""))
        
    def test_password_valid(self):
        self.testAcc = Account("user", "normal")
        self.assertTrue(self.testAcc.isValidPassword())
        
    def test_password_invalid(self):
        self.testAcc = Account("user", "")
        self.assertFalse(self.testAcc.isValidPassword())
        
    def test_account_exists_student(self):
        self.testAcc = Account()
        self.assertTrue(self.testAcc.doesAccountExist("Alice", AccountType.S))
        
    def test_account_exists_instr(self):
        self.testAcc = Account()
        self.assertTrue(self.testAcc.doesAccountExist("Danny", AccountType.I))  
        
    def test_account_exists_wrong_type(self):
        self.testAcc = Account()
        self.assertFalse(self.testAcc.doesAccountExist("Danny", AccountType.S))
        
    def test_account_exists_blank(self):
        self.testAcc = Account()
        self.assertFalse(self.testAcc.doesAccountExist("", AccountType.S))
        
    # some whitebox testing
    def test_account_reading(self):
        self.testAcc = Account()
        self.testAcc.readAccountInfo("Alice", AccountType.S)
        self.assertTrue(self.testAcc._password == "password")
        
    def test_account_reading_not_exist(self):
        self.testAcc = Account()
        self.assertFalse(self.testAcc.readAccountInfo("Alice", AccountType.I))
        
if __name__ == '__main__':
    unittest.main()
    
    