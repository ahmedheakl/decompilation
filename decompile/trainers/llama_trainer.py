"""Trainer implementation for LLaMa model"""
from typing import Tuple, Dict, List
import os
import random
from dataclasses import dataclass
import logging

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
)
from peft import LoraConfig
from trl import SFTTrainer
from datasets import DatasetDict

from decompile.trainers.trainer import Trainer


_LOG = logging.getLogger(__name__)


@dataclass
class LLaMaOpt:
    """Optimizers data model for LLaMa model"""

    dataset_text_field: str = "text"
    model_name: str = "NousResearch/Llama-2-7b-chat-hf"
    new_model: str = "llama-2-7b-decompilation"
    test_ratio: float = 0.14
    lora_r: int = 64
    lora_alpha: int = 16
    lora_dropout: float = 0.1
    use_4bit: bool = True
    bnb_4bit_compute_dtype: str = "float16"
    bnb_4bit_quant_type: str = "nf4"
    use_nested_quant: bool = False
    output_dir: str = "./results"
    num_train_epochs: int = 2
    eval_steps: int = 20
    fp16: bool = False
    bf16: bool = False
    per_device_train_batch_size: int = 4
    per_device_eval_batch_size: int = 4
    gradient_accumulation_steps: int = 1
    gradient_checkpointing: bool = True
    max_grad_norm: float = 0.3
    learning_rate: float = 2e-4
    weight_decay: float = 0.001
    optim: str = "paged_adamw_32bit"
    lr_scheduler_type: str = "constant"
    max_steps: int = -1
    warmup_ratio: float = 0.03
    group_by_length: bool = True
    save_steps: int = 25
    logging_steps: int = 25
    max_seq_length: int = 1100
    packing: bool = False

    instruction: str = "Write the cpp code for this assembly."


