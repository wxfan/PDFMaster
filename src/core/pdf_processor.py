from pathlib import Path
import fitz  # type: ignore

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
