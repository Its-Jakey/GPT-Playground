import openai
import json
import sys
import os

from PyQt6 import uic
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QUrl, QModelIndex
from PyQt6.QtCore import Qt
from PyQt6 import QtCore, QtGui, QtWidgets


Form, Window = uic.loadUiType("ui.ui")
restore = None


def send_gpt(api_key, model_name, system_prompt, user_prompt):
    # Initialize the OpenAI API client with your API key
    openai.api_key = api_key

    # Call the OpenAI API to generate a response
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
        # temperature=0.2,
        # max_tokens=1000,
        # frequency_penalty=0.0
    )

    return response['choices'][0]['message']['content']


def write_restore(api_key, model_name, system_prompt, user_prompt):
    with open('restore.json', 'w') as f:
        json.dump({
            'api_key': api_key,
            'model_name': model_name,
            'system_prompt': system_prompt,
            'user_prompt': user_prompt,
        }, f)


class PlaygroundWindow(Window, Form):
    
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)

        self.btnSubmit.clicked.connect(self.submitClicked)

        if restore is not None:
            self.inpApiKey.setText(restore['api_key'])
            self.drpModelName.setCurrentText(restore['model_name'])
            self.inpSystemPrompt.setPlainText(restore['system_prompt'])
            self.inpUserPrompt.setPlainText(restore['user_prompt'])
    
    def submitClicked(self):
        api_key = self.inpApiKey.text()
        model_name = self.drpModelName.currentText()
        system_prompt = self.inpSystemPrompt.toPlainText()
        user_prompt = self.inpUserPrompt.toPlainText()

        write_restore(api_key, model_name, system_prompt, user_prompt)
        self.inpOutput.setPlainText("Generating...")
        self.inpOutput.repaint()
        response = send_gpt(api_key, model_name, system_prompt, user_prompt)

        self.inpOutput.setPlainText(response)


def main():
    global restore

    if os.path.exists('restore.json'):
        with open('restore.json', 'r') as f:
            restore = json.load(f)

    app = QApplication(sys.argv)
    window = PlaygroundWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
