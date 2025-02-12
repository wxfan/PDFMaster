# -*- mode: python ; coding: utf-8 -*-

# 导入 PyInstaller 所需模块
from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT

# 加密配置（可选）
block_cipher = None

# 分析阶段：指定入口文件和依赖项
a = Analysis(
    ['src/main.py'],  # 入口文件
    pathex=[],  # 添加额外的搜索路径
    binaries=[],  # 添加二进制文件（如 DLL、SO 等）
    datas=[
        ('src/resources', 'resources'),  # 将资源文件打包到输出目录的 resources 文件夹
    ],
    hiddenimports=[],  # 显式指定隐藏的依赖项
    hookspath=[],  # 自定义钩子路径
    hooksconfig={},  # 钩子配置
    runtime_hooks=[],  # 运行时钩子
    excludes=[],  # 排除不需要的模块
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,  # 加密配置
)

# 打包 Python 字节码
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# 配置可执行文件
exe = EXE(
    pyz,  # 打包后的字节码
    a.scripts,  # 入口脚本
    [],  # 排除的二进制文件
    exclude_binaries=True,  # 是否排除二进制文件
    name='PDFMaster',  # 可执行文件名称
    debug=False,  # 是否启用调试模式
    bootloader_ignore_signals=False,  # 是否忽略信号
    strip=False,  # 是否剥离调试信息
    upx=True,  # 是否使用 UPX 压缩
    console=False,  # 是否显示控制台窗口（False 表示无控制台）
    disable_windowed_traceback=False,  # 是否禁用窗口化程序的错误跟踪
    argv_emulation=False,  # 是否启用 macOS 的 argv 模拟
    target_arch=None,  # 目标架构（None 表示自动检测）
    codesign_identity=None,  # macOS 签名标识
    entitlements_file=None,  # macOS 权限文件
)

# 收集所有文件并生成最终输出
coll = COLLECT(
    exe,  # 可执行文件配置
    a.binaries,  # 二进制文件
    a.zipfiles,  # ZIP 文件
    a.datas,  # 数据文件
    strip=False,  # 是否剥离调试信息
    upx=True,  # 是否使用 UPX 压缩
    upx_exclude=[],  # 排除 UPX 压缩的文件
    name='PDFMaster_Windows_Linux',  # 输出目录名称
)
