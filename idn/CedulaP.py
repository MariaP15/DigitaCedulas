


# Written by Lateraluz++.
# 25-8-2019
# I wrote it using Python because I don't ever program using it, so it was a opportunity to learn something new.
# Feel free to improve it and share it, Knowledge belongs to humanity!
# Info got it from  https://github.com/robchava/LectorCedulasCR/blob/master/app/src/main/java/com/vbalex/cedulascr/CedulaCR.java

#imports
import re

# Definitions
def xorOperation(p1, p2):
    return p1 ^ p2


def getString():
    # Private Key to decrypt using Xor Algoritm ()
    key = [0x27, 0x30, 0x04, 0xA0, 0x00, 0x0F, 0x93, 0x12, 0xA0, 0xD1, 0x22, 0xE0, 0x03, 0xD0, 0x00, 0xDf, 0x00]

    # data readed from id in format pdf 417
    # Info can be extracted scanning Identificaciont and upload the file at https://online-barcode-reader.inliteresearch.com/
    dataFromId = [0x15 ,0x00 ,0x3c ,0x97 ,0x34 ,0x3f ,0xaa ,0x23 ,0x91 ,0x9c ,0x76 ,0xae ,0x47 ,0x9f ,0x5a ,0x9e ,
                  0x00 ,0x27 ,0x30 ,0x04 ,0xa0 ,0x00 ,0x0f ,0x93 ,0x12 ,0xa0 ,0xd1 ,0x33 ,0xe0 ,0x03 ,0xd0 ,0x00 ,
                  0xdf ,0x00 ,0x27 ,0x77 ,0x4b ,0xee ,0x5a ,0x4e ,0xdf ,0x57 ,0xfa ,0xd1 ,0x33 ,0xe0 ,0x03 ,0xd0 ,
                  0x00 ,0xdf ,0x00 ,0x27 ,0x30 ,0x04 ,0xa0 ,0x00 ,0x0f ,0x93 ,0x12 ,0xa0 ,0xd1 ,0x79 ,0xa1 ,0x55 ,
                  0x99 ,0x45 ,0x8d ,0x20 ,0x66 ,0x7c ,0x41 ,0xea ,0x41 ,0x41 ,0xd7 ,0x40 ,0xef ,0xd1 ,0x33 ,0xe0 ,
                  0x03 ,0xd0 ,0x00 ,0xdf ,0x00 ,0x27 ,0x30 ,0x04 ,0xa0 ,0x00 ,0x0f ,0xb3 ,0x20 ,0x90 ,0xe1 ,0x05 ,
                  0xd0 ,0x32 ,0xe2 ,0x30 ,0xed ,0x30 ,0x14 ,0x04 ,0x34 ,0x92 ,0x30 ,0x39 ,0x93 ,0x12 ,0xa0 ,0xd1 ,
                  0x33 ,0xe0 ,0x03 ,0xd0 ,0x31 ,0xe9 ,0x1d ,0x6d ,0x06 ,0xca ,0x34 ,0x58 ,0xfa ,0x5c ,0xdb ,0x3f ,
                  0x1e ,0xd5 ,0x68 ,0x92 ,0x00 ,0xba ,0x0b ,0xd2 ,0xf0 ,0x9a ,0x8e ,0x12 ,0xbb ,0x9e ,0x1a ,0xff ,
                  0x59 ,0x3c ,0x97 ,0xd3 ,0x4c ,0x89 ,0x91 ,0xbc ,0x6f ,0x64 ,0x95 ,0x3f ,0xe3 ,0x77 ,0x97 ,0xed ,
                  0x09 ,0xc7 ,0xcc ,0x4f ,0xe7 ,0xa0 ,0xd2 ,0x4d ,0x83 ,0xe2 ,0x47 ,0x49 ,0x0a ,0x16 ,0x03 ,0x4b ,
                  0xb3 ,0x27 ,0xe6 ,0xd3 ,0x1e ,0x6e ,0x37 ,0xaf ,0x1a ,0x38 ,0x2c ,0x7b ,0x23 ,0x59 ,0x96 ,0x72 ,
                  0x21 ,0x00 ,0x1e ,0xdd ,0x84 ,0xc1 ,0x4e ,0x67 ,0xf0 ,0x63 ,0x1f ,0x7b ,0x39 ,0xb9 ,0x35 ,0xd2 ,
                  0x32 ,0x92 ,0xbd ,0x3f ,0xb7 ,0xc6 ,0x1b ,0xe1 ,0x1e ,0xf8 ,0x77 ,0x84 ,0x34 ,0x9c ,0x26 ,0x2c ,
                  0x49 ,0xbc ,0x07 ,0xfe ,0xad ,0xc0 ,0x73 ,0x78 ,0x58 ,0x25 ,0xdb ,0x4d ,0x3a ,0x5d ,0x0f ,0x71 ,
                  0xb8 ,0x5e ,0xd2 ,0x44 ,0x75 ,0x0b ,0x56 ,0xd3 ,0xd9 ,0xf1 ,0x2b ,0xaf ,0xd0 ,0x4b ,0x72 ,0x7b ,
                  0xd8 ,0x5a ,0x8d ,0x72 ,0xdc ,0xf1 ,0xa1 ,0xf6 ,0x7e ,0x4a ,0x54 ,0x5f ,0x3f ,0x13 ,0x8d ,0x7b ,
                  0xec ,0x46 ,0x0e ,0xf9 ,0xe6 ,0x92 ,0x97 ,0x14 ,0x63 ,0x62 ,0xd8 ,0xd9 ,0xc4 ,0xec ,0x7c ,0x84 ,
                  0xf0 ,0x8d ,0x3f ,0x07 ,0x71 ,0x27 ,0xc6 ,0xd5 ,0x9c ,0xe9 ,0xbc ,0x40 ,0x6f ,0xf9 ,0xad ,0x75 ,
                  0x7f ,0x2c ,0x72 ,0x49 ,0xe5 ,0x9a ,0x7b ,0x4b ,0x36 ,0x6c ,0x99 ,0xf8 ,0x92 ,0x56 ,0x56 ,0xaf ,
                  0x9c ,0x62 ,0x79 ,0x50 ,0x9c ,0x57 ,0x8d ,0x59 ,0xa1 ,0xb7 ,0x7b ,0xc1 ,0x0e ,0xfc ,0xe8 ,0x67 ,
                  0xd0 ,0x00 ,0xdf ,0x00 ,0x27 ,0x30 ,0x04 ,0xa0 ,0x00 ,0x0f ,0x93 ,0x12 ,0xa0 ,0xd1 ,0x33 ,0xe0 ,
                  0x03 ,0xd0 ,0x00 ,0xdf ,0x00 ,0x27 ,0x30 ,0x04 ,0xa0 ,0x00 ,0x0f ,0x93 ,0x12 ,0xa0 ,0xd1 ,0x33 ,
                  0xe0 ,0x03 ,0xd0 ,0x00 ,0xdf ,0x00 ,0x27 ,0x30 ,0x04 ,0xa0 ,0x00 ,0x0f ,0x93 ,0x12 ,0xa0 ,0xd1 ,
                  0x33 ,0xe0 ,0x03 ,0xd0 ,0x00 ,0xdf ,0x00 ,0x27 ,0x30 ,0x04 ,0xa0 ,0x00 ,0x0f ,0x93 ,0x12 ,0xa0 ,
                  0xd1 ,0x33 ,0xe0 ,0x03 ,0xd0 ,0x00 ,0xdf ,0x00 ,0x27 ,0x2d ,0x4e ,0x96 ,0xce ,0x9b ,0xcf ,0xa3 ,
                  0x2b ,0x1a ,0xa8 ,0x2b ,0x85 ,0x1c ,0x95 ,0x2d ,0xba ,0xb1 ,0x86 ,0xb5 ,0x2c ,0xce ,0x9f ,0x2e ,
                  0xa1 ,0x0b ,0x3e ,0x88 ,0x0d ,0x83 ,0x3e ,0x91 ,0x4f ,0x9a ,0x4e ,0x5f ,0x39 ,0x05 ,0x3b ,0x43 ,
                  0x98 ,0x8a ,0xde ,0xce ,0xe1 ,0x31 ,0x70 ,0xce ,0xac ,0x73 ,0x4d ,0x7d ,0xa5 ,0x8b ,0xd9 ,0x06 ,
                  0x58 ,0x19 ,0x56 ,0xeb ,0xca ,0xe8 ,0xda ,0x35 ,0xcb ,0xda ,0x98 ,0x1d ,0x08 ,0xaf ,0x73 ,0x8d ,
                  0x03 ,0xae ,0xd9 ,0x3c ,0x95 ,0x5a ,0x4e ,0xb4 ,0x42 ,0x57 ,0x77 ,0xf7 ,0x2d ,0xa2 ,0x60 ,0x0f ,
                  0xc7 ,0xac ,0x6e ,0xbb ,0xe5 ,0x02 ,0xfc ,0x3a ,0xfd ,0x6c ,0xe9 ,0x03 ,0x8c ,0x8d ,0x57 ,0x17 ,
                  0x1b ,0xeb ,0x03 ,0x0b ,0xa9 ,0x64 ,0xe6 ,0x8a ,0x41 ,0x81 ,0x70 ,0x93 ,0x35 ,0xaa ,0x4d ,0x3a ,
                  0xe8 ,0x29 ,0xca ,0x46 ,0xf9 ,0x90 ,0x45 ,0xac ,0x95 ,0x14 ,0xc9 ,0x02 ,0xcc ,0x55 ,0x8b ,0x3b ,
                  0x86 ,0xb3 ,0x73 ,0xaf ,0x91 ,0x2b ,0xca ,0x22 ,0x3e ,0xf3 ,0x65 ,0xaf ,0xf3 ,0xac ,0x5c ,0x12 ,
                  0xef ,0x2b ,0x73 ,0xec ,0x07 ,0x8e ,0x56 ,0x47 ,0x1d ,0x60 ,0xef ,0xc2 ,0x43 ,0x20 ,0xfa ,0xfb ,
                  0xc6 ,0x63 ,0x7c ,0xe4 ,0xc0 ,0xa3 ,0x28 ,0xc6 ,0xb5 ,0x45 ,0xe6 ,0x46 ,0xc2 ,0xc9 ,0x48 ,0x46 ,
                  0x92 ,0x0f ,0x5e ,0xf9 ,0x60 ,0x5a ,0xe1 ,0x89 ,0x50 ,0x7a ,0x6e ,0x6f ,0xc6 ,0x67 ,0xe2 ,0xc4 ,
                  0x30 ,0xe9 ,0xa0 ,0x8b ,0x79 ,0x5d ,0x58 ,0x1f ,0x2d ,0x54 ,0xd9 ,0x8a ,0x72 ,0x80 ,0x65 ,0x09 ,
                  0x46 ,0xb2 ,0x64 ,0x49 ,0x0c ,0x6a ,0x73 ,0xb7 ,0x35 ,0x0a ,0x56 ,0x3a ,0x2b ,0xb1 ,0xef ,0xbd ,
                  0x3b ,0xfd ,0xe9 ,0x80 ,0xf4 ,0x5e ,0x44 ,0x89 ,0x17 ,0xca ,0x3b ,0x94 ,0xa2 ,0x45 ,0xde ,0x1f ,
                  0x83 ,0xe0 ,0x70 ,0x19 ,0xc4 ,0x8b ,0x4d ,0x27 ,0x30 ,0x04 ,0xa0 ,0x00 ,0x0f ,0x93 ,0x12 ,0xa0 ,
                  0xd1 ,0x33 ,0xe0 ,0x03 ,0xd0 ,0x00 ,0xdf ,0x00 ,0x27 ,0x30 ,0x04 ,0xa0 ,0x00 ,0x0f ,0x93 ,0x12 ,
                  0xa0 ,0xd1 ,0x33 ,0xe0 ,0x03 ,0xd0 ,0x00 ,0xdf  ,0x00 ,0x27 ,0x30 ,0x0]

    # Convert the list to byte array
    keyBytes = bytearray(key)
    dataFromIdBytes = bytearray(dataFromId)

    # index used in order to get info from dataFromId
    index = 0
    data = ""

    for byteFromArray in dataFromIdBytes:
        # Xor array to decrypt is 17 long bytes, reset when counter is 17
        if index == 17:
            index = 0

        caracter = xorOperation(keyBytes[index], byteFromArray)

        # From byte to char
        char_caracter = chr(caracter)

        # MUST include either letters or numbers
        if re.match("^[a-zA-Z0-9]*$", char_caracter):
            data += char_caracter
        else:
            data += " "
        # increment index
        index = index + 1
    return data

class Tico:
    def __init__(self,data):
        self.data = data

    def getId(self):
        return self.data[0:9]

    def getApellido1(self):
        return self.data[9:35]

    def getApellido2(self):
        return self.data[35:61]

    def getNombre(self):
        return self.data[60:91]

    def getSexo(self):
        return self.data[91]

    def getFechaNacimiento(self):
        return self.data[92: 96] + "-" + self.data[96: 98] + "-" + self.data[98: 100]

    def getFechaVencimiento(self):
        return self.data[100: 104] + "-" + self.data[104: 106] + "-" + self.data[106: 108]

def main():
    data = getString()
   
    tico = Tico(data)
    tico_data = {
        "id": tico.getId(),
        "apellido1": tico.getApellido1(),
        "apellido2": tico.getApellido2(),
        "nombre": tico.getNombre(),
        "sexo": tico.getSexo(),
        "fecha_nacimiento": tico.getFechaNacimiento(),
        "fecha_vencimiento": tico.getFechaVencimiento()
    }
    return tico_data 
    



