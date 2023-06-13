import argparse
import os
import time
import logging

def reassemble_blocks(input_dir, output_file):
    # Get the base name and extension of the output file
    base_name, extension = os.path.splitext(os.path.basename(output_file))

    # Get a list of block files in the input directory
    block_files = [filename for filename in os.listdir(input_dir) if filename.startswith(f"{base_name}_block")]

    # Sort the block files based on the block number
    block_files.sort(key=lambda x: int(x.split('_block')[1].split('.')[0]))

    # Open the output file in binary mode for writing
    with open(output_file, 'wb') as output:
        # Reassemble the blocks into the output file
        for block_file in block_files:
            # Read the contents of the current block file
            block_path = os.path.join(input_dir, block_file)
            with open(block_path, 'rb') as block:
                block_contents = block.read()

            # Write the contents of the current block to the output file
            output.write(block_contents)

            # Log the block reassembly with time and date
            logging.info(f"Reassembled {block_file} at {time.strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    # Set up the command-line argument parser
    parser = argparse.ArgumentParser(description='Reassemble blocks into the original file.')
    parser.add_argument('input_dir', help='path to the directory containing the blocks')
    parser.add_argument('output_file', help='path to the output file')
    args = parser.parse_args()

    # Set up logging to a file
    logging.basicConfig(filename='reassemble_blocks.log', level=logging.INFO)

    # Reassemble the blocks into the original file
    reassemble_blocks(args.input_dir, args.output_file)
