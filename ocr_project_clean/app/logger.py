from quality_logger import QualityLogger
from log_decorators import log_ocr_operation


logger = QualityLogger(log_dir="logs", log_level="INFO")


def on_exit(root):
    import shutil, os
    from datetime import datetime

    dir_path = 'captured'
    try:
        if os.path.isdir(dir_path):
            shutil.rmtree(dir_path, ignore_errors=True)
            logger.log_file_generation("清理", "captured目录", "删除临时文件目录")
    finally:
        logger.log_file_generation("程序", "退出", "清理资源并退出")
        root.destroy()


