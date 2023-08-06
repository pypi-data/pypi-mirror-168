from gnutools.fs import parent, listfiles
import os


def gdrivezip(gdrive_filename, output_dir=None):
    """_summary_

    Args:
        gdrive_filename (_type_): _description_
        output_dir (_type_, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """
    assert gdrive_filename.startswith("gdrive://")
    gdrive_id = gdrive_id = gdrive_filename.split("gdrive://")[1]
    output_dir = f"/tmp/{gdrive_id}" if output_dir is None else output_dir
    if not os.path.exists(output_dir):
        zip_file = f"{output_dir}.zip"
        os.makedirs(parent(output_dir), exist_ok=True)
        command = f"wget --no-check-certificate 'https://docs.google.com/uc?export=download&id={gdrive_id}' -O {zip_file} && \
        unzip {zip_file} -d {output_dir}"
        os.system(command)
        assert os.path.exists(output_dir)
    return listfiles(output_dir)

