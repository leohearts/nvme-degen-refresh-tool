# NVME degen refresh tool

A minimal python script to refresh NVMe block devices using O_DIRECT.

## Background

NVME devices are typically going slower over time. For most of our devices, NVME firmware will do the job of refreshing what we call "cold data" . However, for some devices, the firmware isn't designed well to refresh data over time, so we'll need to do it manually.

## Warning

This tool is still experimental and may not work as expected. Even as we got exception handling and tested multiple times, you are still highly recommended to run it with caution, on a stable machine . We don't take any responsibility for any damage caused by using this tool, do your own research and test.

Your NVME device could be very hot during refreshing. Make sure to have enough cooling on it to prevent the device from further degrading.

## Usage

```bash
sudo python3 app.py [-h] [--verbose] [--start_offset START_OFFSET] device
```
Refresh NVMe block device

positional arguments:
  device                Name of the NVMe block device (without /dev/)

options:
  -h, --help            show this help message and exit
  --verbose             Enable verbose output.
  --start_offset START_OFFSET
                        Starting block offset, for continue. default: 0


## Ref

https://nga.178.com/read.php?tid=24388822&rand=356