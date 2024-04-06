sudo apt update
sudo apt upgrade
sudo apt install cmake build-essential libgl1-mesa-dev
cmake -DCMAKE_BUILD_TYPE=Release .
cmake --build . --target backup_tool -j 1
