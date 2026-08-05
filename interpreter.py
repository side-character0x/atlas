from pathlib import Path

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel


class AtlasInterpreter:
    def __init__(
        self,
        base_model="Qwen/Qwen2.5-0.5B-Instruct",
        adapter_path=None
    ):
        if adapter_path is None:
            adapter_path = Path(__file__).parent / "data" / "atlas-interpreter"

        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.tokenizer = AutoTokenizer.from_pretrained(
            base_model
        )

        base = AutoModelForCausalLM.from_pretrained(
            base_model,
            torch_dtype="auto"
        )

        base = base.to(self.device)

        self.model = PeftModel.from_pretrained(
            base,
            adapter_path
        )

        self.model.eval()

    def interpret(self, command):
        messages = [
            {
                "role": "user",
                "content": command
            }
        ]

        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        inputs = self.tokenizer(
            text,
            return_tensors="pt"
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=30,
                do_sample=False
            )

        result = self.tokenizer.decode(
            outputs[0][inputs["input_ids"].shape[1]:],
            skip_special_tokens=True
        ).strip()

        return result
class WakeupInterpreter:
    def __init__(
        self,
        base_model="Qwen/Qwen2.5-0.5B-Instruct",
        adapter_path=None
    ):
        if adapter_path is None:
            adapter_path = Path(__file__).parent / "data" / "wakeup-interpreter"

        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.tokenizer = AutoTokenizer.from_pretrained(
            base_model
        )

        base = AutoModelForCausalLM.from_pretrained(
            base_model,
            torch_dtype="auto"
        )

        base = base.to(self.device)

        self.model = PeftModel.from_pretrained(
            base,
            adapter_path
        )

        self.model.eval()
    def interpret(self, command):   
        messages = [
                {
                    "role": "user",
                    "content": command
                }
            ]
    
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        inputs = self.tokenizer(
            text,
            return_tensors="pt"
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=30,
                do_sample=False
            )

        result = self.tokenizer.decode(
            outputs[0][inputs["input_ids"].shape[1]:],
            skip_special_tokens=True
        ).strip()

        return result