# libraries import
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from PIL import Image
import requests
from io import BytesIO
import base64
import tkinter

# spotify API login
colorify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='0f5166c39f0d42baaf124bce6deece44', \
    client_secret='7d7797ac5cce4b8698e0774e5dcbc6e8', redirect_uri='https://www.bmthofficial.com/', \
        scope='user-library-read playlist-read-private playlist-modify-public playlist-modify-private ugc-image-upload'))

# setting variables for output results
search_results_textify = ''
search_results_colorify = ''

# textify search algorithm
def find_track_name(offset):
    global window
    global track_uris
    global search_results_textify

    track_uris = []
    results = colorify.search(q=str(test[i]), type='track', limit=50, offset=offset)
    unmatch = True
    j = 0

    if not results['tracks']['items']:
        return
    
    # multiple checks for name to correspond to input sentence
    while unmatch and j<50:
        track = results['tracks']['items'][j]
        if test[i].lower() in str(track['name']).lower() and test[i][0].lower() == str(track['name'])[0].lower() \
            and test[i][len(test[i])-1].lower() == str(track['name'])[len(test[i])-1].lower():
            # check if there is next symbol after end of the word
            if len(str(test[i])) != len(track['name']):
                # check if it is a space
                if str(track['name'])[len(test[i])] == ' ':
                    search_results_textify += f"{track['name']} — {track['artists'][0]['name']}, https://open.spotify.com/track/{str(track['uri'])[14:]}\n"
                    track_uris.append(track['uri'])
                    colorify.playlist_add_items(playlist['id'], track_uris)
                    unmatch = False
            else:
                search_results_textify += f"{track['name']} — {track['artists'][0]['name']}, https://open.spotify.com/track/{str(track['uri'])[14:]}\n"
                track_uris.append(track['uri'])
                colorify.playlist_add_items(playlist['id'], track_uris)
                unmatch = False
        j += 1
    # if not found, try next set of results until found
    if unmatch:
        find_track_name(offset+50)

#algorithm to convert HEX to RGB
def convert_colour(needed_colour, input_colour, check):
    global red
    global green
    global blue

    # separate different parts of HEX format for Red, Green and Blue in RGB
    if check == 'red':
        index = 0
    elif check == 'green':
        index = 2
    elif check == 'blue':
        index = 4
    
    # convert first symbol from decimal to hexadecimal
    if input_colour[index] == 'A':
        needed_colour += 10 * 16
    elif input_colour[index] == 'B':
        needed_colour += 11 * 16
    elif input_colour[index] == 'C':
        needed_colour += 12 * 16
    elif input_colour[index] == 'D':
        needed_colour += 13 * 16
    elif input_colour[index] == 'E':
        needed_colour += 14 * 16
    elif input_colour[index] == 'F':
        needed_colour += 15 * 16
    else:
        needed_colour += int(input_colour[index]) * 16
    
    # convert second symbol from decimal to hexadecimal
    if input_colour[index+1] == 'A':
        needed_colour += 10
    elif input_colour[index+1] == 'B':
        needed_colour += 11
    elif input_colour[index+1] == 'C':
        needed_colour += 12
    elif input_colour[index+1] == 'D':
        needed_colour += 13
    elif input_colour[index+1] == 'E':
        needed_colour += 14
    elif input_colour[index+1] == 'F':
        needed_colour += 15
    else:
        needed_colour += int(input_colour[index+1])
    
    # set variables to calculated colour
    if index == 0:
        red = needed_colour
    elif index == 2:
        green = needed_colour
    elif index == 4:
        blue = needed_colour

