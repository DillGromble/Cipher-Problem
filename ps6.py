import string


def load_words(file_name):
    '''
    file_name: word list text file  
    Returns: a list of valid words. Words are strings of lowercase letters.
    '''
    
    print('Loading word list from file...')
    
    in_file = open(file_name, 'r')
    line = in_file.readline()
    word_list = line.split()
    
    print('  ', len(word_list), 'words loaded.')
    
    in_file.close()
    return word_list



def is_word(word_list, word):
    '''
    Determines if word is a valid word
    Returns: True if word is in word_list, False otherwise
    '''
    
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list



def get_story_string():
    """
    Tester function for importing encrypted .txt files
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story



WORDLIST_FILENAME = 'words.txt'


class Message(object):
    
    def __init__(self, text):
        '''                
        text (string): the message's text
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)


    
    def get_message_text(self):
        return self.message_text



    def get_valid_words(self):
        return self.valid_words[:]


        
    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.             
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26
        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''

        shiftDict = {}
        shifter = shift
        sample = string.ascii_letters
        sampleLower = string.ascii_lowercase
        sampleUpper = string.ascii_uppercase
        
        for letter in sample:
            
            if (sampleLower.index(letter.lower()) + shifter) > 25:
                    shifter -= 26
            if letter.isupper():  
                shiftDict[letter] = sampleUpper[sampleUpper.index(letter) + shifter]
            elif letter.islower():
                shiftDict[letter] = sampleLower[sampleLower.index(letter) + shifter]
            
            if shifter < shift:
                shifter = shift
                
        return shiftDict    
        
    

    def apply_shift(self, shift):
        '''
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''

        shiftDict = Message.build_shift_dict(self, shift)
        newMsg = ''
        
        for char in self.message_text:
            if char in shiftDict.keys():
                newMsg += shiftDict[char]
            else:
                newMsg += char
                
        return newMsg



class PlaintextMessage(Message):
    def __init__(self, text, shift):
        ''' 
        text (string): the message's text
        shift (integer): the shift associated with this message
        '''
        
        Message.__init__(self, text)
        self.shift = shift
        self.encrypting_dict = Message.build_shift_dict(self, shift)
        self.message_text_encrypted = Message.apply_shift(self, shift)


    def get_shift(self):
        return self.shift


    def get_encrypting_dict(self):
        return self.encrypting_dict.copy()


    def get_message_text_encrypted(self):
        return self.message_text_encrypted


    def change_shift(self, shift):
        self.shift = shift
        self.encrypting_dict = Message.build_shift_dict(self, shift)
        self.message_text_encrypted = Message.apply_shift(self, shift)


class CiphertextMessage(Message):
    def __init__(self, text):
        Message.__init__(self, text)
        


    def decrypt_message(self):
        '''
        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        
        prevWordNum = 0
        actualWords = 0
        bestString = ''
        bestShift = 0
        
        for shifts in range(26):
            actualWords = 0
            words = Message.apply_shift(self, shifts)
            words = words.split()
            
            for word in words:
                if is_word(self.valid_words, word):
                    actualWords += 1
            if actualWords > prevWordNum:
                prevWordNum = actualWords
                bestString = ' '.join(words)
                bestShift = shifts
                
        return (bestShift, bestString)



joke = CiphertextMessage(get_story_string())
joke.decrypt_message()


#Example test case (PlaintextMessage)
plaintext = PlaintextMessage('hello', 2)
print('Expected Output: jgnnq')
print('Actual Output:', plaintext.get_message_text_encrypted())
    
#Example test case (CiphertextMessage)
ciphertext = CiphertextMessage('jgnnq')
print('Expected Output:', (24, 'hello'))
print('Actual Output:', ciphertext.decrypt_message())
