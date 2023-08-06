# Importing required libraries
import json
import os
import pandas as pd
from pandas.io.json import json_normalize


def data_reader(arm_template_base_path):
    json_path = os.path.join(arm_template_base_path, "arm_template.json")
    with open(json_path, "r") as read_file:
        data = json.load(read_file)
    return data


def obsolete_datasets(arm_template_base_path, resource_cleaned_flag=0):
    # Preparing list of obsolete datasets which are not getting used in any pipelines.
    dict_object = data_reader(arm_template_base_path)
    resource = dict_object["resources"]
    res_df = json_normalize([res for res in resource])

    # #Creating list of all the datasets which are dependent on pipelines.
    dependent_component_list = [x for x in res_df["dependsOn"]]
    dependent_datasets = []
    for component_list in dependent_component_list:
        for component in component_list:
            if "datasets" in component:
                dependent_datasets.append(
                    component.replace("variables('factoryId'), '/datasets", "parameters('factoryName'), '"))
    dependent_datasets = list(set(dependent_datasets))

    # Creating new resource list which can be further used to find obsolete connections.
    if resource_cleaned_flag == 1:
        resource_cleaned = [res for res in resource if (res["name"] in dependent_datasets) or (
                res["type"] != "Microsoft.DataFactory/factories/datasets")]
        return resource_cleaned

    # Detecting obsolete datasets from resource list which are not present in dataset dependent list.
    resource_obsolete = [res for res in resource if (res["name"] not in dependent_datasets) and (
            res["type"] == "Microsoft.DataFactory/factories/datasets")]
    dataset_obs_df = pd.DataFrame(
        [res["name"].split(",")[-1].replace(" '/", "").replace("')]", "") for res in resource_obsolete],
        columns=["Obsolete_Datasets"])
    return dataset_obs_df


def obsolete_linked_services(arm_template_base_path, resource_cleaned_flag=0):
    # Preparing list of obsolete linked services which are not getting used in any pipelines/datasets.
    dict_object = data_reader(arm_template_base_path)
    resource = dict_object["resources"]
    resource_cleaned = obsolete_datasets(arm_template_base_path, resource_cleaned_flag=1)
    res_df = json_normalize([res for res in resource_cleaned])

    # Creating list of all the linked services which are dependent on pipelines/datasets.
    dependent_component_list = [x for x in res_df["dependsOn"]]
    dependent_linked_service = []
    for component_list in dependent_component_list:
        for component in component_list:
            if "linkedServices" in component:
                dependent_linked_service.append(
                    component.replace("variables('factoryId'), '/linkedServices", "parameters('factoryName'), '"))
    dependent_linked_service = list(set(dependent_linked_service))

    # Creating new resource list which can be further used to find obsolete connections.
    if resource_cleaned_flag == 1:
        resource_cleaned = [res for res in resource_cleaned if (res["name"] in dependent_linked_service) or (
                res["type"] != "Microsoft.DataFactory/factories/linkedServices")]
        return resource_cleaned

    # Detecting obsolete linked service from resource list which are not present in connections dependent list
    resource_obsolete = [res for res in resource if (res["name"] not in dependent_linked_service) and (
            res["type"] == "Microsoft.DataFactory/factories/linkedServices")]
    linked_service_obs_df = pd.DataFrame(
        [res["name"].split(",")[-1].replace(" '/", "").replace("')]", "") for res in resource_obsolete],
        columns=["Obsolete_Linked_Services"])
    return linked_service_obs_df
