from django.contrib import admin
from .models import *

admin.site.register(Godown)
@admin.register(GodownItem)
class GodownItemAdmin(admin.ModelAdmin):
    model = GodownItem
    autocomplete_fields = ['item']
    search_fields = GodownItem.SearchableFields
    list_display = GodownItem.Display_fields
    list_filter = GodownItem.FilterFields

    def get_queryset(self,request):
        abc = super(GodownItemAdmin, self).get_queryset(request) 
        if request.user.groups.filter(name = "Inventory Operators").exists():
            profile = Profile.objects.filter(user = request.user).first()
            return abc.filter(godown = profile.godown_assigned)
        else:
            return abc
            
class InwardDocumentItemInLineAdmin(admin.TabularInline):
    model = InDocumentItem
    autocomplete_fields = ["item"]
    
class InDocumentAdmin(admin.ModelAdmin):
    inlines = [InwardDocumentItemInLineAdmin]
    list_display = InDocument.Display_fields
    search_fields = InDocument.SearchableFields
    list_filter = InDocument.FilterFields
    readonly_fields = ('person',)

    def get_readonly_fields(self, request, obj=None):
        if request.user.groups.filter(name = "Inventory Operators").exists(): # editing an existing object
            return self.readonly_fields + ('godown',)
        else:
            pass
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        user = request.user
        person = Profile.objects.filter(user = user).first()
        obj.person = person
        if request.user.groups.filter(name = "Inventory Operators").exists():
            obj.godown = Godown.objects.filter(godown_name = person.godown_assigned).first()
        else:
            pass
        super().save_model(request, obj, form, change)

    def get_queryset(self,request): # display only those objects created by the logged user 
        abc = super(InDocumentAdmin, self).get_queryset(request) 
        if request.user.is_superuser:
            return abc
        else:
            profile = Profile.objects.filter(user = request.user).first()
            return abc.filter(person = profile)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = Profile.DisplayFields

admin.site.register(InDocument,InDocumentAdmin)

#------------------------------------------OUTGOING DOCUMENT----------------------------------------
class OutDocumentItemInLineAdmin(admin.TabularInline):
    model = OutDocumentItem
    autocomplete_fields = ["godownitem"]
    
class OutDocumentAdmin(admin.ModelAdmin):
    inlines = [OutDocumentItemInLineAdmin]
    list_display = OutDocument.Display_fields
    search_fields = OutDocument.SearchableFields
    list_filter = OutDocument.FilterFields
    readonly_fields = ('person',)

    def get_readonly_fields(self, request, obj=None):
        if request.user.groups.filter(name = "Inventory Operators").exists(): # editing an existing object
            return self.readonly_fields + ('godown',)
        else:
            pass
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        user = request.user
        person = Profile.objects.filter(user = user).first()
        obj.person = person
        if request.user.groups.filter(name = "Inventory Operators").exists():
            obj.godown = Godown.objects.filter(godown_name = person.godown_assigned).first()
        else:
            pass
        super().save_model(request, obj, form, change)

    def get_queryset(self,request): # display only those objects created by the logged user 
        abc = super(OutDocumentAdmin, self).get_queryset(request) 
        if request.user.is_superuser:
            return abc
        else:
            profile = Profile.objects.filter(user = request.user).first()
            return abc.filter(person = profile)
        
admin.site.register(OutDocument,OutDocumentAdmin)
#--------------------------------------------------------------------------------------------------

# @admin.register(DocumentItem)
# class DocumentItemAdmin(admin.ModelAdmin):
#     autocomplete_fields = ["item"] # dealing with huge dropdown list, instead displays searchable dropdown list
#     list_display = DocumentItem.Display_fields
#     search_fields = DocumentItem.SearchableFields
#     list_filter = DocumentItem.FilterFields

#     def get_queryset(self,request):
#         abc = super(DocumentItemAdmin, self).get_queryset(request) 
#         if request.user.is_superuser:
#             return abc
#         else:
#             profile = Profile.objects.filter(user = request.user).first()
#             return abc.filter(document__person = profile)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = Item.Display_fields
    search_fields = Item.SearchableFields
    list_filter = Item.FilterFields