from pathlib import Path
import shutil
import re

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {}

path_parent = 'C://Users/Yaroslav/OneDrive/Рабочий стол/ToSort/'
text_file = 'C://Users/Yaroslav/OneDrive/Рабочий стол/ToSort/data_written.bin'

p = Path(path_parent)
p_audio = Path(path_parent + '/' + 'audio')
p_img = Path(path_parent + '/' + 'images')
p_docs = Path(path_parent + '/' + 'documents')
p_arhs = Path(path_parent + '/' + 'archives')
p_video = Path(path_parent + '/' + 'video')


#l = Path(text_file)
#print(l)


for c, t in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = t
    TRANS[ord(c.upper())] = t.upper()
    #print(TRANS)

def normalize(name):
    
    list_names = list()     
    #print(name)
    element = name.translate(TRANS)
    symbols = re.findall('\W+', element)
    #print(element)
    #print(symbols)
    for i in symbols:
        element = element.replace(i,'_') 
        #list_names.append(element)
        
    return element


    
def sort_files_folders(p):

    # print(p)
    for i in p.iterdir():
        p_new = ''
        if i.is_dir():
            #print(i.name)
            p_new = str(i)
            sort_files_folders(Path(p_new))
        
        if i.is_file():  
            name_without_extension = i.stem
            ext = i.suffix
            new_name = normalize(name_without_extension) #передать имя каждого файла
            #print(new_name)
            if ext == '.jpeg' or ext == '.png' or ext == '.jpg' or ext == '.svg':
                i.rename(Path(p_img, new_name + ext))
            elif ext == '.doc' or ext == '.docx' or ext == '.txt' or ext == '.pdf' or ext == '.xlsx' or ext == '.pptx':            
                i.rename(Path(p_docs, new_name + ext))                
            elif ext == '.mp3' or ext == '.ogg' or ext == '.wav' or ext == '.amr': 
                i.rename(Path(p_audio, new_name + ext))
            elif ext == '.avi' or ext == '.mp4' or ext == '.mov' or ext == '.mkv': 
                i.rename(Path(p_video, new_name + ext))
            elif ext == '.zip' or ext == '.gz' or ext == '.tar': 
                i.rename(Path(p_arhs, new_name + ext))
                for arc in p_arhs.iterdir():
                    if arc.exists() and arc.is_file():
                        shutil.unpack_archive(arc, Path(str(p_arhs) + '/' + name_without_extension))
            else: 
                i.rename(Path(p, new_name + ext))

        if i.is_dir() and i.stat().st_size == 0 \
                and i.name != p_audio.name \
                    and i.name != p_arhs.name \
                        and i.name != p_img.name \
                            and i.name != p_docs.name \
                                and i.name != p_video.name:        
            shutil.rmtree(i)
        

    # with open(text_file, 'w') as fh:
    #     fh.write(i.name+'\n')    
            
                 
sort_files_folders(p)

#удалить пустые папки (непонятно) +++++
#записать инфо в файл.bin (write)
#загрузить в гитхаб (практика) +++++
#символы в имени файлах сделать как в задании сказано (replace) +++++