#
#   Created by Brendan Bowler
#   Created on 5/5/2022
#

import datetime
from datetime import timedelta
import sys
from google.cloud import storage
from google.cloud import logging

logging_client  = logging.Client()


class Restorer:
    ''' 
        Class that hold the functionality to restore the data lake
        up to the specified restore date 
    '''
    client_uuid     = ''
    restore_date    = ''
    gcs_client      = None
    gcs_client_read = None
    client_bucket   = None
    restored_bucket = None
    patient_id      = ''
    archive_bucket  = ''


    def __init__(self, client_id, restore_date, patient_id, archive_bucket):
        self.client_uuid        = client_id
        self.restore_date       = restore_date
        self.gcs_client         = storage.Client()
        self.restored_bucket    = self.gcs_client.get_bucket(client_id)
        self.patient_id         = patient_id
        self.archive_bucket     = archive_bucket
        self.logger             = logging_client.logger(client_id + '-restore-logger')
        

    def restore(self):
        ''' 
            Public class used to restore a datalake to a particular point in time
            Returns:
                boolean: True if all files had been restored, False if otherwsie
        '''
        self.logger.log_text("starting restore for " + self.client_uuid + " " + \
            self.patient_id, severity="INFO")
        first_day = self.__get_first_day_in_archive()
        
        if not self.__iteratively_restore_archive(first_day):
            self.logger.log_text("Failed to Restore Client or Patient", severity="ERROR")
            return False

        self.logger.log_text("finished restore for " + self.client_uuid + " " + \
            self.patient_id, severity="INFO")
        return True


    def __get_first_day_in_archive(self):
        ''' 
            Gets the earliest date in the dummy archive for the client
            Returns:
                date (string): The first date in the archive in format yyyymmdd
        '''
        blobs = self.__get_all_blobs_for_client()
        date = self.__compare_blobs_and_get_earliest_date(blobs)
        return date

    def __get_all_blobs_for_client(self):
        ''' 
            Gets a list of all blobs for the client to find the earliest date
            Returns:
                blob_list (list of blobs): List of all blobs for the client
        '''
        blob_list = self.gcs_client.list_blobs(self.archive_bucket, prefix=self.client_uuid + '/')
        
        return blob_list

    def __compare_blobs_and_get_earliest_date(self, blobs):
        ''' 
            Take the list of blobs and finds the lowest date among all their paths
            Args:
                blobs (list of cloud storage blobs): The list of blobs for the client
            Returns:
                date (string): The earliest day in the archive for the client
        '''
        #not sure what I should use for random date to get earliest one
        date = '20990101'
        for blob in blobs:
            date = self.__compare_date_of_blob(blob, date)
        
        return date

    def __get_date_from_blob(self, blob):
        ''' 
            Strips out the date from the given blob and returns it in string format
            Args:
                blob (cloud storage blob): The blob whose date to get
            Returns:
                date (string): The day in the path of the blob
        '''     
        full_path = blob.name
      
        split_path = full_path.split("/", 2)
        date = split_path[1]

        return date

    def __compare_date_of_blob(self, blob, date):
        ''' 
            Compares the provided blobs date and current earliest date and returns the earlier of the two
            Args:
                blob (cloud storage blob): The blob whose date to compare
                date (string): The current earliest date in the archive 
            Returns:
                date (string): The earlier of the two days
        '''     
        if not self.__check_if_blob_is_directory(blob):
            return date

        blob_date = self.__get_date_from_blob(blob)
        blob_date_obj = datetime.datetime.strptime(blob_date, "%Y%m%d")
        current_earliest_date_obj = datetime.datetime.strptime(date, "%Y%m%d")

        if blob_date_obj.date() < current_earliest_date_obj.date():
            return blob_date

        return date


    def __iteratively_restore_archive(self, date):
        ''' 
            Traverses the archive bucket getting all files and restoring them
            in the data lake day by day starting at the first date in the archive 
            and ending at the provided restore date
            Args:
                date (string): The date to be incremented
            Returns:
                boolean: True if the date is the same as the restore date false otherwise
        '''
        restore_date = datetime.datetime.strptime(self.restore_date, "%Y%m%d")
        date = datetime.datetime.strptime(date, "%Y%m%d")
        while (date <= restore_date):
            date = date.strftime('%Y%m%d')
            if not self.__get_blob_list_and_restore_for_day(date):

                return False
            date = self.__increment_date(date)
            date = datetime.datetime.strptime(date, "%Y%m%d")

        return True

    def __get_blob_list_and_restore_for_day(self, date):
        ''' 
            Gets all blobs for the provided day in ther archive bucket and 
            restores those changes in the data lake
            Args:
                date (string): The date for the files to retrieve
            Returns:
                boolean: True if files for specified day were successfully archived
                         False otherwise
        '''
        print("restoring for day")
        print('---------' + date + '--------')
        blobs = self.__get_all_blobs_in_archive_for_date(date)
        if not self.__restore_for_day(blobs):
            return False

        return True


    def __increment_date(self, date):
        ''' 
            Increments the provided day by 1 in yyyymmdd format
            Args:
                date (string): The date to be incremented
            Returns:
                nextDay (string): The date in format yyyymmdd incremented by one day
        '''
        d = datetime.datetime.strptime(date, "%Y%m%d")
        nextDay = (d + timedelta(days=1)).strftime('%Y%m%d')
        return nextDay

    

    def __get_all_blobs_in_archive_for_date(self, date): 
        ''' 
            Gets all files in the archive bucket pertaining to the provided client for that date
            Args:
                date (string): The date indicating which blobs to get
            Returns:
                blob_list (list of cloud storage blobs):  List of blobs for the specified date in the archive
        '''

        blob_list = self.gcs_client.list_blobs(self.archive_bucket, prefix=self.client_uuid + '/' + date + '/')
            
        if self.patient_id != '':
            patient_blob_list = []
            for blob in blob_list:
                if self.patient_id.lower() in blob.name.lower():
                    patient_blob_list.append(blob)
            blob_list = patient_blob_list
        return blob_list

    def __restore_for_day(self, blobs):
        ''' 
            Iterates over the list of blobs and performs the restorion for each one
            Args:
                blobs (list of cloud storage blobs): The list of blobs for a day
            Returns:
                boolean: True if data lake was able to be restored for day False otherwsie
        '''
        for blob in blobs:
            if not self.__restore_blob(blob):
                self.logger.log_text("Failed to Restore Blob: " + blob.name, severity="ERROR")
                return False
            self.logger.log_text("Restored Blob: " + blob.name, severity="INFO")
        
        return True


    def __restore_blob(self, blob):
        ''' 
            Restores the provided blob into the client data lake
            Args:
                blob (cloud storage blob): The current blob to update in the data lake
            Returns:
                boolean: True if data lake was able to be restored for blob False otherwsie
        '''
        
        file_name_and_action = self.__get_file_name_and_action_from_blob(blob)
        if file_name_and_action == '':
            return True

        file_name = file_name_and_action[1]
        action = file_name_and_action[0]

        if not self.__restore_blob_based_on_action(blob, action, file_name):
            return False
        
        return True

    def __get_file_name_and_action_from_blob(self, blob):
        ''' 
            Returns the name of the file of the given blob
            Args:
                blob (cloud storage blob): The current blob to parse
            Returns:
                listOfActionAndName (list): List containing the seperated action and file name
        '''
        if not self.__check_if_blob_is_directory(blob):
            return ''

        full_path = blob.name
        fileNameWithAction = full_path.split("/")[-1]
        listOfActionAndName = fileNameWithAction.split(".", 1)
        
        return  listOfActionAndName

    def __check_if_blob_is_directory(self, blob):
        ''' 
            Checks to make sure the given blob is a file and not a directory. We have seen instances where
            certain folders will return nested folders as blobs and others will only return the files
            Args:
                blob (cloud storage blob): The current blob to check
            Returns:
                boolean: True if blob is a file, false otherwise
        '''
        full_path = blob.name
        blob_list = self.gcs_client.list_blobs(self.archive_bucket, prefix=blob.name)
        if len(list(blob_list)) > 1:
            return False
        return True


    def __restore_blob_based_on_action(self, blob, action, file_name):
        ''' 
            Performs the correct type of restoration based on the action type
            Args:
                blobs (cloud storage blob): The current blob to update in the data lake
                action (string): The action for the file. CREATED UPDATED or DELETED
                file_name (string): Name of the actual file in cloud storage  
            Returns:
                boolean: True if data lake was able to be restored for blob False otherwsie
        '''
        file_path = self.__get_path_from_blob(blob)
        if action == 'CREATED' or action == 'UPDATED':
            if not self.__create_or_update_blob(blob, file_path, file_name):
                return False
        else: 
            if not self.__delete_blob(blob, file_path, file_name):
                return False

        return True


    def __create_or_update_blob(self, blob, file_path, file_name):
        ''' 
            Creates or updates the blob in the data lake
            Args:
                blobs (cloud storage blob): The current blob to update in the data lake
                file_path (string): Path to the file in cloud storage
                file_name (string): Name of the actual file in cloud storage
            Returns:
                boolean: True blob was successfully deleted
        '''
        blob_name = file_path + '/' + file_name
        new_blob = self.restored_bucket.blob(blob_name)
        new_blob.metadata = blob.metadata

        new_blob.upload_from_string(blob.download_as_bytes())
        if new_blob.exists():
            print('Copied Blob: ' + file_name + ' to ' + blob_name)
            return True
        
        return False

    def __get_path_from_blob(self, blob):
        ''' 
            Retrieves the file path for the blob to be restored in the client archive
            Args:
                blob (cloud storage blob): The current blob to get the file path from
            Returns:
                file_path (string): Path to the file in cloud storage
        '''
        full_path = blob.name
        path_list = full_path.split('/')
        file_path = path_list[2] + '/' + path_list[3]
        
        return file_path


    def __delete_blob(self, blob, file_path, file_name):
        ''' 
            Deletes the provided blob from the data lake
            Args:
                blobs (cloud storage blob): The current blob to delete in the data lake
                file_path (string): Path to the file in cloud storage
                file_name (string): Name of the actual file in cloud storage
            Returns:
                boolean: True if blob was successfully deleted false otherwise
        '''
        blob_name = file_path + '/' + file_name
        new_blob = self.restored_bucket.get_blob(blob_name)
        new_blob.delete()

        return True

if __name__ == "__main__":
    ''' Entry point to restore script '''
    print('Performing Restore')
    print(len(sys.argv))
    if len(sys.argv) == 5:
        client          = sys.argv[1]
        restore_date    = sys.argv[2]
        patient_id      = sys.argv[3]
        archive_bucket  = sys.argv[4]
    else:
        client          = sys.argv[1]
        restore_date    = sys.argv[2]
        patient_id      = ''
        archive_bucket  = sys.argv[3]

    restorer        = Restorer(client, restore_date, patient_id, archive_bucket)
    restorer.restore()