from django.shortcuts import render,get_object_or_404,redirect
from blog.models import Yazi 
# Create your views here.
from django.http import HttpResponse
from blog.models import Yazi
from blog.forms import RegisterForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserChangeForm,AuthenticationForm
from django.contrib.auth.decorators import login_required
from blog.forms import KullaniciProfiliGuncelleForm

def ana_sayfa(request):
    #modelden tüm yazıları çeker
    yazilar=Yazi.objects.all().order_by('-id')[:5] #son 5 yazıyı alır

    return render(request,'blog/ana_sayfa.html',{'yazilar':yazilar}
                  
                  )
def guncelle(request,id):
    yazi=get_object_or_404(Yazi,id=id)
    if request.method =='POST':
        
        
        yazi.baslik =request.POST['baslik']
        yazi.yazar =request.POST['yazar']
        yazi.icerik=request.POST['icerik']
        
        yazi.save()

        return redirect('ana_sayfa')
    return render(request,'blog/guncelle.html',{'yazi': yazi})

def sil(request, id):
    yazi = get_object_or_404(Yazi, id=id)
    if request.method == "POST":
        yazi.delete()
        return redirect('ana_sayfa')
    
    return render(request, 'blog/sil.html', {'yazi': yazi})

def tum_yazilar(request):
        yazilar = Yazi.objects.all() # tüm yazılar gelicektir bu fonksiyonla
        return render(request,'blog/tum_yazilar.html',{'yazilar':yazilar})

def yazi_detay(request,id):
    
    try:
        yazi = Yazi.objects.get(id=id)
        return render(request, 'blog/yazi_detay.html', {'yazi': yazi})
    except Yazi.DoesNotExist:
        return HttpResponse("Bu ID ile eşleşen bir yazı bulunamadı!")
    except Yazi.MultipleObjectsReturned:
        return HttpResponse("Birden fazla eşleşen yazı var, filtreleme kullanmalısın!")


def test_view(request):
     return HttpResponse("<h1>Bu bir test sayfasıdır</h1>")

def register(request):
    if request.method =="POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user= form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request,user)  #bu kısımda kullanıcıya giriş yaptıracağız
            return redirect("ana_sayfa") # kayıt sonrası yönlendirme
          
    else:
            form = RegisterForm()

    return render(request,"blog/register.html",{"form":form}) 


def profil_guncelle(request):
    if request.method =="POST":
        form = KullaniciProfiliGuncelleForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('ana_sayfa') #güncelleyince ana sayfaya yönlendir
    else:
        form = KullaniciProfiliGuncelleForm(instance=request.user)

    return render(request,'blog/profil_guncelle.html',{'form':form})
          
def hesap_sil(request):
     if request.method =="POST":
          request.user.delete() # kullanıcıyı veritabanından sil 
          logout(request)
          return redirect("ana_sayfa")
     return render(request,"blog/hesap_sil.html")

def kullanici_giris(request):
    if request.method =="POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect("ana_sayfa")
        else:
            return render(request, "blog/giris.html", {"form": form, "hata": "Kullanıcı adı veya şifre hatalı!"})
  
    else:
         form =AuthenticationForm()

    return render(request,"blog/giris.html",{"form":form})
