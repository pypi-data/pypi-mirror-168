import os
import zipfile

import gdown

from gnutools import fs


def gdrive(gdrive_uri, output_dir=None):
    assert gdrive_uri.startswith("gdrive://")
    gdrive_id = gdrive_uri.split("gdrive://")[1]
    output_dir = f"/tmp/{gdrive_id}" if output_dir is None else output_dir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        output_file = f"/tmp/.{gdrive_id}"
        gdown.download(f"https://drive.google.com/uc?id={gdrive_id}", output_file)
        try:
            with zipfile.ZipFile(output_file, "r") as zObject:
                zObject.extractall(output_dir)
            os.system(f"rm -r {output_file}")
        except zipfile.BadZipFile:
            os.system(f"mv {output_file} {output_dir}/{gdrive_id}")
    return fs.listfiles(output_dir)


gdrivezip = gdrive
