from .models import (
    SignList,
    TransitionManager,
    Action,
    workevents,
    workflowitems,
    Flowmodel
)
from .middleware import get_current_user
from .exception import (
    ModelNotFound,
    TransitionNotAllowed,
    ReturnModelNotFound
)
from django.db.models import Q
from django.conf import settings
from collections import deque



####################################################
#############       CORE     #######################
####################################################


class FinFlotransition():

    # BASE CONSTRUCTORS # 

    def __init__(self, action :str  , type : str , t_id : str , state :str  , *args, **kwargs) -> None :
        self.action = action
        self.type = type 
        self.t_id = t_id if t_id else None
        self.state = state if state else []
        # core conditions
        gets_current_Action = None
        gets_return_action = self.gets_default_return_action()
        if gets_return_action.intermediator == True :
            self.intermediator_transition_handler(type = self.type, action = self.action , t_id = self.t_id)
        elif gets_return_action.description == action.upper():
            self.return_transition()
        else:
            self.transition()
        # return None


    # def get_action(self):
    #     self._action = None

    # def set_action(self):
    #     self._action = None

    # action = property(get_action, set_action)

    def __repr__():
        return "it works here"
        

    # GETS THE DEFAULT RETURN ACTION #

    def gets_default_return_action(self):
        try:
            qs = Action.objects.get(id = 1)
            return qs
        except:
            raise ReturnModelNotFound()


    # VALUE FOR SIGN_LIST #

    def get_value(sign_list, i):
        try:
            return sign_list[i]
        except IndexError:
            return 0

    


    # GETS WORKFLOW MODEL ID #

    def gets_wf_item(gets_model):
        ws = workflowitems.objects.get(transitionmanager=gets_model.id)
        return ws


    # GETS THE ALL MODEL VALUE FOR TRANSITION #
    
    def gets_all_models(self):
        try:
            gets_model = TransitionManager.objects.get(type = self.type.upper() , t_id = self.t_id)
            gets_flows = Flowmodel.objects.get(description  = self.type.lower())
            gets_action = Action.objects.get(Q(model = gets_flows.id ) | Q(model = None), description=self.action)
            gets_wf  = FinFlotransition.gets_wf_item(gets_model)
            sign_lists = sub_action_list = []
            try:
                for item in SignList.objects.all():
                    sign_lists.append(item.name)
                    if item.name == gets_action.stage_required.name :
                        break
                next_avail_trans = sign_lists[gets_model.sub_sign : ]
                next_avail_trans_value = deque(next_avail_trans)
                next_avail_trans_value.popleft()
                next_states = list(next_avail_trans_value)
                next_avail_Transition = {'values' : next_states}
            except:
                next_avail_Transition = None
                pass
            return gets_model , gets_action , gets_flows , gets_wf , sign_lists , next_avail_Transition
        except:
            raise ModelNotFound()



    # SPECIAL FUNCTION FOR RETURN TRANSITION  #

    def return_transition(self):
        
        overall_model = FinFlotransition.gets_all_models(self)
       
        if self.action == self.gets_default_return_action().description.upper():
            wf = workflowitems.objects.update_or_create( transitionmanager=overall_model[0] or overall_model[0].id, defaults= {"initial_state" : overall_model[3].initial_state, "interim_state" : overall_model[1].to_state.description ,
                    "final_state" : overall_model[1].to_state.description, "action" : self.action, "subaction" : self.action , "next_available_transitions" : None, "model_type" : self.type.upper(), "event_user" : get_current_user() , "current_from_party" : overall_model[1].from_party , "current_to_party" : overall_model[1].to_party})
            workevents.objects.create(workflowitems=overall_model[3] , event_user=get_current_user(),  initial_state=overall_model[3].initial_state,final_value = True , record_datas = "values" , 
                interim_state = overall_model[1].to_state.description , final_state=overall_model[1].to_state.description, action= self.action, subaction = self.action ,type=self.type.upper(), from_party = overall_model[1].from_party , to_party = overall_model[1].to_party)
            overall_model[0].sub_sign = 0
            overall_model[0].save()                      





    # INTERIM ACTION FOR THE TRANSITION HANDLING #

    def intermediator_transition_handler(self, type, action, t_id):
        overall_model = FinFlotransition.gets_all_models(type = type, action = action , t_id = t_id)
        
        # len action and sub_sign
        
        if overall_model.gets_model.sub_sign <= overall_model.gets_action.sign_required:
            def Transition_Handler():
                    gets_sign = overall_model.gets_action.sign_required
                    
                    
                    # if len(overall_model.sign_lists)-1 != overall_model.gets_model.sub_sign:
                    #     ws = workflowitems.objects.update_or_create( transitionmanager=overall_model.gets_model or overall_model.gets_model.id, defaults= {"initial_state" : gets_action.from_state.description, "interim_state" :  sign_lists[1 + gets_model.sub_sign], 
                    #         "final_state" : overall_model.gets_action.to_state.description, "action" : action, "subaction" : overall_model.sign_lists[1 + gets_model.sub_sign], "model_type" : type.upper(), "event_user" : get_current_user() , "current_from_party" : gets_action.from_party , "current_to_party" : gets_action.to_party})
                    #     we = workevents.objects.create(workflowitems=overall_model.gets_wf, event_user=get_current_user(),  initial_state=overall_model.gets_action.from_state.description,
                    #                               interim_state = overall_model.sign_lists[1 + overall_model.gets_model.sub_sign], final_state=overall_model.gets_action.to_state.description, action=action, subaction=sub_action[0], type=type.upper(), from_party = gets_action.from_party , to_party = gets_action.to_party)
                    #     overall_model.gets_model.sub_sign += 1
                    #     overall_model.gets_model.save()

                    # elif len(overall_model.sign_lists)-1 == int(overall_model.gets_model.sub_sign):
                    #     ws = workflowitems.objects.update_or_create( transitionmanager=overall_model.gets_model or gets_model.id, defaults= {"initial_state" : gets_action.from_state.description, "interim_state" : gets_action.to_state.description ,
                    #         "final_state" : overall_model.gets_action.to_state.description, "action" : action, "subaction" : sign_lists[1 + gets_model.sub_sign], "model_type" : type.upper(), "event_user" : get_current_user() , "current_from_party" : gets_action.from_party , "current_to_party" : gets_action.to_party})
                    #     workevents.objects.create(workflowitems=gets_wf, event_user=get_current_user(),  initial_state=gets_action.from_state.description,final_value = True , 
                    #                               interim_state = gets_action.to_state.description, final_state=gets_action.to_state.description, action=action, subaction=sub_action[0], type=type.upper(), from_party = gets_action.from_party , to_party = gets_action.to_party)
                    #     overall_model.gets_model.sub_sign += 1
                    #     overall_model.gets_model.save()
            return Transition_Handler()   
            
        else:
            raise TransitionNotAllowed()
        


    ## CORE TRANSITION ###

    def transition(self):
       
        overall_model = FinFlotransition.gets_all_models(self)

        
        # if ((gets_model.sub_sign <= gets_action.sign_required) and (gets_model.sub_sign != gets_action.sign_required)):
        if overall_model[0] is not None :
            def Transition_Handler():
                
        
                    # NO SIGN -> ONLY_MAKER TRANSITION 
                    
                    if len(overall_model[4])  == 0:
                        print("SET 1 ")
                        workflowitems.objects.update_or_create( transitionmanager=overall_model[0] or overall_model[0].id, defaults= {"initial_state" : overall_model[1].from_state.description, "interim_state" :  overall_model[1].from_state.description, 
                            "final_state" : overall_model[1].to_state.description, "action" : self.action, "subaction" : None, "model_type" : self.type.upper(), "event_user" : get_current_user() , "current_from_party" : overall_model[1].from_party , "current_to_party" : overall_model[1].to_party})
                        workevents.objects.create(workflowitems=overall_model[3], event_user=get_current_user(),  initial_state=overall_model[1].from_state.description,
                                                  interim_state = overall_model[1].from_state.description, final_state=overall_model[1].to_state.description, action= self.action, subaction= None , type= self.type.upper(), from_party = overall_model[1].from_party , to_party = overall_model[1].to_party)
                        overall_model[0].sub_sign = 0
                        overall_model[0].save()

                    # MAKER TRANSITION 

                    elif overall_model[0].sub_sign == 0:
                        print("SET 2 ")
                        ws = workflowitems.objects.update_or_create( transitionmanager=overall_model[0] or overall_model[0].id, defaults= {"initial_state" : overall_model[1].from_state.description, "interim_state" :  overall_model[4][1 + overall_model[0].sub_sign], 
                            "final_state" : overall_model[1].to_state.description, "next_available_transitions" : overall_model[5],"action" : self.action, "subaction" : overall_model[4][overall_model[0].sub_sign], "model_type" : self.type.upper(), "event_user" : get_current_user() , "current_from_party" : overall_model[1].from_party , "current_to_party" : overall_model[1].from_party})
                        workevents.objects.create(workflowitems=overall_model[3], event_user=get_current_user(),  initial_state=overall_model[1].from_state.description,
                                                  interim_state = overall_model[4][1 + overall_model[0].sub_sign], record_datas = None , final_state=overall_model[1].to_state.description, action= self.action, subaction= self.action, type= self.type.upper(), from_party = overall_model[1].from_party , to_party = overall_model[1].from_party)
                        overall_model[0].sub_sign +=1
                        overall_model[0].save()

                    #  TRANSITION 

                    elif len(overall_model[4]) != overall_model[0].sub_sign:
                        print("SET 3 ")
                        print(overall_model[0].sub_sign)
                        try:
                            ws = workflowitems.objects.update_or_create( transitionmanager=overall_model[0] or overall_model[0].id, defaults= {"initial_state" : overall_model[1].from_state.description, "interim_state" :  overall_model[4][1 + overall_model[0].sub_sign], 
                                "final_state" : overall_model[1].to_state.description, "next_available_transitions" : overall_model[5],"action" : self.action, "subaction" : overall_model[4][overall_model[0].sub_sign], "model_type" : self.type.upper(), "event_user" : get_current_user() , "current_from_party" : overall_model[1].from_party , "current_to_party" : overall_model[1].from_party})
                            workevents.objects.create(workflowitems=overall_model[3], event_user=get_current_user(),  initial_state=overall_model[1].from_state.description,
                                                    interim_state = overall_model[4][1 + overall_model[0].sub_sign], record_datas = None ,final_state=overall_model[1].to_state.description, action= self.action, subaction= self.action, type= self.type.upper(), from_party = overall_model[1].from_party , to_party = overall_model[1].from_party)
                            overall_model[0].sub_sign += 1
                            overall_model[0].save()
                        except:
                            ws = workflowitems.objects.update_or_create( transitionmanager=overall_model[0] or overall_model[0].id, defaults= {"initial_state" : overall_model[1].from_state.description, "interim_state" :  overall_model[1].to_state.description, 
                            "final_state" : overall_model[1].to_state.description, "action" : self.action,  "next_available_transitions" : None , "subaction" : self.action, "model_type" : self.type.upper(), "event_user" : get_current_user() , "current_from_party" : overall_model[1].from_party , "current_to_party" : overall_model[1].to_party , "final_value" : True})
                            workevents.objects.create(workflowitems=overall_model[3], event_user=get_current_user(),  initial_state=overall_model[1].from_state.description,
                                                  interim_state = overall_model[1].to_state.description,record_datas = None ,  final_state=overall_model[1].to_state.description, action= self.action, subaction= self.action, type = self.type.upper(), from_party = overall_model[1].from_party , to_party = overall_model[1].to_party , final_value = True)
                            overall_model[0].sub_sign = 0
                            overall_model[0].save()

            return Transition_Handler()   
        else:
            raise TransitionNotAllowed()





## BASE STATEMACHINE SETUP FOR COUNTERPARTY TRANSITION FLOWS ##



class States(FinFlotransition):


    def __init__(self,state , *args, **kwargs):
        self.state = state if state else None


    def next(self):
        FinFlotransition.__init__(action = self.state)