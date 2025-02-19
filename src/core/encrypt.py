import fitz  # type: ignore

def encrypt_pdf(input_path, output_path, password):
    """
    给PDF文件加密
    :param input_path: 输入文件路径
    :param output_path: 输出文件路径
    :param password: 加密密码
    """
    try:
        with fitz.open(input_path) as doc:
            # Set standard permissions and encryption
            permissions = (
                fitz.PDF_PERM_COPY |        # 允许复制内容
                fitz.PDF_PERM_PRINT |      # 允许打印
                fitz.PDF_PERM_ANNOTATE     # 允许添加注释
            )
            doc.save(
                output_path,
                encryption=fitz.PDF_ENCRYPT_AES_256,  # 使用AES-256加密
                user_pw=password,
                owner_pw=password,  # 必须设置所有者密码以防止加密问题
                permissions=permissions
            )
    except Exception as e:
        print(f"加密PDF时出错: {str(e)}")
        raise

