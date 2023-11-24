# install llama_cpp_python and llama-index for linux with cuda gpu
# python -m venv ./venv
./venv/scripts/activate.ps1
LLAMA_OPENBLAS=1 pip install llama_cpp_python --force-reinstall --upgrade --no-cache-dir
pip install llama-index