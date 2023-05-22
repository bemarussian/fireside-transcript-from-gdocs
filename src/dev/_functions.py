import tkinter.messagebox as messagebox
import tkinter as tk
import time
import re
import gdown
from bs4 import BeautifulSoup
import requests
import os
import sys
sys.path.append("../../../cred")
from cred import *

def clear_text (field):
    field.delete("1.0", tk.END)

def update_text (field, text):
    clear_text(field)
    field.insert(tk.END, text)
    field.update()

def get_first_ep_number():
    ## NOTE! One can get from podacst if url returns "Page not found"
    first_ep_number = -1
    return first_ep_number

def get_latest_ep_number():
    ## NOTE! One can get from podacst if url returns "Page not found"
    latest_ep_number = 1
    return latest_ep_number


def get_ep_number(ep_value):
    try:
        ep_int = int(ep_value)
        ep_text = f"Integer value [{ep_int}]"
    except ValueError:
        if (ep_value == "From"):
            ep_int = get_first_ep_number()
        elif (ep_value == "To"):
            ep_int = get_latest_ep_number()
        else:
            messagebox.showerror("Error", f"Not supported value [{ep_value}]")
            #raise Exception(f"Not supported value [{ep_value}]")

        ep_text = f"Non-numerical value [{ep_value}], setting to [{ep_int}]"
    return ep_int, ep_text


def extract_text_from_google_docs(link):
    # # Download the HTML content of the Google Docs link
    tmp = "./tmp"
    response = gdown.download(link, output=tmp)
    with open(tmp, 'r', encoding='utf-8') as file:
        html_content = file.read()
    os.remove(tmp)

    # Create a BeautifulSoup object with the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all text within <p> tags
    paragraphs = soup.find_all('p')

    # Extract the plain text from the paragraphs
    plain_text = '\n\n'.join([p.get_text() for p in paragraphs])

    return plain_text

def get_podcast_root_url():
    url = f"https://www.bemadiscipleship.com"
    url = f"https://transcript-tst.fireside.fm"
    return url

def get_episode_soup(episode):
    url = f"{get_podcast_root_url()}/{episode}"
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Get the content of the response
        content = response.content
    else:
        print("Error:", response.status_code)
    
    # Parse the HTML code with BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')
    return soup


def get_transcript_text(episode):

    soup = get_episode_soup(episode)
    # Find the <a> tag with the text "Transcript for BEMA"
    transcript_link = soup.find('a', text=re.compile(r'^Transcript for'))

    # Extract the href value
    if transcript_link:
        href_value = transcript_link['href']
    else:
        print("Error:", f"Transcript link not found in episode {episode}")

    # response = requests.get(href_value)
    transcript_text =  extract_text_from_google_docs(href_value)


    return transcript_text




def get_transcript_file_path(episode):
    file_path = f"transcripts/e{str(episode)}.txt"
    return file_path

def get_episode_fireside_id(episode):
    ## https://aphid.fireside.fm/d/1437767933/99762f8d-e4a7-4955-a344-e4ad167f24e7/b0cd4cc6-8f99-4907-89fd-1a001ee75b1f.mp3
    soup = get_episode_soup(episode)

    for link in soup.find_all('a'):
        if "Download" in link.get_text():
            href_value = link['href']
            break

    # Extract the href value
    # Ex.: href="https://aphid.fireside.fm/d/1437767933/99762f8d-e4a7-4955-a344-e4ad167f24e7/cca1c14d-188d-44c7-ac5c-3d8081efb645.mp3"
    if (not href_value):
        print("Error:", f"Download link not found in episode {episode}")

    # response = requests.get(href_value)
    # id = "b0cd4cc6-8f99-4907-89fd-1a001ee75b1f"
    id =  os.path.splitext(os.path.basename(href_value))[0]

    print (f"For episode [{episode}] found episode id: [{id}]")
    return id

def get_podcast_name():
    name = "transcript-tst"
    return name

def get_episode_edit_url(episode):
    # https://app.fireside.fm/podcasts/transcript-tst/episodes/99762f8d-e4a7-4955-a344-e4ad167f24e7/edit
    url = f"https://app.fireside.fm/podcasts/{get_podcast_name()}/episodes/{get_episode_fireside_id(episode)}/edit"
    return url

def handle_button_click(ep_from, ep_to,transcript_preview):
    # Retrieve the value from the text area
    ep_from_int, ep_from_text = get_ep_number(ep_from.get("1.0", "end-1c"))
    ep_to_int, ep_to_text = get_ep_number(ep_to.get("1.0", "end-1c"))
    
    update_text(transcript_preview, f"Updating transcripts from: \n{ep_from_text} to \n{ep_to_text}")

    for episode in range(ep_from_int, ep_to_int + 1):
        time.sleep(1)
        print(f"Getting transcripts for ep.: \n{episode}")
        text = get_transcript_text(episode)
        transcript_file_path = get_transcript_file_path(episode)

        update_text(transcript_preview, f"Transcripts for ep. {episode}:\n{text}")
        time.sleep(1)

        with open(transcript_file_path, 'w') as file:
            file.write(text)

        exec_command = f"robot --variable username:{username} --variable password:{password} --variable ep_edit_url:{get_episode_edit_url(episode)} --variable ep_transcript_file:{os.path.abspath(transcript_file_path)} -d ./logs/ _robot_actions.robot"
        os.system(exec_command)

