# airavat

#### arm_template
This template detects obsolete datasets and connections of Azure Data Factory(ADF) using ARM template.
##
  > obsolete_datasets: This method detects all the obsolete datasets present in ADF.
   >>Input: arm_template_folder_path; Output: Pandas dataframe having one column (Obsolete_Datasets).
##
  > obsolete_linked_services: This method detects all the obsolete linked services present in ADF.
  >> Input: arm_template_folder_path; Output: Pandas dataframe having one column (Obsolete_Linked_Services).