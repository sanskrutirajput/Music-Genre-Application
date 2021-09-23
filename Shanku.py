
# Course_Project:   Music App(No name yet)
# Course Project Code:

import urllib.request
# import PIL
from tkinter import messagebox
from os import makedirs, mkdir, chdir, listdir, remove, removedirs, getcwd
# from shutil import rmtree
from tkinter import *
# from mutagen import mp3
from pygame import mixer
from tkinter.filedialog import askdirectory, askopenfilename
from lyrics_extractor import SongLyrics
import pygame
import pyttsx3

engine = pyttsx3.init()
pygame.init()

mixer.init()
x = 0
song_list = []
pause = False
lyrics = 0
playlist_names = []
switch = 0
path = ''
lyrics_state = False
original_btn_color = ''
temp_song_name = ''
state = False
SONG_END = pygame.USEREVENT + 1

try:
    makedirs('C:/Vibe/')
except OSError:
    playlist_names = listdir('C:/Vibe/')

if 'background_img.png' not in listdir(getcwd()):
    urllib.request.urlretrieve('https://hdwallsource.com/img/2014/11/music-wallpaper-41678-42656-hd-wallpapers.jpg',
                               "background_img.png")


def window6():
    def del_playlst():
        ans = messagebox.askyesno('Vibe',
                                  'You are deleting a playlist, this playlist cannot be retrieved, are you sure '
                                  'you want to do this?')
        print(ans)
        if ans:
            global playlist_names
            selected = lst.curselection()
            index = int(selected[0])
            print(index)

            remove(f'C:/Vibe/{playlist_names[index]}.txt')

            playlist_names = [a.split('.')[-2] for a in listdir('C:/Vibe/')]

            if state:
                playlist_box.delete(0, END)

            for i1 in [lst, custom_playlist]:
                update_list(i1, playlist_names)

            del_lib.destroy()
        else:
            del_lib.destroy()

    del_lib = Tk()
    del_lib.geometry('300x400')

    lst = Listbox(del_lib, selectmode=SINGLE)
    lst.pack(side=TOP, fill=BOTH, expand=1, padx=5, pady=(5, 0))
    Button(del_lib, text='Delete', height=1, command=del_playlst).pack(side=TOP, pady=5)

    update_list(lst, [a.split('.')[-2] for a in listdir('C:/Vibe/')])

    del_lib.mainloop()


def window5():
    def del_song_playlist():
        global song_list
        messagebox.askyesno('Vibe', 'You are deleting a playlist, this playlist cannot be retrieved, are you sure you'
                                    ' want to do this?')
        pos = del_song_lst.curselection()
        # songs = [str(song_list[i]) for i in pos]
        data.pop()
        if state:
            update_list(playlist_box, data)
        # print(playlist_names[i] for i in playlist)
        # print(songs)
        # print(playlist_names[playlist[0]])
        # f = open(f'C:/Vibe/{playlist_names[playlist[0]]}.txt', 'w')
        # f.write(f'{a}\n' for a in data)
        # f.close()
        # song_list = data.copy()
        del_song.destroy()

    playlist = custom_playlist.curselection()
    if len(playlist) != 0:
        del_song = Tk()
        del_song.geometry('300x400')

        del_song_lst = Listbox(del_song, selectmode=MULTIPLE)
        del_song_lst.pack(side=TOP, fill=BOTH, expand=1, padx=5, pady=(5, 0))
        Button(del_song, text='Delete Songs', height=1, command=del_song_playlist).pack(side=TOP, pady=5)

        f = open(f'C:/Vibe/{playlist_names[playlist[0]]}.txt', 'r')
        data = f.read().split('\n')
        data.pop(-1)
        f.close()

        print(data)

        update_list(del_song_lst, data)

        del_song.mainloop()
    else:
        messagebox.showerror('Playlist not selected', 'Please select a playlist.')


def window4():
    global song_list

    def add_song_playlist():
        pos = add_song_lst.curselection()
        songs = [str(song_list[i]) for i in pos]
        # print(playlist_names[i] for i in playlist)
        print(songs)
        print(playlist_names[playlist[0]])
        f = open(f'C:/Vibe/{playlist_names[playlist[0]]}.txt', 'a')
        f.writelines(f'{i}\n' for i in songs)
        f.close()
        add_song.destroy()

    playlist = custom_playlist.curselection()
    if len(playlist) != 0:
        add_song = Tk()
        add_song.geometry('300x400')

        add_song_lst = Listbox(add_song, selectmode=MULTIPLE)
        add_song_lst.pack(side=TOP, fill=BOTH, expand=1, padx=5, pady=(5, 0))
        Button(add_song, text='Add Songs', height=1, command=add_song_playlist).pack(side=TOP, pady=5)

        update_list(add_song_lst, song_list)

        add_song.mainloop()
    else:
        messagebox.showerror('Playlist not selected', 'Please select a playlist.')


