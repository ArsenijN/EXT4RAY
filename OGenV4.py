import os
import re

def get_input(prompt, default):
    """Helper function to get user input with a default value."""
    value = input(f"{prompt} (Default: {default}): ").strip()
    return int(value) if value.isdigit() else default

def generate_bad_blocks(bads_file, output_file, offset, block_size, sector_size):
    """Reads bads.txt and writes unique block allocations to bad_blocks.txt."""
    try:
        with open(bads_file, "r") as bads, open(output_file, "w") as output:
            prev_block = None  # Track the last written block to prevent duplicates

            for line in bads:
                match = re.match(r"(\d+),\s*(\d+)", line)
                if match:
                    start_lba = int(match.group(1))
                    length = int(match.group(2))

                    # Convert LBA to block allocation using correct formula
                    for lba in range(start_lba, start_lba + length):
                        block = (lba * sector_size + offset) // block_size

                        if block != prev_block:  # Skip if the same as last written
                            output.write(f"{block}\n")
                            prev_block = block  # Update previous block tracker

        print(f"✅ Bad blocks list saved to {output_file}")

    except FileNotFoundError:
        print(f"❌ Error: {bads_file} not found.")
    except Exception as e:
        print(f"❌ Error generating bad_blocks.txt: {e}")

def main():
    bads_txt = "bads.txt"
    output_txt = "bad_blocks.txt"

    # Get user inputs with defaults
    offset = get_input("Enter partition offset (bytes)", 0)
    block_size = get_input("Enter block size (bytes)", 4096)
    sector_size = get_input("Enter sector size (bytes)", 512)

    # Generate bad blocks list without duplicate entries
    generate_bad_blocks(bads_txt, output_txt, offset, block_size, sector_size)

if __name__ == "__main__":
    main()
