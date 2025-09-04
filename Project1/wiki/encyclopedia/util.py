import re
import os
import random

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None

def search_results(search):
    """
    Return list of entries that contain the query in the title.
    """
    _, filenames = default_storage.listdir("entries")
    #Faire la liste des items dans la liste des pages qui contiennent le string recherché
    result = []
    for filename in filenames:
        if search in filename:
            result.append(filename)

    return list(sorted(re.sub(r"\.md$", "", filename)
            for filename in result if filename.endswith(".md")))

def create_new_page(title, content):
    file_name = ".\entries\\" + str(title) + ".md"
    file_content = "#" + str(title) + "\n\r" + content
    with open(file_name, "x") as file:
        file.write(file_content)
    return (print("page successfuly created"))

def edit_page(title, new_title, new_content):
    file_name = ".\entries\\" + str(title) + ".md"
    file_new_name = ".\entries\\" + str(new_title) + ".md"
    with open(file_name, "w") as file:
        file.write(new_content)
    if title != new_title:
        os.rename(file_name, file_new_name)
    return (print("page successfuly edited"))

def get_random_page():
    return (random.choice(list_entries()))
    