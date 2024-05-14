import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
import datetime
import pywhatkit as kit
import time
import requests
import smtplib
import wikipedia
from translate import Translator

class TextChatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Chatbot")
        self.root.geometry("1000x600")

        self.chat_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE, height=10, width=30)
        self.chat_listbox.pack(side=tk.LEFT, padx=10, pady=10)
        self.chat_listbox.bind("<<ListboxSelect>>", self.load_chat)

        self.chats = {"Первый чат": []}
        self.add_chat("Первый чат")

        self.create_chat_button = tk.Button(self.root, text="Создать чат", command=self.create_chat)
        self.create_chat_button.pack(side=tk.LEFT, padx=10, pady=20)

        self.delete_chat_button = tk.Button(self.root, text="Удалить чат", command=self.delete_chat)
        self.delete_chat_button.pack(side=tk.LEFT, pady=20)

        self.chat_frame = tk.Frame(self.root)
        self.chat_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        self.text_area = scrolledtext.ScrolledText(self.chat_frame, wrap=tk.WORD, width=60, height=20, state='disabled')
        self.text_area.pack(pady=10)

        self.user_input = tk.Entry(self.chat_frame, width=60)
        self.user_input.pack(pady=10)
        self.user_input.bind('<Return>', lambda event=None: self.send_message_and_clear())

        self.send_button = tk.Button(self.chat_frame, text="Отправить", command=self.send_message)
        self.send_button.pack(pady=10)

        self.greet_user()

        self.text_area.tag_configure('padding', spacing1=15)

    def add_chat(self, chat_name):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        chat_info = f"{timestamp} - {chat_name}"
        self.chat_listbox.insert(tk.END, chat_info)

    def create_chat(self):
        chat_name = f"Новый чат {self.chat_listbox.size() + 1}"
        self.chats[chat_name] = []
        self.add_chat(chat_name)
        self.speak(f"Создан новый чат: {chat_name}")

    def delete_chat(self):
        selected_chat_index = self.chat_listbox.curselection()
        if selected_chat_index:
            selected_chat_info = self.chat_listbox.get(selected_chat_index)
            _, chat_name = selected_chat_info.split(" - ")
            del self.chats[chat_name]
            self.chat_listbox.delete(selected_chat_index)
            self.speak(f"Чат удален: {chat_name}")

    def load_chat(self, event):
        selected_chat_index = self.chat_listbox.curselection()
        if selected_chat_index:
            self.text_area.delete(1.0, tk.END)
            selected_chat_info = self.chat_listbox.get(selected_chat_index)
            _, chat_name = selected_chat_info.split(" - ")
            self.speak(f"Загружен чат: {chat_name}")

            chat_content = self.chats.get(chat_name, [])
            for message in chat_content:
                speaker, text = message
                self.speak(f"{speaker}: {text}", user=(speaker == 'Вы'))

    def speak(self, audio, user=False):
        self.text_area.configure(state='normal')
        if user:
            self.text_area.insert(tk.END, f"Вы: {audio}\n", ('user', 'padding'))
        else:
            self.text_area.insert(tk.END, f"Бот: {audio}\n", ('bot', 'padding'))
        self.text_area.configure(state='disabled')
        self.root.update()

    def greet_user(self):
        hour = datetime.datetime.now().hour
        if 0 <= hour < 12:
            self.speak("Доброе утро! Как я могу помочь вам сегодня?")
        elif 12 <= hour < 17:
            self.speak("Добрый день! Как я могу помочь вам сегодня?")
        else:
            self.speak("Добрый вечер! Как я могу помочь вам сегодня?")

    def robot(self, user_input):
        try:
            # if "блокнот" in user_input:
            #     self.speak("Открываю Блокнот")
            #     open("notepad")

            if "воспроизвести на youtube" in user_input:
                self.speak("Что вы хотите воспроизвести на YouTube?")
                req = input("Введите ваш запрос: ")
                kit.playonyt(req)

            elif "дата" in user_input:
                self.speak(datetime.date.today())

            elif "время" in user_input:
                self.speak(time.strftime("%H:%M:%S", time.localtime()))

            elif "сообщение" in user_input:
                self.speak("Конечно, введите номер с кодом страны, кому я должен отправить сообщение")
                number = input("Введите номер здесь: ")
                self.speak("Теперь введите сообщение, которое вы хотите отправить")
                msg = input("Введите сообщение здесь: ")
                kit.sendwhatmsg_instantly(number, msg)

            elif "шутка" in user_input:
                res = requests.get("https://api.chucknorris.io/jokes/random").json()
                joke_text = res["value"]
                translator = Translator(to_lang="ru")
                joke_text_ru = translator.translate(joke_text)
                self.speak(joke_text_ru)
                print(joke_text_ru)

            # https://fucking-great-advice.ru/api/random
            elif "совет" in user_input:
                res = requests.get("https://api.adviceslip.com/advice").json()
                advice_text = res["slip"]["advice"]
                translator = Translator(to_lang="ru")
                advice_text_ru = translator.translate(advice_text)
                self.speak(advice_text_ru)
                print(advice_text_ru)

            elif "email" in user_input:
                sender_email = input("Пожалуйста, введите ваш адрес электронной почты: ")
                sender_password = input("Пожалуйста, введите пароль: ")
                receiver = input("Введите адрес электронной почты получателя: ")
                li = [sender_email, receiver]
                for des in li:
                    s = smtplib.SMTP('smtp.gmail.com', 587)
                    s.starttls()
                    s.login(sender_email, sender_password)
                    message = "Сообщение, которое вы хотите отправить"
                    s.sendmail(sender_email, des, message)
                    s.quit()

            else:
                self.speak("Я нашел это в сети")
                wikipedia.set_lang("ru")  
                wikipedia_summary = wikipedia.summary(user_input, sentences=5)
                self.speak(wikipedia_summary)

        except Exception as e:
            self.speak(f"Произошла ошибка: {str(e)}")

    def send_message(self, event=None):
        user_input = self.user_input.get().lower()

        if user_input:
            selected_chat_index = self.chat_listbox.curselection()
            if selected_chat_index:
                selected_chat_info = self.chat_listbox.get(selected_chat_index)
                _, chat_name = selected_chat_info.split(" - ")
                self.chats[chat_name].append(('Вы', user_input))
                self.user_input.delete(0, tk.END)
                self.load_chat(None)
                self.robot(user_input)

    def send_message_and_clear(self, event=None):
        self.send_message()

root = tk.Tk()
chatbot = TextChatbot(root)

style = ttk.Style()
style.configure('user.TLabel', foreground='blue', font=('Arial', 12, 'normal'))
style.configure('bot.TLabel', foreground='green', font=('Arial', 12, 'normal'))

root.mainloop()