# colorify algorithm
def colorify_search(offset, red, green, blue, limit, playlist):
    global colorify
    global search_results_colorify
    global window

    liked_tracks = colorify.current_user_saved_tracks(limit=limit, offset=offset)
    for item in liked_tracks['items']:
        track = item['track']
        track_uris = []
        if track['album']['images']:
            # get colours of pixels of cover
            track_cover_img = requests.get(track['album']['images'][0]['url'])
            track_cover = Image.open(BytesIO(track_cover_img.content)).convert('RGB')
            pixels = list(track_cover.getdata())
            # calculating average colour for red, green and blue
            avg_red_track_cover = sum([pixel[0] for pixel in pixels]) / len(pixels)
            avg_green_track_cover = sum([pixel[1] for pixel in pixels]) / len(pixels)
            avg_blue_track_cover = sum([pixel[2] for pixel in pixels]) / len(pixels)
            # check difference of actual average colour and needed colour
            if abs(avg_red_track_cover - red) < 30 and abs(avg_green_track_cover - green) < 30 and abs(avg_blue_track_cover - blue) < 30:
                search_results_colorify += f'{track['name']} — {track['artists'][0]['name']}, https://open.spotify.com/track/{str(track['uri'])[14:]}\n'
                track_uris.append(track['uri'])
                colorify.playlist_add_items(playlist['id'], track_uris)

# colorify option
def colorify_go():
    global window
    global colorify

    # updating window
    window.title("Colorify")
    name.grid_remove()
    exit_button.grid_remove()
    colorify_button.grid_remove()
    textify_button.grid_remove()
    text1 = tkinter.Label(window, text='Please enter desired colour below in HEX format')
    text1.grid(column=0, row=0)
    desired_colour_input = tkinter.Entry(window)
    desired_colour_input.grid(column=0, row=1)

    def colorify_go_go():
        global colorify
        global window
        global colorify
        global red
        global green
        global blue

        # setting up please wait label
        go_colorify_button.grid_remove()
        text1.grid_remove()
        desired_colour = desired_colour_input.get()
        desired_colour_input.grid_remove()
        wait_sign = tkinter.Label(window, text='Please wait')
        wait_sign.grid(column=0, row=0)
        window.update()

        # creating error elements
        error_sign = tkinter.Label(window, text='Please input HEX code')
        error_button = tkinter.Button(window, text='OK', command=window.destroy)

        # arrays for HEX symbols
        HEX_code = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']

        # remove hashtag if it was present
        if desired_colour[0] == '#':
            desired_colour = desired_colour[1:]
        # check for 6 symbols
        if len(desired_colour) != 6:
            # showing error elements
            wait_sign.grid_remove()
            error_sign.grid(column=0, row=0)
            error_button.grid(column=0, row=1)
            window.update()
        else:
            # check for HEX symbols
            j1 = 0
            checkHEX = 0
            while j1 < 6 and checkHEX == 0:
                if desired_colour[j1] in HEX_code:
                    j1 += 1
                else:
                    checkHEX = 1
            if checkHEX == 1:
                # showing error elements
                wait_sign.grid_remove()
                error_sign.grid(column=0, row=0)
                error_button.grid(column=0, row=1)
                window.update()
            else:
                saved_desired_colour = desired_colour
                red = 0
                green = 0
                blue = 0

                # convert from HEX to RGB
                convert_colour(red, desired_colour, 'red')
                convert_colour(green, desired_colour, 'green')
                convert_colour(blue, desired_colour, 'blue')

                # creation of a playlist
                playlist = colorify.user_playlist_create(user=colorify.current_user()['id'], name=f'#{saved_desired_colour}', \
                description='Hope you enjoy this colourful playlist', public=False)

                # create and upload image as a cover for playlist
                RGB_n = (red, green, blue)
                new_cover = Image.new('RGB', size=(300, 300), color=RGB_n)
                buffered = BytesIO()
                new_cover.save(buffered, format='JPEG')
                new_cover_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
                colorify.playlist_upload_cover_image(playlist['id'], new_cover_str)

                results = colorify.current_user_saved_tracks(limit=1)
                total_liked_songs = results['total']
                # start search for tracks for every liked song
                j2 = 0
                while j2 <= total_liked_songs//50*50:
                    colorify_search(offset=j2, red=red, green=green, blue=blue, limit=50, playlist=playlist)
                    j2 += 50
                colorify_search(offset=j2, red=red, green=green, blue=blue, limit=total_liked_songs%50, playlist=playlist)
                
                # updating window
                results_label_colorify = tkinter.Text(window, wrap='word', height=20, width=60)
                results_label_colorify.insert('1.0', search_results_colorify[:-1])
                results_label_colorify.config(state='disabled')
                wait_sign.grid_remove()
                done_sign = tkinter.Label(window, text='Thank you for waiting, here is your playlist:')
                done_sign.pack(anchor='n')
                results_label_colorify.pack(anchor='center')
                done_button = tkinter.Button(window, text='Exit', command=window.destroy)
                done_button.pack(anchor='s')
                window.update()

    go_colorify_button = tkinter.Button(window, text='Go', command=colorify_go_go)
    go_colorify_button.grid(column=0, row=2)

    window.update()

