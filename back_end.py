

class Conversor:

    def __init__(self):
        
        self.keys = {"ADD":"0001" , "AND":"0101" ,"BR":"0000" , "JMP":"1100", "JSR":"0100" ,
                     "LD":"0010", "LDI":"1010", "LDR":"0110" , "LEA":"1110" , "NOT":"1001" ,
                     "RET":"1100" , "RTI":"1000" , "ST":"0011" , "STI":"1011" ,"STR":"0111" ,
                     "TRAP":"1111" , "reserved":"1101"}
        
        self.keysSp = {}

        self.registers = {"R0":0 , "R1":0 , "R2":0 , "R3":0 , "R4":0 , "R5":0 , "R6":0}


    def assambly_to_binary (self,textAssambly:str):

        pass

        return textBinary

    def binary_to_assambly (self,textBinary:str):

        pass

        return textAssambly

    def registerChecker (self):

        pass
        return self.registers