def window2():
    def play_selected():
        global song_list, pause, x, path, state
        song_list = load_list.copy()
        print('songlist', song_list)
        playlist_box.delete(0, END)
        # for song in song_list:
        #     location = 1
        #     playlist_box.insert(END, song)
        #     location += 1

        update_list(playlist_box, song_list)

        mixer.music.stop()
        mixer.music.unload()
        pause, x = False, 0
        play()
        load.destroy()
        state = True

    pos = custom_playlist.curselection()
    if len(pos) != 0:
        playlist_name = playlist_names[pos[0]]
        # load_list = listdir(f'C:/Vibe/{playlist_name}')
        f = open(f'C:/Vibe/{playlist_name}.txt', 'r')
        load_list = f.read().split('\n')
        load_list.pop(-1)
        # load_list = a.split('/') for a in load_list
        if len(load_list[0]) == 0:
            messagebox.showerror('Empty dir', 'The playlist may be empty.')
            return
        print(len(load_list))

        f.close()

        load = Tk()
        load.geometry('300x400')

        selected_playlist = Listbox(load)
        selected_playlist.pack(side=TOP, fill=BOTH, expand=1, padx=5, pady=(5, 0))

        update_list(selected_playlist, load_list)

        Button(load, text='Play', height=1, command=play_selected).pack(side=TOP, pady=5)

        load.mainloop()
    else:
        messagebox.showerror('No Playlist Found', "Seems like you haven't selected a playlist.")


def window3():
    def del_playlst():
        ans = messagebox.askyesno('Vibe',
                                  'You are deleting a playlist, this playlist cannot be retrieved, are you sure '
                                  'you want to do this?')
        print(ans)
        if ans:
            global playlist_names
            selected = lst.curselection()
            index = int(selected[0])
            print(index)

            remove(f'C:/Vibe/{playlist_names[index]}.txt')

            playlist_names = [a.split('.')[-2] for a in listdir('C:/Vibe/')]

            if state:
                playlist_box.delete(0, END)

            for i1 in [lst, custom_playlist]:
                update_list(i1, playlist_names)

            del_lib.destroy()
        else:
            del_lib.destroy()

    del_lib = Tk()
    del_lib.geometry('300x400')

    lst = Listbox(del_lib, selectmode=SINGLE)
    lst.pack(side=TOP, fill=BOTH, expand=1, padx=5, pady=(5, 0))
    Button(del_lib, text='Delete', height=1, command=del_playlst).pack(side=TOP, pady=5)

    update_list(lst, [a.split('.')[-2] for a in listdir('C:/Vibe/')])

    del_lib.mainloop()


def window1():
    global playlist_names

    def create_dir():
        f_name = playlist.get()
        if len(f_name) == 0:
            messagebox.showerror('Vibe App', 'Please enter a valid name.')
            lib_name.destroy()
        elif f'{f_name}.txt' not in listdir('C:/Vibe/'):
            f = open(f'C:/Vibe/{f_name}.txt', 'w')
            f.close()
        else:
            messagebox.showerror('Vibe App', 'Playlist already exists.')
        custom_playlist.delete(0, 'end')
        update_playlist_dir()
        update_list(custom_playlist, playlist_names)
        lib_name.destroy()

        # try:
        #     p_name = playlist.get()
        #     mkdir(f'C:/Vibe/{p_name}')
        #     print('directory created')
        # except OSError as error:
        #     messagebox.showerror('Vibe App', error)
        # custom_playlist.delete(0, 'end')
        # update_playlist_dir()
        # update_list(custom_playlist, playlist_names)

    lib_name = Tk()
    lib_name.geometry('200x60')
    lib_name.resizable(False, False)

    playlist = Entry(lib_name)
    playlist.pack(side=TOP, fill=X, expand=1, padx=5, pady=(5, 0))
    Button(lib_name, text='Create Playlist', height=1, command=create_dir).pack(side=TOP, pady=5)

    lib_name.mainloop()


def update_list(w, l2):
    w.delete(0, END)
    for i1 in l2:
        song = i1.split('/')
        w.insert(END, song[-1])


