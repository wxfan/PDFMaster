import fitz  # type: ignore

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