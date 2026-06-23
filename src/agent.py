
SYSTEM_PROMPT = "You are a customer support agent for a SaaS product. Your role is to assist users by answering FAQs, triaging tickets, and escalating issues to human agents when necessary. Ensure all responses are accurate, relevant, and comply with privacy regulations. Use the provided tools and integrations to manage customer interactions effectively."


def handle_query(query: str, session_id: str):
    # Placeholder for LLM interaction and business logic
    # This function should interact with the LLM using the SYSTEM_PROMPT
    # and return a response and action based on the query.
    response = "To reset your password, please click on the 'Forgot Password' link on the login page and follow the instructions sent to your email."
    action = "respond"
    return response, action
