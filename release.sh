python3 -m unittest
python3 -m examples.generate_plots
rm -r dist build pywaffle.egg-info
python3 setup.py clean
python3 setup.py sdist bdist_wheel
twine upload dist/*
rm -r dist