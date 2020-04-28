import os


f = open('patchnote.html', 'w')
f2 = open('patch.txt', 'r')

f.write('{% extends "base.html" %}\n\n{% block content %}\n<br><br/>\n')
for s in f2:
    if s[0] == '@':
        f.write('<p class="patch_txt">*' + s[1:-1] + '</p>\n')
        print('@')
    if s[0] == '!':
        f.write('<p class="patch_head">' + s[1:-1] + '</p>\n')
        print('!')
    if s[0] == '#':
        f.write('<p class="patch_mhead">>' + s[1:-1] + '</p>\n')
        print('#')
    if s[0] == '~':
        f.write('<img src="' + s[1:-1] + '" class="patch_img_resized">\n')
        print('~')
    if s[0] == '^':
        f.write('<img src="' + s[1:-1] + '" class="patch_img">\n')
        print('^')
    if s[0] == '(':
        f.write('<p style="margin-left: 15%;">\n')
        print('(')
    if s[0] == ')':
        f.write('</p>\n')
        print(')')


f.write('{% endblock %}')
f.close()
f2.close()
try:
    os.remove('templates/patchnote.html')
except BaseException:
    pass
os.replace('patchnote.html', 'templates/patchnote.html')
