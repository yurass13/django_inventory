from django.db import models

# ________________________________Products_____________________________________
class Country(models.Model):

    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Supplier(models.Model):

    name = models.CharField(max_length=50)
    contact_info = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class ProductModel(models.Model):

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    def __str__(self) -> str:
        if self.name is not None:
            return self.name
        else:
            return 'empty pm'


class ProductPrototype(models.Model):

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    model = models.ForeignKey(ProductModel, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self) -> str:

        if self.name is None:
            return "Unnamed ProductPrototype!"
        elif self.model is None:
            return str(self.name)
        else:
            return self.name + ' ' + str(self.model)


# ______________________________Organisation___________________________________
class Employee(models.Model):

    full_name = models.CharField(max_length=200)
    ...

    def __str__(self) -> str:
        if self is not None:
            return str(self.full_name)
        else:
            return 'empty employee'


class Storage(models.Model):

    location = models.CharField(max_length=200)
    ...

    def __str__(self) -> str:
        return self.location

# ______________________________Transactions___________________________________
class Inventory(models.Model):
    # FIXME try add into the ItemToDictMixin overloading by user_context
    # for getting choosed fields from FK.
    # After that, inheir it and use in context with refactoring templates
    # for reusing templates.

    product_prototype = models.ForeignKey(ProductPrototype, on_delete=models.PROTECT)
    storage = models.ForeignKey(Storage, on_delete=models.PROTECT)
    on_employee = models.ForeignKey(Employee, on_delete=models.SET_DEFAULT, blank=True, null=True, default=None)
    write_off = models.BooleanField(blank=True, default=False)


    def __str__(self) -> str:

        avaliable = ''
        if self.is_avaliable():
            avaliable = ' avaliable'

        if self.product_prototype is None:
            return "No prototype error!"
        elif self.storage is None:
            return "No storage error!"
        else:
            return str(self.product_prototype) + ' on ' + str(self.storage) + avaliable


    def is_avaliable(self):
        if self.write_off is False and self.on_employee is None:
            return True