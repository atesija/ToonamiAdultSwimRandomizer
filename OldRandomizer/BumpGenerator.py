import pygame
import time
import sys
import glob
import random
import json
from FileFinder import get_files_of_type_from_folders

def play_bump(channel_json):
    pygame.init()
    random.seed()

    #We don't want to see the mouse over the bump
    pygame.mouse.set_visible(False)

    #Set up the screen
    size = 0, 0
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    screen_width = pygame.display.Info().current_w
    screen_height = pygame.display.Info().current_h

    #Open a random music file and play it
    pygame.mixer.init()
    if channel_json:
        configuration_json = json.load(open(channel_json))  
        song = random.choice(get_files_of_type_from_folders(configuration_json["folders"]["music"], ".mp3"))
        song = song.rstrip()
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()

    #Find all bump templates
    bump_template_list = glob.glob("BumpTemplates/*.json")

    #Choose a random template and open it
    bump_file = random.choice(bump_template_list)
    bump_json = None
    with open(bump_file) as json_file:
        bump_json = json.load(json_file)
        
    if(bump_json == None):
        print "Unable to load file %s" % bump_file
        pygame.quit()
        sys.exit()

    #Replace text in the template
    for bump_part in bump_json["bumpTemplate"]:
        for replacement in bump_json["replacements"]:
            bump_part["text"] = bump_part["text"].replace(replacement, random.choice(bump_json["replacements"][replacement]))

    #Replace text where each option has to be at the same index
    if(len(bump_json["orderedReplacements"]) > 0):
        replacement_index = random.randint(0, len(bump_json["orderedReplacements"].values()[0]) - 1)
        for bump_part in bump_json["bumpTemplate"]:
            for replacement in bump_json["orderedReplacements"]:
                bump_part["text"] = bump_part["text"].replace(replacement, bump_json["orderedReplacements"][replacement][replacement_index])

    #Set up font
    white = 255, 255, 255
    font = pygame.font.Font(None, screen_height / 10)

    #Loop through each part of the bump and display it for the proper time
    black = 0, 0, 0
    for bump_part in bump_json["bumpTemplate"]:
        screen.fill(black)
        text = font.render(bump_part["text"], True, white)
        textrect = text.get_rect(center = (screen_width / 2, screen_height / 2))
        screen.blit(text, textrect)
        pygame.display.flip()
        time.sleep(float(bump_part["time"]))

    #Display the logo at the end 
    logo = pygame.image.load("Logo.png")
    logo = pygame.transform.scale(logo, (int(screen_width / 3.5), int(screen_height / 3.5)))
    logorect = logo.get_rect(center = (screen_width / 2, screen_height / 2))
    screen.fill(black)
    screen.blit(logo, logorect)
    pygame.display.flip()

    #Fade msuic out, wait, then exit
    pygame.mixer.music.fadeout(2000)
    time.sleep(2)

    pygame.quit()
    #sys.exit()

if __name__ == '__main__':
    play_bump(None)
