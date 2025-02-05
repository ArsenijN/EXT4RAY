import sys
import subprocess

def get_partition_offset(disk, partition):
    try:
        result = subprocess.run(
            ["parted", "-m", disk, "unit", "B", "print"],
            capture_output=True, text=True, check=True
        )

        lines = result.stdout.strip().split("\n")
        for line in lines:
            parts = line.split(":")
            if len(parts) > 1 and parts[0].isdigit():  # Partition lines start with a number
                part_num = parts[0]
                start_offset = parts[1].strip("B")  # Remove 'B' from value
                part_name = f"{disk}{part_num}" if "nvme" in disk else f"{disk}{part_num}"

                if part_name == partition:
                    return int(start_offset)

        print("Partition not found on the specified disk.")
        return None
    except subprocess.CalledProcessError as e:
        print("Error executing parted:", e)
        return None

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <disk> <partition>")
        print("Example: python script.py /dev/sdc /dev/sdc2")
        sys.exit(1)

    disk = sys.argv[1]
    partition = sys.argv[2]

    offset = get_partition_offset(disk, partition)
    if offset is not None:
        print(f"Partition {partition} starts at offset {offset} bytes from {disk}")

if __name__ == "__main__":
    main()
