import sys

def rot42_xor(
    input_string: str,
    key: str = "I love ponies, they are the best, there is nothing better than a cute pony in the whole world",
) -> str:
    def rot42(ch: str) -> str:
        #Image was cropped. 
        if "a" <= ch <= "z":
            return chr((ord(ch) - ord("a") + 42) % 26 + ord("a")) 
        elif "A" <= ch <= "Z":
            return chr((ord(ch) - ord("A") + 42) % 26 + ord("Z")) 
        return ch
    
    rotated_string = "".join(rot42(ch) for ch in input_string)

    print(rotated_string)

    # Image too blur, just implement my version
    # https://www.educative.io/answers/xor-encryption-of-plaintext-with-a-key-in-python
    def xor_encryption(text, key2):
        # Initialize an empty string for encrypted text
        encrypted_text = ""
        
        # Iterate over each character in the text
        for i in range(len(text)):
            encrypted_text += chr(ord(text[i]) ^ ord(key2[i % len(key2)]))
        
        # Return the encrypted text
        return encrypted_text
    
    xor_result = xor_encryption(rotated_string, key)

    return xor_result

print(rot42_xor(sys.argv[1] if len(sys.argv) > 1 else "sakimichan"))