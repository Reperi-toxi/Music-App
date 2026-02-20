import os
import pygame
import time
"""
used for warmup. training with pygame music. will be enhanced with gui and
the desktop app will be connected to mobile device, which will serve as a remote
"""

def play_music(folder, music_file_name):
    music_path = os.path.join(folder, music_file_name)
    pygame.mixer.music.load(music_path)

    current_position = 0.0
    last_update_time = time.time() # 10 000

    pygame.mixer.music.play(start=current_position)

    while True:
        if not pygame.mixer.music.get_busy(): # only update if it's playing
            current_position += time.time() - last_update_time # 10 005 - 10 000 = 5
        last_update_time = time.time()

        print("P - pause; R - Resume; S - stop; D - +5 seconds; A - -5 seconds")
        user_input = input('-> ')

        match user_input.lower().strip():
            case 'p':
                pygame.mixer.music.pause()

            case 'r':
                pygame.mixer.music.unpause()
                last_update_time = time.time()

            case 's':
                pygame.mixer.music.stop()
                break

            case 'a':  # Go back 5 seconds
                current_position = max(0, current_position - 5)
                pygame.mixer.music.play(start=current_position)
                last_update_time = time.time()

            case 'd':  # Go forward 5 seconds
                current_position += 5
                pygame.mixer.music.play(start=current_position)
                last_update_time = time.time()

            case _:
                print('Invalid input')
def main():
    try:
        pygame.mixer.init()
    except pygame.error as e:
        print('error initializing!', e)
    folder = "songs"
    if not os.path.isdir(folder):
        print(f" folder '{folder}' not found!")
    music_files = [file for file in os.listdir(folder) if file.endswith('.mp3')] # checks if the files are mp3
    if not music_files:
        print('no mp3 files found!')
        return
    while True:
        print('Music app!')
        for i, songs in enumerate(music_files, start=1):
            print(f"{i}, {songs.strip(".mp3")}")
        choice = input("Choose the song by number, or press 'q' to quit: ")
        if choice.lower().strip() == "q":
            break
        elif not choice.isdigit():
            print("invalid input")
            continue
        else:
            music_choice_index = int(choice) - 1
            play_music(folder, music_files[music_choice_index])


if __name__ == "__main__":
    main()