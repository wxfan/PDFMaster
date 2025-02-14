from pathlib import Path
import fitz  # type: ignore
from io import BytesIO
from PIL import Image, ImageEnhance
import os

class PDFProcessor:
    @staticmethod
    def merge_pdfs(file_list, output_path, keep_bookmarks=True):
        """
        合并多个 PDF 文件
        :param file_list: 要合并的文件路径列表
        :param output_path: 输出文件路径
        :param keep_bookmarks: 是否保留书签
        """
        merged_doc = fitz.open()
        bookmarks = []
        for file_path in file_list:
            with fitz.open(file_path) as doc:
                if keep_bookmarks:
                    bookmarks.extend(doc.get_toC())
                merged_doc.insert_pdf(doc)
        if keep_bookmarks:
            merged_doc.set_toc(bookmarks)
        merged_doc.save(output_path)
        merged_doc.close()
    @staticmethod
    def split_pdf(input_path, output_dir, mode="single", page_range=None, progress_callback=None):
        """
        拆分 PDF 文件
        :param input_path: 输入文件路径
        :param output_dir: 输出目录
        :param mode: 拆分模式 ("single" 或 "range")
        :param page_range: 页码范围，格式为 (start, end)
        :param progress_callback: 进度回调函数，接受一个0-1之间的浮点数
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        with fitz.open(input_path) as doc:
            total_pages = len(doc)
            if mode == "single":
                for i in range(total_pages):
                    new_doc = fitz.open()
                    new_doc.insert_pdf(doc, from_page=i, to_page=i)
                    output_path = output_dir / f"page_{i + 1:03d}.pdf"
                    progress = (i + 1) / total_pages
                    new_doc.save(output_path)
                    new_doc.close()
                    if progress_callback:
                        progress_callback(progress)
            elif mode == "range":
                if not page_range or len(page_range) != 2:
                    raise ValueError("Invalid page range")
                start, end = max(0, page_range[0] - 1), min(total_pages - 1, page_range[1] - 1)
                new_doc = fitz.open()
                new_doc.insert_pdf(doc, from_page=start, to_page=end)
                output_path = output_dir / f"pages_{start + 1}-{end + 1}.pdf"
                new_doc.save(output_path)
                new_doc.close()
                if progress_callback:
                    progress_callback(1.0)
    @staticmethod
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
            with fitz.open(input_path) as doc:
                total_pages = doc.page_count
                if total_pages == 0:
                    raise ValueError("The PDF document is empty or damaged")

                for page_num in range(total_pages):
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

                    # Save the modified page
                    output_path = os.path.join(
                        output_dir,
                        f"page_{page_num + 1:03d}_watermarked.pdf"
                    )
                    new_doc = fitz.open()
                    new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
                    new_doc.save(output_path)
                    new_doc.close()

        except Exception as e:
            # Log any exceptions to help with debugging
            print(f"Error adding watermark: {str(e)}")
            raise

    @staticmethod
    def verify_password(pdf_path, password):
        """
        验证PDF密码
        :param pdf_path: PDF文件路径
        :param password: 密码字符串
        :return: bool 是否成功验证
        """
        try:
            with fitz.open(pdf_path, password=password):
                return True
        except fitz.PasswordError:
            return False
        except Exception as e:
            print(f"验证密码时出错: {str(e)}")
            return False

    @staticmethod
    def encrypt_pdf(input_path, output_path, password):
        """
        给PDF文件加密
        :param input_path: 输入文件路径
        :param output_path: 输出文件路径
        :param password: 加密密码
        """
        try:
            with fitz.open(input_path) as doc:
                doc.save(
                    output_path,
                    encryption=fitz.PDF_ENCRYPT_V4,  # 使用AES-256加密
                    user_pw=password,
                    permissions=fitz.PDF_PERMISSIONS_NONE  # 禁止所有修改和打印
                )
        except Exception as e:
            print(f"加密PDF时出错: {str(e)}")
            raise

    @staticmethod
    def extract_pages(input_path, output_path, page_range):
        """
        提取指定页码范围
        :param input_path: 输入文件路径
        :param output_path: 输出文件路径
        :param page_range: 页码范围，格式为 "1,3-5,7"
        """
        ranges = []
        try:
            for part in page_range.split(","):
                if "-" in part:
                    start, end = map(int, part.split("-"))
                    ranges.extend(list(range(start-1, end)))
                else:
                    ranges.append(int(part) - 1)

            with fitz.open(input_path) as doc:
                new_doc = fitz.open()
                for page_num in ranges:
                    if page_num < 0 or page_num >= len(doc):
                        raise ValueError("Invalid page number")
                    new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
                new_doc.save(output_path)
                new_doc.close()
        except Exception as e:
            raise e
