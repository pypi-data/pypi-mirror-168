quip.exe -c .\.uip_config.yml version %1
python setup.py sdist bdist_wheel
twine upload .\dist\* --skip-existing 
timeout /t 20
pip install --upgrade quip-cli
quip --version