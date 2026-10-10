import threading
import asyncio
import discord
from discord.ext import commands

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock

class DiscordBotApp(App):
    def build(self):
        self.bot_thread = None
        self.loop = None
        self.bot = None

        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        layout.add_widget(Label(text="🤖 مشغل بوتات ديسكورد", font_size='22sp', size_hint_y=None, height=50))

        # حقل التوكن
        self.token_input = TextInput(
            hint_text="أدخل توكن البوت هنا...",
            multiline=False,
            size_hint_y=None,
            height=60
        )
        layout.add_widget(self.token_input)

        # زر التشغيل
        self.start_btn = Button(
            text="🚀 تشغيل البوت",
            background_color=(0.2, 0.8, 0.2, 1),
            size_hint_y=None,
            height=60
        )
        self.start_btn.bind(on_press=self.start_bot)
        layout.add_widget(self.start_btn)

        # زر الإيقاف
        self.stop_btn = Button(
            text="🛑 إيقاف البوت",
            background_color=(0.8, 0.2, 0.2, 1),
            size_hint_y=None,
            height=60,
            disabled=True
        )
        self.stop_btn.bind(on_press=self.stop_bot)
        layout.add_widget(self.stop_btn)

        # حالة البوت
        self.status_label = Label(text="الحالة: متوقف", font_size='16sp')
        layout.add_widget(self.status_label)

        return layout

    def update_status(self, text):
        def _update(dt):
            self.status_label.text = f"الحالة: {text}"
        Clock.schedule_once(_update)

    def run_discord_bot(self, token):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        intents = discord.Intents.default()
        self.bot = commands.Bot(command_prefix="!", intents=intents)

        @self.bot.event
        async def on_ready():
            self.update_status(f"🟢 أونلاين: {self.bot.user}")

        try:
            self.loop.run_until_complete(self.bot.start(token))
        except Exception as e:
            self.update_status(f"❌ خطأ: {e}")

    def start_bot(self, instance):
        token = self.token_input.text.strip()
        if not token:
            self.status_label.text = "⚠️ يرجى أدخال توكن!"
            return

        self.update_status("جاري الاتصال بديسكورد...")
        self.start_btn.disabled = True
        self.stop_btn.disabled = False

        self.bot_thread = threading.Thread(target=self.run_discord_bot, args=(token,), daemon=True)
        self.bot_thread.start()

    def stop_bot(self, instance):
        if self.loop and self.bot:
            asyncio.run_coroutine_threadsafe(self.bot.close(), self.loop)
            self.update_status("🔴 تم إيقاف البوت")
            self.start_btn.disabled = False
            self.stop_btn.disabled = True

if __name__ == '__main__':
    DiscordBotApp().run()
      
