from typing import Any, Dict, List
import os, re
from pydantic import root_validator

from langchain.memory.chat_memory import BaseChatMemory
from langchain.memory.summary import SummarizerMixin
from langchain.schema.messages import BaseMessage, get_buffer_string


class ConversationSummaryBufferMemory(BaseChatMemory, SummarizerMixin):
    """Buffer with summarizer for storing conversation memory."""

    max_token_limit: int = 2000
    moving_summary_buffer: str = ""
    memory_key: str = "history"
    character: str = ""

    @property
    def buffer(self) -> List[BaseMessage]:
        return self.chat_memory.messages

    @property
    def memory_variables(self) -> List[str]:
        """Will always return list of memory variables.

        :meta private:
        """
        return [self.memory_key]

    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Return history buffer."""
        buffer = self.buffer
        if self.moving_summary_buffer != "":
            first_messages: List[BaseMessage] = [
                self.summary_message_cls(content=self.moving_summary_buffer)
            ]
            buffer = first_messages + buffer
        if self.return_messages:
            final_buffer: Any = buffer
        else:
            final_buffer = get_buffer_string(
                buffer, human_prefix=self.human_prefix, ai_prefix=self.ai_prefix
            )
        return {self.memory_key: final_buffer}

    @root_validator()
    def validate_prompt_input_variables(cls, values: Dict) -> Dict:
        """Validate that prompt input variables are consistent."""
        prompt_variables = values["prompt"].input_variables
        expected_keys = {"summary", "new_lines"}
        if expected_keys != set(prompt_variables):
            raise ValueError(
                "Got unexpected prompt input variables. The prompt expects "
                f"{prompt_variables}, but it should have {expected_keys}."
            )
        return values

    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        """Save context from this conversation to buffer."""
        super().save_context(inputs, outputs)
        self.prune()

    def prune(self) -> None:
        """Prune buffer if it exceeds max token limit"""
        buffer = self.chat_memory.messages
        curr_buffer_length = self.llm.get_num_tokens_from_messages(buffer)
        if curr_buffer_length > self.max_token_limit:
            pruned_memory = []
            while curr_buffer_length > self.max_token_limit and len(self.chat_memory.messages) >= 4:
                pruned_memory.append(buffer.pop(0))
                pruned_memory.append(buffer.pop(0))
                curr_buffer_length = self.llm.get_num_tokens_from_messages(buffer)
            self.moving_summary_buffer = self.character + self.predict_new_summary(
                pruned_memory, self.moving_summary_buffer[len(self.character):]
            )

    def clear(self) -> None:
        """Clear memory contents."""
        super().clear()
        self.moving_summary_buffer = ""

    def load_from_file(self, directory):
        with open(os.path.join(directory, "character.txt"), "r", encoding='utf-8') as old_file:
            self.character = old_file.read()
        last_one = 'ai'
        with open(os.path.join(directory, 'last_conversations.txt'), "r", encoding='utf-8') as old_file:
            lines = old_file.readlines()
            for line in lines:
                prefix = line.split(':')[0]
                if prefix == self.ai_prefix and last_one != 'ai':
                    self.chat_memory.add_ai_message(line)
                    last_one = 'ai'
                elif (prefix == 'Environment' or prefix == 'Human') and last_one == 'ai':
                    self.chat_memory.add_user_message(line)
                    last_one = 'other'
                # elif prefix == self.env_prefix:
                #     self.chat_memory.add_message(EnvMessage(content=line[5:]))
        with open(os.path.join(directory, "memory.txt"), "r", encoding='utf-8') as old_file:
            summary = old_file.read()
            self.moving_summary_buffer = self.character + summary
        return

    def save_to_file(self, directory):
        os.remove(os.path.join(directory, "last_conversations.txt"))
        with open(os.path.join(directory, "last_conversations.txt"), "w", encoding='utf-8') as conversations_file:
            for i in range(0, len(self.chat_memory.messages)):
                conversations_file.write(self.chat_memory.messages[i].content + '\n')
        os.remove(os.path.join(directory, "memory.txt"))
        with open(os.path.join(directory, "memory.txt"), "w", encoding='utf-8') as memory_file:
            memory_file.write(self.moving_summary_buffer[len(self.character):] + '\n')
