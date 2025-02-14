# PDFMaster - PDF Document Processing Tool

A powerful tool to merge, split, and extract pages from PDF documents.

## Features

- **Merge PDFs**: Combine multiple PDF files into one.
- **Split PDFs**: Split a PDF into individual pages or by page ranges.
- **Extract Pages**: Extract specific pages or page ranges from a PDF.
- **Bookmark Retention**: OPTIONALLY keep bookmarks when merging PDFs.

## Requirements

- **Python 3.8+**
- **PyQt6** (2.3.0+)
- **PyMuPDF (fitz)** (1.20.0+)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/username/PDFMaster.git
   ```

2. Install the required dependencies:
   ```bash
   pip install pyqt6 pymupdf
   ```

3. Build the application (optional):
   ```bash
   python scripts/package.py
   ```

4. Run the application:
   ```bash
   python src/main.py
   ```

## Usage

1. Add PDF files to the application either by:
   - Drag-and-drop files into the application window.
   - Using the "Add Files" option from the File menu.

2. Use the "PDF 处理" menu under the Edit menu to:
   - **Merge PDFs**: Combine selected files into one PDF.
   - **Split PDFs**: Split a selected PDF file either by individual pages or by specifying a range of pages.
   - **Extract Pages**: Extract specific pages from a selected PDF file.

3. After configuring your desired settings in the respective dialog windows, click "OK" to execute the operation.

4. The processed PDF files will be saved to the specified output directory.

## Contributing

Contributions are welcome! If you have any suggestions, find any bugs, or would like to add new features, please:

1. Fork this repository.
2. Create a new branch for your changes.
3. Commit your changes.
4. Push your changes to your fork.
5. Open a Pull Request.

Please ensure any new features or changes are discussed in an issue first.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For any questions or feedback, please reach out to us at:
- Email: support@pdfmaster.com
- GitHub Issues: [GitHub Issues](https://github.com/username/PDFMaster/issues)

## Acknowledgments

-Built with ❤️ using **PyQt6** and **PyMuPDF**.
