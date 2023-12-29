from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher, executor, types
import openai
import sys


class Reference:
    '''
    A class to store previously response from the chatGPT API
    '''

    def __init__(self) -> None:
        self.response = ""


load_dotenv()
openai.api_key = os.getenv("OpenAI_API_KEY")  

reference = Reference()

TOKEN = os.getenv("TOKEN")

#model name
MODEL_NAME = "gpt-3.5-turbo"


# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot)


def clear_past():
    """A function to clear the previous conversation and context.
    """
    reference.response = ""



@dp.message_handler(commands=['start', 'help','Hi','hi','Hello','hello'])
async def command_start_handler(message: types.Message):
    """
    This handler receives messages with `/start` or  `/help `command
    """
    await message.reply("Hi\nI am Aramandi Bot!\nPowered by Aikya Kala Academy. \nHow can I help you? \nYou can use \Menu to browse options or type in any question for me")



@dispatcher.message_handler(commands=['Menu'])
async def welcome(message: types.Message):
    """
    This handler receives messages with `/start` or  `/help `command
    """
    await message.reply("Use below options\nFounder\nBatces")

@dispatcher.message_handler(commands=['Founder'])
async def welcome(message: types.Message):
    """
    This handler receives messages with `/start` or  `/help `command
    """
    await message.reply("Our founder is Mrs/ Rashmi Ruikar Mujumdar-MA Bharatnatyam.\nShe is a Bharatnatyam practitioner and performer, practicing Baratnatyam since last 20 years\nShe has vast experience of teaching, conduction workshops and baithaks.")

@dispatcher.message_handler(commands=['Batches'])
async def welcome(message: types.Message):
    """
    This handler receives messages with `/start` or  `/help `command
    """
    await message.reply("We have batches covering all levels of Bharatnatyam till MA")


@dispatcher.message_handler(commands=['clear'])
async def clear(message: types.Message):
    """
    A handler to clear the previous conversation and context.
    """
    clear_past()
    await message.reply("I've cleared the past conversation and context.")



@dispatcher.message_handler(commands=['help'])
async def helper(message: types.Message):
    """
    A handler to display the help menu.
    """
    help_command = """
    Hi There, I'm chatGPT Telegram bot created by Bappy! Please follow these commands - 
    /start - to start the conversation
    /clear - to clear the past conversation and context.
    /help - to get this help menu.
    I hope this helps. :)
    """
    await message.reply(help_command)



@dispatcher.message_handler()
async def chatgpt(message: types.Message):
    """
    A handler to process the user's input and generate a response using the chatGPT API.
    """
    print(f">>> USER: \n\t{message.text}")
    response = openai.ChatCompletion.create(
        model = MODEL_NAME,
        messages = [
            {"role": "assistant", "content": reference.response}, # role assistant
            {"role": "user", "content": message.text} #our query 
        ]
    )
    reference.response = response['choices'][0]['message']['content']
    print(f">>> chatGPT: \n\t{reference.response}")
    await bot.send_message(chat_id = message.chat.id, text = reference.response)



if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates=False)