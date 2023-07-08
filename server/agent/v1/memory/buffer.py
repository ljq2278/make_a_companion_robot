from typing import Any, Dict, List, Optional

from pydantic import root_validator

from langchain.memory.chat_memory import BaseChatMemory, BaseMemory
from langchain.memory.utils import get_prompt_input_key
from langchain.schema.messages import get_buffer_string

import os, re


class ConversationBufferMemory(BaseChatMemory):
    """Buffer for storing conversation memory."""

    human_prefix: str = "Human"
    ai_prefix: str = "AI"
    memory_key: str = "history"  #: :meta private:

    @property
    def buffer(self) -> Any:
        """String buffer of memory."""
        if self.return_messages:
            return self.chat_memory.messages
        else:
            return get_buffer_string(
                self.chat_memory.messages,
                human_prefix=self.human_prefix,
                ai_prefix=self.ai_prefix,
            )

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
        files = os.listdir(directory)
        files = sorted(files, key=lambda x: int(x.split('.')[0]))
        for file in files:
            with open(os.path.join(directory, file), "r") as old_file:
                lines = old_file.readlines()
                for line in lines:
                    prefix = line.split(': ')[0]
                    if prefix == 'Human':
                        self.chat_memory.add_user_message(line[7:])
                    elif prefix == 'AI':
                        self.chat_memory.add_user_message(line[4:])
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
                prefix = 'Human: ' if i % 2 == 0 else 'AI: '
                new_file.write(prefix + self.chat_memory.messages[-i].content + '\n')


class ConversationStringBufferMemory(BaseMemory):
    """Buffer for storing conversation memory."""

    human_prefix: str = "Human"
    ai_prefix: str = "AI"
    """Prefix to use for AI generated responses."""
    buffer: str = ""
    output_key: Optional[str] = None
    input_key: Optional[str] = None
    memory_key: str = "history"  #: :meta private:

    @root_validator()
    def validate_chains(cls, values: Dict) -> Dict:
        """Validate that return messages is not True."""
        if values.get("return_messages", False):
            raise ValueError(
                "return_messages must be False for ConversationStringBufferMemory"
            )
        return values

    @property
    def memory_variables(self) -> List[str]:
        """Will always return list of memory variables.
        :meta private:
        """
        return [self.memory_key]

    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, str]:
        """Return history buffer."""
        return {self.memory_key: self.buffer}

    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        """Save context from this conversation to buffer."""
        if self.input_key is None:
            prompt_input_key = get_prompt_input_key(inputs, self.memory_variables)
        else:
            prompt_input_key = self.input_key
        if self.output_key is None:
            if len(outputs) != 1:
                raise ValueError(f"One output key expected, got {outputs.keys()}")
            output_key = list(outputs.keys())[0]
        else:
            output_key = self.output_key
        human = f"{self.human_prefix}: " + inputs[prompt_input_key]
        ai = f"{self.ai_prefix}: " + outputs[output_key]
        self.buffer += "\n" + "\n".join([human, ai])

    def clear(self) -> None:
        """Clear memory contents."""
        self.buffer = ""
