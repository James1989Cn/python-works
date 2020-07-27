def crc16(x, invert):
    a = 0xFFFF
    b = 0xA001
    for byte in x:
        a ^= byte
        for i in range(8):
            last = a % 2
            a >>= 1
            if last == 1:
                a ^= b
    if invert:
        pu = a>>8
        pd = a & 0xFF
        return pd<<8 | pu
    return a
if __name__ == "__main__":
	y = [0x01,0x03,0x00,0x01,0x00,0x01]
	print(hex(crc16(y,1)))
	y = [0x01,0x06,0x00,0x01,0x00,0x17]
	print(hex(crc16(y,1)))

