run:
	python ./gitlogs/main.py
clean:
	pip uninstall git-logs -y
	rm -rf build/ dist/ git_logs.egg-info/ 

install: 
	python setup.py sdist bdist_wheel 
	pip install -e . 

build:
	python setup.py sdist bdist_wheel 

restart: 
	make clean
	make install