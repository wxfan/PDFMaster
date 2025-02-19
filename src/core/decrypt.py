# src/ui/decrypt_current_file.py
import fitz  # type: ignore

def decrypt_pdf(input_path, output_path, password, owner_password=None):
    """
    解密PDF文件
    :param input_path: 输入文件路径
    :param output_path: 输出文件路径
    :param password: 用户密码
    :param owner_password: 所有者密码（可选）
    :raises Exception: 如果解密失败
    """
    try:
        with fitz.open(input_path) as doc:
            # Check if password is required
            if doc.is_encrypted:
                if password and doc.authenticate(password):
                    effective_pw = password
                elif owner_password and doc.authenticate(owner_password):
                    effective_pw = owner_password
                else:
                    raise Exception("密码无效，请检查输入的密码。")

            # Save the decrypted version
            doc.save(output_path)
    except mupdf_errors.DocumentError as e:
        raise Exception(f"解密PDF时出错: {str(e)}")
    except Exception as e:
        raise Exception(f"Error decrypting PDF: {str(e)}")
