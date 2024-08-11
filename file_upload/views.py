from django.shortcuts import render
from .forms import UploadFileForm
import pandas as pd
from django.core.mail import send_mail

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            data = pd.read_excel(file)
            
            # Generate summary
            # summary = data.groupby('Cust State')['DPD'].sum().reset_index()
            summary = data.groupby(['Cust State', 'Cust Pin']).size().reset_index(name='DPD')
            summary_final = summary[summary['DPD'] > 1]

            # Convert the summary to a string for email body
            summary_str = summary_final.to_string(index=False)

            # Send the email
            send_mail(
                'Python Assignment - Aman Gupta',
                summary_str,
                'esportsevilorg@gmail.com',
                ['aman775503@gmail.com'],
                fail_silently=False,
            )

            return render(request, 'file_upload/success.html', {'summary': summary_str})
    else:
        form = UploadFileForm()
    return render(request, 'file_upload/upload.html', {'form': form})
