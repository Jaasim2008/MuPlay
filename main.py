from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from json_manager import *
from pygame import mixer
from pytube import YouTube
from moviepy.video.io.VideoFileClip import VideoFileClip
import threading as thr

root = Tk()
root.title('MuPlay [vs1]')
root.geometry('400x500')
root.resizable(False, False)
my_icon = PhotoImage(file='ast/MuPlay_logo.png')
root.iconphoto(False, my_icon)
dark = '#3d3d3d'
my_font = 'Segoe UI Bold Italic'
root.config(bg=dark)

main_frame = Frame(root, bg=dark)
main_frame.pack(fill=BOTH, expand=True)

start_frame = Frame(root, bg=dark)


def download_song():
    dwn_frame = Frame(root, bg=dark)
    main_frame.pack_forget()
    dwn_frame.pack(fill=BOTH, expand=True)

    lbl30 = Label(dwn_frame, text='Enter Youtube Video URL : ', bg=dark, fg='white',
                  font=(my_font, 20))
    lbl30.pack(pady=10)

    def return_to_main():
        dwn_frame.pack_forget()
        main_frame.pack(fill=BOTH, expand=True)

    def on_enter4(e):
        btn30['fg'] = 'orange'
        btn30['bg'] = dark

    def on_leave2(e):
        btn30['fg'] = 'white'
        btn30['bg'] = dark

    btn30 = Button(dwn_frame, text='<-- Back', relief=FLAT, bd=0, bg=dark, fg='white',
                   font=(my_font, 20), activebackground=dark, activeforeground='orange',
                   command=return_to_main)
    btn30.pack(side=BOTTOM, pady=5)
    btn30.bind('<Enter>', on_enter4)
    btn30.bind('<Leave>', on_leave2)

    ent30 = Entry(dwn_frame, bg=dark, bd=1, fg='white', width=50)
    ent30.pack(pady=10)

    def play_song_ui():
        download_frame = Frame(root, bg=dark)
        main_frame.pack_forget()
        dwn_frame.pack_forget()
        download_frame.pack(fill=BOTH, expand=True)

        messagebox.showinfo('Downloaded Song!', 'Song Downloaded at '
                                                '~/musicsong/downloadedMusic/')

        def start_playing_music():
            def play_music_cmd():
                mixer.init()
                mixer.music.load('musicsong/downloadedMusic/my_audio.mp3')
                mixer.music.play()

            func = thr.Thread(target=play_music_cmd)
            func.start()

        def stop_music():
            mixer.init()
            mixer.music.stop()

        global paused_if
        paused_if = False

        def pause_music(is_paused):
            global paused_if
            paused_if = is_paused
            if paused_if:
                mixer.music.unpause()
                paused_if = False
            else:
                mixer.music.pause()
                paused_if = True

        play_logo_inactive = PhotoImage(file='ast/play_logo.png')
        play_logo_active = PhotoImage(file='ast/play_logo_act.png')
        pause_logo_inactive = PhotoImage(file='ast/pause_logo.png')
        pause_logo_active = PhotoImage(file='ast/pause_logo_act.png')
        stop_logo_inactive = PhotoImage(file='ast/stop_logo.png')
        stop_logo_active = PhotoImage(file='ast/stop_logo_act.png')

        def on_ent5(e):
            lbl20_play['image'] = play_logo_active

        def on_ent6(e):
            lbl21_pause['image'] = pause_logo_active

        def on_ent7(e):
            btn22['image'] = stop_logo_active

        def on_ent8(e):
            btn23['fg'] = 'orange'
            btn23['bg'] = dark

        def on_lv(e):
            lbl21_pause['image'] = pause_logo_inactive
            lbl20_play['image'] = play_logo_inactive
            btn22['image'] = stop_logo_inactive
            btn23['fg'] = 'white'
            btn23['bg'] = dark

        lbl20_play = Button(download_frame, image=play_logo_inactive, command=start_playing_music,
                            bd=0, relief=SOLID, highlightthickness=0)
        lbl20_play.pack(pady=20)

        lbl20_play.bind('<Enter>', on_ent5)
        lbl20_play.bind('<Leave>', on_lv)

        lbl21_pause = Button(download_frame, image=pause_logo_inactive, command=lambda: pause_music(paused_if),
                             bd=0, highlightthickness=0)
        lbl21_pause.pack(pady=20)

        lbl21_pause.bind('<Enter>', on_ent6)
        lbl21_pause.bind('<Leave>', on_lv)

        btn22 = Button(download_frame, image=stop_logo_inactive,
                       highlightthickness=0, bd=0, relief=SOLID, command=stop_music)
        btn22.pack(pady=20)

        btn22.bind('<Enter>', on_ent7)
        btn22.bind('<Leave>', on_lv)

        def return_to_start():
            stop_music()
            download_frame.pack_forget()
            dwn_frame.pack_forget()
            start_frame.pack_forget()
            main_frame.pack(fill=BOTH, expand=True)

        btn23 = Button(download_frame, text='<-- Back',
                       bd=0, relief=SOLID, command=return_to_start,
                       bg=dark, fg='white', font=(my_font, 10), highlightthickness=0)
        btn23.pack(side=BOTTOM, pady=5)

        btn23.bind('<Enter>', on_ent8)
        btn23.bind('<Leave>', on_lv)

    def vid_to_aud_conv():
        mp4_file_dir = 'musicsong/downloadedMusic/my_video.mp4'
        mp3_file_dir = 'musicsong/downloadedMusic/my_audio.mp3'

        videoClip = VideoFileClip(mp4_file_dir)
        audioClip = videoClip.audio
        audioClip.write_audiofile(mp3_file_dir)
        audioClip.close()
        videoClip.close()
        play_song_ui()

    def download_video():
        vid_url = ent30.get()
        my_vid = YouTube(vid_url)
        my_vid = my_vid.streams.get_highest_resolution()
        my_vid.download(output_path='musicsong/downloadedMusic',
                        filename='my_video.mp4')
        vid_to_aud_conv()

    btn31 = Button(dwn_frame, text='Download & Play', relief=FLAT, bd=0, bg=dark, fg='white',
                   font=(my_font, 20), activebackground=dark, activeforeground='orange',
                   command=download_video)
    btn31.pack(pady=10, side=BOTTOM)


