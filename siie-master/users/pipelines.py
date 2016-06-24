from django.core.mail import EmailMessage
import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

def get_avatar(backend, strategy, details, response, user=None,*args,**kwargs):

	url=None
	if backend.name == 'facebook':
		url="http://graph.facebook.com/%s/picture?type=large"%response['id']
		
	if backend.name == 'twitter' :
		url = response.get('profile_image_url' , '').replace('_normal','')
	
	
	if backend.name == 'google-oauth2' :
		url = response['image'].get('url')


	if url:
		save_image_from_url(user,url)

def save_image_from_url(model, url):
    r = requests.get(url)

    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(r.content)
    img_temp.flush()

    model.avatar.save("image.jpg", File(img_temp), save=True)

def enviar_email(backend, strategy,request , details, response,is_new=False, user=None,*args,**kwargs):
	if user and is_new:
		send_email(details)
	else:
		return


def send_email(details):

	msg = EmailMessage(subject='Bienvenida',
						from_email = 'info@karatbarsamerica.com',
						to=[details['email']])

	msg.template_name = 'welcome'
	msg.template_content = {
		'std_content00' : '<h1>HOLA %s Bienvenido </h1>' % details['fullname']
	}
	msg.send()
