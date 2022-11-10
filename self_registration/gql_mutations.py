import base64
from django.core.files.base import ContentFile

import graphene
from core.schema import OpenIMISMutation
from graphql import GraphQLError
from insuree.schema import InsureeGQLType
from .models import ChfidTempInsuree

def dfprint(i):
    print(i)
    pass


# format base64 id string
def fbis64(inp):
    if not inp:
        return inp
    dfprint('fbis64')
    # NoticeGQLType:38
    # 
    bstr = base64.b64decode(inp)
    sstr = bstr.decode('utf-8')
    istrs = sstr.split(':')
    istr = istrs[1]
    dfprint([bstr, sstr, istr])
    return istr


from .models import Notice, VoucherPayment, Feedback, Config
from graphene_django import DjangoObjectType
from graphene import Connection, Int
from insuree import models as insuree_models
import core


class ExtendedConnection(Connection):
    class Meta:
        abstract = True

    total_count = Int()
    edge_count = Int()

    def resolve_total_count(root, info, **kwargs):
        print(root.length)
        return root.length

    def resolve_edge_count(root, info, **kwargs):
        return len(root.edges)


class VoucherPaymentType(DjangoObjectType):
    class Meta:
        model = VoucherPayment
        fields = ['voucher']


from .models import Profile


class CreateOrUpdateProfileMutation(graphene.Mutation):
    # _mutation_module = "self_registration"
    # _mutation_class = "CreateNoticeMutation"
    class Arguments(object):
        file = graphene.List(graphene.String)
        insureeCHFID = graphene.String()  # basically chfid
        email = graphene.String()
        phone = graphene.String()

    ok = graphene.Boolean()

    # @classmethod
    def mutate(self, info, file, insureeCHFID, email, phone):
        files = info.context.FILES
        print(files)
        insuree_obj = insuree_models.Insuree.objects.filter(chf_id=insureeCHFID).first()
        print(insuree_obj.pk)
        instance = Profile.objects.filter(insuree_id=insuree_obj.pk).first()
        if not instance:
            instance = Profile()
        instance.photo = files.get('file') if files.get('file') else instance.photo
        instance.email = email if email else instance.email
        instance.phone = phone if phone else instance.phone
        instance.save()
        return CreateOrUpdateProfileMutation(ok=True)


from .models import Notification


class CreateVoucherPaymentMutation(graphene.Mutation):
    # _mutation_module = "self_registration"
    # _mutation_class = "CreateNoticeMutation"
    class Arguments(object):
        file = graphene.List(graphene.String)
        insuree = graphene.String()

    ok = graphene.Boolean()

    # @classmethod
    def mutate(self, info, file, insuree):
        files = info.context.FILES
        insuree_obj = insuree_models.Insuree.objects.filter(chf_id=insuree).first()
        VoucherPayment.objects.create(voucher=files.get('file'), insuree=insuree_obj)
        Notification.objects.create(insuree=insuree_obj, message="Your Submission has been saved thank you",
                                    chf_id=insuree)
        return CreateVoucherPaymentMutation(ok=True)


class NoticeInput(graphene.InputObjectType):
    # id = graphene.Int(required=False)
    title = graphene.String(required=True)
    description = graphene.String(required=True)


class NoticeType(DjangoObjectType):
    class Meta:
        model = Notice
        fields = ['title', 'description']


class FeedbackAppGQLType(DjangoObjectType):
    class Meta:
        model = Feedback
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            "fullname": ['exact', 'icontains', 'istartswith'],

        }

        connection_class = ExtendedConnection


class CreateFeedbackMutation(graphene.Mutation):
    class Arguments:
        fullname = graphene.String(required=True)
        email_address = graphene.String(required=True)
        mobile_number = graphene.String(required=True)
        queries = graphene.String(required=True)

    feedback = graphene.Field(FeedbackAppGQLType)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        print(kwargs)
        feedback = Feedback.objects.create(**kwargs)
        return CreateFeedbackMutation(feedback=feedback)


