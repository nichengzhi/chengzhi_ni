import boto
from boto.s3.key import Key
import io
aws_access_key_id='xxxxxx'
aws_access_key='xxxxxx'
s3_bucket_name = "xxxx"
s3_folder = "xxxx"
connec = boto.connect_s3(aws_access_key_id, aws_access_key)
bucket = connec.get_bucket(s3_bucket_name, validate=False)
upload = Key(bucket)
csv_filename = 'aerio_{0}_to_{1}.csv'.format(start_date.strftime('%Y%m%d'), end_date.strftime('%Y%m%d'))
temp_aerio_df = io.BytesIO()
df.to_csv(temp_aerio_df, index=False, encoding='utf8')
temp_aerio_df.seek(0)

upload.key = '{0}/{1}'.format(s3_folder, csv_filename)

upload.set_contents_from_string(temp_aerio_df.getvalue())
logging.info('upload s3 end')

# Download file from s3
modified_date = [(file.last_modified, file) for file in bucket if (s3_folder_name in file.name) & ('xlsx' in file.name)]

file_to_download = sorted(modified_date)[-1][1]
filename = str(file_to_download.key).split('/')[1]

file_to_download.get_contents_to_filename(filename)

#catalog = pd.read_excel('amazon_catalog.xlsx')