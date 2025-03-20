import argparse
from pdf2image import convert_from_path
from PIL import Image
import os
import glob


def pdf_to_images_horizontal_with_gap(pdf_path, output_folder, pages_per_image=3, dpi=200, poppler_path=None, gap=10):
    """
    Converts a PDF file into images, merging every 'pages_per_image' pages into a single horizontal image with a gap.

    Parameters:
      pdf_path: Path to the PDF file.
      output_folder: Folder to store the output images.
      pages_per_image: Number of PDF pages per output image (default: 3).
      dpi: Resolution for PDF conversion (default: 200).
      poppler_path: Path to the Poppler installation (for Windows users if Poppler is not in the system PATH).
      gap: Horizontal gap (in pixels) between images (default: 10).
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    if poppler_path:
        pages = convert_from_path(pdf_path, dpi=dpi, poppler_path=poppler_path)
    else:
        pages = convert_from_path(pdf_path, dpi=dpi)

    total_pages = len(pages)
    image_index = 1
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]  # Get the PDF filename

    for i in range(0, total_pages, pages_per_image):
        group = pages[i:i + pages_per_image]
        num_pages = len(group)
        total_width = sum(page.width for page in group) + gap * (num_pages - 1)
        max_height = max(page.height for page in group)
        combined_image = Image.new('RGB', (total_width, max_height), color=(255, 255, 255))

        current_width = 0
        for j, page in enumerate(group):
            combined_image.paste(page, (current_width, 0))
            current_width += page.width + (gap if j < num_pages - 1 else 0)

        output_path = os.path.join(output_folder, f'{pdf_name}_output_{image_index:03d}.jpg')
        combined_image.save(output_path)
        print(f"Saved horizontal merged image: {output_path}")
        image_index += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert PDF to images with horizontal merging.')
    parser.add_argument('--dpi', type=int, default=300, help='Resolution for PDF conversion (default: 300)')
    args = parser.parse_args()

    pdf_folder = "pdfData"
    horizontal_output_folder = "output_images"
    poppler_path = None  # Windows users can set the Poppler path, e.g., r'C:\path\to\poppler\bin'
    horizontal_gap = 50  # Pixel gap between horizontal images
    pages_per_image = 3
    dpi = args.dpi

    pdf_files = sorted(glob.glob(os.path.join(pdf_folder, "*.pdf")))
    if not pdf_files:
        print("No PDF files found.")
    else:
        for pdf_path in pdf_files:
            print(f"Processing: {pdf_path}")
            pdf_to_images_horizontal_with_gap(pdf_path, horizontal_output_folder,
                                              pages_per_image=pages_per_image,
                                              dpi=dpi,
                                              poppler_path=poppler_path,
                                              gap=horizontal_gap)

    print("All processing completed!")
