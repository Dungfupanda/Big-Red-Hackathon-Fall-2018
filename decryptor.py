from PIL import Image
import hashlib
import hash_image
def decrypt(directory, pwd):
    """
    This function will decrypt a message inside an image.
    :var directory: string ~ file path to image
    :var pwd: string ~ password used to retrieve encryption. 
    """
    pwd_hash = hashlib.sha256()
    pwd_hash.update(pwd.encode('utf-8'))

    orig_im = Image.open(directory)
    pixels = list(orig_im.getdata())
    width, height = orig_im.size
    pixels = [pixels[i * width : (i+1) * width] for i in range(height)]
    sequence = hash_image.get_indices(key_to_int(pwd_hash.digest()), 100, width, height)
    message = ''
    bits = ''
    enc_error_count = 0
    for i in range(len(sequence)):
        row = sequence[i][0]
        col = sequence[i][1]
        pixel = pixels[row][col][i%3]
        changed_bits = pixel%4  # last two bits
        bits += str(int(changed_bits > 1)) + str(changed_bits%2)
    for bit_idx in range(0, len(bits), 8):
        ch_bits = bits[bit_idx : bit_idx + 8]
        asc = int(ch_bits, 2)
        if asc < 128:
            message += chr(asc)
        else:
            enc_error_count += 1
    if enc_error_count > 0:
        print("There were", enc_error_count, "encoding errors.")
        print("Output may not return expected result")
    return message


def key_to_int(key):
    st = ""
    for val in key:
        st += str(val)
    return int(st)%(2**32-1)

print(decrypt('./slack-profile-picture.jpeg', 'sister-saster'))
        
