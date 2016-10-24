from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib import messages
from django.db.models import Count
import bcrypt, re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validateReg(self, request):
        errors = self.validate_inputs(request)

        if len(errors) > 0:
            return (False, errors)

        # No errors, time to hash the pw
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

        # pw is hashed, time to create new user
        user = self.create(name=request.POST['name'], uname=request.POST['uname'], hire_date=request.POST['hire_date'], pw_hash=pw_hash)
        return (True, user)

    def validateLogin(self, request):
        try:
            user = User.objects.get(uname=request.POST['uname'])
            # The email matched a record in the database, now test passwords
            password = request.POST['password'].encode()

            if user.pw_hash == bcrypt.hashpw(password.encode(),user.pw_hash.encode()):
                return (True, user)

        except ObjectDoesNotExist:
            print "ObjectDoesNotExist: there is some error"

        return (False, "Email/password don't match - Please recheck.")

    def validate_inputs(self, request):
        errors = []
        if len(request.POST['name']) < 3 :
            messages.error(request, "Please include a name longer than three characters.", extra_tags='regis_name')
            errors.append("Please include a first longer than two characters.")
        if len(request.POST['uname']) < 3:
            messages.error(request, "Please include a Username longer than three characters.", extra_tags='regis_uname')
            errors.append("Please include a Username longer than three characters.")
        if User.objects.filter(uname=request.POST['uname']).count():
            messages.error(request, "The Username is already taken - try picking another name.", extra_tags='regis_uname')
            errors.append("The Username is already taken - can you pick another username.")
        if len(request.POST['password']) < 8 :
            messages.error(request, "Passwords must at least 8 characters.", extra_tags='regis_pwdshort')
            errors.append("Passwords must be at least 8 characters.")
        if request.POST['password'] != request.POST['confirm_pw']:
            messages.error(request, "Passwords must match.", extra_tags='regis_pwdmatch')
            errors.append("Passwords must match.")
        if not request.POST['hire_date']:
            messages.error(request, "The date is empty - please select a valid date.", extra_tags='regis_hire_date')
            errors.append("The date is empty - please select a valid date.")

        return errors

    def fetch_user_info(self, id):
        return self.filter(id=id).annotate(total_reviews=Count('review'))[0]

class User(models.Model):
    name = models.CharField(max_length = 100)
    uname = models.CharField(max_length = 50)
    hire_date = models.DateTimeField(auto_now = False)
    pw_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()
