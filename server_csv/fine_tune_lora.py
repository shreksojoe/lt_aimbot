# fine_tune_lora.py
from transformers import LlamaForCausalLM, LlamaTokenizer, Trainer, TrainingArguments
from datasets import load_dataset
from peft import LoraConfig, get_peft_model

# Load dataset
dataset = load_dataset("json", data_files="dataset.jsonl")  # JSONL from your PDFs/CSVs

# Load base LLaMA 2 3B model
model_name = "meta-llama/Llama-2-3b-hf"
tokenizer = LlamaTokenizer.from_pretrained(model_name)
model = LlamaForCausalLM.from_pretrained(model_name, device_map="auto", load_in_8bit=True)

# Configure LoRA
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj","v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)
model = get_peft_model(model, lora_config)

# Tokenize dataset
def tokenize(batch):
    inputs = tokenizer(batch["input"], truncation=True, max_length=2048)
    outputs = tokenizer(batch["output"], truncation=True, max_length=1024)
    inputs["labels"] = outputs["input_ids"]
    return inputs

tokenized_dataset = dataset.map(tokenize, batched=True)

# Training arguments
training_args = TrainingArguments(
    output_dir="./lora_finetuned",
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    num_train_epochs=3,
    learning_rate=2e-4,
    fp16=True,
    logging_steps=10,
    save_strategy="epoch",
    save_total_limit=2
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"]
)

# Train and save LoRA adapter
trainer.train()
trainer.save_model("./lora_finetuned")
