import requests

headersList = {
    "Accept": "*/*",
    "User-Agent": "3xBp",
    "Content-Type": "application/json",
}

urlBase = ""

###############################################################################
#####                           CRIAR SPA                                 #####
# Params:                                                                     #
newSpaName = "SPA Automáticas"
newSpaPipelines = "Pipe 1, Pipe2, Pipe 3"
newSpaStages = "Fazer,Fazendo,Resolvido"
#                                                                             #
#####                                                                     #####
###############################################################################

payload = {
    "fields": {
        "title": newSpaName,
        "isCategoriesEnabled": "Y",
        "isStagesEnabled": "Y",
        "isBeginCloseDatesEnabled": "Y",
        "isClientEnabled": "Y",
        "isUseInUserfieldEnabled": "Y",
        "isLinkWithProductsEnabled": "N",
        "isMycompanyEnabled": "Y",
        "isDocumentsEnabled": "Y",
        "isSourceEnabled": "Y",
        "isObserversEnabled": "Y",
        "isRecyclebinEnabled": "Y",
        "isAutomationEnabled": "Y",
        "isBizProcEnabled": "Y",
        "isSetOpenPermissions": "N",
        "isPaymentsEnabled": "N",
        "isCountersEnabled": "Y",
        "relations": {
            "parent": [
            {
                "entityTypeId": 3,
                "isChildrenListEnabled": "Y",
                "isPredefined": "Y"
            },
            {
                "entityTypeId": 4,
                "isChildrenListEnabled": "Y",
                "isPredefined": "Y"
            }
            ],
            "child": []
        },
        "linkedUserFields": {
            "CALENDAR_EVENT|UF_CRM_CAL_EVENT": "Y",
            "TASKS_TASK|UF_CRM_TASK": "N",
            "TASKS_TASK_TEMPLATE|UF_CRM_TASK": "N"
        },
        "customSections": []
    }    
}

print("############### List Categories: crm.type.add")
print(payload)
response = requests.post(urlBase + 'crm.type.add', json=payload)
objResponse = response.json()

newSpaId = objResponse["result"]["type"]["id"]
newSpaEntityTypeId = objResponse["result"]["type"]["entityTypeId"]

print("NewSpaId: " + str(newSpaId))
print("NewSpaEntityTypeId: " + str(newSpaEntityTypeId))

###############################################################################

###############################################################################
#####                      CRIAR CUSTOM FIELDS                            #####
###############################################################################
customFields = [
    {"name": "nomeTarefa",         "type": "string",         "label": "Nome da Tarefa",         "code": "UF_CRM_" + str(newSpaId) + "_NOMETAREFA"},
    {"name": "prazoTarfa",         "type": "datetime",       "label": "Prazo da Tarefa",        "code": "UF_CRM_" + str(newSpaId) + "_PRAZOTAREFA"},
    {"name": "categoria",          "type": "enumeration",    "label": "Subdepartamento",        "code": "UF_CRM_" + str(newSpaId) + "_CATEGORIA"},
    {"name": "conclusao",          "type": "string",         "label": "Feedback Conclusão",     "code": "UF_CRM_" + str(newSpaId) + "_CONCLUSAO"},
    {"name": "motivoCancelamento", "type": "string",         "label": "Motivo Cancelamento",    "code": "UF_CRM_" + str(newSpaId) + "_MOTIVOCANCELAMENTO"},
    {"name": "spaOrigem",          "type": "integer",        "label": "SPA Origem",             "code": "UF_CRM_" + str(newSpaId) + "_SPAORIGEM"},
    {"name": "cardOrigem",         "type": "integer",        "label": "Card Origem",            "code": "UF_CRM_" + str(newSpaId) + "_CARDORIGEM"},
    {"name": "atividadeOrigem",    "type": "integer",        "label": "Atividade Origem",       "code": "UF_CRM_" + str(newSpaId) + "_ATIVIDADEORIGEM"},
    {"name": "spaDestino",         "type": "iblock_element", "label": "Departamento Subtarefa", "code": "UF_CRM_" + str(newSpaId) + "_SPADESTINO"},
    {"name": "subTarefa",          "type": "string",         "label": "Subtarefa",              "code": "UF_CRM_" + str(newSpaId) + "_SUBTAREFA"},
    {"name": "prazoSubTarefa",     "type": "datetime",       "label": "Prazo Subtarefa",        "code": "UF_CRM_" + str(newSpaId) + "_PRAZOSUBTAREFA"}
]

categoriaValues = []

