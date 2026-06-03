from pydantic import BaseModel, Field, model_validator, field_validator
from typing import Annotated

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
  "declared_total": "285.50"
}

class Item(BaseModel):
    product_name: str
    unit_price: float
    quantity: int = Field(default=1)


class E_commerce(BaseModel):
    order_id: str
    customer_email: str
    items: list[Item]
    declared_total: float
    
    @field_validator('customer_email', mode='before')
    @classmethod
    def validate_customer_email(cls, value:str) -> str:
        if value and isinstance(value ,str):
            return value.strip().lower()
        return value
        
    @model_validator(mode='after')
    def validate_declared_total(self) -> 'E_commerce':
    
        total = sum(item.unit_price * item.quantity for item in self.items)
            
        if total != self.declared_total:
            raise ValueError(f'Total mismatch: Calculated {total}, but got {self.declared_total}')
        return self

        
parse_shopping_data = E_commerce(**shopping_data)
print(parse_shopping_data.model_dump())
     
        
    