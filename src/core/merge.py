from pathlib import Path
import fitz  # type: ignore

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
                bookmarks.extend(doc.get_outline())
            merged_doc.insert_pdf(doc)
    if keep_bookmarks:
        merged_doc.set_toc(bookmarks)
    merged_doc.save(output_path)
    merged_doc.close()