def play_custom_music():
    sub_frame = Frame(root, bg=dark)
    start_frame.pack_forget()
    sub_frame.pack(fill=BOTH, expand=True)

    file_dir = filedialog.askopenfilename(title='Choose Your Song ( .mp3 only )',
                                          filetypes=(("MP3 Files", "*.mp3"),))

    if file_dir == '':
        messagebox.showerror('Error!', 'Please Choose a File To Continue')
        sub_frame.pack_forget()
        start_frame.pack(fill=BOTH, expand=True)
    else:

        def start_playing_music():
            def play_music_cmd():
                mixer.init()
                mixer.music.load(file_dir)
                mixer.music.play()

            func = thr.Thread(target=play_music_cmd)
            func.start()

        def stop_music():
            mixer.init()
            mixer.music.stop()

        global paused_if
        paused_if = False

        def pause_music(is_paused):
            global paused_if
            paused_if = is_paused
            if paused_if:
                mixer.music.unpause()
                paused_if = False
            else:
                mixer.music.pause()
                paused_if = True

        play_logo_inactive = PhotoImage(file='ast/play_logo.png')
        play_logo_active = PhotoImage(file='ast/play_logo_act.png')
        pause_logo_inactive = PhotoImage(file='ast/pause_logo.png')
        pause_logo_active = PhotoImage(file='ast/pause_logo_act.png')
        stop_logo_inactive = PhotoImage(file='ast/stop_logo.png')
        stop_logo_active = PhotoImage(file='ast/stop_logo_act.png')

        def on_ent5(e):
            lbl20_play['image'] = play_logo_active

        def on_ent6(e):
            lbl21_pause['image'] = pause_logo_active

        def on_ent7(e):
            btn22['image'] = stop_logo_active

        def on_ent8(e):
            btn23['fg'] = 'orange'
            btn23['bg'] = dark

        def on_lv(e):
            lbl21_pause['image'] = pause_logo_inactive
            lbl20_play['image'] = play_logo_inactive
            btn22['image'] = stop_logo_inactive
            btn23['fg'] = 'white'
            btn23['bg'] = dark

        lbl20_play = Button(sub_frame, image=play_logo_inactive, command=start_playing_music,
                            bd=0, relief=SOLID, highlightthickness=0)
        lbl20_play.pack(pady=20)

        lbl20_play.bind('<Enter>', on_ent5)
        lbl20_play.bind('<Leave>', on_lv)

        lbl21_pause = Button(sub_frame, image=pause_logo_inactive, command=lambda: pause_music(paused_if),
                             bd=0, highlightthickness=0)
        lbl21_pause.pack(pady=20)

        lbl21_pause.bind('<Enter>', on_ent6)
        lbl21_pause.bind('<Leave>', on_lv)

        btn22 = Button(sub_frame, image=stop_logo_inactive,
                       highlightthickness=0, bd=0, relief=SOLID, command=stop_music)
        btn22.pack(pady=20)

        btn22.bind('<Enter>', on_ent7)
        btn22.bind('<Leave>', on_lv)

        def return_to_start():
            stop_music()
            sub_frame.pack_forget()
            start_frame.pack(fill=BOTH, expand=True)

        btn23 = Button(sub_frame, text='<-- Back',
                       bd=0, relief=SOLID, command=return_to_start,
                       bg=dark, fg='white', font=(my_font, 10), highlightthickness=0)
        btn23.pack(side=BOTTOM, pady=5)

        btn23.bind('<Enter>', on_ent8)
        btn23.bind('<Leave>', on_lv)


