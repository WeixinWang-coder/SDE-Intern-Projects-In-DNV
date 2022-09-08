import requests
import json
from xml.etree import ElementTree as ET
import os
import shutil
from zipfile import ZipFile
from datetime import date

def synergi_function(sp_username, sp_password, sp_script, sp_path):
    PipelineUser = sp_username
    PipelinePass = sp_password
    url_Endpoint = sp_script                                
    s = requests.Session()
    payload = {"username": PipelineUser, "password": PipelinePass}
    response = s.post(url_Endpoint + '/login',json=payload)
    if response.status_code == 200:
        print("\nSite works, hold on......")
    else:
        print('\nSite faild log in')

    name = url_Endpoint[url_Endpoint.index('//') + 2: len(url_Endpoint) - 4]
    day = date.today().strftime("%b-%d-%Y")
    main_path = f'{sp_path}/{name}     ' + day
    #8 paths for secondary folder 
    path_analysis_items = main_path + '/Analysis_items'
    path_data_templates = main_path + '/Data_templates'
    path_questionnaire_templates = main_path + '/Questionnaire_templates'
    path_risk_model = main_path + '/Risk_model_library'
    path_analytical_model = main_path + '/Analytical_model_library'
    path_integrity_activity = main_path + '/Integrity_activity_methods'
    path_data_upload_templates = main_path + '/Data_upload_templates'
    path_defect_model_library = main_path + '/Defect_model_library'

    #saving path to path list 
    path_list = []
    path_list.append(path_analysis_items)
    path_list.append(path_data_templates)
    path_list.append(path_questionnaire_templates)
    path_list.append(path_risk_model)
    path_list.append(path_analytical_model)
    path_list.append(path_integrity_activity)
    path_list.append(path_data_upload_templates)
    path_list.append(path_defect_model_library)

    #Create folders
    if os.path.exists(main_path):
        shutil.rmtree(main_path)
    for item in path_list:
        os.makedirs(item)


    #functions for fectching the data from different sections
    #---------------------------------------------------------------------------------------------------------------------------------------------------------------
    #Analysis items section
    def analysis_items_section():
        dataOverview_analysis_items = url_Endpoint + '/AssetTypes/Overview'
        try:
            r1 = s.get(dataOverview_analysis_items)
            datasheetDefinitions_json = json.loads(r1.text)
                # save name and oid pair
            sheet_map = datasheetDefinitions_json["assetTypes"]
            name_list = []
            for sheet in sheet_map:
                sheet_list = sheet.get("name")
                name_list.append(sheet_list)

            for item in name_list:
                dataOverview_datasheet = url_Endpoint + f'/AssetTypes/export/{item}'
                r = s.get(dataOverview_datasheet)
                tree = ET.XML(r.text)
                myPath = f"{path_list[0]}/{item}.xml"
                with open(myPath, 'wb') as f:
                    f.write(ET.tostring(tree))
        except:
            shutil.rmtree(main_path)
            print("no authorization")
    #Date Templates section
    def data_templates_section():
        dataOverview_datasheetDefinitions = url_Endpoint + '/DataSheetsDefinitions'
        r1 = s.get(dataOverview_datasheetDefinitions)
        datasheetDefinitions_json = json.loads(r1.text)
            # save name and oid pair
        sheet_dic = {}
        for sheet in datasheetDefinitions_json:
            oid = sheet.get('oid')
            sheet_name = sheet.get('name')
            sheet_dic[sheet_name] = oid

        for key in sheet_dic:
            sheet_oid = sheet_dic[key]
            dataOverview_datasheet = url_Endpoint + f'/DataSheetsDefinitions/{sheet_oid}/exportDefinition'
            r = s.get(dataOverview_datasheet)
            tree = ET.XML(r.text)
            myPath = f"{path_list[1]}/{key}.xml"
            with open(myPath, 'wb') as f:
                f.write(ET.tostring(tree))

    #Questionaire Templates section
    def questionnaire_templates_section():
        dataOverview_quetionaire = url_Endpoint + '/questionnaire'
        r2 = s.get(dataOverview_quetionaire)
        datasheet_questionnaire_json = json.loads(r2.text)
                
            # save name and oid pair
        questionnaire_pair = {}
        for sheet in datasheet_questionnaire_json:
            oid = sheet.get('oid')
            sheet_name = sheet.get('name')
            questionnaire_pair[sheet_name] = oid

        for key in questionnaire_pair:
            sheet_oid = questionnaire_pair[key]
            dataOverview_datasheet = url_Endpoint + f'/questionnaire/{sheet_oid}/exportDefinition'
            r = s.get(dataOverview_datasheet)
            tree = ET.XML(r.text)
            myPath = f"{path_list[2]}/{key}.xml"
            with open(myPath, 'wb') as f:
                f.write(ET.tostring(tree))

    #risk model template section
    def risk_model_section():
        dataOverview_analysis_items = url_Endpoint + '/riskModels'
        r1 = s.get(dataOverview_analysis_items)
        datasheetDefinitions_json = json.loads(r1.text)
        name_list = []
        for sheet in datasheetDefinitions_json:
            name = sheet.get("name")
            name_list.append(name)
        for item in name_list:
            dataOverview_datasheet = url_Endpoint + f'/riskModels/ExportModels/{item}'
            r = s.get(dataOverview_datasheet)
            with open(f"{path_list[3]}/{item}.zip",'wb') as tmp:
                tmp.write(r.content)
            with ZipFile(f"{path_list[3]}/{item}.zip", 'r') as z:
                z.extractall(f"{path_list[3]}/{item}")
            # os.remove(f"{path_list[3]}/{item}.zip")
            
    #analysis model templates section
    def analysis_model_templates():
        dataOverview_analysis_items = url_Endpoint + '/AnalysisTypes'
        r1 = s.get(dataOverview_analysis_items)
        datasheetDefinitions_json = json.loads(r1.text)
        name_list = []
        for sheet in datasheetDefinitions_json:
            name = sheet.get("name")
            name_list.append(name)
        for item in name_list:
            dataOverview_datasheet = dataOverview_analysis_items + f'/ExportModels/{item}'
            r = s.get(dataOverview_datasheet)
            with open(f"{path_list[4]}/{item}.zip",'wb') as tmp:
                tmp.write(r.content)
            with ZipFile(f"{path_list[4]}/{item}.zip", 'r') as z:
                z.extractall(f"{path_list[4]}/{item}")
            # os.remove(f"{path_list[4]}/{item}.zip")

    #integrity_activity_methods_section section
    def integrity_activity_methods_section():
        dataOverview_quetionaire = url_Endpoint + '/IntegrityActivityResultGroup/Overview'
        r2 = s.get(dataOverview_quetionaire)
        datasheet_questionnaire_json = json.loads(r2.text)
            # save name and oid pair
        questionnaire_pair = {}
        for sheet in datasheet_questionnaire_json.get("groups"):
            oid = sheet.get('oid')
            sheet_name = sheet.get('name')
            questionnaire_pair[sheet_name] = oid

        for key in questionnaire_pair:
            sheet_oid = questionnaire_pair[key]
            dataOverview_datasheet = url_Endpoint + f'/IntegrityActivityResultGroup/Export/{sheet_oid}'
            r = s.get(dataOverview_datasheet)
            tree = ET.XML(r.text)
            myPath = f"{path_list[5]}/{key}.xml"
            with open(myPath, 'wb') as f:
                f.write(ET.tostring(tree))

    def data_upload_templates():
        dataOverview_quetionaire = url_Endpoint + '/IntegrityActivityResultsDataTemplates'
        r2 = s.get(dataOverview_quetionaire)
        datasheet_questionnaire_json = json.loads(r2.text)
            # save name and oid pair
        questionnaire_pair = {}
        for sheet in datasheet_questionnaire_json:
            oid = sheet.get('oid')
            sheet_name = sheet.get('name')
            questionnaire_pair[sheet_name] = oid

        for key in questionnaire_pair:
            sheet_oid = questionnaire_pair[key]
            dataOverview_datasheet = url_Endpoint + f'/IntegrityActivityResultsDataTemplates/Export/{sheet_oid}'
            r = s.get(dataOverview_datasheet)
            tree = ET.XML(r.text)
            myPath = f"{path_list[6]}/{key}.xml"
            with open(myPath, 'wb') as f:
                f.write(ET.tostring(tree))

    #defect_model_library section
    def defect_model_library():
        dataOverview_defectModelScheme = url_Endpoint + '/DefectModelScheme/overview'
        r1 = s.get(dataOverview_defectModelScheme)

        datasheetDefinitions_json = json.loads(r1.text)
        name_list = []
        for sheet in datasheetDefinitions_json["schemes"]:
            name = sheet.get("name")
            name_list.append(name)
        for item in name_list:
            dataOverview_datasheet = url_Endpoint + f'/DefectModelScheme/ExportModels/{item}'
            r = s.get(dataOverview_datasheet)
            with open(f"{path_list[7]}/{item}.zip",'wb') as tmp:
                tmp.write(r.content)
            with ZipFile(f"{path_list[7]}/{item}.zip", 'r') as z:
                z.extractall(f"{path_list[7]}/{item}")
            # os.remove(f"{path_list[7]}/{item}.zip")
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #run and save sections
    #try except are for the future maintainance
    
    analysis_items_section()
    data_templates_section()
    questionnaire_templates_section()
    risk_model_section()
    analysis_model_templates()
    data_upload_templates()
    integrity_activity_methods_section()
    defect_model_library()

    
        #remove empty folders
    for item in path_list:
        with os.scandir(item) as it:
            if not any(it):
                shutil.rmtree(item)


    print("\nBacked-up!!!")
    print(f"Created Location: {main_path}\n")

        #Create a site zipfile if needed
    shutil.make_archive(main_path, 'zip', main_path)
        
        