import os
import sys
import logging
import argparse
import shutil
from datetime import datetime
import qrcode
import argparse
import uuid
import zlib


#FONCTION DE COMPRESSION 
def compress_file(input_file, output_file):
    with open(input_file, 'rb') as file_in:
        with open(output_file, 'wb') as file_out:
            compressor = zlib.compressobj()
            for chunk in iter(lambda: file_in.read(1024), b''):
                compressed_chunk = compressor.compress(chunk)
                file_out.write(compressed_chunk)
            compressed_chunk = compressor.flush()
            file_out.write(compressed_chunk)


#SI DOSSIER OUTPUT par default N'EXISTE PAS, DEMANDER à LE CREER
def create_output_directory(output_dir):
    if not os.path.exists(output_dir):
        print(f"The output directory '{output_dir}' does not exist.")
        choice = input("Do you want to create it? (y/n): ")
        if choice.lower() == 'y':
            os.makedirs(output_dir)
        else:
            print("Output directory not created. Exiting.")
            sys.exit(1)



# Function to delete a directory and its contents
def delete_directory(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            os.rmdir(dir_path)
    os.rmdir(directory)




def split_file(file_to_split, output_directory, block_size=2000):
    """Split the input file into blocks with the specified size."""
    with open(file_to_split, 'rb') as file:
        block_number = 1
        while True:
            data = file.read(block_size)
            if not data:
                break

            output_file = os.path.join(output_directory, f"{block_number}{file_to_split}")
            with open(output_file, 'wb') as outfile:
                
                block_number_in_bytes = block_number.to_bytes(1, byteorder='big')
                outfile.write(block_number_in_bytes)
                outfile.write(data)
                
                
            block_number += 1

def file_to_qrcode(file_path, output_dir):
    # # Read the file content in binary mode
    # with open(file_path, 'rb') as file:
    #     file_content = file.read()

    # # Generate the QR code
    # qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    # qr.add_data(file_content)
    # qr.make()

    # # Save the QR code as an image
    # qr.make_image().save(output_path)
        
    # Read the file contents
    with open(file_path, 'rb') as file:
        file_content = file.read()

    # Generate the QR code
    qr = qrcode.QRCode(version=40, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(file_content)
    qr.make()

    # Save the QR code as an image
    file_name = os.path.basename(file_path)
    random_filename = str(uuid.uuid4())
    #output_path = os.path.join(output_dir, f'{file_name}.png') ##pour voir si le premier byte correspond bien au numero du bloc
    output_path = os.path.join(output_dir, f'{random_filename}.png')

    qr.make_image().save(output_path)
    print(f'Successfully generated QR code for {file_name}.')


def setup_logging(logs_file):
    """Configure logging to write to the specified logs file."""
    logging.basicConfig(
        filename=logs_file,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

def main():
    parser = argparse.ArgumentParser(description='File Splitter')
    parser.add_argument('filepath', type=str, help='path to the file')
    parser.add_argument('-o', '--output-dir', type=str, default='output', help='output directory')
    parser.add_argument('-s', '--block-size', type=int, default=2000, help='block size in bytes')
    args = parser.parse_args()

    create_output_directory(args.output_dir)

    logs_file = 'file_splitter_logs.txt'
    setup_logging(logs_file)

    logging.info(f"File Splitter started: {args.filepath}")
    logging.info(f"Output Directory: {args.output_dir}")
    logging.info(f"Block Size: {args.block_size}")
    

    blocks_output_directory = 'blocks_output'
    os.mkdir(blocks_output_directory)
    compressed_file_path = args.filepath + '.gz'
    compress_file(args.filepath, compressed_file_path)
    split_file(compressed_file_path, blocks_output_directory, args.block_size)




    # Get a list of all files in the directory
    file_list = os.listdir(blocks_output_directory)

    # Generate QR code for each file
    for file_name in file_list:
        file_path = os.path.join(blocks_output_directory, file_name)
        file_to_qrcode(file_path, args.output_dir)



    logging.info("File Splitter completed.")

    delete_directory(blocks_output_directory)

if __name__ == '__main__':
    main()