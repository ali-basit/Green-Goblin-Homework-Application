class mChoiceQuestion:
    '''
    A simple class representing a single multiple choice question
    '''
    def __init__(self, question, possibleAnsList, correctAns, instantFeedback):
        ''' (multiChoiceQuestion, string, list of string, string) -> NoneType
        Initialize a multiple choice question with given parameters
        Number of possible answers is inferred from size of given list
        '''
        self._questionBody = question
        self._possibleAnsList = possibleAnsList
        self._possibleAnsList.append(correctAns)
        # we append the correct answer to the end of the list and
        # actually keep track of its index for randomization reasons
        self._correctAnsIndex = self._possibleAnsList[-1]
        self._instantFeedback = instantFeedback

    def getQuestionBody(self):
        return self._questionBody

    def getPossibleAnswers(self):
        '''
        Returns a list of all possible answers including the correct one
        '''
        return self._possibleAnsList

    def getCorrectAnsIndex(self):
        '''
        Returns the index which the correct answer resides in the
        possible answer list
        '''
        return self._correctAnsIndex

    def getInstantFeedback(self):
        '''(multiChoiceQuestion) -> str
        Returns the instant feedback for the question.
        '''
        return self._instantFeedback

    def randomizeAnswerOrder(self):
        '''
        Randomizes the order in which the possible answers appear, this
        includes the index of the correct answer, which is updated.
        '''
        # TODO isn't high enough priority for me to do this right now
        pass
