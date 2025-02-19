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
            # 检查文档是否加密
            if doc.is_encrypted:
                # 尝试使用用户密码认证
                if password and doc.authenticate(password):
                    effective_pw = password
                # 如果用户密码无效，尝试使用所有者密码
                elif owner_password and doc.authenticate(owner_password):
                    effective_pw = owner_password
                else:
                    raise Exception("密码无效，请检查输入的密码。")
            
            # 保存解密后的版本
            doc.save(output_path)
    except fitz.FileDataError as e:
        raise Exception(f"解密PDF时出错: {str(e)}")
    except Exception as e:
        raise Exception(f"解密PDF时出错: {str(e)}")