def update_playlist_dir():
    global playlist_names
    playlist_names.clear()
    playlist_names = listdir('C:/Vibe/')
    playlist_names = [i.split('.')[-2] for i in playlist_names]
    update_list(custom_playlist, playlist_names)


def addfile():
    try:
        directory = askdirectory()
        chdir(directory)
        lst = listdir(directory)
        global song_list, state, x, pause
        song_list.clear()

        if len(song_list) > 0:
            mixer.music.stop()

        for i1 in lst:
            if 'mp3' == i1.split('.')[-1] or 'wav' == i1.split('.')[-1]:
                song_list.append(directory + '/' + i1)
        if len(song_list) == 0:
            messagebox.showerror('File not found', 'Vibe music player could not find any .mp3 or .wav files. '
                                                   'Please try again.')
        update_list(playlist_box, song_list)

        if state:
            mixer.music.stop()
            pause, x = False, 0

        play()

    except OSError as error:
        messagebox.showerror("Vibe Couldn't Load File", error)


def add_single():
    global song_list
    song_path = askopenfilename()
    print(song_path)
    if len(song_path) == 0:
        messagebox.showerror('File Not Available', 'Please select a valid file')
        return
    temp_song_path = song_path.split('/')
    print(0)
    if '.mp3' in temp_song_path[-1] or '.wav' in temp_song_path[-1]:
        print(1)
        song_list.append(song_path)
        playlist_box.delete(0, END)
        update_list(playlist_box, song_list)


def del_single():
    global song_list
    song = playlist_box.curselection()
    if len(song) == 0:
        messagebox.showerror('Song not selected', 'Please select a song.')
        return
    song_list.remove(song_list[song[0]])
    print(song_list)

    update_list(playlist_box, song_list)
    # print(0)
    # if '.mp3' in temp_path[-1] or '.wav' in temp_path[-1]:
    #     print(1)
    #     song_list.append(path)
    #
    #     playlist_box.delete(0, END)
    #     for a in song_list:
    #         pos = 1
    #         playlist_box.insert(pos, a.split('/')[-1])
    #         pos += 1
    #     mixer.music.stop()
    #     play()


def volume(vol):
    mixer.music.set_volume(int(vol) / 100)


def get_lyrics():
    global lyrics, lyrics_output, lyrics_state, original_btn_color, temp_song_name
    try:
        if not lyrics_state:
            song_name = str(song_lyrics.get())
            temp_song_name = song_name
            if len(song_name) != 0:
                lyrics_out = ''
                extract_lyrics = SongLyrics("AIzaSyBS34l_WqpgJPrKIwyzBDOWZsKYf_1gRPY", "02363b24da173245d")
                temp = extract_lyrics.get_lyrics(str(song_lyrics.get()))
                res = temp['lyrics']
                lyrics_out += str(res)
                if len(lyrics_out) != 0:
                    lyrics_state = True
                    lyrics_output = Text(banner, width=70, height=18, font=('Times New Roman', 14, 'bold'))
                    # lyrics_output.image_create(END, image=banner_img)
                    # lyrics_output.see(END)
                    lyrics_output.pack(side=TOP)
                    lyrics_output.insert(END, lyrics_out)
                    lyrics_output.config(state=DISABLED)
                    search_btn.config(bg='green')
                    lyrics = 1
                    if image.winfo_exists():
                        image.pack_forget()
        else:
            lyrics_output.pack_forget()
            image.pack()
            search_btn.config(bg=original_btn_color)
            lyrics_state = False
    except NameError:
        messagebox.showerror('Song Name Not Found',
                             "Couldn't find lyrics, please try another name, and check your network")


# def que():
#     global x
#     print('!!!!!!!!!!!!!')
#     if len(song_list) > 0:
#         state = mixer.music.get_pos()
#
#         if state == -1:
#             x += 1
#             mixer.music.load(f'{path}'+song_list[x])
#             mixer.music.play()
#         print(state)
#         que.after(1, que)


def play():
    try:
        global pause, song_list, x
        print(x, song_list)
        if not pause:
            if not mixer.music.get_busy():
                mixer.music.set_volume(0.5)
                mixer.music.load(song_list[x])
                mixer.music.play()
                play_btn.config(image=Pause_img)
                name.config(text=f"{song_list[x].split('/')[-1]}")
                mixer.music.set_endevent(SONG_END)
                update_index_color()
            else:
                mixer.music.pause()
                pause = True
                play_btn.config(image=Play_img)
        else:
            mixer.music.unpause()
            pause = False
            play_btn.config(image=Pause_img)
    except UserWarning:
        messagebox.showerror('Vibe App', 'The application ran into an error, please make sure you have selected '
                                         'valid file, and try again')


