import base64

# This is the version I made. It took me like an hour or two to make from scratch, and it was actually my first time actually coding in python. I usually prefer C since it is faster, more lightweight, and easier to read than python, but python is more writable than C. 5/10 language.

# Starting Base 64 string. Turns into Binary

base64_string ="MDAxMTAxMDEwMDExMDAxMTAwMTEwMTAwMDAxMTAxMTEwMDExMDEwMTAwMTEwMTEwMDAxMTAxMTEwMDExMDAxMTAwMTEwMTEwMDAxMTAwMTAwMDExMDEwMDAwMTEwMTExMDAxMTAwMTEwMDExMTAwMDAwMTEwMTExMDAxMTAwMTEwMDExMDEwMDAwMTExMDAxMDAxMTAxMDAwMDExMDExMDAwMTEwMTEwMDAxMTAxMDAwMDExMDExMTAwMTEwMTEwMDAxMTAxMTAwMDExMDAxMTAwMTEwMTEwMDEwMDAxMDAwMDExMDExMTAwMTExMDAwMDAxMTAxMTAwMTAwMDAxMDAwMTEwMTAwMDAxMTEwMDEwMDExMDEwMTAwMTEwMDAxMDAxMTAwMTEwMTAwMDEwMDAwMTEwMDExMDEwMDAxMDA="
base64_bytes = base64_string.encode("ascii")

base_64_first_pass_string_bytes = base64.b64decode(base64_bytes)
base_64_first_string = base_64_first_pass_string_bytes.decode("ascii")

#print(f"Decoded string: {base_64_first_string}")

# Taking the translated Base 64 output from Binary and turning it into the next Base 64 string

import codecs

hex_string = hex(int(base_64_first_string, 2))[2:]

if len(hex_string) % 2 != 0:
    hex_string = '0' + hex_string
oneszeros = codecs.decode(hex_string, 'hex').decode()
#print()
#print(oneszeros)

# Turning hex into the next Base 64 string

result = bytearray.fromhex(oneszeros).decode()

#print()
#print(result)
#print()

# Turning Base 64 into the final Hello, World!

b64_bytes = result.encode("ascii")

b64_string_bytes = base64.b64decode(b64_bytes)
b64_string = b64_string_bytes.decode("ascii")

print(f"{b64_string}")
