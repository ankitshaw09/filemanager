import os
from django.shortcuts import render
from .models import FileScan
from django.http import HttpResponse

def index(request):
    # Handle search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        file_scans = FileScan.objects.filter(name__icontains=search_query)
    else:
        file_scans = FileScan.objects.all()

    # Handle directory input and save folder names
    if request.method == 'POST':
        directory = request.POST.get('directory')

        if directory and os.path.isdir(directory):
            # Get all subfolders and sub files in the directory
            
            folders = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
            files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
            
            # Save the file names to the database (FileScan model)
            for file_name in files:
                FileScan.objects.get_or_create(name=file_name)
                
            # Save the folder names to the database (FileScan model)
            for folder_name in folders:
                FileScan.objects.get_or_create(name=folder_name)
                

            

            # Save the folder names to the database (FileScan model)
            # for folder_name in folders:
            #     FileScan.objects.get_or_create(name=folder_name)

            # Show success message
            return render(request, 'index.html', {'file_scans': file_scans})
            # return HttpResponse("Folders have been saved successfully!")
        
        
        
                
            
        else:
            return HttpResponse("The directory does not exist or is invalid.")

    return render(request, 'index.html', {'file_scans': file_scans})
