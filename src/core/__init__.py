# 标记 core 为 Python 包
from src.core.merge import merge_pdfs
from src.core.split import split_pdf
from src.core.watermark import add_watermark
from src.core.password import verify_password
from src.core.encrypt import encrypt_pdf
from src.core.extract import extract_pages
from src.core.decrypt import decrypt_pdf


__all__ = [
    'merge_pdfs',
    'split_pdf',
    'add_watermark',
    'verify_password',
    'encrypt_pdf',
    'extract_pages',
    'decrypt_pdf',
]