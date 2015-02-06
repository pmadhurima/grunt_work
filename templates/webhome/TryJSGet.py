from django.conf import settings
import os
from django_work import urls
from django.core import urlresolvers

# for url_pattern in urlpatterns:
#     print url_pattern._callback.func_code


class MyError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def get_list_of_files(filename, app_name):
    template_paths = settings.TEMPLATE_DIRS
    file_list = []
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
            list2 = get_parent_files(full_path, app_name)
            if list2 is not None:
                for file_name in file_list:
                    list2.append(file_name)
            else:
                list2 = file_list
            return list2


def get_parent_files(filename, app_name):
    ptr = open(filename, "r")
    temp = ptr.readline()
    if temp.find("{% extends ") != -1:
        pos = temp.find("{% extends ") + 12
        endpos = temp.find(" %}") - 1
        parent_name = temp[pos:endpos]
        list_files = get_list_of_files(parent_name, app_name)
        return list_files


# def find_urls(urls_path):
#     ptr = open(urls_path, "r")
#     temp = ptr.readline()
#     while temp.find("urlpatterns = [") == -1:
#         temp = ptr.readline()
#     while temp.find("]") == -1:
#         temp = ptr.readline()
#         if temp.find("url(") != -1:
#             startpos = temp.find(",") + 1
#             endpos = temp.find(',', startpos)
#             loc = temp[startpos:endpos]
#             loc = loc.strip()
#             path = loc.split('.')
#             new_path = os.path.join(settings.BASE_DIR, "webhome")
#             new_path = os.path.join(new_path, path[0] + ".py")
#             print new_path
#             ptr2 = open(new_path, "r")
#             temp2 = ptr2.readline()
#             while temp2.find("def " + path[1]) == -1:
#                 temp2 = ptr2.readline()
#             temp2 = ptr2.readline()
#             while temp2.find("def") == -1 and temp2 != '':
#                 if temp2.find("return render") != -1:
#                     startpos2 = temp2.find(",") + 3
#                     endpos2 = temp2.find(",", startpos2) - 1
#                     if endpos2 == -1:
#                         endpos2 = temp2.find(")")-1
#                     name_of_file = temp2[startpos2:endpos2]
#                     list_names = get_list_of_files(name_of_file)
#                     print
#                     print name_of_file, "---", list_names
#                     print
#                 temp2 = ptr2.readline()


def find_urls_2():
    for url in urls.urlpatterns:
        app_name = url.regex.pattern[1:-1]
        if hasattr(url, 'url_patterns'):
            for each in url.url_patterns:
                find_urls_pattern(each, app_name)
        else:
            find_urls_pattern(url, app_name)


def find_urls_pattern(each,app_name):
    ptr = open(each._callback.func_code.co_filename, "r")
    start_line = each._callback.func_code.co_firstlineno
    while start_line > 0:
        ptr.readline()
        start_line -= 1
    temp2 = ptr.readline()
    while temp2.find("def") == -1 and temp2 != '' and temp2.find("class") == -1:
        if temp2.find("return render") != -1:
            startpos2 = temp2.find(",") + 3
            endpos2 = temp2.find(",", startpos2) - 1
            if endpos2 <= 0:
                endpos2 = temp2.find(")")-1
            name_of_file = temp2[startpos2:endpos2]
            list_names = get_list_of_files(name_of_file,app_name)
            print app_name
            print name_of_file, "---", list_names
        temp2 = ptr.readline()

find_urls_2()

# _js_file_list = [
#     ['js/vendor/modernizr.js', 'js/vendor/jquery.js', 'js/foundation.min.js'],
#     ['js/jquery.cookie.js', 'js/owl.carousel.min.js', 'js/jquery.lazyload.min.js'],
#     ['js/underscore.js', 'js/async.js', 'js/kinetic.js']]
# # _file_names_list = ["file1.html", "file2.html", "file3.html"]
# _file_names_list = ['file1.html']
# count = -1
# try:
#     for name in _file_names_list:
#         count += 1
#         file_names = get_list_of_files(name)
#         if cmp(file_names, _js_file_list[count]) == 0:
#             print "test passed"
#         else:
#             print "test failed"
#     find_urls("/media/madhurima/D6FA282FFA280DF5/django_work/webhome/urls.py")
# except MyError as e:
#     print e.value
