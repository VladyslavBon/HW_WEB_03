import os
from pathlib import Path
from shutil import move, unpack_archive
from re import sub
from threading import Thread

def normalise(string):
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u", "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    TRANS = {}

    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()

    string = string.translate(TRANS)
    string = sub(r"\W+", "_", string)
    return string

def main(folder):
    folder = Path(folder)

    os.mkdir(folder / "images")
    os.mkdir(folder / "video")
    os.mkdir(folder / "documents")
    os.mkdir(folder / "audio")
    os.mkdir(folder / "archives")
    
    images = []
    video = []
    documents = []
    audio = []
    archives = []
    
    known_extensions = set()
    unknown_extensions = set()

    for el in folder.rglob("*.*"):
        if os.path.commonpath([folder / "archives"]) == os.path.commonpath([folder / "archives", el]):
            continue
        elif os.path.commonpath([folder / "audio"]) == os.path.commonpath([folder / "audio", el]):
            continue
        elif os.path.commonpath([folder / "documents"]) == os.path.commonpath([folder / "documents", el]):
            continue
        elif os.path.commonpath([folder / "images"]) == os.path.commonpath([folder / "images", el]):
            continue
        elif os.path.commonpath([folder / "video"]) == os.path.commonpath([folder / "video", el]):
            continue
        
        if el.suffix in ['.jpeg', '.png', '.jpg', '.svg']:
            images.append(el.name)
            known_extensions.add(el.suffix)
            move(el, folder / "images")
        elif el.suffix in ['.avi', '.mp4', '.mov', '.mkv']:
            video.append(el.name)
            known_extensions.add(el.suffix)
            move(el, folder / "video")
        elif el.suffix in ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx']:
            documents.append(el.name)
            known_extensions.add(el.suffix)
            move(el, folder / "documents")
        elif el.suffix in ['.mp3', '.ogg', '.wav', '.amr']:
            audio.append(el.name)
            known_extensions.add(el.suffix)
            move(el, folder / "audio")
        elif el.suffix in ['.zip', '.gz', '.tar']:
            archives.append(el.name)
            known_extensions.add(el.suffix)
            unpack_archive(el, folder / "archives" / el.name.rsplit(".")[0])
            el.unlink()
        else:
            unknown_extensions.add(el.suffix)

    for root, dirs, files in os.walk(folder, topdown=False):
        for file in files:
            split_file = file.rsplit(".")
            trans_file = normalise(split_file[0])
            file_name = os.path.join(root, file)
            file_rename = os.path.join(root, (f"{trans_file}.{split_file[1]}"))
            os.rename(file_name, file_rename)
        for dir in dirs:
            if not os.listdir(os.path.join(root, dir)):
                os.rmdir(os.path.join(root, dir))
                continue
            trans_dir = normalise(dir)
            dir_name = os.path.join(root, dir)
            dir_rename = os.path.join(root, trans_dir)
            os.rename(dir_name, dir_rename)
            
    print("Done!")
    print(f"All known extensions in the target folder: {known_extensions}")
    print(f"All unknown extensions in the target folder: {unknown_extensions}")

if __name__ == "__main__":
    thread = Thread(target=main, args=(input("Enter path to folder: "),))
    thread.start()