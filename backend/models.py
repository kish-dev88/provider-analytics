from typing import Literal
from pydantic import BaseModel, Field
Severity = Literal["Critical","High","Medium","Low"]
class Provider(BaseModel):
    id:int; name:str; npi:str; change_type:str; severity:Severity; confidence:int; status:str
    old_value:str; proposed_value:str; payer_address:str; nppes_address:str; pecos_address:str
    payer_specialty:str; nppes_specialty:str; pecos_specialty:str; payer_status:str; nppes_status:str; pecos_enrollment:str
    submitted_by:str; submitted_at:str; agent_reason:str
class ProposedChange(BaseModel): proposed_value:str=Field(min_length=1)
class BulkApproval(BaseModel): provider_ids:list[int]=Field(min_length=1)
class SourceRefreshResponse(BaseModel): source:str; last_refreshed:str; status:str
