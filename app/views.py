from django.shortcuts import render
from django.http import HttpResponse
import os
from .privateGPT_logic import get_response
import asyncio

# Define an asynchronous view to handle chatbot interactions
async def chatbot(request):
    if request.method == 'POST':
        # Get the user's question from the form
        user_question = request.POST.get('input_text', '')

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, lambda: get_response(user_question))

        # Display the response to the user
        return HttpResponse(response, content_type="text/html")

    return render(request, 'chatbot.html')
