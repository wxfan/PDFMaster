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
        merged_doc = fitz.open()  # 创建一个空文档
        for file_path in file_list:
            with fitz.open(file_path) as doc:
                merged_doc.insert_pdf(doc)  # 将文档插入到合并文档中
                if keep_bookmarks:
                    # 保留书签（可选）
                    pass  # TODO: 实现书签合并逻辑

        # 保存合并后的文档
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
                # 每页拆分为单独文件
                for i in range(total_pages):
                    new_doc = fitz.open()
                    new_doc.insert_pdf(doc, from_page=i, to_page=i)
                    output_path = output_dir / f"page_{i + 1:03d}.pdf"  # 使用三位数编号
                    new_doc.save(output_path)
                    new_doc.close()
                    if progress_callback:
                        progress_callback((i + 1) / total_pages)
            elif mode == "range" and page_range:
                # 按页码范围拆分
                start, end = page_range
                new_doc = fitz.open()
                new_doc.insert_pdf(doc, from_page=start - 1, to_page=end - 1)
                output_path = output_dir / f"pages_{start}-{end}.pdf"
                new_doc.save(output_path)
                new_doc.close()
    @staticmethod
    def extract_pages(input_path, output_path, page_range):
        """
        提取指定页码范围
        :param input_path: 输入文件路径
        :param output_path: 输出文件路径
        :param page_range: 页码范围，格式为 "1,3-5,7"
        """
        with fitz.open(input_path) as doc:
            new_doc = fitz.open()
            for part in page_range.split(","):
                if "-" in part:
                    start, end = map(int, part.split("-"))
                    new_doc.insert_pdf(doc, from_page=start - 1, to_page=end - 1)
                else:
                    page_num = int(part) - 1
                    new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
            new_doc.save(output_path)
            new_doc.close()
