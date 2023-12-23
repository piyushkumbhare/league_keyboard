#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <wchar.h>
#include <stdint.h>
#include <unistd.h>

#include <hidapi/hidapi.h>
#define RAW_EPSIZE 32
struct hid_device_info* first;

struct hid_device_info* get_interface(unsigned short vendor_id, unsigned short product_id, unsigned short usage, unsigned short usage_page) {
    //Start by enumerating all HID devices
    struct hid_device_info* device = hid_enumerate(vendor_id, product_id);
    
    first = device;

    //March through list until usage_page & usage match
    while(device) {
        printf("Name: %ls, Usage: %d, Usage Page: %d\n", device->manufacturer_string, device->usage, device->usage_page);
        printf("Interface number: %d\n", device->interface_number);

        // if(device->interface_number == 1) break;

        if(device->usage_page != usage_page || device->usage != usage) {
            device = device->next;
            continue;
        } else {
            break;
        }
    }

    
    return device;
}


int main(int argc, char* argv[]) {
    if(argc < 2) {
        printf("Incorrect usage: %s <RGB1> <RGB2>\nWhere RGB values are of the form rrrgggbbb\n", argv[0]);
        exit(1);
    }

    unsigned short usage_page       = 0xFF60;
    unsigned short usage            = 0x61;

    unsigned short vendor_id             = 0x3434;
    unsigned short product_id             = 0x0121;
    
    wchar_t wstr[255];
    unsigned char buf[RAW_EPSIZE];
    if(strcmp(argv[1], "N") == 0) {
        for(int i = 0; i < RAW_EPSIZE; i++) {
            buf[i] = 0x0;
        }
        buf[1] = 0x4E;
    }else if(strlen(argv[1]) != 9 || strlen(argv[1]) != 9) {
        printf("Incorrect usage: %s <RGB1> <RGB2>\nWhere RGB values are of the form rrrgggbbb\n", argv[0]);
        exit(1);
    }else {
        buf[0] = 0x0;
        sprintf((char*)(buf + 1), "X%s%s", argv[1], argv[2]);

    }


    hid_init();

    struct hid_device_info* device = get_interface(
        vendor_id,
        product_id,
        usage,
        usage_page
    );

    hid_device* handle;

    if(!device) {
        printf("Unable to open device\n");
		hid_exit();
 		return 1;
    } else {
        handle = hid_open_path(device->path);
    }

    hid_get_manufacturer_string(handle, wstr, 255);
    printf("%ls\n", wstr);

    printf("data to send: %s\n", &buf[1]);

    int byteswritten = hid_write(handle, buf, RAW_EPSIZE);

    printf("Bytes written: %d\n", byteswritten);

    // res = hid_read(handle, buf, RAW_EPSIZE);
    // printf("Data received: %s", buf);


    hid_close(handle);
    
    hid_free_enumeration(first);
    
    hid_exit();
}