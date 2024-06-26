from fastapi import FastAPI, Form, Request, HTTPException
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from creditcard import CreditCard
import re

app = FastAPI()
templates = Jinja2Templates(directory='templates')

def is_numeric(s):
    return all(char.isdigit() for char in s)

# Valid credit card numbers:
 
#     Visa: 4111111111111111
#     Mastercard: 5555555555554444
#     American Express: 378282246310005
#     Discover: 6011111111111117
 
# Invalid credit card numbers:
 
#     Invalid length: 123456789012345
#     Invalid checksum: 4111111111111112
#     Invalid format: 1234-5678-9012-3456
#     Empty: ""


@app.post("/validate")
async def validate_credit_card_endpoint(card_number: str = Form(...)):    
    # Check if the input consists only of digits
    if not is_numeric(card_number):
        raise HTTPException(status_code=400, detail="Card number must contain only digits")

    # Check if the card is valid
    card = CreditCard(card_number)
    if not card.is_valid:
        return {"valid": False}
    
    return {"valid": True}
 

@app.post("/validate_multiple")
async def validate_multiple_credit_cards(file: UploadFile = File(...)):
    # Read the contents of the uploaded file
    file_content = await file.read()

    # Split the content into lines and filter out any empty lines
    card_numbers = [line.strip().replace("-", "") for line in file_content.decode("utf-8").split("\n") if line.strip()]

    validation_results = []
    for card_number in card_numbers:
        # Check if the input consists only of digits
        if not is_numeric(card_number):
            raise HTTPException(status_code=400, detail=f"Card number '{card_number}' must contain only digits")

        # Check if the card is valid
        card = CreditCard(card_number)
        validation_results.append({"card_number": card_number, "valid": card.is_valid})

    return validation_results

@app.get('/validate-page', response_class=HTMLResponse)
def main(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.get('/validate_multiple-page', response_class=HTMLResponse)
def main(request: Request):
    return templates.TemplateResponse('upload.html', {'request': request})


@app.get('/', response_class=HTMLResponse)
def main(request: Request):
    return templates.TemplateResponse('main.html', {'request': request})

