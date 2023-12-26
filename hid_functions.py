import hid
import sys

# ID Constants
VENDOR_ID     = 0x3434
PRODUCT_ID    = 0x0121

# QMK Constants - used to identify device when enumerating devices. RAW_EPSIZE is the size of a HID report in bytes.
USAGE_PAGE = 0xFF60
USAGE = 0x61
RAW_EPSIZE = 32

def get_raw_hid_interface(vendor_id: int, product_id: int):
    device_interfaces = hid.enumerate(vendor_id, product_id)
    raw_hid_interfaces = [i for i in device_interfaces if i['usage_page'] == USAGE_PAGE and i['usage'] == USAGE]

    if len(raw_hid_interfaces) == 0:
        return None

    interface = hid.Device(path=raw_hid_interfaces[0]['path'])

    return interface





def send_raw_report(payload: list[int]):
    interface = get_raw_hid_interface(VENDOR_ID, PRODUCT_ID)

    if(interface is None):
        print("ERROR: No device found")
        sys.exit(1)

    report = [0x00, *payload]
    # print(report)


    try:
        report_bytes = bytes(report)
        interface.write(report_bytes)

    finally:
        interface.close()





def send_group_report(payloads: list[list[int]]):
    interface = get_raw_hid_interface(VENDOR_ID, PRODUCT_ID)

    if(interface is None):
        print("ERROR: No device found")
        sys.exit(1)
        
    try:
        for payload in payloads:
            report = [0x00, *payload]
            # print(report)
            
            report_bytes = bytes(report)
            interface.write(report_bytes)
    
    finally:
        interface.close()


