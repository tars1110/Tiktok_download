import re
import os
import tkinter as tk
import requests
from PIL import Image, ImageTk

header = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36"}

def videos(surl):
    print('正在解析视频链接')
    if len(surl) > 60:
        id = re.search(r'video/(\d.*)/', surl).group(1)
    else:
        id = re.search(r'video/(\d.*)', surl).group(1)

    u_id = "https://m.douyin.com/web/api/v2/aweme/iteminfo/?item_ids={}&a_bogus=".format(id)
    v_rs = requests.get(url=u_id, headers=header).json()

    titles = re.search(r'^(.*?)[；;。.#]', v_rs['item_list'][0]['desc']).group(1)

    if not os.path.exists('video'):
        os.makedirs('video')

    req = v_rs['item_list'][0]['video']['play_addr']['uri']

    print('正在下载无水印视频')

    v_url = "https://www.douyin.com/aweme/v1/play/?video_id={}".format(req)
    v_req = requests.get(url=v_url, headers=header).content

    with open(f'video/{titles}.mp4', 'wb') as f:
        f.write(v_req)



def pics(surl):
    result_label.config(text="正在解析图片链接")

    if len(surl) > 60:
        pid = re.search(r'note/(\d.*)/', surl).group(1)
    else:
        pid = re.search(r'note/(\d.*)', surl).group(1)

    p_id = "https://m.douyin.com/web/api/v2/aweme/iteminfo/?reflow_source=reflow_page&item_ids={}&a_bogus=".format(pid)

    p_rs = requests.get(url=p_id, headers=header).json()

    images = p_rs['item_list'][0]['images']

    ptitle = re.search(r'^(.*?)[；;。.#]', p_rs['item_list'][0]['desc']).group(1)

    if not os.path.exists('pic'):
        os.makedirs('pic')

    if not os.path.exists(f'pic/{ptitle}'):
        os.makedirs(f'pic/{ptitle}')
    result_label.config(text="正在下载无水印图片")

    for i, im in enumerate(images):
        p_req = requests.get(url=im['url_list'][0]).content
        with open(f'pic/{ptitle}/{str(i + 1)}.jpg', 'wb') as f:
            f.write(p_req)
def show_images():
    image_path1 = "pic0.jpg"
    image_path2 = "pic1.jpg"

    img1 = Image.open(image_path1)
    img2 = Image.open(image_path2)

    img1 = img1.resize((306, 410))
    img2 = img2.resize((306, 410))

    new_window = tk.Toplevel(root)
    new_window.title("链接获取指南")

    photo1 = ImageTk.PhotoImage(img1)
    photo2 = ImageTk.PhotoImage(img2)

    label1 = tk.Label(new_window, image=photo1)
    label1.image = photo1
    label1.pack(side=tk.LEFT)

    label2 = tk.Label(new_window, image=photo2)
    label2.image = photo2
    label2.pack(side=tk.RIGHT)

def download_content():
        shares = entry.get()
        share = re.search(r'/v.douyin.com/(.*?)/', shares)

        if share:
            share = share.group(1)
            share_url = "https://v.douyin.com/{}/".format(share)
            s_html = requests.get(url=share_url, headers=header)
            surl = s_html.url

            if re.search(r'/video', surl):
                videos(surl)
                print("视频下载完成")
                result_label.config(text='视频下载完成')
            elif re.search(r'/note', surl):
                pics(surl)
                print("图片下载完成")
                result_label.config(text='图片下载完成')
            else:
                result_label.config(text='解析失败')
        else:
            result_label.config(text='链接不正确')


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("600x140")
    root.title("抖音视频图文无水印下载")

    input_label = tk.Label(root, text="请输入移动端分享链接：")
    input_label.place(x =230, y = 10)

    entry = tk.Entry(root, width=80)
    entry.place(x = 20, y = 45)

    download_button = tk.Button(root, text="下载", command=download_content)
    download_button.place(x = 270, y = 75)

    result_label = tk.Label(root, text="")
    result_label.place(x = 255, y = 110)

    show_images_button = tk.Button(root, text="链接获取指南", command=show_images)
    show_images_button.place(x = 500, y = 75)
       
    root.mainloop()