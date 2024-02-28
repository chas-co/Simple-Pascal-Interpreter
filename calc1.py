import operator
#Token Types
#EOF (end of file ) token used to indicate that there is no more input left for lexical analysis

INTEGER , PLUS, MINUS, EOF, TIMES, DIVIDE = 'INTEGER', 'PLUS', 'MINUS', 'EOF', 'TIMES','DIVIDE'

class Token (object):
    def __init__ (self,type,value):
        self.type = type
        # token value: 0,1,2,3,4,5,6,7,8,9,'+',or None
        self.value = value
    
    def __str__(self):
        '''String representation of the class
        
        Example:
            Token(INTEGER,3)
            Token(PLUS, '+')
        '''
        return f'Token({self.type},{self.value})'

    def __repr__(self):
        return self.__str__()

class Interpreter (object):
    def __init__(self,text):
        #client string input, e.g. "3+5"
        self.text = text
        #self.pos is an index into self.text
        self.pos = 0
        #current token instance
        self.current_token = None
    def remove_whitespace(self):
        """This method removes white spaces from client input to aid lexical analysis"""
        self.text = self.text.replace(' ','')

    def error(self):
        raise Exception('Error parsing input')
    
    def get_next_token(self):
        """Lexical analyser also know as scanner or tokeniser

        This method is responsible for breaking a sentence 
        apart into tokens. One token at a time
        """
        #remove any whitespaces in the input
        self.remove_whitespace()

        text = self.text
        #is self.pos index past the end of self.text?
        #if so then return the EOF token because there is no more
        #input left to convert to tokens
        if self.pos > len(text)-1:
            return Token(EOF,None)
        
        #get a character at the position self.pos and decide
        #what token to create base on the single character 
        current_char = text[self.pos]

        #for digits we convert them and integer, create an INTEGER
        #token. To do this we check if the current char and next char
        #are both digits. when we find a non digit in the next char 
        # we slice the client string input to that point to get our 
        # integer value. We inscrement self.pos to point to the next char
        #return the INTEGER token
        start = self.pos
        while current_char.isdigit():
            if self.pos < len(text) -1 :
                if text[self.pos+1].isdigit():
                    self.pos += 1
                    current_char = text[self.pos]
                    continue   
            self.pos += 1
            token = Token(INTEGER, int(text[start:self.pos]))
            return token

        if current_char == '+':
            token = Token(PLUS, current_char)
            self.pos += 1
            return token
        elif current_char == '-':
            token = Token(MINUS,current_char)
            self.pos +=1
            return token

        self.error()
        
    def eat(self,token_type):
        # compare the current token type with the passed token type
        # and if they match then "eat" the current token and assign
        # the next token to the self.current_token, otherwise raise
        # an Exception
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()
        
    def expr(self):
        """expr -> INTEGER PLUS INTEGER"""
        ops = {
            '+' : operator.add,
            '-' : operator.sub,
        }
        # set current token to the first token taken from the input
        self.current_token = self.get_next_token()

        #we expect the current token to be a single digit integer
        left = self.current_token
        self.eat(INTEGER)

        #we expect the current token to be a "+" token
        op = self.current_token
        self.eat(self.current_token.type)

        #we expect the current token to be a single-digit integer
        right = self.current_token
        self.eat(INTEGER)

        #the self.current token is set to EOF after this call
        #we has successfully interpreted the client input at
        # this point and we can then add the two integers 
        # and return the result
        #result = left.value + right.value
        return ops[op.value](left.value,right.value)

def main():
    while True:
        try:
            text = input('calc>')
        except EOFError():
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)

if __name__ == '__main__':
    main()
