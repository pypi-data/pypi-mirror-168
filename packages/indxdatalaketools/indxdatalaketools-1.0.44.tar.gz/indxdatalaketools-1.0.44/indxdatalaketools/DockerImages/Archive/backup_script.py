#
#   Created by Ryan McDermott
#   Created on 3/16/2022
#

import datetime
import sys
from google.cloud import storage
from google.cloud import bigquery
from google.cloud import logging

logging_client  = logging.Client()

class Archiver:
    ''' 
        Class that hold the functionality to archive the data lake
        from the Changelog table   
    '''
    client_uuid     = ''

    bq_client       = None
    gcs_client      = None
    gcs_client_read = None
    client_bucket   = None
    archive_bucket  = None


    def __init__(self, client_id,read_credentials, archive_bucket):
        self.client_uuid        = client_id
        self.bq_client          = bigquery.Client()
        self.gcs_client         = storage.Client()
        self.gcs_client_read    = storage.Client.from_service_account_json(read_credentials)
        self.client_bucket      = self.gcs_client_read.get_bucket(client_id)
        self.archive_bucket     = self.gcs_client.bucket(archive_bucket)
        self.logger             = logging_client.logger(client_id + '-archive-logger')



    def archive(self):
        ''' 
            Public class used to update a datalake to archive the files added/removed/updated 
            the previous day
            Returns:
                boolean: True if all files had been archived, False if otherwsie
        '''
        # get table from yetsterday
        change_log_table    = self.__get_table_from_yetsterday()
        rows                = self.bq_client.list_rows(change_log_table)
        result              = True

        self.logger.log_text("Starting archive service", severity="INFO")
        for row in list(rows):
            print(row)
            if not self.__perform_archive_on_row(row):
                print('Could not archive row ' + str(row))
            if not self.__update_row_in_changelog_table(row):
                print('could not update changelog table for row ' + str(row))

        self.logger.log_text("Finished archive service", severity="INFO")
        return result

    
    def __get_table_from_yetsterday(self):
        '''
            Gets all table rows that were inserted yesterday
            Args:
                None
            Returns:
                table rows: The rows inserted to the changelog yesterday
        '''
        dataset_id          = 'SNAPSHOTS_'+self.__transform_client_id()
        yesterday_date      = self.__get_yesterday_date()

        dataset_ref         = self.bq_client.dataset(dataset_id, project='indx-data-services')
        table_ref           = dataset_ref.table(yesterday_date)
        table               = self.bq_client.get_table(table_ref)
    
        return table
        
    
    def __transform_client_id(self):
        '''
            Transforms the client id to contain no dashes and have all
            letters uppercase:
            Args:
                None
            Returns:
                string: transformed string
        '''
        transformed_client_id = self.client_uuid
        transformed_client_id = transformed_client_id.replace('-','')
        transformed_client_id = transformed_client_id.upper()

        return transformed_client_id

    
    def __get_yesterday_date(self):
        ''' 
            Gets yesterdays date in YYYYMMDD format 
            Returns:
                string: yesterday in YYYYMMDD format
        '''
        yesterday       = datetime.datetime.now() - datetime.timedelta(1)
        yesterday_date  = yesterday.date()
        yesterday       = yesterday_date.strftime('%Y%m%d')

        return str(yesterday)


    def __perform_archive_on_row(self, row):
        '''
            Performs the archive on the file represented by the row
            Args:
                row (google.cloud.bigquery.Row): The row repesenting the file we wish to archive
            Returns:
                boolean: True if the row was successfully archived, False if otherwise
        '''
        if row.get('REPLICATED') == True:
            print(str(row) + ': Already archived skipping')
            self.logger.log_text(str(row) + ': Already archived in ChangeLog', severity='INFO')
            return True

        if row.get('ACTION') == 'CREATED' or row.get('ACTION') == 'UPDATED':
           return self.__perform_archive_created_or_updated(row)

        elif row.get('ACTION') == 'DELETED':
            return self.__perform_archive_deleted(row)

        return False

    
    def __perform_archive_created_or_updated(self, row):
        '''
            Performs the archive operation on a created or updated file
            Args:
                row (google.cloud.bigquery.Row): The row repesenting the file we wish to archive
            Returns:
                boolean: True if the row was successfully archived, False if otherwise
        '''
        blob_name           = row.get('FILE_PATH') + '/' + row.get('FILE_NAME')
        copy_file_name      = row.get('ACTION') + '.' + row.get('FILE_NAME')
        blob                = self.client_bucket.get_blob(blob_name)
        blob_copy_name      = self.client_uuid + '/' + \
            self.__get_yesterday_date() + '/' + row.get('FILE_PATH') + '/' + copy_file_name
            
        new_blob            = self.archive_bucket.blob(blob_copy_name)
        if blob is None:
            # The file must have been created and deleted in the 
            # same day put empty string as place holder
            new_blob.upload_from_string('')
            self.logger.log_text(blob_name + ' was created then deleted on the same day',
                severity='INFO')
            print(blob_name + ' was created then deleted on the same day')
            return True
        new_blob.metadata   = blob.metadata
        if new_blob.exists():
            self.logger.log_text('This blob ' + blob_copy_name + ' has already been archived',
                severity='INFO')
            print('This blob ' + blob_copy_name + ' has already been archived')
            return True
        new_blob.upload_from_string(blob.download_as_bytes())
        
        if new_blob.exists():
            self.logger.log_text('Copied Blob: ' + blob_name + ' to ' + blob_copy_name,
                severity='INFO')
            print('Copied Blob: ' + blob_name + ' to ' + blob_copy_name)
            return True
        
        self.logger.log_text('Failed to archive Blob: ' + blob_name,
                severity='ERROR')
        return False


    def __perform_archive_deleted(self, row):
        '''
            Performs the steps neccesary to arhcive a file delete in the archive bucket
            Args:
                row (google.cloud.bigquery.Row): The row repesenting the file we wish to archive
            Returns:
                boolean: True if the row was successfully archived, False if otherwise
        '''
        copy_file_name  = row.get('ACTION') + '.' + row.get('FILE_NAME')
        blob_copy_name  = self.client_uuid + '/' + \
            self.__get_yesterday_date() + '/' + row.get('FILE_PATH') + '/' + copy_file_name
        blob            = self.archive_bucket.blob(blob_copy_name)
        if blob.exists():
            self.logger.log_text('This blob ' + blob_copy_name + ' has already been archived',
                severity='INFO')
            print('This blob ' + blob_copy_name + ' has already been archived')
            return True
        blob.upload_from_string('')

        if blob.exists():
            self.logger.log_text('Archived Deleted Blob to ' + blob_copy_name,
                severity='INFO')
            print('Archived Deleted Blob to ' + blob_copy_name)
            return True

        self.logger.log_text('Failed to archive deleted Blob: ' + blob_copy_name,
                severity='ERROR')
        return False


    def __update_row_in_changelog_table(self, row):
        '''
            Updates the changelog table's row from processed to True, and inserts the 
            processed time
            Args:
                row (google.cloud.bigquery.Row): The row repesenting the file we wish to update
            Returns:
                boolean: True if the row was updated False if otherwise
        '''
        if row.get('REPLICATED') == True:
            self.logger.log_text(str(row) + ': Already updated in ChangeLog', severity='INFO')
            print(str(row) + ': Already updated in ChangeLog')
            return True

        dml_query = self.__create_dml_query(row)
        return self.__run_dml_query_on_table(dml_query)


    def __create_dml_query(self, row):
        '''
            Function that creates a dml query to updated the changlog table processed
            column for the given row
            Args:
                row (google.cloud.bigquery.Row): The row repesenting the file we wish to update
            Returns:
                boolean: True if the changelog table was updated, False if otherwise
        '''
        table_name  = "indx-data-services.SNAPSHOTS_"+\
            self.__transform_client_id()+"."+self.__get_yesterday_date()
        now         = self.__get_datetime_now()
        dml_query   = 'UPDATE ' + table_name + ' SET '
        dml_query   += 'REPLICATED = true, REPLICATED_AT = \'' + now + '\' '
        # remove last comma
        
        dml_query   += 'WHERE FILE_PATH = \'' + row.get('FILE_PATH') + '\' '
        dml_query   += 'AND FILE_NAME = \'' + row.get('FILE_NAME') + '\' '
        dml_query   += 'AND ACTION = \'' + row.get('ACTION') + '\' '
        dml_query   += 'AND ACTION_AT = \'' + str(row.get('ACTION_AT')) + '\''
        return dml_query


    def __get_datetime_now(self):
        '''
            Gets the current datetime for now and returns it
            Returns:
                datetime: The datetime of now
        '''
        now             = datetime.datetime.now()
        time_now_string = now.strftime('%Y-%m-%d %H:%M:%S')
        
        return time_now_string


    def __run_dml_query_on_table(self, dml_query):
        '''
            Runs the query on the PATIENTS table
            args:
                dml_query (string): The string containging the query command to run on the
                    PATIENTS table
            Returns:
                boolean: True if the operation was a success, False if otherwise
        '''
        try:
            query_job = self.bq_client.query(dml_query)
            rows = query_job.result()
            print(rows.num_results)
            if query_job.errors is None:
                self.logger.log_text(str(dml_query) + ': updated in ChangeLog', severity='INFO')
                return True
            self.logger.log_text(str(dml_query) + ': failed to update in ChangeLog', severity='ERROR') 
            return False
        except Exception as e:
            print("FAILURE to update patient: " +str(e))
            self.logger.log_text(str(dml_query) + ': failed to update in ChangeLog with error: ' + \
                str(e), severity='ERROR')
            return False


if __name__ == "__main__":
    ''' Entry point to archiving script '''
    print('Performing Archive')
    client          = sys.argv[1]
    cred            = sys.argv[2]
    archive_bucket  = sys.argv[3]
    archiver        = Archiver(client, cred, archive_bucket)
    archiver.archive()
