# Problem Set 4C
# Name: Thai Hong Curi
# Collaborators:
# Time Spent: x:xx

import string
from numba import njit, prange
from itertools import permutations

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

wordlist = load_words(WORDLIST_FILENAME)
    

class SubMessage(object):
    def __init__(self, text):
        '''
        Initializes a SubMessage object
                
        text (string): the message's text

        A SubMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
         #delete this line and replace with your code here
        self.message_text = text
        text_copy = text[:]
        self.valid_words = list()
        words = list(text_copy.split())

        for word in words:
            if is_word(wordlist, word=word):
                self.valid_words.append(word)
    
    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        #delete this line and replace with your code here
        return self.message_text
    
    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        
         #delete this line and replace with your code here
        return self.valid_words.copy()
    

    def build_transpose_dict(self, vowels_permutation):
        '''
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)
        
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to an
        uppercase and lowercase letter, respectively. Vowels are shuffled 
        according to vowels_permutation. The first letter in vowels_permutation 
        corresponds to a, the second to e, and so on in the order a, e, i, o, u.
        The consonants remain the same. The dictionary should have 52 
        keys of all the uppercase letters and all the lowercase letters.

        Example: When input "eaiuo":
        Mapping is a->e, e->a, i->i, o->u, u->o
        and "Hello World!" maps to "Hallu Wurld!"

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        lower_perm = vowels_permutation[:]
        upper_perm = vowels_permutation[:].upper()
        #delete this line and replace with your code here
        mapping = dict()
        for i in range(26):
            mapping[chr(ord('A')+i)] = chr(ord('A') + i)
            mapping[chr(ord('a')+i)] = chr(ord('a') + i) 
        for i in range(5):
            mapping[VOWELS_LOWER[i]] = lower_perm[i]
            mapping[VOWELS_UPPER[i]] = upper_perm[i]

        return mapping
    
    def apply_transpose(self, vowels_perm):
        '''
        transpose_dict (dict): a transpose dictionary
        
        Returns: an encrypted version of the message text, based 
        on the dictionary
        '''
        
        #delete this line and replace with your code here
        letter = list()
        mapping = self.build_transpose_dict(vowels_perm)

        for char in self.message_text:
            letter.append(char)

        for i in range(len(letter)):
            if ord('A') <= ord(letter[i]) <= ord('Z') or ord('a') <= ord(letter[i]) <= ord('z'):
                letter[i] = mapping[letter[i]]
            else:
                continue

        transposed = ''.join(letter)
        return transposed   

class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        '''
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        #delete this line and replace with your code here
        SubMessage.__init__(self, text)

    def decrypt_message(self):
        '''
        Attempt to decrypt the encrypted message 
        
        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. For each permutation, check how many
        words in the decrypted text are valid English words, and return
        the decrypted message with the most English words.
        
        If no good permutations are found (i.e. no permutations result in 
        at least 1 valid word), return the original string. If there are
        multiple permutations that yield the maximum number of words, return any
        one of them.

        Returns: the best decrypted message    
        
        Hint: use your function from Part 4A
        '''
        pass #delete this line and replace with your code here
        list_of_perm =['aeiou']+[''.join(vow) for vow in permutations(VOWELS_LOWER)]
        total_count = dict()

        for perm in list_of_perm:
            transposed_text = self.apply_transpose(perm)
            transposed_words = transposed_text.split()
            count = 0
            for word in transposed_words:
                if is_word(wordlist, word=word):
                    count += 1
            total_count[perm] = count

        max_count = 0
        for k, v in total_count.items():
            if v > max_count:
                max_count = v

        for k, v in total_count.items():
            if v == max_count:
                break

        riu_transpose = k
        final_transposed_text = self.apply_transpose(riu_transpose)
        return (riu_transpose, final_transposed_text)

        

if __name__ == '__main__':

    # Example test case
    message = SubMessage("Hello World!")
    permutation = "eaiuo"
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Hallu Wurld!")
    print("Actual encryption:", message.apply_transpose(permutation))
    enc_message = EncryptedSubMessage(message.apply_transpose(permutation))
    print("Decrypted message:", enc_message.decrypt_message())
     
    #TODO: WRITE YOUR TEST CASES HERE
    mes = EncryptedSubMessage('i am goy')
    print(mes.decrypt_message())
    mes = EncryptedSubMessage('u im goy')
    print(mes.decrypt_message())