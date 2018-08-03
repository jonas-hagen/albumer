# albumer

A simple tool to copy all JPG pictures (or any files with XMP metadata)
that have a certain rating (1-5) to another location while preserving the folder structure.


## Install

Clone the repository, then install the requirements:
```
pip3 install -r requirements.txt
```
You can make the file executable:
```
chmod +x albumer.py
```
Then try
```
./albumer.py --help
```

If `~/bin` is in your `PATH` you might want to move the script so you can use it from every location by just typing `albumer.py`:
```
cp albumer.py ~/bin/
```  