class CreateNoticeMutation(OpenIMISMutation):  # graphene.relay.ClientIDMutation):
    class Input:
        title = graphene.String(required=True)
        description = graphene.String(required=True)
        client_mutation_id = graphene.String()
        client_mutation_label = graphene.String()

    notice = graphene.Field(NoticeType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        print('CreateNoticeMutation mutate')
        data = input
        if "client_mutation_id" in data:
            data.pop('client_mutation_id')
        if "client_mutation_label" in data:
            data.pop('client_mutation_label')
        notice = Notice.objects.create(title=input['title'], description=input['description'])
        return CreateNoticeMutation(notice=notice)


class UpdateNoticeMutation(OpenIMISMutation):
    notice = graphene.Field(NoticeType)

    class Input(OpenIMISMutation.Input):
        id = graphene.String()
        title = graphene.String(required=False, )
        description = graphene.String(required=True)
        client_mutation_id = graphene.String()
        client_mutation_label = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        dfprint('UpdateNoticeMutation mutate')
        data = input
        if "client_mutation_id" in data:
            data.pop('client_mutation_id')
        if "client_mutation_label" in data:
            data.pop('client_mutation_label')
        try:
            notice = Notice.objects.filter(pk=fbis64(input['id']))  # ;dfprint(notice)
            notice.update(title=input['title'], description=input['description'])
            return UpdateNoticeMutation(notice=notice)
        except:
            return GraphQLError('The notice you are updating might not exist anymore')


class DeleteNoticeMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    notice = graphene.Field(NoticeType)

    @classmethod
    def mutate(self, info, cls, id):
        try:
            notice = Notice.objects.filter(pk=id).first()
            notice.active = False  # soft_delete
            notice.save()
            return DeleteNoticeMutation(notice=notice)
        except:
            return GraphQLError('The notice you are deleting might not exist anymore')


from .models import InsureeTempReg
import base64




class CreateTempRegInsureeMutation(graphene.Mutation):
    class Arguments:
        json = graphene.JSONString()
    ok = graphene.Boolean()

    @classmethod
    def mutate(self, info, cls, **kwargs):
        dfprint(kwargs)
        inp_json = kwargs['json']
        str_json = json.dumps(inp_json)  # stringify json to save imp_json.get("Isurees"]
        dfprint(str_json)
        jantu = inp_json.get("Insurees")[0]
        phone_number=jantu.get("Phone")
        
        tempReg=None
        tempReg=InsureeTempReg.objects.filter(phone_number=phone_number).first()
        if tempReg:
            tempReg.json = str_json
        else:
            tempReg = InsureeTempReg.objects.create(json=str_json)
        tempReg.name_of_head=jantu.get("OtherNames") + ' ' + jantu.get("LastName"),
        tempReg.phone_number=phone_number
        tempReg.save()

        return CreateTempRegInsureeMutation(ok=True)


import json


def mdlInsureePhoto():
    mdl = None
    if 'Photo' in dir(insuree_models): mdl = insuree_models.Photo
    if not mdl: mdl = insuree_models.InsureePhoto
    return mdl


""" Register family from form  """
def process_family(args):
    json_dict = args.get('json_dict')
    family_save = json_dict.get("Family")

    chfid = None
    family_id = None
    if json_dict.get("ExistingInsuree"):
        chfid = json_dict.get('ExistingInsuree').get('CHFID')
        family = insuree_models.Insuree.objects.filter(chf_id=chfid).first()
        if family:
            family_id = family.family.id
    if not family_id:
        insuree_ = insuree_models.Insuree.objects.all().first()
        family_create = {
            "head_insuree_id": insuree_.pk,
            # "location_id" : 1,
            "poverty": family_save.get('Poverty', False),
            "family_type_id": family_save.get('FamilyType', "C"),
            "address": family_save.get("FamilyAddress"),
            "ethnicity": family_save.get("Ethnicity"),
            "validity_from": "2020-01-01",
            "audit_user_id": 1,
            "is_offline": True,
            # "confirmation_no" : None,
            # "confirmation_type_id": None,

        }
        family_create["head_insuree_id"] = insuree_.id
        print('familty-save-after', family_create)
        family = insuree_models.Family.objects.create(**family_create)
        family_id = family.id
    return family_id

def process_b64photo_write(args):
    photo = args.get('b64photo')
    save_path=args.get('save_path')
    img_name=""
    if photo:
        img_type, img = photo.split(',')
        image_data = base64.b64decode(img)

        s = img_type  # 'data:image/jpeg;base64'
        img_name = s[5:s.index(';')].replace('/', '.')
        import time;
        img_name = str(time.time()) + img_name
        import os 
        os.makedirs(save_path, exist_ok=True)
        img_fullpath=os.path.join(save_path, img_name)
        image_result = open(img_fullpath, 'wb')
        final_image = image_result.write(image_data)
    return img_name

def process_photo(args):
    dfprint('process_photo')
    insuree_save = args.get('insuree_save')
    photo = insuree_save.get('B64Photo')  # dbg_tmp_insuree_photo()
    # print( insuree_models.__dict__ )

    save_path=""
    img_name=""
    if photo:  # and False:        
        cfg = Config.objects.filter(key='InsureeImageDir').first()
        if cfg:
            save_path = cfg.value
        img_name=process_b64photo_write({"b64photo": photo, "save_path":save_path})

    
    modelPhoto = mdlInsureePhoto().objects.create(**{
        # "insuree_id":insuree_save.get('InsureeId'),
        "folder": save_path,
        "filename": img_name,
        "officer_id": 3,  # todo
        "date": '2018-03-28',  # todo
        "validity_from": "2018-03-28",
    })

    cfg = Config.objects.filter(key='IdImageDir').first()
    process_b64photo_write({"b64photo":  insuree_save.get('B64IdPhoto'), "save_path":cfg.value})

    return modelPhoto.pk


def process_insuree(args):
    insuree_save = args.get('insuree_save')
    family_id = args.get('family_id')
    dob = insuree_save.get("DOB", )
    dob = dob if len(dob) == 10 else "2022-02-02"  # todo fix
    photo_id = args.get('photo_id')
    insuree_create = {
        "last_name": insuree_save.get("LastName", None),
        "other_names": insuree_save.get("OtherNames", None),
        "dob": insuree_save.get("DOB"),
        "gender_id": insuree_save.get("Gender"),
        "marital": insuree_save.get("Marital"),
        "head": insuree_save.get("IsHead") if insuree_save.get('IsHead') else False,
        "passport": insuree_save.get("passport", 0),
        "phone": insuree_save.get("Phone"),
        "email": insuree_save.get("Email"),
        "relationship_id": insuree_save.get("Relationship"),
        "education_id": insuree_save.get("Education"),
        "current_address": insuree_save.get("CurrentAddress"),
        "current_village_id": fbis64(insuree_save.get("VillId")),  # base64
        "profession_id": insuree_save.get("Profession"),
        # "validity_from" : "2020-01-01",
        "card_issued": False,
        "audit_user_id": 1,
        'photo_id': photo_id,
        # "audit_user_id" : 1,
    }
    insuree_create["family_id"] = family_id
    dfprint(insuree_create)
    modelInsuree = insuree_models.Insuree.objects.create(**insuree_create)
    return modelInsuree.pk
    pass


"""
mutation {
  createInsureeMutationFromTemp(id:"7"){
      ok
  }
}

SELECT TOP 10 * FROM tblInsuree ORDER BY insureeId DESC;
SELECT TOP 10 * FROM tblPhotos ORDER BY PhotoId DESC;
sp_help tblPhotos
"""



class CreateInsureeMutation(graphene.Mutation):
    class Arguments:
        id = graphene.String()
        is_hold = graphene.Boolean()
        is_rejected = graphene.Boolean()
        is_approved = graphene.Boolean()
        status_message = graphene.String()

    ok = graphene.Boolean()
    message = graphene.String()

    @classmethod
    def mutate(self, info, cls, **kwargs):
        dfprint('CreateInsureeMutation mutate')
        message = ""
        try:
            pk = kwargs['id']  # access Arguments #13 testing
            temp_insuree = InsureeTempReg.objects.filter(pk=pk).first()
            print('kwargs----------',kwargs)
            if kwargs.get('is_hold'):
                temp_insuree.is_hold = True
                temp_insuree.status_message = kwargs.get('status_message')
                temp_insuree.save()
            if kwargs.get('is_rejected'):
                temp_insuree.is_rejected = True
                temp_insuree.status_message = kwargs.get('status_message')
                temp_insuree.save()
            if kwargs.get('is_hold'):
                temp_insuree.is_hold = True
                temp_insuree.status_message = kwargs.get('status_message')
                temp_insuree.save()
            if kwargs.get("is_approved"):
                
                str_json = temp_insuree.json
                json_dict = json.loads(str_json)  # dbg_tmp_insuree_json()
                family_id = process_family({'json_dict': json_dict})
                
                cfg = Config.objects.filter(key='RegVoucherImageDir').first()
                process_b64photo_write({"b64photo": json_dict.get('B64VoucherPhoto'), "save_path":cfg.value})

                if family_id:
                    insurees_from_form = json_dict.get("Insurees")
                    for insuree_save in insurees_from_form:
                        photo_id = process_photo({'insuree_save': insuree_save})
                        insuree_id = process_insuree(
                            {'insuree_save': insuree_save, 'photo_id': photo_id, 'family_id': family_id})
                        mdlInsureePhoto().objects.filter(pk=photo_id).update(**{"insuree_id": insuree_id})
                        chfif_assign = ChfidTempInsuree.objects.filter(is_approved=False).first()
                        if not chfif_assign:
                            message = "No CHFID available in database"
                        else:
                            chfif_assign.is_approved = True
                            # chfif_assign.save()
                            insuree_models.Insuree.objects.filter(pk=insuree_id).update(**{"chf_id": chfif_assign.chfid})
                            temp_insuree.is_approved = True
                            temp_insuree.save()

                    # everything ok, then approved flag changed
                    temp_insuree.is_approved = True
                    temp_insuree.status_message = kwargs.get('statusMessage')
                    temp_insuree.save()
        except Exception as e:
            print(e)
            import traceback
            traceback.print_exc()
            return CreateInsureeMutation(ok=False, message=message)
            # raise
        return CreateInsureeMutation(ok=True)

