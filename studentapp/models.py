from django.db import models
from .services.utils import *
import uuid

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
        super(Student, self).delete(*args, **kwargs)
        if id:
            self.delete_firebase(id)


    def delete_firebase(self,id):
        db = get_fb()
        db = db.database()
        fb_user = get_fb_auth()
        if db and fb_user:
            ref = db.child('student')
            key =  None
            if ref.get().each():
                for es in ref.get().each():
                    for k,itm in es.val().items():
                        if itm['id'] == str(id):
                            key = k
                        break     

            if key:
                 db.child('student').child(key).remove(fb_user['idToken'])


    def update_firebase(self,instance):
        db = get_fb()
        db = db.database()
        fb_user = get_fb_auth()
        if db and fb_user:
            ref = db.child('student')
            instance = Student.objects.get(pk=instance.id)
            marksobtain = {}
            try:
            # if MarksObtain.objects.get(student_id=instance.id).exists():
                marks = MarksObtain.objects.filter(student=Student.objects.get(pk=instance.id))
                if marks:
                    for mks in marks:
                        marksobtain[ mks.subject.name] = {                        
                            "id":str(mks.id),
                            # "subject": mks.subject.name,
                            "marks": mks.marks,
                            # "created_at": str(marks.created_at),
                            # "updated_at":  str(marks.updated_at),
                        }
            except:
                pass

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
                    "marksobtain": marksobtain,
                    "created_at":str( instance.created_at),
                    "updated_at": str(instance.updated_at),
            }
            key =  None
            if ref.get().each():
                for es in ref.get().each():
                    for k,itm in es.val().items():
                        if itm['id'] == str(instance.id):
                            key = k
                        break        
            try:
                if key:
                    db.child('student').child(key).update(data,fb_user['idToken']) 
                else:
                    db.child('student').push(data, fb_user['idToken'])
            except :
                pass

class Subject(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.name}"

class MarksObtain(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    marks = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.student.std_name}({self.student.std_class}):{self.subject.name}"

    def save(self, *args, **kwargs): 
        super(MarksObtain, self).save(*args, **kwargs)
        if self:
            try:
                self.update_firebase_marks(self)   
            except:
                pass  
    
    def delete(self, *args, **kwargs): 
        id = self.id
        super(MarksObtain, self).delete(*args, **kwargs)
        if id:
            self.delete_firebase_marks(self)

    def delete_firebase_marks(self,instance):
        db = get_fb()
        db = db.database()
        fb_user = get_fb_auth()
        if db:
            ref = db.child('student')
            key =  None
            if ref.get().each():
                for es in ref.get().each():
                    for k,itm in es.val().items():
                        if itm['id'] == str(instance.student.id):
                            key = k
                        break 

            if key:
                db.child('student').child(key).child("marksobtain").child(instance.subjet.name).remove()
           
    def update_firebase_marks(self,instance):
        db = get_fb()        
        db = db.database()
        fb_user = get_fb_auth()
        if db:
            ref = db.child('student')
            try:
                marksobtain = {}
                try:
                    marks = MarksObtain.objects.filter(student=Student.objects.filter(pk=instance.student.id).first())
                    if marks:
                        for mks in marks:
                            marksobtain[ mks.subject.name] = {                        
                                "id":str(mks.id),
                                # "subject": mks.subject.name,
                                "marks": mks.marks,
                                # "created_at": str(marks.created_at),
                                # "updated_at":  str(marks.updated_at),
                            }
                except:
                    pass
            
                if instance:
                    marksobtain = {
                        "id":str(instance.id),
                        "subject": instance.subject.name,
                        "marks": instance.marks,
                        # "created_at": str(instance.created_at),
                        # "updated_at":  str(instance.updated_at),
                    }
                key =  None
                if ref.get().each():
                    for es in ref.get().each():
                        for k,itm in es.val().items():
                            if itm['id'] == str(instance.student.id):
                                key = k
                            break

                    if key:
                        db.child('student').child(key).child('marksobtain').child(instance.subject.name).set(marksobtain,fb_user['idToken']) 
            except:
                pass


