import uuid

from datetime import date, datetime
from string import ascii_letters
from secrets import token_urlsafe, choice
from slugify import slugify


def get_ymd_date() -> str:
    """
    Get the current date in YMD format

    Returns:
         The current date in YMD format
    """
    now = datetime.now()
    return now.strftime("%y%m%d")


def get_hms_time() -> str:
    """
    Get the current time in HM format

    Returns:
         The current time in HM format
    """
    now = datetime.now()
    return now.strftime("%H%M%S")


def get_current_date() -> date:
    """
    Get the current date

    Returns:
         The current date
    """
    return date.today()


def gen_short_uuid(string_length: int) -> str:
    """
    Generate a UUID with the given string length

    Args:
        string_length: length of string to generate.

    Returns:
         The UUID
    """
    rdm = str(uuid.uuid4())
    rdm = rdm.upper()
    rdm = rdm.replace("-", "")
    return rdm[0:string_length]


def gen_order_number() -> str:
    """
    Generate a order number

    Returns:
         The order number
    """
    u = gen_short_uuid(6)
    t = get_hms_time()
    d = get_ymd_date()
    return f"{d}-{t}-{u}"


def get_file_extension(filename: str) -> str:
    """
    Get the file extension.

    Args:
        filename: name of file.

    Returns:
        file extension
    """
    from os import path
    return path.splitext(filename)[1][1:]


def allowed_file(filename: str) -> bool:
    """
    Check if the file is allowed.

    Args:
        filename: name of file.

    Returns:
        The return value. True for success, False otherwise.
    """
    from flask import current_app
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config[
               'ALLOWED_EXTENSIONS']


def delete_file(file_path: str, file_name: str):
    """
    Delete a file if it exists.

    Args:
        file_path: path fo file
        file_name: name of file
    """
    try:
        from os import path
        from os import remove
        remove(path.join(file_path, file_name))
    except FileNotFoundError:
        pass


def gen_urlsafe_token(length: int) -> str:
    """
    Generate a URL-safe, Base64-encoded securely generated random string.

    Args:
        length: length of string to generate.
    Return:
         URL-safe, Base64-encoded securely generated random string.
    """
    return token_urlsafe(length)


def create_folder(folder_path: str, folder_name: str) -> None:
    """
    Create a folder if it doesn't exist.

    Args:
        folder_path: path to the folder.
        folder_name: name of the folder.
    """
    try:
        from os import path
        from os import mkdir
        mkdir(path.join(folder_path, folder_name))
    except FileExistsError:
        pass


def create_file(file_path: str, file_name: str, file_mode: str = "x",
                file_content: str = '') -> None:
    """
    Create a file if it doesn't exist

    Args:
        file_path: path to file.
        file_name: name of file.
        file_mode: open file mode.
        file_content:
    """
    try:
        from os import path
        with open(path.join(file_path, file_name), file_mode) as f:
            f.write(file_content)
    except FileExistsError:
        pass


def gen_slug(text: str, length: int = 10) -> str:
    """
    Generate a slug from the given text

    Args:
        text (str): text to slug
        length (int): max length of slug

    Returns:
         The slugify text
    """
    if text is None:
        text = ''.join(choice(ascii_letters) for _ in range(10))

    return slugify(text, max_length=length, word_boundary=True, save_order=True)
