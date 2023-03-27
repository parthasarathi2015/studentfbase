from django.db import models
from .services.utils import get_fb
import uuid
#    Create your models here.
class Classroom(models.Model):
    Credits = (
        ('1', 'One'),
        ('2', 'Two'),
        ('3', 'three'),
        ('4', 'four'),
        ('6', 'Six'),
    )
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    room_no = models.CharField(max_length=20, default='1')
    room_location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now = True)
    updated_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.room_no


class Student(models.Model):
    GENDER = (
        ('F', 'Female'),
        ('M', 'Male'),
        ('O', 'Other'),
    )
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    std_name = models.CharField(max_length=50, default='')
    father_name = models.CharField(max_length=50, null=True,blank=True)
    std_gender = models.CharField(max_length=1, choices=GENDER, default='M')
    std_class = models.CharField(max_length=50, default='V')
    classroom = models.ForeignKey(Classroom,on_delete=models.CASCADE, related_name="classroom")
    created_at = models.DateTimeField(auto_now = True)
    updated_at = models.DateTimeField(auto_now_add = True)

    def save(self, *args, **kwargs):          
        super(Student, self).save(*args, **kwargs)
        if self:
            self.update_firebase(self)  

    def __str__(self):
        return f"{self.std_name}({self.std_class})"
    
    def delete(self, *args, **kwargs): 
        id = self.id
        print("id:",self.id)
        super(Student, self).delete(*args, **kwargs)
        if id:
            self.delete_firebase(id)


    def delete_firebase(self,id):
        db = get_fb()
        if db:
            print("uuid:",id)
            ref = db.child('student')
            key =  None
            for es in ref.get().each():
                if es.val()['id'] == str(id):
                    key = es.key()
                    break                 
                    

            if key:
                ref.child(key).delete()
           



    def update_firebase(self,instance):
        db = get_fb()
        if db:
            ref = db.child('student')
            instance = Student.objects.get(pk=instance.id)
            classroom = {}
            if instance.classroom:
                classroom = {
                    "id":str(instance.classroom.id),
                    "room_no": instance.classroom.room_no,
                    "room_location": instance.classroom.room_location,
                    "created_at": str(instance.classroom.created_at),
                    "updated_at":  str(instance.classroom.updated_at),
                }

            data = {
                    "id": str(instance.id),
                    "std_name": instance.std_name,
                    "father_name": instance.father_name,
                    "std_gender": instance.std_gender,
                    "std_class": instance.std_class,
                    "classroom": classroom,
                    "created_at":str( instance.created_at),
                    "updated_at": str(instance.updated_at),
            }
            key =  None
            if ref.get().each():
                for es in ref.get().each():
                    if es and 'id' in es.val() and es.val()['id'] == str(instance.id):
                        key = es.key()
                        break                  
                    

            if key:
                db.child('student').child(key).update(data) 
            else:
                db.child('student').push(data)

class Subject(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.name}({self.id})"

class MarksObtain(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    marks = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.student.std_name}({self.student.std_class})"

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # self.update_firebase(self)
        
        return super().save(force_insert, force_update, using, update_fields)