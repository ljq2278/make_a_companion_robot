from __future__ import annotations
from abc import ABC
from abc import abstractmethod
from typing import Any, Dict, List, Sequence, Tuple, Optional

from pydantic import Field

from langchain.memory.chat_memory import BaseChatMemory, BaseMemory
from langchain.schema import get_buffer_string

import os, re


class ConversationBufferMemory(BaseChatMemory):
    """Buffer for storing conversation memory."""

    human_prefix: str = "Human"
    # env_prefix: str = "Env"
    ai_prefix: str = "AI"
    memory_key: str = "history"  #: :meta private:

    @property
    def buffer(self) -> Any:
        """String buffer of memory."""
        if self.return_messages:
            return self.chat_memory.messages
        else:
            return '\n'.join([x.content for x in self.chat_memory.messages])


    @property
    def memory_variables(self) -> List[str]:
        """Will always return list of memory variables.

        :meta private:
        """
        return [self.memory_key]

    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Return history buffer."""
        return {self.memory_key: self.buffer}

    def load_from_file(self, directory):
        files = [x for x in os.listdir(directory) if x.split('.')[0].isdigit()]
        files = sorted(files, key=lambda x: int(x.split('.')[0]))
        for file in files:
            with open(os.path.join(directory, file), "r") as old_file:
                lines = old_file.readlines()
                for line in lines:
                    prefix = line.split(':')[0]
                    if prefix == self.ai_prefix:
                        self.chat_memory.add_ai_message(line)
                    elif prefix == 'Environment' or prefix == 'Human':
                        self.chat_memory.add_user_message(line)
                    # elif prefix == self.env_prefix:
                    #     self.chat_memory.add_message(EnvMessage(content=line[5:]))
        return

    def save_to_file(self, directory, save_period):

        # Get the list of files in the directory
        files = os.listdir(directory)

        # Find the current highest numbered file
        highest_number = 0
        for file in files:
            match = re.match(r"(\d+)\.txt", file)
            if match:
                number = int(match.group(1))
                if number > highest_number:
                    highest_number = number

        # Create a new file with the next number in the sequence
        new_file_number = highest_number + 1
        new_file_name = f"{new_file_number}.txt"

        # Write the last 10 conversation to the new file

        with open(os.path.join(directory, new_file_name), "w") as new_file:
            for i in reversed(range(1, save_period + 1)):
                # prefix = self.env_prefix if i % 3 == 0 else self.human_prefix if i % 3 == 1 else self.ai_prefix
                new_file.write(self.chat_memory.messages[-i].content + '\n')

