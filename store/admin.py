from django.contrib import admin
from . models import Category, Customer, Product, Order, Profile
from django.contrib.auth.models import User

admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Profile)


#mezclar info de perfil e info de usuario
class ProfileInLine(admin.StackedInline):
    model = Profile

#Extend user model
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username", "first_name", "last_name", "email"]
    inlines = [ProfileInLine]


#quitar formato antiguo

admin.site.unregister(User)

#re-registrar nueva forma

admin.site.register(User, UserAdmin)