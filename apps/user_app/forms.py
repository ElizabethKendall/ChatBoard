from django import forms
from .models import User

class RegistrationForm(forms.Form):
	email = forms.EmailField()
	first_name = forms.CharField(max_length=100)
	last_name = forms.CharField(max_length=100)
	password = forms.CharField(max_length=100, widget=forms.PasswordInput)
	confirm_password = forms.CharField(max_length=100, widget=forms.PasswordInput)

class RegisterForm(forms.ModelForm):
	# Confirm pword code from Savai Maheshwari at https://stackoverflow.com/questions/34609830/django-modelform-how-to-add-a-confirm-password-field
	password = forms.CharField(max_length=100, widget=forms.PasswordInput)
	confirm_password = forms.CharField(max_length=100, widget=forms.PasswordInput)
	class Meta:
		model = User
    #   fields = '__all__'
		fields = ['email','first_name','last_name','password']
	def clean(self):
		cleaned_data = super(RegisterForm, self).clean()
		
		password = cleaned_data.get("password")
		confirm_password = cleaned_data.get("confirm_password")
		
		if password != confirm_password:
			self.add_error('confirm_password', "Password does not match.")

		email = cleaned_data.get('email')
		users = User.objects.filter(email=email)
		if len(users) != 0:
			self.add_error('email', "Email address is already registered in this system. Please try again.")
		return cleaned_data

class SignInForm(forms.Form):
	email = forms.EmailField()
	password = forms.CharField(max_length=100, widget=forms.PasswordInput)

class SignIn_Form(forms.ModelForm):
	password = forms.CharField(max_length=100, widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = ['email','password']
	def clean(self):
		cleaned_data = super(SignIn_Form, self).clean()	
		email = cleaned_data.get('email')
		password = cleaned_data.get("password")
		users = User.objects.filter(email=email)		
		if len(users) == 0:
			self.add_error('email', "Email address is not registered in this system. Please try again.")
		users = User.objects.filter(email=email, password=password)		
		if len(users) == 0:
			self.add_error('password', "Email address and password combo is not registered in this system. Please try again.")
		return cleaned_data

class UpdateInfoForm(forms.Form):
	email = forms.EmailField()
	first_name = forms.CharField(max_length=100)
	last_name = forms.CharField(max_length=100)

class UpdateInfo_Form(forms.ModelForm):
	class Meta: 
		model = User
		fields = ['email', 'first_name', 'last_name']
	def clean(self):
		cleaned_data = super(UpdateInfo_Form, self).clean()
		email = cleaned_data.get('email')
		first_name = cleaned_data.get('first_name')
		last_name = cleaned_data.get('last_name')
		user_id = self.instance.pk
		users = User.objects.filter(email=email)
		if len(users) != 0:
			if users[0].id != user_id:
				self.add_error('email', "Email address is already registered in this system. Please try again.")
			else:
				pass
		return cleaned_data

class UpdateInfoAdminForm(forms.Form):
	email = forms.EmailField()
	first_name = forms.CharField(max_length=100)
	last_name = forms.CharField(max_length=100)
	user_level = forms.ChoiceField()

class UpdateInfoAdmin_Form(forms.ModelForm):
	class Meta: 
		model = User
		fields = ['email', 'first_name', 'last_name', 'user_level']
		# fields = ['email', 'first_name', 'last_name']
	def clean(self):
		cleaned_data = super(UpdateInfoAdmin_Form, self).clean()
		email = cleaned_data.get('email')
		first_name = cleaned_data.get('first_name')
		last_name = cleaned_data.get('last_name')
		user_level = cleaned_data.get('user_level')
		user_id = self.instance.pk
		if len(users) != 0:
			if users[0].id != user_id:
				self.add_error('email', "Email address is already registered in this system. Please try again.")
			else:
				pass
		return cleaned_data

class UpdatePasswordForm(forms.Form):
	password = forms.CharField(max_length=100, widget=forms.PasswordInput)
	confirm_password = forms.CharField(max_length=100, widget=forms.PasswordInput)

class UpdatePassword_Form(forms.ModelForm):
	password = forms.CharField(max_length=100, widget=forms.PasswordInput)
	confirm_password = forms.CharField(max_length=100, widget=forms.PasswordInput)	
	class Meta: 
		model = User
		fields = ['password']
	def clean(self):
		cleaned_data = super(UpdatePassword_Form, self).clean()
		password = cleaned_data.get("password")
		confirm_password = cleaned_data.get("confirm_password")
		if password != confirm_password:
			self.add_error('confirm_password', "Password does not match.")
		return cleaned_data

class UpdateDescriptionForm(forms.Form):
	# description = forms.CharField(max_length=1000)
	description = forms.CharField(widget=forms.Textarea)

class UpdateDescription_Form(forms.ModelForm):
	class Meta: 
		model = User
		fields = ['description']		
	def clean(self):
		cleaned_data = super(UpdateDescription_Form, self).clean()
		description = cleaned_data.get("description")
		return cleaned_data

