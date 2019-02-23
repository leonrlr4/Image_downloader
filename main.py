import photo_module as m
import os

while True:
    photo_name = input('輸入要下載的關鍵字： ')
    download_num = int(input('輸入要下載的圖片數量： '))
    photo_list = m.get_photolist(photo_name, download_num)


    if photo_list == None:
        print('找不到圖片， 請換一個關鍵字再試試看')
    else:
        if len(photo_list) < download_num:
            print(f'只有找到{len(photo_list)}張')
        else:
            print('已取得所有圖片連結')
        break

folder_name = m.create_folder(photo_name)

print(f'將下載{len(photo_list)}張圖片')
print('開始下載圖片')

#'/Users/tobias/Desktop/download_pics/pics' + j[j.rfind('/'):]

try:
    # for i,j in zip(range(len(photo_list)), photo_list):
    #     #d_path = input('請輸入要保存圖片的路徑： ')
    #     m.download_pic(photo_list[i], folder_name + os.sep + photo_name + os.sep + j[j.rfind('/'):])
    m.get_photobythread(folder_name, photo_name, photo_list)
finally:
    print('下載完成！')