class LLaMaTrainer(Trainer):
    """Trainer implementation for LLaMa model"""

    train_dataset_file: str = "train.jsonl"
    test_dataset_file: str = "test.jsonl"

    def __init__(
        self,
        dataset_path: str,
        input_field_name: str = "input",
        output_field_name: str = "output",
        **kwargs,
    ) -> None:
        """Initialize trainer object

        Args:
            dataset_path (str): Path for the dataset folder.
            input_field_name (str): Name of the input field in the dataset.
            output_field_name (str): Name of the output field in the dataset.
        """
        self.dataset_path = dataset_path
        self._split_dataset()
        self.train_dataset, self.test_dataset = self._load_dataset()
        self.train_dataset, self.test_dataset = self._map_dataset(
            input_field_name,
            output_field_name,
        )
        super().__init__(**kwargs)

    def _split_dataset(self) -> None:
        """Load dataset from path and split into train and test"""
        _LOG.info("Splitting dataset...")
        with open(self.dataset_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        random.shuffle(lines)
        test_size = int(len(lines) * LLaMaOpt.test_ratio)
        train_dataset = lines[test_size:]
        test_dataset = lines[:test_size]

        with open(LLaMaTrainer.train_dataset_file, "w", encoding="utf-8") as train_file:
            train_file.writelines(train_dataset)

        with open(LLaMaTrainer.test_dataset_file, "w", encoding="utf-8") as test_file:
            test_file.writelines(test_dataset)

    def _load_dataset(self) -> Tuple[DatasetDict, ...]:
        """Load train and test dataset from path"""
        _LOG.info("Loading dataset...")
        train_dataset = DatasetDict.load_from_disk(LLaMaTrainer.train_dataset_file)
        test_dataset = DatasetDict.load_from_disk(LLaMaTrainer.test_dataset_file)
        return train_dataset, test_dataset

    def _map_dataset(self, input_field: str, output_field: str) -> DatasetDict:
        """Map dataset to LLaMa model

        Args:
            input_field (str): Name of the input field in the dataset.
            output_field (str): Name of the output field in the dataset.
        """
        _LOG.info("Mapping dataset...")

        def mapper_handler(examples: Dict[str, str]) -> Dict[str, List[str]]:
            """Dataset mapper handler"""
            return {
                LLaMaOpt.dataset_text_field: [
                    f"[INST] <<SYS>>\n{input}\n<</SYS>>\n\n"
                    + LLaMaOpt.instruction
                    + " [/INST] "
                    + output
                    for input, output in zip(
                        examples[input_field], examples[output_field]
                    )
                ]
            }

        train_dataset_mapped = self.train_dataset.map(mapper_handler, batched=True)
        test_dataset_mapped = self.test_dataset.map(mapper_handler, batched=True)
        return train_dataset_mapped, test_dataset_mapped

    def train(self):
        """Train LLaMa model"""

        _LOG.info("Training model...")
        compute_dtype = getattr(torch, LLaMaOpt.bnb_4bit_compute_dtype)

        bnb_config = BitsAndBytesConfig(
            load_in_4bit=LLaMaOpt.use_4bit,
            bnb_4bit_quant_type=LLaMaOpt.bnb_4bit_quant_type,
            bnb_4bit_compute_dtype=compute_dtype,
            bnb_4bit_use_double_quant=LLaMaOpt.use_nested_quant,
        )

        model = AutoModelForCausalLM.from_pretrained(
            LLaMaOpt.model_name,
            quantization_config=bnb_config,
            device_map={"": 0},
        )
        model.config.use_cache = False
        model.config.pretraining_tp = 1

        tokenizer = AutoTokenizer.from_pretrained(
            LLaMaOpt.model_name,
            trust_remote_code=True,
        )
        tokenizer.pad_token = tokenizer.eos_token
        tokenizer.padding_side = "right"

        peft_config = LoraConfig(
            lora_alpha=LLaMaOpt.lora_alpha,
            lora_dropout=LLaMaOpt.lora_dropout,
            r=LLaMaOpt.lora_r,
            bias="none",
            task_type="CAUSAL_LM",
        )

        training_arguments = TrainingArguments(
            output_dir=LLaMaOpt.output_dir,
            num_train_epochs=LLaMaOpt.num_train_epochs,
            per_device_train_batch_size=LLaMaOpt.per_device_train_batch_size,
            gradient_accumulation_steps=LLaMaOpt.gradient_accumulation_steps,
            optim=LLaMaOpt.optim,
            save_steps=LLaMaOpt.save_steps,
            logging_steps=LLaMaOpt.logging_steps,
            learning_rate=LLaMaOpt.learning_rate,
            weight_decay=LLaMaOpt.weight_decay,
            fp16=LLaMaOpt.fp16,
            bf16=LLaMaOpt.bf16,
            max_grad_norm=LLaMaOpt.max_grad_norm,
            max_steps=LLaMaOpt.max_steps,
            warmup_ratio=LLaMaOpt.warmup_ratio,
            group_by_length=LLaMaOpt.group_by_length,
            lr_scheduler_type=LLaMaOpt.lr_scheduler_type,
            report_to="all",
            evaluation_strategy="steps",
            eval_steps=LLaMaOpt.eval_steps,
        )

        trainer = SFTTrainer(
            model=model,
            train_dataset=self.train_dataset,
            eval_dataset=self.test_dataset,
            peft_config=peft_config,
            dataset_text_field=LLaMaOpt.dataset_text_field,
            max_seq_length=LLaMaOpt.max_seq_length,
            tokenizer=tokenizer,
            args=training_arguments,
            packing=LLaMaOpt.packing,
        )

        _LOG.info("Training...")
        trainer.train()
        save_path = os.path.join(LLaMaOpt.output_dir, LLaMaOpt.new_model)
        trainer.model.save_pretrained(save_path)

        return model, tokenizer

    @staticmethod
    def add_template(assembly_text: str) -> str:
        """Add template to assembly text

        Args:
            assembly_text (str): Assembly text
        """
        return (
            "[INST] <<SYS>>\n"
            + assembly_text
            + "\n<</SYS>>\n\n"
            + LLaMaOpt.instruction
            + " [/INST] "
        )

    @staticmethod
    def load_model(model_path: str, tokenizer_path: str):
        """Load model from path

        Args:
            model_path (str): Path to the model.
            tokenizer_path (str): Path to the tokenizer.
        """
        model = AutoModelForCausalLM.from_pretrained(model_path)
        tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
        return model, tokenizer
