open-singly
===========

Implementation of singly API for Python


Installation
-------------


	pip install open-singly


or

	pip install git+https://github.com/MagicSolutions/open-singly.git



How to use
----------


	from open_singly import Singly

	client_id = 'My_Client_ID'
	client_secret = 'My_Client_Secret'
	redirect_uri = 'http://www.mywebsite.com/singly/callback/'

	singly = Singly(client_id, client_secret, redirect_uri)

	# Get authentication URL for facebook for example
	auth_url = singly.get_authentication_url('facebook')

	# The user must be redirected to this URL. After authentication
	# Singly will redirect user to your redirect_uri
	# in the GET parameters there will be a code which You must
	# provide to Singly.authenticate metod

	api = singly.authenticate(code)

	# After successfull authentication you can execute all methods
	# provided from Singly API like that

	all_profiles = api.profile.get(verify='true')

	facebook_data = api.profiles.facebook.get()

	facebook_friends = api.services.facebook.friends.get()



Enjoy!
