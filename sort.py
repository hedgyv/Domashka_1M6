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

    list_name_files = list()

    suf_archives_list = list()
    suf_audio_list = list()
    suf_documents_list = list()
    suf_images_list = list()
    suf_video_list = list()
    suf_unknown_list = list()
    suf_dict_of_ext = dict()
    suf_list_of_dict = list()
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
                new_name = i.rename(Path(p_img, new_name + ext)).name
                suf_images_list.append(ext)
                list_name_files.append(new_name)
                
            elif ext == '.doc' or ext == '.docx' or ext == '.txt' or ext == '.pdf' or ext == '.xlsx' or ext == '.pptx':            
                new_name = i.rename(Path(p_docs, new_name + ext)).name   
                suf_documents_list.append(ext) 
                list_name_files.append(new_name)
                
                            
            elif ext == '.mp3' or ext == '.ogg' or ext == '.wav' or ext == '.amr': 
                new_name = i.rename(Path(p_audio, new_name + ext)).name
                suf_audio_list.append(ext)
                list_name_files.append(new_name)

            elif ext == '.avi' or ext == '.mp4' or ext == '.mov' or ext == '.mkv': 
                new_name = i.rename(Path(p_video, new_name + ext)).name
                suf_video_list.append(ext)
                list_name_files.append(new_name)

            elif ext == '.zip' or ext == '.gz' or ext == '.tar': 
                new_name = i.rename(Path(p_arhs, new_name + ext)).name
                suf_archives_list.append(ext)
                list_name_files.append(new_name)
                
                for arc in p_arhs.iterdir():
                    if arc.exists() and arc.is_file():
                        shutil.unpack_archive(arc, Path(str(p_arhs) + '/' + name_without_extension))
            else: 
                new_name = i.rename(Path(p, new_name + ext)).name
                suf_unknown_list.append(ext)
                list_name_files.append(new_name)
                

        if i.is_dir() and i.stat().st_size == 0 \
                and i.name != p_audio.name \
                    and i.name != p_arhs.name \
                        and i.name != p_img.name \
                            and i.name != p_docs.name \
                                and i.name != p_video.name:        
            shutil.rmtree(i)
    suf_dict_of_ext.update({'archives': suf_archives_list})
    suf_dict_of_ext.update({'audio': suf_audio_list}) 
    suf_dict_of_ext.update({'documents': suf_documents_list}) 
    suf_dict_of_ext.update({'images': suf_images_list})
    suf_dict_of_ext.update({'video': suf_video_list})
    suf_dict_of_ext.update({'unknown': suf_unknown_list})     

    suf_list_of_dict.append(suf_dict_of_ext)
    print(list_name_files)
    

    with open(text_file, 'w') as fh:
        #print(suf_list_of_dict)
        for elem in suf_list_of_dict:  

            #print(','.join(elem.get('documents')))
            fh.write(  
                f"{','.join(elem.get('archives'))}\n{','.join(elem.get('audio'))}\n{','.join(elem.get('documents'))}\n{','.join(elem.get('images'))}\n{','.join(elem.get('video'))}\n{','.join(elem.get('unknown'))}\n")  
        for elem in list_name_files:
            fh.write(elem + '\n')  
                 
sort_files_folders(p)

