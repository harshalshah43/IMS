from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django import forms

class Godown(models.Model):
    godown_name = models.CharField(max_length=40,blank=False)
    
    def __str__(self):
        return f'{self.godown_name}'
    
class Profile(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    godown_assigned = models.ForeignKey(Godown,on_delete=models.DO_NOTHING,default = 1)
    DisplayFields = ['user','godown_assigned']
    def __str__(self):
        return f'{self.user.username}'
    
class Item(models.Model):
    item_code = models.CharField(max_length=50,unique=True,blank = False)
    item_description = models.CharField(max_length=75,null=True,blank = True )
    MOQ = models.IntegerField(default=0)
    brand_choices = [('abb','ABB'),('legrand','LEGRAND'),('phoenix mecano','PHEONIX MECANO'),('eaton','EATON'),('Bussmann','Bussmann'),('socomec','SOCOMEC'),('Scame','SCAME')]
    brand = models.CharField(choices = brand_choices,max_length = 40,default="Bussmann",null = True)
    Display_fields = ['item_code','item_description']
    SearchableFields = ['item_code','item_description']
    FilterFields = ['brand']

    def __str__(self):
        godownitem = GodownItem.objects.filter(item = self).first()
        return f'{self.item_code}'

class GodownItem(models.Model):
    godown = models.ForeignKey(Godown,on_delete=models.CASCADE)
    item = models.ForeignKey(Item,on_delete=models.DO_NOTHING)
    qty = models.IntegerField(default=0)
    Display_fields = ['godown','item','qty']
    SearchableFields = ['item__item_code','item__item_description','item__brand']
    FilterFields = ['godown','item__brand']

    def __str__(self):
        return f'{self.item} Avl Nos {self.qty}({self.godown.godown_name})'

class InDocument(models.Model):
    date_posted=models.DateTimeField(default=timezone.now)
    total_qty = models.IntegerField(default=0)
    total_rows = models.IntegerField(default=0)
    type_choices = [('INC','Incoming')]
    type = models.CharField(choices = type_choices,max_length = 10,default = "INC",null = True)
    godown = models.ForeignKey(Godown,on_delete=models.CASCADE)
    person = models.ForeignKey(Profile,on_delete=models.CASCADE)
    invoiceno = models.CharField(max_length=75,null=True,blank=True)
    OAno = models.CharField(max_length=75,null=True,blank=True)
    remarks = models.CharField(max_length=30,blank=True,null=True)
    Display_fields = ['type','date_posted','invoiceno','remarks','total_qty','person','godown']
    SearchableFields = ['invoiceno','OAno']
    FilterFields = ['godown','person']

    def __str__(self):
        return f'{self.type} {self.date_posted.date()} {self.invoiceno}'

    def delete(self,*args,**kwargs):
        this_document = InDocument.objects.get(id = self.id)        
        docitems = InDocumentItem.objects.filter(indocument = this_document)
        for docitem in docitems:
            docitem.delete()
        super().delete(*args,**kwargs)

class InDocumentItem(models.Model):
    item = models.ForeignKey(Item,on_delete = models.DO_NOTHING)
    qty = models.IntegerField(default=0)
    indocument = models.ForeignKey(InDocument,on_delete = models.CASCADE)
    Display_fields = ['indocument','item','qty']
    SearchableFields = ['item']
    FilterFields = ['item','qty']
    # godownitem = models.ForeignKey(GodownItem,on_delete = models.DO_NOTHING)
    
    def __str__(self):
        return f'{self.item} {self.qty}'
    
    def save(self, *args, **kwargs):
        if GodownItem.objects.filter(item = self.item,godown = self.indocument.godown).exists():
            item = GodownItem.objects.filter(item = self.item,godown = self.indocument.godown).first()
        else:
            item = GodownItem.objects.create(item = self.item,qty = 0,godown = self.indocument.godown)
        # if self.document.type == "OUT": 
        #     item.qty -= self.qty
        #     item.save()
            
        if self.indocument.type == "INC":
            item.qty+=self.qty
            item.save()

        document = self.indocument
        document.total_qty += self.qty
        document.total_rows+=1
        document.save()
        item.godown = self.indocument.godown
        item.save()
        super().save()

    def delete(self,*args,**kwargs):
        # item = self.item
        item = GodownItem.objects.filter(item = self.item,godown = self.indocument.godown).first()
        print(self.indocument.godown,self.item)
        # if self.document.type == "OUT":
        #     item.qty += self.qty
        #     item.save()
        if self.indocument.type == "INC":
            item.qty-=self.qty
            item.save()
        
        document = self.indocument
        document.total_qty -= self.qty
        document.save()
        if item.qty == 0:
            item.delete()
        super().delete(*args,**kwargs)

#----------------------------------------------------------------OUTWARD DOCUMENT----------------------------------------------
class OutDocument(models.Model):
    date_posted=models.DateTimeField(default=timezone.now)
    total_qty = models.IntegerField(default=0)
    total_rows = models.IntegerField(default=0)
    type_choices = [('OUT','Outgoing')]
    type = models.CharField(choices = type_choices,max_length = 10,default = "OUT",null = True)
    godown = models.ForeignKey(Godown,on_delete=models.CASCADE)
    person = models.ForeignKey(Profile,on_delete=models.CASCADE)
    invoiceno = models.CharField(max_length=75,null=True,blank=True)
    OAno = models.CharField(max_length=75,null=True,blank=True)
    remarks = models.CharField(max_length=30,blank=True,null=True)
    Display_fields = ['type','date_posted','invoiceno','remarks','total_qty','person','godown']
    SearchableFields = ['invoiceno','OAno']
    FilterFields = ['godown','person']

    def __str__(self):
        return f'{self.type} {self.date_posted.date()} {self.invoiceno}'

    def delete(self,*args,**kwargs):
        this_document = OutDocument.objects.get(id = self.id)        
        docitems = OutDocumentItem.objects.filter(outdocument = this_document)
        for docitem in docitems:
            docitem.delete()
        super().delete(*args,**kwargs)

class OutDocumentItem(models.Model):
    godownitem = models.ForeignKey(GodownItem,on_delete = models.DO_NOTHING)
    qty = models.IntegerField(default=0)
    outdocument = models.ForeignKey(OutDocument,on_delete = models.CASCADE)
    Display_fields = ['outdocument','godownitem','qty']
    SearchableFields = ['godownitem']
    FilterFields = ['godownitem','qty']
    
    def __str__(self):
        return f'{self.godownitem} {self.qty}'
    
    def save(self, *args, **kwargs):
        # if GodownItem.objects.filter(item = self.item,godown = self.document.godown).exists():
        #     item = GodownItem.objects.filter(item = self.item,godown = self.document.godown).first()
        # else:
        #     item = GodownItem.objects.create(item = self.item,qty = 0,godown = self.document.godown)
        
        godownitem = self.godownitem
            
        if self.outdocument.type == "OUT": 
            godownitem.qty -= self.qty
            godownitem.save()
            
        # if self.document.type == "INC":
        #     godownitem.qty+=self.qty
        #     godownitem.save()

        document = self.outdocument
        document.total_qty += self.qty
        document.total_rows+=1
        document.save()
        godownitem.godown = self.outdocument.godown
        godownitem.save()
        super().save()

    def delete(self,*args,**kwargs):
        item = self.godownitem
        # item = GodownItem.objects.filter(item = self.item,godown = self.document.godown).first()
        if self.outdocument.type == "OUT":
            item.qty += self.qty
            item.save()

        # if self.document.type == "INC":
        #     item.qty-=self.qty
        #     item.save()
        
        outdocument = self.outdocument
        outdocument.total_qty -= self.qty
        outdocument.save()
        # if item.qty == 0:
        #     item.delete()
        super().delete(*args,**kwargs)

'''
You can make all items qty 0 via following command in shell
Item.objects.all().update(qty = 0)

Above command helps you update values of multiple fields of multiple objects
'''