# NVME degen refresh tool

A minimal python script to refresh NVMe block devices using O_DIRECT.

## Background

NVME devices are typically going slower over time. For most of our devices, NVME firmware will do the job of refreshing data. However, for some devices, the firmware isn't designed well to refresh data over time, so we'll need to do it manually.

## Warning

This tool is still experimental and may not work as expected. Even as we got exception handling and tested multiple times, you are still highly recommended to run it with caution, on a stable machine .

## Usage

```bash
python3 app.py <device> [--verbose]
```

- `device` is the name of the NVMe block device (without /dev/)
- `--verbose` enables verbose output
