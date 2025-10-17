# cpu_inference.py
from transformers import LlamaForCausalLM, LlamaTokenizer
from peft import PeftModel
import torch

# Paths to model folders
base_model_path = "/path/to/llama-2-3b-hf"
lora_path = "/path/to/lora_finetuned"

# Load tokenizer and models
tokenizer = LlamaTokenizer.from_pretrained(base_model_path)
base_model = LlamaForCausalLM.from_pretrained(base_model_path, device_map="cpu")
model = PeftModel.from_pretrained(base_model, lora_path)

# Example PDF text
pdf_text = open("example.txt").read()
prompt = f"Convert the following text to CSV:\n{pdf_text}\n\nCSV:"

# Tokenize and generate CSV
inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=512)
csv_output = tokenizer.decode(outputs[0], skip_special_tokens=True)

print(csv_output)
