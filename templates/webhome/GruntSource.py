from django_work import urls
import os
from django_work import settings


class MyError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def get_parent_files(filename, app_name):
    ptr = open(filename, "r")
    temp = ptr.readline()
    if temp.find("{% extends ") != -1:
        startpos = temp.find("{% extends ") + 12
        endpos = temp.find(" %}") - 1
        parent_name = temp[startpos:endpos]
        list_files = get_total_files_list(parent_name, app_name)
        if list_files is None:
            parent_name = os.path.join(app_name,parent_name)
            list_files = get_total_files_list(parent_name, app_name)
        return list_files


def get_total_files_list(filename, appname):
    template_paths = settings.TEMPLATE_DIRS
    file_list = []
    template_paths = template_paths + (os.path.join(settings.BASE_DIR, appname, "templates"),)
    for path in template_paths:
        full_path = os.path.join(path, filename)
        if os.path.exists(full_path):
            ptr = open(full_path, 'r')
            temp = ptr.readline()
            while temp != '':
                while temp.find("{% block javascript") == -1 and temp != '':
                    temp = ptr.readline()
                if temp == '':
                    break
                temp = ptr.readline()
                while temp.find("{% endblock") == temp.find("</html>") == temp.find("{% block") == -1:
                    temp = ptr.readline()
                    if temp.find("{% else %}") != -1:
                        while temp.find("{% endif %}") == temp.find("{% endblock") == temp.find("</html>") == -1:
                            temp = ptr.readline()
                            if temp.find("}}") != -1 and temp.find('">') != -1 and temp != '':
                                sfname = temp.find("}}") + 2
                                efname = temp.find('">')
                                js_file_name = temp[sfname: efname]
                                file_list.append(js_file_name)
                        if temp.find("{% endblock") != -1 or temp.find("</html>") != -1:
                            msg = "endblock before endif in file -" + filename
                            raise MyError(msg)
                if temp.find("</html>") != -1:
                    msg = "closing tag before endblock in file - " + filename
                    raise MyError(msg)
                if temp.find("{% block") != -1:
                    msg = "new block opened before endblock tag in file - " + filename
                    raise MyError(msg)
            ptr.close()
            list2 = get_parent_files(full_path, appname)
            if list2 is not None:
                for file_name in file_list:
                    list2.append(file_name)
            else:
                list2 = file_list
            return list2


def find_templates(urlName, appName):
    file_ptr = open(urlName._callback.func_code.co_filename, "r")
    startLine = urlName._callback.func_code.co_firstlineno
    while startLine >= 0:
        line = file_ptr.readline()
        startLine -= 1
    line.lstrip()
    while line.find("def") == -1 and line.find("class") == -1 and line != '':
        if line.find("return render") != -1 and (line.find("#") > line.find("return render") or line.find("#") == -1):
            nameStart = line.find(",") + 3
            nameEnd = line.find(",", nameStart) - 1
            if nameEnd < 0:
                nameEnd = line.find(")") - 1
            fileName = line[nameStart:nameEnd]
            filesList = get_total_files_list(fileName, appName)
            print "app name - ", appName
            print "file name - ", fileName
            print "list - ", filesList
            print "______________________________________________"
        line = file_ptr.readline()
        line.lstrip()


def fetch_urls():
    for eachURL in urls.urlpatterns:
        appName = eachURL.regex.pattern[1:-1]
        if hasattr(eachURL,'url_patterns'):
            for each in eachURL.url_patterns:
                find_templates(each, appName)
        else:
            find_templates(eachURL, appName)


fetch_urls()