import os
from pathlib import Path
from shutil import move, unpack_archive
from threading import Thread
import logging

def sort(el, folder):
        if el.suffix in ['.jpeg', '.png', '.jpg', '.svg']:
            move(el, folder / "images")
            logging.debug("Finished task")
        elif el.suffix in ['.avi', '.mp4', '.mov', '.mkv']:
            move(el, folder / "video")
            logging.debug("Finished task")
        elif el.suffix in ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx']:
            move(el, folder / "documents")
            logging.debug("Finished task")
        elif el.suffix in ['.mp3', '.ogg', '.wav', '.amr']:
            move(el, folder / "audio")
            logging.debug("Finished task")
        elif el.suffix in ['.zip', '.gz', '.tar']:
            unpack_archive(el, folder / "archives" / el.name.rsplit(".")[0])
            el.unlink()
            logging.debug("Finished task")
        else:
            move(el, folder / "unknown")
            logging.debug("Finished task")

def main():
    folder = Path(input("Enter path to folder: "))
    
    os.mkdir(folder / "images")
    os.mkdir(folder / "video")
    os.mkdir(folder / "documents")
    os.mkdir(folder / "audio")
    os.mkdir(folder / "archives")
    os.mkdir(folder / "unknown")

    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')
    for el in folder.rglob("*.*"):
        if not any(folders in str(el) for folders in ["audio", "video", "images", "documents", "archives", "unknown"]):
            thread = Thread(target=sort, args=(el, folder,))
            thread.start()

    for root, dirs, _ in os.walk(folder, topdown=False):
        for dir in dirs:
            if not os.listdir(os.path.join(root, dir)):
                os.rmdir(os.path.join(root, dir))
                continue

if __name__ == "__main__":
    main()