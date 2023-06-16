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
from pyzbar import pyzbar

import qrcode
from PIL import Image
import argparse
from pyzbar.pyzbar import decode
from PIL import Image


# # # # file_path = "output_file.gz"

# # # # with open(file_path, "rb") as file:
# # # #     # Read the first byte
# # # #     first_byte = file.read(1)



# # # # # Convert the first byte to an integer
# # # # integer_value = int.from_bytes(first_byte, byteorder='big')

# # # # print(integer_value)



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





def setup_logging(logs_file):
    """Configure logging to write to the specified logs file."""
    logging.basicConfig(
        filename=logs_file,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )







def qrcode_to_file(qrcode_path, output_path):
    # Load the QR code image
    qr_image = Image.open(qrcode_path)

    # Convert the image to grayscale
    qr_image = qr_image.convert('L')

    # Decode the QR code
    qr_codes = pyzbar.decode(qr_image)

    if qr_codes:
        # Get the decoded content from the first QR code
        qr_content = qr_codes[0].data

        # Save the decoded content to a file
        with open(output_path, 'wb') as file:
            file.write(qr_content)
    else:
        print("No QR code found in the image.")






def main():
    parser = argparse.ArgumentParser(description='File Assembler')
    parser.add_argument('directory_path', type=str, help='path to the directory with the qr codes')
    parser.add_argument('-o', '--output-dir', type=str, default='filesoutput', help='output directory')
    args = parser.parse_args()


    logs_file = 'file_assembler_logs.txt'
    setup_logging(logs_file)

    logging.info(f"File assembler started:")
    logging.info(f"Output Directory: {args.output_dir}")
    

    create_output_directory(args.output_dir)



    my_files = []

    # Get a list of all files in the directory
    file_list = os.listdir(args.directory_path)

    # Generate QR code for each file
    for file_name in file_list:
        file_path = os.path.join(args.directory_path, file_name)
        # print(file_path)
        # print(f"filesoutput\{file_name}.gz"'')
        qrcode_to_file(file_path, f"filesoutput\{file_name}.gz"'')
        
        ff = f"filesoutput\{file_name}.gz"''
        with open(ff, "rb") as file:
            print(ff)
            # Read the first byte
            first_byte = file.read(1)
            integer_value = int.from_bytes(first_byte, byteorder='big')
            print(integer_value)
            number_and_filename = {ff : integer_value}
            my_files.append(number_and_filename)
            
    print(my_files)




        # Convert the first byte to an integer

    # for filename in os.listdir(args.directory_path):
    #     file_path = os.path.join(args.directory_path, filename)
    #     qrcode_to_file(file_path, args.output_dir)










    logging.info("File assembler completed.")

if __name__ == '__main__':
    main()



#     return binary_data

# def save_binary_data(binary_data, output_path):
#     if binary_data is None:
#         return

#     with open(output_path, 'wb') as file:
#         file.write(binary_data.encode('utf-8'))

# # Usage example
# png_path = 'output/00e95714-f181-4093-af0e-1ac0ab12df2d.png'
# output_path = 'output_file.gz'

# binary_data = decode_qr_code(png_path)
# save_binary_data(binary_data, output_path)


