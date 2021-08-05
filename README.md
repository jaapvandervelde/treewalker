# Python Package Template

This project is intended as a generic starting point, if you want to develop a Python package.

TODO: replace the text in this file with a text appropriate to your package.

## Usage of the template

1. Clone this repository:
```commandline
git clone https://gitlab.com/bmt-aus/lib/python_package_template.git
```
Or you can use PyCharm, from the start screen or the menu `Git - Clone...` to clone it into a new project directory.

2. Run the [scripts/rename_package.py](scripts/rename_package.py) script, either directly or using the .bat or .sh provided to rename the package to your package name.
```commandline
./scripts/rename_package.sh my_package
./scripts/rename_package.bat my_package
```
3. Create your own GitLab / GitHub project on the site and then update the remote:
```commandline
git remote set-url origin https://gitlab.com/your_repo.git
git push -u origin master
```
4. Go through all of the TODO items in the project and update them to match your package's required settings.

In PyCharm, you may also want to set [output](output), [bin](bin), and created folders like `build` as 'Excluded', so they don't affect indexing and don't show up as 'duplicated code'.

## Distributing your package

Once you write and test your script and are ready to deploy, you can either:
- Build a wheel and distribute that to users:
```commandline
./scripts/build_whl.bat
./scripts/build_whl.sh
```
- Build and deploy the package on PyPI:
```commandline
./scripts/deploy_to_pypi.bat
./scripts/deploy_to_pypi.sh
```
- Get people to install your package directly through git:
```commandline
pip install git+https://gitlab.com/your_repo.git
```

A good places to publish your project would be https://gitlab.com, in the https://gitlab.com/bmt-aus/lib group, or in the https://gitlab.com/public group if your project is intended for public use. If you publish in the `public` group, your project and source code will be visible to anyone. If you publish in the `lib` group, it will be visible to anyone in the business with access to that group and you can invite specific users to your project yourself (for example, a client or supplier).
