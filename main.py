import flet as ft
import json
import nltk
import random
from random_resonses import random_string
from getUserInput import getUserInput
from nltk.tokenize import word_tokenize
from Matching_utils import lemmatizer, lemmatize_input, enhance_required_words_matching
import math

if not nltk.data.find('tokenizers/punkt'):
    nltk.download('punkt')

# Load JSON data
def load_conversation_data(file):
    with open(file) as BotAnswers:
        print(f"successfully Loaded '{file}'!")
        return json.load(BotAnswers)

# Store JSON data
response_data = load_conversation_data("application/Training.json")

# Initialize WordNet Lemmatizer

def Tokenize__input(input_string):
    return word_tokenize(input_string)
    
last_selected_response = None

def generate_response(user_input):

    global last_selected_response

    split_query = Tokenize__input(user_input.lower())
    matching_scores = []

    # Check if input is empty
    if user_input == "":
        return "Please say something so we can chat :("
    
    # Check if the input is very short
    if len(split_query) < 3:
        for response in response_data:
            if any(word in split_query for word in response["user_input"]):
                list_count = len(response["user_input"])
                random_item = random.randrange(list_count)
                if response["bot_response"][random_item] != last_selected_response:
                    last_selected_response = response["bot_response"][random_item]
                    return last_selected_response

        # If no direct match found, return a generic response for short input
        return "I'm not sure what to make of such a short input. Can you provide more details?"

    for response in response_data:
        response_matching = 0
        required_matching = enhance_required_words_matching(user_input, response["required_words"])

        # Amount of required words should match the required score
        if required_matching > 0:
            # Check each word the user has typed
            for word in split_query:
                # If the word is in the response, add to the score
                if word in response["user_input"]:
                    response_matching += 1
            
            # Normalize the response matching score by dividing by the length of user input
            if split_query:
                response_matching /= len(split_query)

        # Add score to list
        matching_scores.append(response_matching)

    # Find the best response and return it if they're not all 0
    best_response = max(matching_scores)
    response_index = matching_scores.index(best_response)

    if best_response != 0:
        selected_response = response_data[response_index]
        bot_responses = selected_response["bot_response"]
        list_count = len(bot_responses)
        random_item = random.randrange(list_count)
        if bot_responses[random_item] != last_selected_response:
            last_selected_response = bot_responses[random_item]
            return last_selected_response

    # If there is no good response, return a random one.
    return random_string()

def main(page: ft.Page):
    page.horizontal_alignment = page.vertical_alignment = "center"
    page.theme_mode = "dark"
    chat = ft.ListView(
            expand=True,
            spacing=15,
            auto_scroll=True,
            )
    new_message = ft.TextField(
        hint_text=" Write a message...",
        autofocus=True,
        shift_enter=False,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        border_radius=50,
        )


    def submit_msg(e):
        chat.controls.append(ft.Row(
            controls=[
                ft.CircleAvatar(
                    content=ft.Icon(ft.icons.PERSON),
                    color=ft.colors.WHITE,
                    bgcolor=ft.colors.GREY_300,
                ),

                ft.Column(
                    [
                        ft.Text("You", opacity=0.6),
                        ft.Text(new_message.value, weight="bold"),
                    ],
                    tight=True,
                    spacing=5,
                    
                ),
            ]
        ))
        page.update()

        botResponse = generate_response(new_message.value)

        chat.controls.append(ft.Row(
            controls=[
                ft.CircleAvatar(
                    content= ft.Icon(ft.icons.REDDIT),
                    color=ft.colors.WHITE,
                    bgcolor=ft.colors.GREY_300,
                ),

                ft.Column(
                    [
                        ft.Text("Bot", opacity=0.6),
                        ft.Text(botResponse, weight="bold"),
                    ],
                    tight=False,
                    spacing=5,
                    wrap = True,
                    expand=True,
                ),
            ]
        ))
        new_message.value = ""
        page.update()


    def send_voice(e):
        e.control.selected = not e.control.selected
        e.control.update()
        if e.control.selected == True:
            print("voice recorded")
            user_input = getUserInput()
            chat.controls.append(ft.Row(
                    controls=[
                        ft.CircleAvatar(
                            content=ft.Icon(ft.icons.PERSON),
                            color=ft.colors.WHITE,
                            bgcolor=ft.colors.GREY_300,
                        ),

                        ft.Column(
                            [
                                ft.Text("You", opacity=0.6),
                                ft.Text(user_input, weight="bold"),
                            ],
                            tight=True,
                            spacing=5,
                        ),
                    ]
                ))
            page.update()

            botResponse = generate_response(user_input)
            chat.controls.append(ft.Row(
                    controls=[
                        ft.CircleAvatar(
                            content=ft.Icon(ft.icons.REDDIT),
                            color=ft.colors.WHITE,
                            bgcolor=ft.colors.GREY_300,
                        ),

                        ft.Column(
                            [
                                ft.Text("Bot", opacity=0.6),
                                ft.Text(botResponse, weight="bold"),
                            ],
                            tight=True,
                            spacing=5,
                        ),
                    ]
                ))

            page.update()
            e.control.selected = False
            e.control.update()

    page.title = "TimaChat"
    page.appbar = ft.AppBar(
        title=ft.Text("TimaChatBot"),
        center_title=True,
        automatically_imply_leading=False,
    )
    page.add(
        ft.Container(
            content=chat,
            border=ft.border.all(2, ft.colors.WHITE),
            border_radius=10,
            padding=10,
            expand=True,
        ),
        ft.Divider(height=6, color = ft.colors.WHITE ),
        ft.Row(controls=[
            ft.IconButton(
                icon=ft.icons.MIC,
                selected_icon = ft.icons.MIC,
                tooltip="Send voice",
                selected=False,
                on_click=send_voice,
                icon_size = 30,
                style=ft.ButtonStyle(
                    bgcolor={"selected": ft.colors.GREEN},
                    color={"selected": ft.colors.WHITE, "":ft.colors.RED}),                    
                ),
            new_message,
            ft.IconButton(
                icon=ft.icons.SEND_ROUNDED,
                tooltip="Send message",
                on_click=submit_msg,
                icon_size = 25,
                ),])
        )

ft.app(main)
