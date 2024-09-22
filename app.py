import errno
import mmap
import os
import time
from tqdm import tqdm
import argparse

# Instantiate the parser
parser = argparse.ArgumentParser(description='Refresh NVMe block device')
# Required positional argument
parser.add_argument('device', type=str,
                    help='Name of the NVMe block device (without /dev/)')
parser.add_argument('--verbose', action='store_true',
                    help='Enable verbose output')
parser.add_argument('--start_offset', type=int, default=0, help='Starting block offset, for continue.')
args = parser.parse_args()

# Parameters
BLOCK_SIZE = 1024 * 1024 * 512 # * MB block size, should be aligned to 4096
SLOW_THRESHOLD_MBPS = 200 # MB/s
DEVICE = args.device  # Name of the NVMe block device (without /dev/)
DEVICE_PATH = f"/dev/{DEVICE}"  # Path to the NVMe block device
# DEVICE_PATH = "testdisk"
VERBOSE = args.verbose


start_offset = args.start_offset

def log_verbose(message):
    if VERBOSE:
        print(message)

def get_total_size(): 
    """
    Reads the total size of the block device from sysfs.
    """
    if os.path.isfile(DEVICE_PATH):
        return os.path.getsize(DEVICE_PATH)
    size_path = f"/sys/block/{DEVICE}/size"
    try:
        with open(size_path, "r") as size_file:
            # Size is in 512-byte sectors, convert to bytes
            sectors = int(size_file.read().strip())
            total_size = sectors * 512  
            return total_size
    except Exception as e:
        print(f"Error reading device size: {e}")
        return None

def align_buffer(size):
    """
    Create a memory-aligned buffer (required for O_DIRECT).
    """
    return mmap.mmap(-1, size)

def read_block(fd, offset, block_size):
    """
    Reads a block of data from a file or block device using O_DIRECT and returns the time taken and data.
    """ 
    start_time = time.time()
    buffer = align_buffer(block_size)
    seek = offset * block_size
    os.lseek(fd, seek, os.SEEK_SET)  # Seek to the correct block

    try:    
        bytes_read = os.readv(fd, [buffer])
    except OSError as e:
        if e.errno == errno.EINVAL:
            print(f"Error: Direct I/O requires buffer and file system alignment.")
        raise
    elapsed_time = time.time() - start_time
    return elapsed_time, buffer, bytes_read


def write_block(fd, offset, block_size, data):
    """
    Writes a block of data back to the file or block     device using O_DI  RECT.
    """
    os.lseek(fd, offset * block_size, os.SEEK_SET)  # Seek to the correct block
    bytes_written = os.writev(fd, [data])  # Write the block back with direct I/O
    return bytes_written

def refresh_block(fd, offset, block_size):
    """
    Reads a block from the device or file and refreshes it by rewriting it if it's slow.
    """
    elapsed_time, data, bytes_read = read_block(fd, offset, block_size)
    speed_mbps = (block_size / 1024 / 1024) / elapsed_time
    log_verbose(f"Block {offset} is {speed_mbps:.2f} MB/s")
    if speed_mbps < SLOW_THRESHOLD_MBPS:
        if bytes_read != block_size:
            print("ERROR: Block size mismatch, skipping block", offset) 
            return
        log_verbose(f"Refreshing block {offset} with {speed_mbps:.2f} MB/s")
        write_block(fd, offset, block_size, data)

def main():
    total_size = get_total_size()
    if total_size is None:
        print(f"Could not determine total size of file/device {DEVICE}")
        return
    total_blocks = total_size // BLOCK_SIZE
    print(f"Total size of {DEVICE}: {total_size / (1024 * 1024 * 1024):.2f} GB")
    print(f"Total blocks to process: {total_blocks}")
    
    fd = os.open(DEVICE_PATH, os.O_RDWR | os.O_DIRECT)
    # Use tqdm to show progress
    for block_num in tqdm(range(start_offset, total_blocks), desc="Refreshing blocks", initial=start_offset):
        try:
            refresh_block(fd, block_num, BLOCK_SIZE)
        except KeyboardInterrupt:
            print("Trying to exit gracefully...")
            break
    os.close(fd)
if __name__ == "__main__":
    main()
