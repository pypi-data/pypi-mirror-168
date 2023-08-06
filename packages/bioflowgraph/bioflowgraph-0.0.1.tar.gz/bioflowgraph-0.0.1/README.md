更新后打包：

N=1 && python setup.py sdist && pip install dist/bioflowgraph-0.0.$N.tar.gz

twine upload dist/bioflowgraph-0.0.1.tar.gz