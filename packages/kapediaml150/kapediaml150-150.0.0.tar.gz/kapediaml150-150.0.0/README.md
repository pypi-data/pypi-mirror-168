## Publishing python code to Pypi package

1. Create accout in [pypi](https://pypi.org/)
2. Generate API tokens from (https://pypi.org/manage/account/token/) and add this token to Github (Repository name/Setting/Sectres/Action Secrets/New reposatory secret/(python-package.yml file ko  password = secrets.test_pypi_password  bata test_pypi_password lai name ma rakhne ra API tokens lai value ma rakhera Add secrfets  ma click garne.) 
API tokens provide an alternative way to authenticate when uploading packages to PyPI.

3. Properly capture dependencies in requirements.txt file

    **venv/bin/python3 -m pip freeze > requirements.txt**

    **venv/bin/python3 -m pip install -r requirements.txt**

    **check the venv lib folder sitepackages to know the capture dependencies**


4. Setup CI/CD pipeline for automatic deployment from github to pypi:
Creats [python-package.yml] file(.github folders vitra Workflows folder creat garne tesvitra pthon-package.yml file creats garera tesma worksflows ko rules lekhne) mainly focused on (password: ${{ secrets.test_pypi_password }},repository_url: https://upload.pypi.org/legacy/).
[link1](https://www.section.io/engineering-education/setting-up-cicd-for-python-packages-using-github-actions/), [Link2](https://py-pkgs.org/08-ci-cd.html)

5. Make Packages  jun folder lai hamile packages bauna xa (src vane folder banyem  tesvitra arko abc vanne folder banayera teslai packages bauna abc vitra __init__.py file creat garna parxa jasle abc folder aba packages ho vanne januxa).
Note: Jun jun kura haru like project ko project.py files ra teyo sanga related vako files haru like input.json, train model haru sabai abc packages vitra nai huna parxa).
Path haru ramro sanga setup garnu parne hunxa python.py files ma.
Note: Non-python files aharu packages ma adda garne tarika package_data={'': ['inputraw.json','ocrmodel']}


6. Creat [setup.py] python files in which we should writes some commands, Focus on requiremnts.txt commands installation, hamile banako packages ko directory, Python files packages banuda nai  setup hunxa ra non-python files haru lai ni xuttai add garnu loarne hunxa.
Path haru ramro sanga setup garnu parne hunxa setup.py files ma.
If hamle README.md ,LICENSE files haru ni add garna xa vane setup.py file bata add garne.

7. Creat .gitignore file ,file which are not required to push on github should be ignored vfrom this files,writs fine names inside this file to ignogres such files like venv/, __pycache__/.

8. Finally make git init,git add .,git push -m "messages",git push.
  Look at  github and go through reposatory and select Action and click on latest workflow to know all workings setups.
  
   Note: while push new verion on  github  and pypi.org, changes the name and version og our packages from setup.py files and delet the old packages     from pypi.org accounts.

9. If our Deployment completed then go through the [https://pypi.org/manage/projects/] and view  pip install command.
   Copy that command and test on local vs-code with short user input and output code we made.
      **from packages.codefile import classname**
      
      **pip install kapediaml**
      
      **from kapediaml.resultkpd import Questionsep**

      **questionsep = Questionsep("/home/tapendra/Desktop/mlkapedia/images/img3.png")**
      
      **result = questionsep.final_function()**
      
      **print(result)**

 10. If we want to install our new veersion packages  more then one times then delet old version packages which are stores in [home/hidden files/.local/lib/python3.8/sitespackages/ our install packages(delete if we want to install new version)].
 
   



# Instruction for run

## Clone or download code

```
git clone https://github.com/TapendraBaduwal/pypi-package

```

## Going project directory

```
cd pypi-package

```

## Install requirements

```
pip3 install -r requirements.txt

```

## Run inference pipeline

```
python3 -m resultkpd

```


## Run inference pipeline from path reader function comming soon(For Pip package)

```
pip install kapediaml

from kapediaml.resultkpd import Questionsep

questionsep = Questionsep("/home/tapendra/Desktop/mlkapedia/images/img3.png")
result = questionsep.final_function()
print(result)

```

## Run From api..


```


```
