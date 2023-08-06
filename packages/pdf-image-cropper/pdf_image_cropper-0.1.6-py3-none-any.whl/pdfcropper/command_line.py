import sys
import os

from pdfcropper.pdf_to_png import PDF_to_PNG
from pdfcropper.config import LoadConfig
from pdfcropper.crop_png import crop_image, add_text


def main():
    if len(sys.argv) == 2:
        cfname = sys.argv[1]
        config = LoadConfig(cfname)
    else:
        raise ValueError("invalid command line input")

    for info in config.pdf_files:
        root = config.root_path
        pdf_file = os.path.join(root, info['path'])
        png_files = info['pages']
        titles = info['titles']
        p2p = PDF_to_PNG(pdf_file, png_files)
        saved_pngs = p2p.convert_pdf_pages_to_png()
        for i, png_file in enumerate(saved_pngs):
            png_file = os.path.join(root, png_file)
            crop_image(png_file, png_file)
            add_text(png_file, png_file, titles[i])



if __name__ == '__main__':
    main()
