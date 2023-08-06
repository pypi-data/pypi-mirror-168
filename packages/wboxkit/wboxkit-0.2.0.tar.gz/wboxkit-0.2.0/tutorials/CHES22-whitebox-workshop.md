# CHES 2022 - White-Box Cryptography Tutorial

## Setup

1. Install jupyter lab (`pip install jupyterlab`). Can be global/user python enviroment (not necessarily the same as the framework).
1. (Optional) create & activate python virtual environment (preferably PyPy3 for performance), install as kernel.
```
TODO
pip install ipykernel
```

3. Clone the tutorial repository:
```sh
git clone https://github.com/hellman/
````
4. Install `wbkit`:
```
pip install wbkit/ graphviz pycryptodome
```
5. Run the jupyter lab and open tutorials notebooks.




## Notes

- How to work with Jupyter lab

- Have a look how things work (code in frameworks)

- do a Make


docker build --network=host -t ches2022wbc -f Dockerfile .
docker build --network=host -t ches2022wbc_nosagemath -f Dockerfile_NoSageMath .

docker tag ches2022wbc hellman1908/ches2022wbc:latest
docker tag ches2022wbc_nosagemath hellman1908/ches2022wbc_nosagemath:latest