def prev():
    try:
        global x, list_box
        playlist_box.itemconfig(x, {'bg': f'{list_box}'})
        print(song_list, '\n', x)
        if x == 1 - len(song_list):
            x = 0
        else:
            x -= 1
        mixer.music.stop()
        mixer.music.load(song_list[x])
        mixer.music.set_endevent(SONG_END)
        mixer.music.play()
        play_btn.config(image=Pause_img)
        name.config(text=f"{song_list[x].split('/')[-1]}")
        update_index_color()
    except OSError:
        messagebox.showerror('Vibe App',
                             'The application ran into an error, please try restarting.')


def nxt():
    try:
        global x, song_list, list_box
        playlist_box.itemconfig(x, {'bg': f'{list_box}'})
        print(song_list)
        if x == len(song_list) - 1:
            x = 0
        else:
            x += 1
        mixer.music.stop()
        mixer.music.load(song_list[x])
        mixer.music.set_endevent(SONG_END)
        mixer.music.play()
        play_btn.config(image=Pause_img)
        name.config(text=f"{song_list[x].split('/')[-1]}")
        update_index_color()
    except OSError:
        messagebox.showerror('Vibe App',
                             'The application ran into an error, please try restarting.')


def check_end():
    global x, pause, list_box
    if not mixer.music.get_busy() and not pause:
        for event in pygame.event.get():
            if event.type == SONG_END:
                playlist_box.itemconfig(x,{'bg':list_box})
                x += 1
                pause = False
                play()


    App.after(100, check_end)


def update_index_color():
    global x
    playlist_box.itemconfig(x, {'bg': 'dark turquoise'})


# def add_single(filename):
#     filename = path.basename(filename)
#     index = 0
#     playlistbox.insert(index, filename)
#     song_list.insert(index, song)
#     index += 1


main_bg = 'black'
bg = 'gray17'
list_box = 'gray70'

App = Tk()
App.geometry(f'{App.winfo_screenwidth() - 30}x{App.winfo_screenheight() - 70}+0+0')
App.title('Vibe')
App.resizable(False, False)
# App.state('zoomed')
App["bg"] = "black"

photo = PhotoImage(file='Play.png')
Play_img = photo.subsample(3, 3)

photo = PhotoImage(file='Pause.png')
Pause_img = photo.subsample(3, 3)

photo = PhotoImage(file='Previous.png')
Previous_img = photo.subsample(3, 3)

banner_img = PhotoImage(width=700, height=400, file='banner_img2.png').subsample(1, 1)

background_img = PhotoImage(width=1266, height=620, file='background_img.png')

Next_img = PhotoImage(file='Next.png').subsample(3, 3)

label1 = Label(App, text="Welcome, User", anchor="nw", font=("Arial 8 italic", 12, 'bold', 'italic'))
label1.pack(fill=X)

# TOP frame

top_frame = Frame(App, bg=main_bg)
top_frame.pack(side=TOP, fill=X)

# LEFT_FRAME

frame1 = Frame(top_frame, height=380, width=290, bg=main_bg)
frame1.pack(side=LEFT, padx=(10, 5), pady=5)

playlist_box = Listbox(frame1, height=15, width=46, bg=list_box)
playlist_box.pack(side=TOP)

frame = Frame(frame1, bg=main_bg)
frame.pack(side=TOP, pady=(5, 5))

add_single_btn = Button(frame, text='Add', width=10, height=2, command=add_single)
add_single_btn.pack(side=LEFT, padx=(0, 5))

dirBtn = Button(frame, text="Change Directory", width=14, height=2, command=addfile)
dirBtn.pack(side=LEFT)

del_single_btn = Button(frame, text='Delete', width=10, height=2, command=del_single)
del_single_btn.pack(side=LEFT, padx=(5, 0))

custom_playlist = Listbox(frame1, height=10, width=46, bg=list_box)
custom_playlist.pack(side=TOP)

for i in listdir('C:/Vibe/'):
    custom_playlist.insert(END, i)

frame = Frame(frame1, bg=main_bg)
frame.pack(side=TOP, pady=(5, 0))

add_playlist = Button(frame, text='Add Playlist', width=10, height=2, command=window1)
add_playlist.pack(side=LEFT, padx=(0, 5))

load_playlist = Button(frame, text='Load Playlist', width=10, height=2, command=window2)
load_playlist.pack(side=LEFT)

del_playlist = Button(frame, text='Delete Playlist', width=10, height=2, command=window3)
del_playlist.pack(side=LEFT, padx=(5, 0))

