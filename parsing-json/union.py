from pydantic import BaseModel, Field, field_validator, model_validator, ValidationError
from typing import Union, Annotated, Literal

shopping_data = {
  "order_id": "ORD-99421",
  "customer_email": "   USER@Example.COM   ",
  "items": [
    {
      "product_name": "Mechanical Keyboard",
      "unit_price": "120.00",
      "quantity": "2"
    },
    {
      "product_name": "Wireless Mouse",
      "unit_price": "45.50"
    }
  ],
  "declared_total": "285.50",
  "payment_type": 
    #   {
    #       "method": "credit_card",
    #       "card_number": "411111111111",
    #       "cvv": "123"
    #   }
        {
          "method": "paypal",
          "paypal_email": "user@example.com",
          "auth_token": "PAY-ATTN839102938X"
      }
}

bad_shopping_data = {
  "order_id": "ORD-99421",
  "customer_email": "   USER@Example.COM   ",
  "items": [
    {
      "product_name": "Mechanical Keyboard",
      "unit_price": "120.00",
      "quantity": "2"
    },
    {
      "product_name": "Wireless Mouse",
      "unit_price": "45.50"
    }
  ],
  "declared_total": "285.50",
  "payment_type": 
    #   {
    #       "method": "credit_card",
    #       "card_number": "411111111111",
    #       "cvv": "123"
    #   }
        {
        #   "method": "paypal",
          "paypal_email": "user@example.com",
          "auth_token": "PAY-ATTN839102938X"
      }
}


class Item(BaseModel):
    product_name: str
    unit_price: float
    quantity: int = Field(default=1)

class CreditCard(BaseModel):
    method: Literal['credit_card']
    card_number: str
    cvv: str
    
class Paypal(BaseModel):
    method: Literal['paypal']
    paypal_email: str
    auth_token: str
    
class E_commerce(BaseModel):
    order_id: str
    customer_email: str
    items: list[Item]
    declared_total: float
    payment_type: Annotated[Union[CreditCard, Paypal], Field(discriminator='method')]
    
    @field_validator('customer_email', mode='before')
    @classmethod
    def validate_customer_email(cls, value:str):
        if value and isinstance(value, str):
            return value.strip().lower()
        return value
    
    @model_validator(mode='after')
    def validate_declared_total(self):
        total = sum(item.quantity * item.unit_price for item in self.items)
        
        if total != self.declared_total:
            raise ValueError(f'Total Mismatch: acutal total price {total} and declared total price {self.declared_total}')
        return self

try:
    parsed_json = E_commerce(**bad_shopping_data)
    print(parsed_json.model_dump())
except ValidationError as e:
    # extract the structured error list
    error_details = e.errors()
    
    for error in error_details:
        if error['type'] == 'union_tag_not_found':
            location = " -> ".join(str(loc) for loc in error['loc'])
            print(f"The field '{location}' is missing its routing method.")
            print(f"Pydantic's raw message: {error['msg']}")

        
        
    

