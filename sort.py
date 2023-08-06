import os
import shutil
import logging
from time import time

from concurrent.futures import ThreadPoolExecutor

FILE_EXTENTION = {
    "Archives": ["ZIP", "GZ", "TAR", 'RAR', '7Z', 'TGZ', 'ISO', 'JAR', 'BZ2'],
    "Video": ["AVI", "MP4", "MOV", "MKV", 'FLV', 'MPEG', '3GP', 'WEBM', 'VOB', 'DIVX'],
    "Audio": ["MP3", "OGG", "WAV", "AMR"],
    "Documents": ["DOC", "DOCX", "TXT", "PDF", "XLSX", "XLS", "PPTX","CAD", "DWG", "ODG", "ODT", "HTML", "URL"],
    "Images": ["JPEG", "PNG", "JPG", "SVG"]
    }



class SortFile:
    def __init__(self, path):
        self.path = path
    
    def remove_folder(self) -> None:
        folder = 'f{self.path}\\New_folder'
        shutil.rmtree(folder)

    def move_file(self, file_path) -> None:
        file_name = os.path.basename(file_path)
        file_extension = self.extension(os.path.splitext(file_name)[1][1:].upper())
        destination_folder = os.path.join(self.path, file_extension)
        os.makedirs(destination_folder, exist_ok=True)

        destination_path = os.path.join(destination_folder, file_name)
        shutil.copy(file_path, destination_path)
        os.remove(file_path)
        self.remove_folder()
    
    def extension(self, ext: str, dictionary=FILE_EXTENTION) -> str:
        for key, extensions_list in dictionary.items():
            if ext in extensions_list:
                return key
        return 'Others'

    def thread(self) -> None:
        logging.basicConfig(level=logging.DEBUG, filename="programm.log",
                            format="%(asctime)s - %(levelname)s - %(message)s")

        with ThreadPoolExecutor() as executor:
            for root, _, files in os.walk(self.path):
                for file in files:
                    file_path = os.path.join(root, file)
                    executor.submit(self.move_file, file_path)
        logging.debug("Programm *sort.py* successfully completed")


if __name__ == "__main__":
    start_count = time()
    sort = SortFile('C:\\Users\\Bianchi\\Desktop\\Мотлох')
    sort.thread()
    finish_count = time()
    print('{:2f} seconds'.format(finish_count - start_count))