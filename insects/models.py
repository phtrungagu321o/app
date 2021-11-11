from django.db import models
from django.contrib.auth.models import User
# Create your models here.
import os
from django.dispatch import receiver

class staticURL:
    upload = "normal"

def save_to(instance, filename):
    print(instance)
    return os.path.join(staticURL.upload + '/' + filename)



def save_to_slug(instance, filename):
    print(instance.slug)
    return os.path.join(instance.slug + '/' + filename)

def save_zip_to_slug(instance, filename):
    return os.path.join('zip/' + instance.insect.slug + '/' + instance.insect.slug + ".zip")


class Kingdom(models.Model):
    eName = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    thumb = models.ImageField(upload_to=save_to_slug, blank=True)

    def __str__(self):
        return self.eName


class Phylum(models.Model):
    kingdom = models.ForeignKey(
        Kingdom, on_delete=models.PROTECT)
    eName = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    thumb = models.ImageField(upload_to=save_to_slug, default=None)

    def __str__(self):
        return self.eName

class Classes(models.Model):
    phylum = models.ForeignKey(Phylum, on_delete=models.PROTECT)
    eName = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    thumb = models.ImageField(upload_to=save_to_slug, default=None)

    def __str__(self):
        return self.eName


class Order(models.Model):
    classes = models.ForeignKey(
        Classes, on_delete=models.PROTECT)
    eName = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    thumb = models.ImageField(upload_to=save_to_slug)

    def __str__(self):
        return self.eName


