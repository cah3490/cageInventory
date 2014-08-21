from django.db import models
from PIL import Image
import datetime


class Mfr(models.Model):
	name = models.CharField(max_length=100)
	def __str__(self):
		return str(self.name)


class Model(models.Model):
	mfr = models.ForeignKey(Mfr)
	model_name = models.CharField(max_length=100)
	value = models.IntegerField(null=True,blank=True)
	def __str__(self):
		return str(self.mfr) + " " + str(self.model_name)


class Item(models.Model):
	status = models.NullBooleanField(default=True)
	# True:  Item is checked in
	# False: Item is checked out
	# None:  Item is missing
	id_num = models.CharField(max_length=20,null=True,blank=True)
	model = models.ForeignKey(Model)
	def __str__(self):
		return str(self.id_num) + " " + str(self.model)


class Major(models.Model):
	code = models.CharField(max_length=20)
	def __str__(self):
		return str(self.code)


class Student(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	uid = models.CharField(max_length=9, null=True, blank=True)
	username = models.CharField(max_length=7, null=True, blank=True)
	year = models.CharField(max_length=1,null=True,blank=True)
	email = models.CharField(max_length=50,null=True,blank=True)
	major = models.ForeignKey(Major, blank=True, null=True)
	def __str__(self):
		retstr = str(self.first_name) + " " + str(self.last_name)
		if self.uid:
			retstr += ": " + str(self.uid)
		if self.email:
			retstr += ", " + str(self.email)
		return retstr


class Transaction(models.Model):
	student = models.ForeignKey(Student)
	this_item = models.ForeignKey(Item)
	start_date = models.DateTimeField()
	end_date = models.DateTimeField(null=True,blank=True)
	signature = models.ImageField(null=True,blank=True,upload_to="signatures")
	def __str__(self):
		return str(self.student) + " borrowed: " + str(self.this_item) + " on " + str(self.start_date)