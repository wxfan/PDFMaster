from pathlib import Path
import fitz  # type: ignore
from io import BytesIO
from PIL import Image, ImageEnhance
import os

def add_watermark(
    input_path,
    output_dir,
    watermark_text=None,
    watermark_image_path=None,
    rotation=0,
    opacity=1.0,
    position=(0, 0)
):
    """
    Add watermark to PDF file
    :param input_path: Path to the input PDF
    :param output_dir: Output directory for watermarked files
    :param watermark_text: Text to use as watermark
    :param watermark_image_path: Path to image for watermark
    :param rotation: Rotation angle for the watermark
    :param opacity: Opacity of the watermark (0-1)
    :param position: Position (x, y) to place the watermark
    """
    if not watermark_text and not watermark_image_path:
        raise ValueError("Please provide either text or image for the watermark")

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        # Enhanced opening of PDF with additional parameters
        doc = fitz.open(input_path, noWarn=True, is_extractable=True)
        
        # Check if document is valid and has pages
        if doc is None or doc.page_count == 0:
            raise ValueError("PDF 文件为空或已损坏，请检查文件并重试")

        # Process each page with error handling
        for page_num in range(doc.page_count):
            try:
                page = doc.load_page(page_num)
                rect = page.rect

                # Create an overlay page for the watermark
                overlay = fitz.open()[0]
                overlay.set_rotation(rotation)

                if watermark_text:
                    text_color = (0, 0, 0, int(255 * opacity))
                    overlay.insert_text(
                        position,
                        watermark_text,
                        fontsize=20,
                        fontname="helv",
                        fontflags=0,
                        color=text_color,
                        rotate=rotation,
                    )

                if watermark_image_path:
                    img = Image.open(watermark_image_path)
                    img = ImageEnhance.Brightness(img).enhance(opacity)
                    img = img.rotate(rotation, expand=True)
                    img_bytes = BytesIO()
                    img.save(img_bytes, format='PNG')
                    img_pixmap = fitz.Pixmap(img_bytes.getvalue())

                    img_rect = fitz.Rect(
                        position[0], position[1],
                        position[0] + img.width, position[1] + img.height
                    )
                    overlay.insert_image(img_rect, pixmap=img_pixmap)

                # Combine original page and overlay
                combined_page = fitz.Page(rect)
                combined_page.show_pdf_page(rect, doc, page_num)
                combined_page.show_pdf_page(rect, overlay)

                # Add the combined page to the modified document
                doc.insert_page(-1, combined_page)

            except Exception as page_error:
                print(f"页面 {page_num + 1} 处理失败: {str(page_error)}")
                continue

        # Save the modified document
        output_path = os.path.join(output_dir, "watermarked.pdf")
        doc.save(output_path)
        doc.close()

    except ValueError as ve:
        print(f"无效操作: {str(ve)}")
        raise
    except Exception as e:
        # Detailed error logging
        print(f"添加水印失败: {str(e)}")
        raise