class Family(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    eName = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    thumb = models.ImageField(upload_to=save_to_slug)

    def __str__(self):
        return self.eName


class Genus(models.Model):
    family = models.ForeignKey(Family, on_delete=models.PROTECT)
    eName = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    thumb = models.ImageField(upload_to=save_to_slug)

    def __str__(self):
        return self.eName


class InsectTest(models.Model):
    genus = models.ForeignKey(Genus, on_delete=models.PROTECT)
    eName = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    characteristic = models.TextField(default="null")
    value = models.TextField(default="null")
    reality = models.TextField(default="null")
    protective = models.TextField(default="null")
    distribution = models.TextField(default="null")
    detail = models.TextField(default="null")
    thumb = models.ImageField(upload_to=save_to_slug, blank=True, default=None)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def snippet(self):
        return self.characteristic[:150] + '...'


class Insect(models.Model):
    genus = models.ForeignKey(Genus, on_delete=models.PROTECT)
    eName = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    characteristic = models.TextField(default="null")
    value = models.TextField(default="null")
    reality = models.TextField(default="null")
    protective = models.TextField(default="null")
    distribution = models.TextField(default="null")
    detail = models.TextField(default="null")
    thumb = models.ImageField(upload_to=save_to_slug, blank=True)
    #date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def snippet(self):
        return self.characteristic[:150] + '...'

class Insect_downloadFile(models.Model):
    insect = models.ForeignKey(Insect, default=None, on_delete=models.PROTECT)
    file = models.FileField(upload_to=save_zip_to_slug, blank=False)
    def __str__(self):
        return self.insect.pk

@receiver(models.signals.post_delete, sender=Insect_downloadFile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


@receiver(models.signals.pre_save, sender=Insect_downloadFile)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Insect.objects.get(pk=instance.pk).file
    except Insect.DoesNotExist:
        return False

    new_file = instance.file
    if not old_file == new_file:
        try:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
        except:
            print("add new")

@receiver(models.signals.post_delete, sender=Insect)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.thumb:
        if os.path.isfile(instance.thumb.path):
            os.remove(instance.thumb.path)

@receiver(models.signals.pre_save, sender=Insect)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Insect.objects.get(pk=instance.pk).thumb
    except Insect.DoesNotExist:
        return False

    new_file = instance.thumb
    if not old_file == new_file:
        try:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
        except:
            print("add new")

def save_img_to(url):
    staticURL.upload = url


class Insect_Image(models.Model):
    insect = models.ForeignKey(Insect, on_delete=models.PROTECT)
    image = models.ImageField(
        upload_to=save_to, default=None, blank=True)
    placeholder = models.CharField(max_length=100, default=None)
    subset = models.CharField(max_length=20, default=None)

    def __str__(self):
        return self.image.url

    def _save(self):
        print(" => ", staticURL.upload)
        self.save()

class New_Image(models.Model):
    insect = models.ForeignKey(Insect, default=None, on_delete=models.PROTECT)
    image = models.ImageField(
        upload_to=save_to, default=None, blank=True)
    placeholder = models.CharField(max_length=100, default=None)
    subset = models.CharField(max_length=20, default=None)
    image_url = models.URLField(default="")
    is_valid = models.BooleanField(default=False)

    def __str__(self):
        try:
            return self.image.url
        except:
            return "null"

    def _save(self):
        print(" => ", staticURL.upload)
        self.save()

    def get_remote_image(self, filename):
        from django.core.files import File
        import os
        import urllib
        if self.image_url and not self.image:
            try:
                result = urllib.request.urlretrieve(self.image_url)
                with open(result[0], 'rb') as f:
                    self.image.save(filename, f)
                    self.save()
            except:
                print("Image not downloaded")

class Rect(models.Model):
    image = models.ForeignKey(
        Insect_Image, default=None, on_delete=models.PROTECT)
    name = models.CharField(max_length=100, default=None)
    x = models.FloatField()
    y = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()

    def __str__(self):
        return 'rect_' + self.image.image.url

class Rect_New_Image(models.Model):
    image = models.ForeignKey(
        New_Image, default=None, on_delete=models.PROTECT)
    name = models.CharField(max_length=100, default=None)
    x = models.FloatField()
    y = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()

    def __str__(self):
        return 'rect_' + self.image.image.url

class Test(models.Model):
    image = models.ImageField(upload_to='media')
    name = models.CharField(max_length=100, default=None)
    x = models.FloatField()
    y = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()


@receiver(models.signals.post_delete, sender=Kingdom)
def auto_delete_file_on_delete_kingdom(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.thumb:
        if os.path.isfile(instance.thumb.path):
            os.remove(instance.thumb.path)


@receiver(models.signals.pre_save, sender=Kingdom)
def auto_delete_file_on_change_kingdom(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Kingdom.objects.get(pk=instance.pk).thumb
    except Kingdom.DoesNotExist:
        return False
    print('chay lenh nay')
    new_file = instance.thumb
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


@receiver(models.signals.post_delete, sender=Phylum)
def auto_delete_file_on_delete_phylum(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.thumb:
        if os.path.isfile(instance.thumb.path):
            os.remove(instance.thumb.path)


@receiver(models.signals.pre_save, sender=Phylum)
def auto_delete_file_on_change_phylum(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Phylum.objects.get(pk=instance.pk).thumb
    except Phylum.DoesNotExist:
        return False

    new_file = instance.thumb
    print(instance.thumb)
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


@receiver(models.signals.post_delete, sender=Classes)
def auto_delete_file_on_delete_class(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.thumb:
        if os.path.isfile(instance.thumb.path):
            os.remove(instance.thumb.path)


@receiver(models.signals.pre_save, sender=Classes)
def auto_delete_file_on_change_class(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Classes.objects.get(pk=instance.pk).thumb
    except Classes.DoesNotExist:
        return False

    new_file = instance.thumb
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


@receiver(models.signals.post_delete, sender=Order)
def auto_delete_file_on_delete_Order(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.thumb):
            os.remove(instance.file.thumb)


@receiver(models.signals.pre_save, sender=Order)
def auto_delete_file_on_change_Order(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Order.objects.get(pk=instance.pk).thumb
    except Order.DoesNotExist:
        return False

    new_file = instance.thumb
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


@receiver(models.signals.post_delete, sender=Family)
def auto_delete_file_on_delete_family(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.thumb:
        if os.path.isfile(instance.thumb.path):
            os.remove(instance.thumb.path)


@receiver(models.signals.pre_save, sender=Family)
def auto_delete_file_on_change_family(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Family.objects.get(pk=instance.pk).thumb
    except Family.DoesNotExist:
        return False

    new_file = instance.thumb
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


@receiver(models.signals.post_delete, sender=Genus)
def auto_delete_file_on_delete_Genus(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.thumb:
        if os.path.isfile(instance.thumb.path):
            os.remove(instance.thumb.path)


@receiver(models.signals.pre_save, sender=Genus)
def auto_delete_file_on_change_Genus(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Genus.objects.get(pk=instance.pk).thumb
    except Genus.DoesNotExist:
        return False

    new_file = instance.thumb
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


@receiver(models.signals.post_delete, sender=Insect_Image)
def auto_delete_file_on_delete_im(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(models.signals.pre_save, sender=Insect_Image)
def auto_delete_file_on_change_im(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Insect_Image.objects.get(pk=instance.pk).image
    except Insect_Image.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
