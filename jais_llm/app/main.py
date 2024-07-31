
from fastapi import FastAPI, UploadFile
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
model_path = "core42/jais-13b-chat"

app = FastAPI()

device = "cuda" if torch.cuda.is_available() else "cpu"

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path, device_map="auto", trust_remote_code=True)

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI app!"}

@app.get("/prediction")
def prediction(text: str, temperature: float, top_p: float):
    
    try:
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        input_ids = inputs.input_ids.to(device)
        attention_mask = inputs.attention_mask.to(device)
        input_len = inputs["input_ids"].shape[-1]
        generate_ids = model.generate(
            input_ids,
            attention_mask=attention_mask,
            top_p=top_p,
            temperature=temperature,
            max_length=2048-input_len,
            min_length=input_len + 4,
            repetition_penalty=1.2,
            do_sample=True,
        )
        response = tokenizer.batch_decode(
            generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True
        )[0]
        
        response = response.split("### Response: [|AI|]")      
        return {"response": response}
    
    except KeyError as e:
        raise HTTPException(status_code=500, detail=f"KeyError: {str(e)}")
    except AttributeError as e:
        raise HTTPException(status_code=500, detail=f"AttributeError: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")