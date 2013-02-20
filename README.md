open-singly
===========

Implementation of singly API for Python


Installation
-------------


	pip install git+git://github.com/MagicSolutions/open-singly.git



How to use
----------


	from open_singly import Singly, get_authentication_url

	service = 'facebook'
	client_id = 'My_Client_ID'
	client_secret = 'My_Client_Secret'
	redirect_uri = 'http://www.mywebsite.com/singly/callback/'

	auth_url = get_authentication_url(service, client_id, redirect_uri)

	# The user must be redirected to this URL. After authentication
	# Singly will redirect user to your redirect_uri
	# in the GET parameters there will be a code which You must
	# provide to Singly.authenticate metod

	singly = Singly(client_id, client_secret)
	singly.authenticate(code)

	# After successfull authentication you can execute all methods
	# provided from Singly API like that

	all_profiles = singly.profile.get(verify='true')

	facebook_data = singly.profiles.facebook.get()

	facebook_friends = singly.services.facebook.friends.get()



Enjoy!
