# NVME degen refresh tool

A minimal python script to refresh NVMe block devices using O_DIRECT.

## Background

NVME devices are typically going slower over time. For most of our devices, NVME firmware will do the job of refreshing what we call "cold data" . However, for some devices, the firmware isn't designed well to refresh data over time, so we'll need to do it manually.

## Warning

This tool is still experimental and may not work as expected. Even as we got exception handling and tested multiple times, you are still highly recommended to run it with caution, on a stable machine . We don't take any responsibility for any damage caused by using this tool, do your own research and test.

Your NVME device could be very hot during refreshing. Make sure to have enough cooling on it to prevent the device from further degrading.

## Usage

- Make sure your device is NOT mounted

```shell
sudo python3 app.py [-h] [--verbose] [--start_offset START_OFFSET] device

Refresh NVMe block device

positional arguments:
  device                Name of the NVMe block device (without /dev/)

options:
  -h, --help            show this help message and exit
  --verbose             Enable verbose output.
  --start_offset START_OFFSET
                        Starting block offset, for continue. default: 0
```

## Screenshot
| Before refresh | After refresh |
| ---- | ---- |
| ![Screenshot_20240922_210945](https://github.com/user-attachments/assets/8451d269-62e9-4f8a-a2e2-fedc84a339e4) | ![Screenshot_20240922_211115](https://github.com/user-attachments/assets/767ad78a-f37c-49ca-95ff-840c1449f90f) |


## Ref

https://nga.178.com/read.php?tid=24388822&rand=356
