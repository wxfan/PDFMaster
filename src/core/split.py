from pathlib import Path
import fitz  # type: ignore

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