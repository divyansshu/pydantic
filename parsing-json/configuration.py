from pydantic import BaseModel, ConfigDict

class model(BaseModel):
    
    model_config = ConfigDict(
                              extra='forbid', # crash if extra fields are passed # allow, ignore
                              frozen=True, # prevent fields from being changed later
                              str_strip_whitespace=True, # cleanup  spaces automatically
                              str_to_lower=True
                              )
    order_id: int
    fname: str

# event = model(order_id='123', name='DIvyanshu', utm_source='google', order_Id='123')
event = model(order_id='123', fname=' DIvyanshu')
print(event.model_dump())
print(event.model_extra)
    