# Usage: - python3 get-gdrive-images.py
#        - select images.csv - sku,images(separated with ", ") & columns separator:";"
#        - select pictures dir

import sys
import gdown

def download_images(csv_path, img_directory):
    csv_file = open( csv_path, 'r' )
    img_count = 0
    row = 0
    new_csv_content = "sku,images\n"
    for line in csv_file:

        line_arr = line.split(';')
        sku = line_arr[0]
        urls = line_arr[1]
        urls_arr = urls.split(', ')

        new_csv_content += sku + ","
        
        count = 1
        for url in urls_arr:
            new_csv_img_filename = ''
            url = url.strip().replace('"', '')
            # Transform from google drive view URL to download URL
            url = url.replace('https://drive.google.com/file/d/', 'https://drive.google.com/uc?export=download&id=').replace('/view?usp=sharing', '')

            if (count == 1) :
                filename = img_directory + '/' + sku + '.jpg'
                new_csv_img_filename += sku + '.jpg'
            else :
                filename = img_directory + '/' + sku + '_' + str(count) + '.jpg'
                new_csv_img_filename += '|' + sku + '_' + str(count) + '.jpg'

            count += 1

            try:
                gdown.download(url, filename, quiet=False)
                new_csv_content += new_csv_img_filename
                img_count += 1
                row += 1
                print("\n" + str( img_count ) + '/' + str( row ) + ' images downloaded.')
            except:
                row += 1
                pass
        
        new_csv_content += "\n"

    new_csv_file = open( csv_path.replace('.csv', '-new.csv'), 'w' )
    new_csv_file.write(new_csv_content)
    new_csv_file.close()
    
    
    print("\n" + str( img_count ) + '/' + str( row ) + ' images downloaded.')


if __name__ == "__main__":
    # show gui for selecting csv file & image directory
    import tkinter as tk
    from tkinter import filedialog
    # display main window
    root = tk.Tk()
    root.withdraw()
    # ask for csv file
    csv_path = filedialog.askopenfilename(title="Select csv file", filetypes=[("csv files", "*.csv")])
    # ask for image directory
    img_directory = filedialog.askdirectory(title="Select image directory")
    # download images
    download_images(csv_path, img_directory)
