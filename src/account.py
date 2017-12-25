import account_types
import os
import os.path

class Account():
    '''A class to represent and handle actions related to creation, reading, and management of user accounts.'''

    def __init__(self, username = '', password = '', userType = account_types.Account_type.S):
        '''(Account, str, str, Account_type Enum) -> NoneType
        Initialize a new account with the given parameters.
        '''
        self.username = username
        self._password = password
        # Note: This is an enum; please don't pass in strings.
        self.userType = userType

    # TODO: Maybe this should actually return an account object instead.
    def readAccountInfo(self, readUsername, readUserType):
        '''(Account, str, Account_type Enum) -> bool
        Try to find an existing account with given type and username and sets
        this account equal to the information if found.
        Return true iff able to find existing account and set.
        '''
        exists = self.doesAccountExist(readUsername, readUserType)
        if exists:
            # user_info.txt assumed to be in directory.
            # TODO: Error catch.
            openFile = readUserType.value + "/" + readUsername + "/user_info.txt"
            with open(openFile, "r") as file:
                accountInfo = file.read().splitlines()
                # Stored as username, password.
                self.username = accountInfo[0]
                self._password = accountInfo[1]
                self.userType = readUserType
        return exists

    def writeAccountInfo(self):
        '''(Account) -> bool
        Write out this account's info to appropriate directory.
        Return true if successful, or false if account exists already or the
        data in this account is malformed.
        '''
        exists = self.doesAccountExist(self.username, self.userType)
        # The special case of empty usernames are treated as existing.
        shouldWriteOut = (not exists 
                          and self.username != '' 
                          and self.isValidPassword())
        if shouldWriteOut:
            openDir = self.userType.value + "/" + self.username
            # Make the directory first and then place user info inside it.
            os.mkdir(openDir)
            with open(openDir + "/user_info.txt", "w") as file:
                file.write(self.username + "\n")
                file.write(self._password)
        return shouldWriteOut

    def doesAccountExist(self, accountUsername, Account_type):
        '''(Account, str, Account_type Enum) -> bool
        Check if an account with the given user name already exists and
        return a boolean representing this.

        An account is considered to 'exist' if its directory exists. 
        It's assumed that its user_info.txt file was created at the same time
        and was not modified/deleted afterwards.
        Blank usernames are ignored and treated as non existant
        '''
        # Get our directory and navigate to where an account should be.
        # NOTE: This takes enum args.
        return (accountUsername != '' 
                and os.path.exists(os.getcwd() 
                                   + "/" + Account_type.value 
                                   + "/" + accountUsername))

    def isValidPassword(self):
        '''(Account) -> bool
        Check this account's password and return whether it is valid.
        '''
        # NOTE: Can easily change this to some other requirement.
        return len(self._password) > 0

    def auth(self, password):
        '''(Account, str) -> bool
        Return whether or not our current password matches the provided
        password.
        '''
        return self._password == password
