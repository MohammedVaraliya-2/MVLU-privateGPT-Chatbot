from django.shortcuts import render, redirect
from django.http import HttpResponse
import os
from .privateGPT_logic import get_response
import asyncio
from .ingest_new_file import main  # Import the ingestion logic

def home(request):
    if request.method == 'POST' and request.FILES.get('file'):
        # Save the uploaded file to a temporary location
        uploaded_file = request.FILES['file']
        file_path = os.path.join('uploads', uploaded_file.name)
        with open(file_path, 'wb') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        # Process the uploaded file using the ingestion logic
        main()  # Run the ingestion logic

        # Redirect the user to the chatbot page after ingestion
        return redirect('chatbot')

    return render(request, 'home.html')

# Define an asynchronous view to handle chatbot interactions
async def chatbot(request):

    ingested_data = request.session.get('ingested_data', None)

    if request.method == 'POST':
        # Get the user's question from the form
        user_question = request.POST.get('input_text', '')

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, lambda: get_response(user_question))

        # Display the response to the user
        return HttpResponse(response, content_type="text/html")

    return render(request, 'chatbot.html')