for categoria in newSpaPipelines.split(","):
    objCategoria = {"value": categoria, "def": "N"}
    categoriaValues.append(objCategoria)

for item in customFields:
    payload = {
        "moduleId": "crm",
        "field": {
            "entityId": "CRM_" + str(newSpaId),
            "fieldName": item["code"],
            "title": item["name"],
            "name": item["name"],
            "userTypeId": item["type"],
            "editFormLabel": {'br': item["label"]}
        }
    }

    if item["name"] == "categoria":
        payload["field"]["enum"] = categoriaValues
        
    if item["name"] == "spaDestino":
        payload["field"]["settings"] = {
        "DISPLAY": "DIALOG",
        "LIST_HEIGHT": 1,
        "IBLOCK_ID": 29,
        "DEFAULT_VALUE": "",
        "ACTIVE_FILTER": "Y"
      }

    print("############### List Categories: userfieldconfig.add: " + item["name"])
    print(payload)
    response = requests.post(urlBase + 'userfieldconfig.add', json=payload)
    objResponse = response.json()
    
###############################################################################

###############################################################################
#####                        CRIAR PIPELINES                              #####
###############################################################################

# resgatar o pipeline original para apagar ele depois
payload = {
  "entityTypeId": newSpaEntityTypeId
}

response = requests.post(urlBase + 'crm.category.list', json=payload)
objResponse = response.json()

print("############### List Categories: crm.category.list")

categoriaApagar = objResponse["result"]["categories"][0]

for index, categoria in enumerate(categoriaValues):
    payload = {
        "entityTypeId": newSpaEntityTypeId,
        "fields": {
           "name": categoria["value"],
            "sort": (index + 1) * 10 
        }
    }
    
    print("Nova Categoria:" + categoria["value"])
    print("############### Add category: crm.category.add")
    print(objResponse)
    response = requests.post(urlBase + 'crm.category.add', json=payload)
    objResponse = response.json()
    
    newCategory = objResponse["result"]["category"]
    
    # resgatar todos o estágios que são criados automaticamente para apgar
    payload = {
      "filter": {
        "ENTITY_ID" : "DYNAMIC_" + str(newSpaEntityTypeId) + "_STAGE_" + str(newCategory["id"]),
        "SYSTEM": "N"
      }
    }

    response = requests.post(urlBase + 'crm.status.list', json=payload)
    objResponse = response.json()
    print("############### List satus:  crm.status.list")
    print(payload)
    newCategoryOriginalStatus = objResponse["result"]
    
    for item in newCategoryOriginalStatus:
      payload = { "id": item["ID"]}
      response = requests.post(urlBase + 'crm.status.delete', json=payload)
      print("############### Delete Status: crm.status.delete")
      print(payload)
      
    # alterar o nome do stágio inicial
    payload = {
      "filter": {
        "STATUS_ID": "DT" + str(newSpaEntityTypeId) + "_" + str(newCategory["id"]) + ":NEW"
      }
    }
    response = requests.post(urlBase + 'crm.status.list', json=payload)
    print("############### GetStatus: crm.status.list")
    print(payload)
    objResponse = response.json()["result"]
    
    payload = {
      "id": objResponse[0]["ID"],
      "fields":
      { 
        "NAME": newSpaStages.split(",")[0]
      }    
    }
    
    print("############### Update Status Name: crm.status.update")
    print(payload)
    response = requests.post(urlBase + 'crm.status.update', json=payload)
    objResponse = response.json()
    
    for item in newSpaStages.split(",")[1:]:
      payload = {
        "fields": {
          "STATUS_ID": "DT" + str(newSpaEntityTypeId) + "_" + str(newCategory["id"]) + ":" + item,
          "ENTITY_ID": "DYNAMIC_" + str(newSpaEntityTypeId) + "_STAGE_" + str(newCategory["id"]),
          "NAME": item,
          "NAME_INIT": item,
          "SYSTEM": "N",
          "CATEGORY_ID": str(newCategory["id"])
        }
      }
      
      response = requests.post(urlBase + 'crm.status.add', json=payload)
      objResponse = response.json()
      
      print("############### Add Status:  crm.status.add")
      print(payload)
       
    
# apagar o pipeline original
payload = {
  "entityTypeId": str(newSpaEntityTypeId),
  "id": str(categoriaApagar["id"])
}

print("############### Delete category: crm.category.delete")    
print(payload)

response = requests.post(urlBase + 'crm.category.delete', json=payload)
objResponse = response.json()

print("fim")
