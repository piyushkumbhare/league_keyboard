import sys
import hid
import asyncio
import random

vendor_id     = 0x3434
product_id    = 0x0121

usage_page    = 0xFF60
usage         = 0x61
report_length = 32

def get_raw_hid_interface():
    device_interfaces = hid.enumerate(vendor_id, product_id)
    raw_hid_interfaces = [i for i in device_interfaces if i['usage_page'] == usage_page and i['usage'] == usage]

    if len(raw_hid_interfaces) == 0:
        return None

    interface = hid.Device(path=raw_hid_interfaces[0]['path'])

    # print(f"Manufacturer: {interface.manufacturer}")
    # print(f"Product: {interface.product}")

    return interface

def send_raw_report(data):
    interface = get_raw_hid_interface()

    if interface is None:
        print("No device found")
        sys.exit(1)

    request_data = [0x00] * (report_length + 1) # First byte is Report ID

    idx = 1
    for char in data:
        request_data[idx] = ord(char)
        idx += 1
    request_report = bytes(request_data)


    try:
        interface.write(request_report)

        # response_report = interface.read(report_length, timeout=1000)

    finally:
        interface.close()

def generate_num():
    string = ""
    n = random.randint(0, 255)
    if(n < 100 and n > 9):
        string = "0" + str(n)
    elif(n < 10):
        string = "00" + str(n)
    else:
        string = str(n)
    return string

async def randomcolors():
    for _ in range(10):
        to_send = "X"
        for _ in range(6):
            to_send += generate_num()
        await asyncio.sleep(0.1)
        # print(to_send)
        send_raw_report(
            to_send
        )


async def flash_red():
    for _ in range(4):
        send_raw_report(
            "X000000000000000000"
        )
        await asyncio.sleep(0.2)
        send_raw_report(
            "X255000000255000000"
        )
        await asyncio.sleep(0.1)

async def main():
    while(True):
        inp = input("Enter 'Random' or 2 RGB values: ")

        if(inp.strip().upper() == 'RANDOM'):
            await randomcolors()
            continue
        elif(inp.strip().upper() == 'N'):
            send_raw_report(
                'N'
            )
            continue
        elif(inp.strip().upper() == 'RED'):
            await flash_red()
            continue
        
        nums = inp.split(' ')

        raw_input = "X"
        print()
        if(len(nums) != 6):
            print("Enter 6 numbers: R1 G1 B1 R2 G2 B2")
            continue
        for num in nums:
            try:
                curr = int(num)
                if(curr < 0 or 255 < curr or len(num) != 3):
                    print("Numbers should be between 000 & 255 and be 3 digits.")
                    exit(1)
                raw_input += num
            except Exception as e:
                print("Enter only numbers!")
                exit(1)
        print(raw_input)
        send_raw_report(
            raw_input
        )
            



if __name__ == '__main__':
    asyncio.run(main())