frame = Frame(frame1, bg=main_bg)
frame.pack(side=TOP, pady=(5, 0))

add_songs = Button(frame, text='Add Songs', width=10, height=2, command=window4)
add_songs.pack(side=LEFT, padx=(0, 2.5))

del_songs = Button(frame, text='Del Songs', width=10, height=2, command=window5)
del_songs.pack(side=LEFT, padx=(2.5, 0))

# RIGHT_FRAME

main_frame2 = Frame(top_frame, width=f'{App.winfo_screenwidth() - 100}', bg='yellow')
main_frame2.pack(side=LEFT, padx=(5, 10), pady=(5, 0), fill=BOTH, expand=1)

# background_ = Canvas(main_frame2, height=f'{App.winfo_screenheight()-137}', bg='yellow')
# background_.pack(fill=BOTH, expand=1)
#
# frame2 = Frame(main_frame2, bg=bg, relief=SUNKEN, bd=4)
# # frame2.pack(side=LEFT, padx=(5, 10), pady=(5, 0), fill=BOTH, expand=1)
# background_.create_window(0, 0, window=frame2, anchor=NW)
# background_.create_image(0, 0, image=background_img, anchor=NW)

background_label = Label(main_frame2, image=background_img)
background_label.pack(fill=BOTH, expand=1)

print(App.winfo_screenheight() - 137, App.winfo_screenwidth() - 100)

banner = Frame(main_frame2, bg='gainsboro')
# background_.create_window(100, 100, anchor=NW, window=banner)
banner.place(x=170, y=30)

print(main_frame2.winfo_width(), main_frame2.winfo_height())

image = Canvas(banner, width=690, height=390)
image.pack(fill=BOTH, expand=1)
# background_.create_window(0, 0, window=image)
image.create_image((0, 0), image=banner_img, anchor=NW)

lyrics_output = Text(banner)

buttons = Frame(main_frame2, bg=bg)
buttons.place(x=450, y=560)
# ()
# background_.create_window(0, 0, window=buttons)

prev_btn = Button(buttons, image=Previous_img, bg=bg, activebackground=main_bg, relief=FLAT, command=prev)
prev_btn.pack(side=LEFT, padx=(0, 10))
# background_.create_window(0, 0, window=prev_btn)

play_btn = Button(buttons, image=Play_img, relief=FLAT, bg=bg, activebackground=main_bg, command=play)
play_btn.pack(side=LEFT)
# background_.create_window(0, 0, window=play_btn)

nxt_btn = Button(buttons, image=Next_img, bg=bg, activebackground=main_bg, relief=FLAT, command=nxt)
nxt_btn.pack(side=LEFT, padx=(10, 0))
# background_.create_window(0, 0, window=nxt_btn)

vol_frame = Frame(main_frame2, bg=bg)
vol_frame.place(x=750, y=570)

# Label(buttons, text='Volume: ', bg=bg, fg='white', font=('Consolas', 12)).pack(side=LEFT, padx=(160, 0))
Label(vol_frame, text='Volume: ', bg=bg, fg='white', font=('Consolas', 12)).pack(side=LEFT, padx=(
5, 0))  # background_.create_window(0, 0, window=vol_label)
volume_scale = Scale(vol_frame, orient=HORIZONTAL, from_=0, to=100, bd=0, bg=bg, showvalue=0, width=5, length=150,
                     command=volume)
volume_scale.pack(side=LEFT, padx=(0, 5))
# background_.create_window(0, 0, window=volume_scale)
volume_scale.set(50)

# time = Label(main_frame2, text='', bg=bg, fg='white', font=14)
# # time.pack(side=BOTTOM, pady=(10, 50))
# background_.create_window(100, 100, window=time)

name = Label(main_frame2, text='', bg=bg, fg='white', font=14)
name.place(x=520, y=500, anchor=CENTER)
# background_.create_window(0, 0, window=name)

lyrics_frame = Frame(App, bg=main_bg)
lyrics_frame.pack(side=BOTTOM, fill=X, expand=1)

song_lyrics = Entry(lyrics_frame, font=('Goudy Old Style', 14))
song_lyrics.pack(side=LEFT, padx=(10, 5), fill=X, expand=True)

search_btn = Button(lyrics_frame, text='Search Lyrics', command=get_lyrics)
search_btn.pack(side=RIGHT, padx=(5, 10))

original_btn_color = add_playlist.cget('background')

update_playlist_dir()
update_list(custom_playlist, playlist_names)

# if not pause:
#     check_end()

App.mainloop()
pygame.quit()
