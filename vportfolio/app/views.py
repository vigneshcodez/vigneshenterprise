from django.shortcuts import render,redirect
from . models import Blog,Testimonial,Projects,Contact

# Create your views here.
def index(request):
    if request.method == 'GET':
        blog = Blog.objects.filter(featured = True)
        testimonial = Testimonial.objects.all()
        projects = Projects.objects.all()
        return render(request,'pages/index.html',{'blog':blog,'testimonial':testimonial,'projects':projects})
    elif request.method == 'POST':
        name = request.POST['name']
        mobile = request.POST['mobile']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        newcntact = Contact(name=name,mobile_number=mobile,email=email,subject=subject,message=message)
        newcntact.save()
        return redirect('allblogs')

def blog(request,pk):
    blog = Blog.objects.get(id=pk)
    return render(request,'pages/blogpage.html',{'blog':blog})

def allblogs(request):
    allblog  = Blog.objects.all()
    return render(request,'pages/allblog.html',{'blog':allblog})

def contact(request):
    if request.method=='POST':
        name = request.POST['name']
        mobile = request.POST['mobile']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        newcntact = Contact(name=name,mobile_number=mobile,email=email,subject=subject,message=message)
        newcntact.save()
        return redirect('allblogs')
    return render(request,'pages/contact.html')



