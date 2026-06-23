from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from .agent import handle_query
from .guardrails import check_pii, check_toxicity, rate_limit
app = FastAPI()

class QueryRequest(BaseModel):
    query: str
    session_id: str

class QueryResponse(BaseModel):
    response: str
    action: str

@app.post('/api/v1/query', response_model=QueryResponse)
async def query_endpoint(request: Request, query_request: QueryRequest):
    rate_limit(request)
    check_pii(query_request.query)
    check_toxicity(query_request.query)
    response, action = handle_query(query_request.query, query_request.session_id)
    if action not in ['respond', 'escalate', 'triage']:
        raise HTTPException(status_code=500, detail='Invalid action returned.')
    return QueryResponse(response=response, action=action)

@app.get('/health')
async def health() -> dict:
    return {'status': 'ok'}
