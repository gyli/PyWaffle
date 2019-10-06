python3 -m examples.generate_plots
python3 setup.py sdist bdist_wheel
twine upload dist/*
rm -r dist