from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Profile, Project, Skill, Education, Experience, Certificate

def profile_details(request):
    try:
        profile = Profile.objects.first()
        projects = Project.objects.all()
        skills = Skill.objects.all()
        educations = Education.objects.all().order_by('-year')  # Most recent first
        experiences = Experience.objects.all().order_by('-id')
        certificates = Certificate.objects.all().order_by('-year')
        featured_project = Project.objects.filter(
            title__iexact="Fixigo"
        ).first()
        
        context = {
            'profile': profile,
            'projects': projects,
            'skills': skills,
            'educations': educations,
            'experiences': experiences,
            'certificates': certificates,
            'projects_count': projects.count(),
            'skills_count': skills.count(),
            'educations_count': educations.count(),
            'experiences_count': experiences.count(),
            'certificates_count': certificates.count(),
            'featured_project': featured_project
        }
        
        return render(request, 'index.html', context)
    
    except Exception as e:
        return render(request, 'index.html', {
            'profile': None,
            'projects': [],
            'skills': [],
            'educations': [],
            'experiences': [],
            'certificates': [],
            'projects_count': 0,
            'skills_count': 0,
            'educations_count': 0,
            'experiences_count': 0,
            'certificates_count': 0,
            'featured_project': None,
            'error': str(e)
        })


def send_contact_message(request):
    """
    Handle contact form submission and send email
    """
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', 'No Subject').strip()
        message = request.POST.get('message', '').strip()
        
        # Validate required fields
        if not name:
            messages.error(request, 'Please enter your name.')
            return redirect('home')
        
        if not email:
            messages.error(request, 'Please enter your email address.')
            return redirect('home')
        
        if not message:
            messages.error(request, 'Please enter your message.')
            return redirect('home')
        
        # Validate email format (basic)
        if '@' not in email or '.' not in email:
            messages.error(request, 'Please enter a valid email address.')
            return redirect('home')
        
        try:
            # Get profile for email template
            profile = Profile.objects.first()
            
            # Prepare email to you (site owner)
            html_message = render_to_string('emails/contact_email.html', {
                'name': name,
                'email': email,
                'subject': subject,
                'message': message,
                'profile': profile
            })
            
            plain_message = strip_tags(html_message)
            
            # Send email to site owner
            send_mail(
                subject=f"Portfolio Contact: {subject} from {name}",
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_HOST_USER],  # Your email address
                html_message=html_message,
                fail_silently=False,
            )
            
            # Send auto-reply to the user
            auto_reply_html = render_to_string('emails/auto_reply.html', {
                'name': name,
                'email': email,
                'profile': profile
            })
            auto_reply_plain = strip_tags(auto_reply_html)
            
            send_mail(
                subject="Thank you for reaching out!",
                message=auto_reply_plain,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                html_message=auto_reply_html,
                fail_silently=False,
            )
            
            messages.success(request, 'Your message has been sent successfully! I will get back to you soon.')
            
        except Exception as e:
            # Log the error (you can use logging module)
            print(f"Email error: {str(e)}")
            messages.error(request, f'Something went wrong. Please try again later or contact me directly at {settings.EMAIL_HOST_USER}.')
            
        return redirect('home')
    
    # If GET request, redirect to home
    return redirect('home')