# textify option
def textify_go():
    global window
    global search_results_textify

    # updating window
    window.title("Textify")
    exit_button.grid_remove()
    name.grid_remove()
    colorify_button.grid_remove()
    textify_button.grid_remove()
    text2 = tkinter.Label(window, text='Please enter desired sentence below')
    text2.grid(column=0, row=0)
    desired_sentence_input = tkinter.Entry(window)
    desired_sentence_input.grid(column=0, row=1)

    def textify_go_go():
        global playlist
        global test
        global window
        global i
        global search_results_textify

        # setting up please wait label
        text2.grid_remove()
        desired_sentence_input.grid_remove()
        go_textify_button.grid_remove()
        wait_sign = tkinter.Label(window, text='Please wait')
        wait_sign.grid(column=0, row=0)
        window.update()

        sentence_input = desired_sentence_input.get()
        # create playlist
        playlist = colorify.user_playlist_create(user=colorify.current_user()['id'], name=sentence_input, \
            description='Read first words/letter of every track name', public=False)
        test = sentence_input.split(' ')
        track_uris = []

        for i in range(len(test)):
            results = colorify.search(q=str(test[i]), type='track', limit=50)
            # check if results are present
            if results['tracks']['items']:
                # trigger algorithm for search
                find_track_name(0)
            else:
                # updating window in case there is no such song
                wait_sign.grid_remove()
                error_sign = tkinter.Label(window, text=f'Sadly, there is no song with name "{test[i]}"')
                error_sign.grid(column=0,row=0)
                error_button = tkinter.Button(window, text='OK', command=window.destroy)
                error_button.grid(column=0, row=1)
                window.update()
        
        if track_uris:
            colorify.playlist_add_items(playlist['id'], track_uris)
        wait_sign.grid_remove()

        # updating window
        done_sign = tkinter.Label(window, text='Thank you for waiting, here is your playlist:')
        done_sign.pack(anchor='n')
        results_label_text = tkinter.Text(window, wrap='word', height=20, width=60)
        results_label_text.insert('1.0', search_results_textify[:-1])  # Remove the trailing newline
        results_label_text.config(state='disabled')  # Make it read-only
        results_label_text.pack(anchor='center')
        done_button = tkinter.Button(window, text='Exit', command=window.destroy)
        done_button.pack(anchor='s')
        window.update()

    go_textify_button = tkinter.Button(window, text='Go', command=textify_go_go)
    go_textify_button.grid(column=0, row=2)
    window.update()

# creation of window
window = tkinter.Tk()
window.title("Colorify/Textify")
name = tkinter.Label(window, text='Welcome')
name.grid(column=1, row=0)
colorify_button = tkinter.Button(window, text='Colorify', command=colorify_go)
colorify_button.grid(column=0, row=1)
textify_button = tkinter.Button(window, text='Textify', command=textify_go)
textify_button.grid(column=2, row=1)
exit_button = tkinter.Button(window, text='Exit', command=window.destroy)
exit_button.grid(column=1, row=2)
window.mainloop()