import fitz  # type: ignore

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