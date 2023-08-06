from django.db import models
from .middleware import get_current_user
from .validators import validate_postive
from .fields import CommaSeparatedCharField
from django.core.exceptions import ValidationError
from .validators import validate_postive
from .base_enum import Values
from django.apps import apps

try:
   from django.conf import settings
except ImportError:
    raise Exception("settings.py file is required to run this package")



## CORE CONFIGURATIONS CLASSES ##



class Flowmodel(models.Model):
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description




class PartyType(models.Model):
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name_plural = "1. PartyType"



class TransitionManager(models.Model):
    t_id = models.IntegerField()
    type = models.CharField(max_length = 255 )
    sub_sign = models.IntegerField(default = 0 )

    # default 1 for initial submit and maker process

    def save(self, *args, **kwargs):
        self.type = self.type.upper()
        return super(TransitionManager,self).save(*args, **kwargs)
    
    def __str__(self):
        return "{0}_{1}".format(self.type.lower() , self.id)
    
    class Meta:
        verbose_name_plural = "4. TransitionManager"


class SignList(models.Model):
    sign_id = models.IntegerField(validators=[validate_postive])
    name = models.CharField(max_length = 255 , blank=True, null=True)
    sub_action_name = models.CharField(max_length = 255 , blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
       self.id = self.sign_id
       return super(SignList, self).save(*args, **kwargs) # Call the real save() method
    
    class Meta:
        verbose_name_plural = "4. Signatures"


    

class States(models.Model):
    description = models.CharField(max_length=255)
    
    class Meta:
        verbose_name_plural = "2. States"

    def __str__(self):
        return self.description


class Action(models.Model):
    description = models.CharField(max_length=255 , blank = True , null=True , help_text = 'e.g., SUBMIT , DELETE') 
    model = models.ForeignKey(Flowmodel , on_delete = models.CASCADE , blank = True , null = True )
    from_state = models.ForeignKey(States , on_delete= models.DO_NOTHING , related_name = 'action_from_state' , blank = True , null = True , help_text = "initial from state for transition ")
    to_state = models.ForeignKey(States , on_delete= models.DO_NOTHING , blank = True , null = True , help_text = "final state for the transition to take place")
    # optional fields
    intermediator = models.BooleanField(default = False)
    from_party = models.ForeignKey(PartyType , models.DO_NOTHING , blank = True , null = True , help_text = 'this field is optional' , related_name = 'from_transition_party_type')
    to_party = models.ForeignKey(PartyType , models.DO_NOTHING , blank = True , null = True , help_text = 'this field is optional' , related_name = 'to_transition_party_type')
    stage_required = models.ForeignKey(SignList , on_delete= models.DO_NOTHING ,blank = True , null = True ,help_text = "IMPORTANT : if 0 means initial_transition ")
    sign_required = models.IntegerField(default=0,help_text = "IMPORTANT : if 0 means initial_transition " , blank=True, null=True )


    def save(self, *args, **kwargs):
        self.description = self.description.upper()
        try:
            sign_len = SignList.objects.get(name = self.stage_required.name )
            self.sign_required = sign_len.sign_id
        except:
            self.sign_required = 0
        return super(Action,self).save(*args, **kwargs)

    # def __str__(self):
    #     return "{0} -> {1} -> sign_required -> {2}".format(self.description , self.model, self.sign_required)
    
    def __str__(self):
        return self.description

    class Meta:
        verbose_name_plural = "3. Action"
        unique_together = ('description', 'model') 
 

class workflowitems(models.Model):
    
    created_date = models.DateTimeField(auto_now_add=True)
    transitionmanager = models.OneToOneField(TransitionManager, on_delete=models.CASCADE,blank=True, null=True )
    initial_state  = models.CharField(max_length=50,default = Values.DRAFT.value)
    interim_state = models.CharField(max_length=50,default = Values.DRAFT.value)
    final_state = models.CharField(max_length=50,default = Values.DRAFT.value) 
    event_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING , blank=True, null=True)
    next_available_transitions =  models.CharField(max_length=500 , blank=True, null=True)
    current_from_party = models.ForeignKey(PartyType , models.DO_NOTHING , blank = True , null = True , editable = False , related_name = 'wf_from_party')
    current_to_party = models.ForeignKey(PartyType , models.DO_NOTHING , blank = True , null = True , editable = False )
    action = models.CharField(max_length=25 , blank=True, null=True , default = Values.DRAFT.value)
    subaction = models.CharField(max_length=55 , blank=True, null=True)
    previous_action = models.CharField(max_length=55 , blank=True, null=True)
    model_type  = models.CharField(max_length=55, blank=True, null=True)
    comments = models.CharField(max_length=500,blank=True, null=True)
    is_read = models.BooleanField(default=True,blank=True, null=True)
    final_value = models.BooleanField(default=False,blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "WorkFlowItem"
        ordering = ['id']

    # def save(self, *args, **kwargs):
    #    if self.from_party is None:
    #         self.from_party = None
    #    super(workflowitems, self).save(*args, **kwargs) # Call the real save() method


# WORKEVENTS
class workevents(models.Model):

    workflowitems = models.ForeignKey(workflowitems, on_delete=models.CASCADE , related_name='WorkFlowEvents')
    action = models.CharField(max_length=25, blank=True, null=True , default = Values.DRAFT.value)
    subaction = models.CharField(max_length=55 , blank=True, null=True , default = Values.DRAFT.value)
    initial_state  = models.CharField(max_length=50 , default = Values.DRAFT.value)
    interim_state = models.CharField(max_length=50,default = Values.DRAFT.value)
    final_state = models.CharField(max_length=50,default = Values.DRAFT.value)
    from_party = models.ForeignKey(PartyType , models.DO_NOTHING  , blank = True , null = True , editable = False ,related_name = 'we_from_party')
    to_party = models.ForeignKey(PartyType , models.DO_NOTHING  , blank = True , null = True , editable = False )
    event_user = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.DO_NOTHING , blank=True, null=True)
    is_read = models.BooleanField(default=True,blank=True, null=True)
    record_datas = models.JSONField(blank=True, null=True)
    final_value = models.BooleanField(default=False,blank=True, null=True)
    comments = models.CharField(max_length=500,blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=55, blank=True, null=True)
    

    class Meta:
        verbose_name_plural = "WorkFlowEvent"
        ordering = ['id']


    # def save(self , *args, **kwargs):
    #     try:
    #         work_model = settings.FINFLO['WORK_MODEL']  
    #         for iter in work_model:
    #             gets_model =  apps.get_model(iter)
    #             values = gets_model.objects.filter(id = self.workflowitems.transitionmanager.t_id).value_list()
    #             print("the data is " ,values)
    #             if values.exists():
    #                 break
    #             continue
    #         self.record_datas = {"values" : values}
    #         print(self.record_datas)
    #         return super(workevents, self).save( *args, **kwargs)
    #     except :
    #         self.record_datas = {"values" : values}
    #         return super(workevents, self).save( *args, **kwargs)
    
        





