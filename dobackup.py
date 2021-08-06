#!/usr/bin/python
# backup all attachments for versions
# Peter Marks for Lauren and Sandra Gravis
from posixpath import expanduser
import shotgun_api3
import json
import os
import sys
#from urllib.parse import urlparse

SHOTGUN_URL = "https://YOURDOMAIN.shotgunstudio.com"
SHOTGUN_USER = "USERNAME"
SHOTGUN_PASSWORD = "PASSWORD"

PROJECT_NAME = "Project Name"
DOWNLOAD_PATH = "/Users/YOURUSER/Downloads/shotgun"

def ensure_dir(directory):
    if not os.path.exists(directory):
        print("Creating: %s" % directory)
        os.makedirs(directory)

def main():
    ensure_dir(DOWNLOAD_PATH)
    print("Logging in...")
    sg = shotgun_api3.Shotgun(SHOTGUN_URL,
                            login=SHOTGUN_USER,
                            password=SHOTGUN_PASSWORD)

    print("Getting versions...")
    required_fields = ['id', 'code', 'sg_uploaded_movie', 'updated_by']
    versions = sg.find("Version", [['project.Project.name', 'is', PROJECT_NAME]], fields=required_fields)
    print("found %d versions" % len(versions)) # 55630
    total_files = len(versions)
    count = 0
    for version in versions:
        #print(json.dumps(version))
        try:
            name = version["sg_uploaded_movie"]["name"]
            type = version["sg_uploaded_movie"]["type"]
            attachment_id = version["sg_uploaded_movie"]["id"]
            attachment = {"type": "Attachment", "id": attachment_id}
            updated_by_name = version['updated_by']['name']
            print("name = %s, type = %s, updated_by = %s" % (name, type, updated_by_name))
            url = sg.get_attachment_download_url(attachment=attachment)
            download_directory = os.path.join(DOWNLOAD_PATH, updated_by_name)
            ensure_dir(download_directory)
            download_file_path = os.path.join(DOWNLOAD_PATH, updated_by_name, name)
            if os.path.exists(download_file_path) == False:
                print("file %s of %s downloading %s..." % (count, total_files, name))
                sg.download_attachment(attachment=attachment, file_path=download_file_path)
            else:
                print("skipping existing download %s" % download_file_path)
        except KeyboardInterrupt:
            print("Keyboard interrupt")
            return
        except:
            print(sys.exc_info()[0])
            print(json.dumps(version))
        count += 1


if __name__ == "__main__":
    main()
