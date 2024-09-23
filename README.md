# NVME degen refresh tool

A minimal python script to refresh NVMe block devices using O_DIRECT.

## Background

NVME devices are typically going slower over time. For most of our devices, NVME firmware will do the job of refreshing what we call "cold data" . However, for some devices, the firmware isn't designed well to refresh data over time, so we'll need to do it manually.

> [!WARNING]
> This tool is still experimental and may not work as expected. Even as we got exception handling and tested multiple times, you are still highly recommended to run it with caution, on a stable machine. We don't take any responsibility for any damage caused by using this tool, do your own research and test.
> 
> Your NVME device could be very hot during refreshing. Make sure to have enough cooling on it to prevent the device from further degrading.
> ONLY use this script if you know what you are doing and you actually need to refresh your NVMe device.
> 
> It shouldn't destroy the data, however, it's still recommended to back up you valuable files before usage.

## Usage

- Make sure your device is NOT mounted

```shell
sudo python3 app.py [-h] [--verbose] [--test] [--start_offset START_OFFSET] device

Refresh NVMe block device

positional arguments:
  device                Name of the NVMe block device (without /dev/)

options:
  -h, --help            show this help message and exit
  --verbose             Enable verbose output
  --test                Only test block speed without refreshing
  --start_offset START_OFFSET
                        Starting block offset, for continue.
```

## Screenshot
| Before refresh | After refresh |
| ---- | ---- |
| ![Screenshot_20240922_211835](https://github.com/user-attachments/assets/8bc3c282-360c-43c4-8bb8-e74dc8c29857) | ![Screenshot_20240922_211920](https://github.com/user-attachments/assets/eebe69b8-da22-42b8-8238-8eda24ecb54a) |

## How does it work?

For every block, it reads data from the device, check if it's slow, and refreshes it by writing the same data back.


## Ref

https://nga.178.com/read.php?tid=24388822&rand=356