# Start of Start_Page: -----

def play_music():
    def start_playing_music():
        def play_music_cmd():
            mixer.init()
            my_selected_playlist = jsn.get_data('currentPlaylist')
            if my_selected_playlist == 'thh':
                mixer.music.load('musicsong/installedMusic/trapHipHop/trapHiphopSong .mp3')
                mixer.music.play()
            elif my_selected_playlist == 'lhh':
                mixer.music.load('musicsong/installedMusic/lofiHipHop/lofiHiphopSong.mp3')
                mixer.music.play()

        func = thr.Thread(target=play_music_cmd)
        func.start()

    def stop_music():
        mixer.init()
        mixer.music.stop()

    global paused_if
    paused_if = False

    def pause_music(is_paused):
        global paused_if
        paused_if = is_paused
        if paused_if:
            mixer.music.unpause()
            paused_if = False
        else:
            mixer.music.pause()
            paused_if = True

    play_frame = Frame(root, bg=dark)
    main_frame.pack_forget()
    play_frame.pack(fill=BOTH, expand=True)

    play_logo_inactive = PhotoImage(file='ast/play_logo.png')
    play_logo_active = PhotoImage(file='ast/play_logo_act.png')
    pause_logo_inactive = PhotoImage(file='ast/pause_logo.png')
    pause_logo_active = PhotoImage(file='ast/pause_logo_act.png')
    stop_logo_inactive = PhotoImage(file='ast/stop_logo.png')
    stop_logo_active = PhotoImage(file='ast/stop_logo_act.png')

    def on_ent5(e):
        lbl20_play['image'] = play_logo_active

    def on_ent6(e):
        lbl21_pause['image'] = pause_logo_active

    def on_ent7(e):
        btn22['image'] = stop_logo_active

    def on_ent8(e):
        btn23['fg'] = 'orange'
        btn23['bg'] = dark

    def on_lv(e):
        lbl21_pause['image'] = pause_logo_inactive
        lbl20_play['image'] = play_logo_inactive
        btn22['image'] = stop_logo_inactive
        btn23['fg'] = 'white'
        btn23['bg'] = dark

    lbl20_play = Button(play_frame, image=play_logo_inactive, command=start_playing_music,
                        bd=0, relief=SOLID, highlightthickness=0)
    lbl20_play.pack(pady=20)

    lbl20_play.bind('<Enter>', on_ent5)
    lbl20_play.bind('<Leave>', on_lv)

    lbl21_pause = Button(play_frame, image=pause_logo_inactive, command=lambda: pause_music(paused_if),
                         bd=0, highlightthickness=0)
    lbl21_pause.pack(pady=20)

    lbl21_pause.bind('<Enter>', on_ent6)
    lbl21_pause.bind('<Leave>', on_lv)

    btn22 = Button(play_frame, image=stop_logo_inactive,
                   highlightthickness=0, bd=0, relief=SOLID, command=stop_music)
    btn22.pack(pady=20)

    btn22.bind('<Enter>', on_ent7)
    btn22.bind('<Leave>', on_lv)

    def return_to_start():
        stop_music()
        play_frame.pack_forget()
        main_frame.pack(fill=BOTH, expand=True)

    btn23 = Button(play_frame, text='<-- Back',
                   bd=0, relief=SOLID, command=return_to_start,
                   bg=dark, fg='white', font=(my_font, 10), highlightthickness=0)
    btn23.pack(side=BOTTOM, pady=5)

    btn23.bind('<Enter>', on_ent8)
    btn23.bind('<Leave>', on_lv)


