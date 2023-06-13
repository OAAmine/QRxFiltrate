import argparse
import os
import time
import logging

def split_file(file_path, block_size, output_dir):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Get the original filename and extension
    file_name = os.path.basename(file_path)
    base_name, extension = os.path.splitext(file_name)

    # Open the file in binary mode for reading
    with open(file_path, 'rb') as file:
        # Read the file contents
        contents = file.read()

        # Calculate the number of blocks needed
        num_blocks = len(contents) // block_size
        if len(contents) % block_size != 0:
            num_blocks += 1

        # Split the file into blocks and write each block to a separate file
        for block_num in range(num_blocks):
            # Calculate the start and end indices of the current block
            start_index = block_num * block_size
            end_index = start_index + block_size

            # Extract the current block from the contents
            block = contents[start_index:end_index]

            # Create a filename for the current block with the block number appended
            block_filename = f"{base_name}_block{block_num}{extension}"

            # Write the block to a separate file in the output directory
            block_path = os.path.join(output_dir, block_filename)
            with open(block_path, 'wb') as block_file:
                block_file.write(block)

            # Log the block creation with time and date
            logging.info(f"Created {block_filename} at {time.strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    # Set up the command-line argument parser
    parser = argparse.ArgumentParser(description='Split a file into multiple blocks.')
    parser.add_argument('file', help='path to the input file')
    parser.add_argument('--block-size', type=int, default=1024, help='size of each block in bytes (default: 1024)')
    parser.add_argument('--output-dir', default='output', help='output directory for the blocks (default: "output")')
    args = parser.parse_args()

    # Set up logging to a file
    logging.basicConfig(filename='split_file.log', level=logging.INFO)

    # Split the file into blocks
    split_file(args.file, args.block_size, args.output_dir)
