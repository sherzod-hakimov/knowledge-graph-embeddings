#### Clone and build the code in https://github.com/thunlp/OpenKE/tree/OpenKE-PyTorch

dir="OpenKE"
if [ -d "$dir" ]; then
  echo "Removing the code"
  rm -rf $dir
fi

echo "Cloning the directory"
git clone -b OpenKE-PyTorch https://github.com/thunlp/OpenKE

cd $dir

echo "Building the code"
bash make.sh

cd ..
