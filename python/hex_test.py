rv = b"050104D0"
# UID = hex(int.from_bytes(rv, byteorder='big', signed=False))
# print(UID)
# UID_str = UID[2:]
# print(UID_str)
# bytes_object = bytes.fromhex(UID_str)
# print(bytes_object)
ascii_string = rv.decode("ASCII")
print(ascii_string)
ascii_string = ascii_string.zfill(8)
print(ascii_string)