def start_page():
    main_frame.pack_forget()
    start_frame.pack(fill=BOTH, expand=True)

    def return_to_start():
        start_frame.pack_forget()
        main_frame.pack(fill=BOTH, expand=True)
        start_frame.pack_forget()

    music_genres = ['Select Here', 'Lofi HipHop', 'Trap HipHop', 'User Custom Playlist']

    lbl10 = Label(start_frame, text='Choose Music Genre : ', relief=FLAT, bd=0, bg=dark, fg='white',
                  font=(my_font, 25))
    lbl10.pack(pady=10)

    def combo_action(e):
        selected_playlist = cmbx.get()
        jsn = Json_Manager('settings.json')
        jsn.write_data('anyError', False)
        if selected_playlist == 'Trap HipHop':
            jsn.append_data('currentPlaylist', 'thh')
        elif selected_playlist == 'Lofi HipHop':
            jsn.append_data('currentPlaylist', 'lhh')
        elif selected_playlist == 'User Custom Playlist':
            jsn.append_data('currentPlaylist', 'uss')

    def check_if_combx_empty():
        selected_playlist = cmbx.get()
        try:
            if selected_playlist == 'Select Here':
                messagebox.showerror('Empty Selection!', 'Please Select Something in The Combobox!')
                jsn.change_data('anyError', True)
        finally:
            check_for_error = jsn.get_data('anyError')
            my_uss_playlist = jsn.get_data('currentPlaylist')
            if not check_for_error:
                if my_uss_playlist == 'uss':
                    play_custom_music()
                else:
                    start_frame.pack_forget()
                    play_music()

    cmbx = ttk.Combobox(start_frame, value=music_genres, width=44)
    cmbx.current(0)
    cmbx.pack(pady=10)
    cmbx.bind('<<ComboboxSelected>>', combo_action)

    def on_enter3(e):
        btn10['fg'] = 'orange'
        btn10['bg'] = dark

    def on_enter4(e):
        btn11['fg'] = 'red'
        btn11['bg'] = dark

    def on_leave2(e):
        btn10['fg'] = 'white'
        btn10['bg'] = dark
        btn11['fg'] = 'white'
        btn11['bg'] = dark

    btn11 = Button(start_frame, text='<-- Back', relief=FLAT, bd=0, bg=dark, fg='white',
                   font=(my_font, 30), activebackground=dark, activeforeground='orange',
                   command=return_to_start)
    btn11.pack(side=BOTTOM, pady=10)
    btn11.bind('<Enter>', on_enter4)
    btn11.bind('<Leave>', on_leave2)

    btn10 = Button(start_frame, text='Continue', relief=FLAT, bd=0, bg=dark, fg='white',
                   font=(my_font, 35), activebackground=dark, activeforeground='orange',
                   command=check_if_combx_empty)
    btn10.pack(side=BOTTOM, pady=10)
    btn10.bind('<Enter>', on_enter3)
    btn10.bind('<Leave>', on_leave2)


# End of Start_Page: -----

logo_dark_theme = PhotoImage(file='ast/MuPlay_logo_darktheme.png')

lbl1 = Label(main_frame, image=logo_dark_theme, relief=SUNKEN, bd=0)
lbl1.pack(pady=10)


def on_enter1(e):
    btn1['bg'] = dark
    btn1['fg'] = '#52ffff'
    btn1.config(font=(my_font, 38))


def on_enter2(e):
    btn2['bg'] = dark
    btn2['fg'] = '#52ffff'
    btn2.config(font=(my_font, 33))


def on_leave1(e):
    btn1['bg'] = dark
    btn1['fg'] = 'white'
    btn2.config(font=(my_font, 30))
    btn2['bg'] = dark
    btn2['fg'] = 'white'
    btn1.config(font=(my_font, 35))


btn1 = Button(main_frame, text='Start!', relief=FLAT, bd=0, bg=dark, fg='white',
              font=(my_font, 35), activebackground=dark, activeforeground='orange',
              command=start_page)
btn1.pack(pady=10)

btn2 = Button(main_frame, text='Download Songs', relief=FLAT, bd=0, bg=dark, fg='white',
              font=(my_font, 30), activebackground=dark, activeforeground='orange',
              command=download_song)
btn2.pack(pady=10)
jsn = Json_Manager('settings.json')

btn1.bind('<Enter>', on_enter1)
btn1.bind('<Leave>', on_leave1)
btn2.bind('<Enter>', on_enter2)
btn2.bind('<Leave>', on_leave1)
root.mainloop()
jsn.clear_data()
