from django.shortcuts import render


def RedirectHTMLView(request):
    redirect_url = 'https://example.com'  # Replace with your desired redirect URL
    context = {'redirect_url': redirect_url}
    return render(request, 'index.html', context)
