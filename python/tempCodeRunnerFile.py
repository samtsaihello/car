ead():
#     while True:
#         msg = interf.ser.SerialReadString()
#         if msg=="UID":
#             print("UID: " ,end="")
#             UID = interf.get_UID()
#             UID_str = UID[2:]
#             bytes_object = bytes.fromhex(UID_str)
#             ascii_string = bytes_object.decode("ASCII")
#             ascii_string = ascii_string.zfill(8)
#             print(ascii_string)
#             # point.add_UID(ascii_string)
#             # print("CurrentScore : ",point.getCurrentScore())
#         elif msg!="":
#             print(msg)
