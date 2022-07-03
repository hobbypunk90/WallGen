import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='wallgen',  
     version='0.2.2',
     scripts=['bin/wallgen'] ,
     author="Marcel Hoppe",
     author_email="hoppe.marcel@gmail.com",
     description="A wallpaper generator for gnome (and kde)",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/hobbypunk90/wallgen",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: POSIX :: Linux",
         "Environment :: X11 Applications :: Gnome",
         "Environment :: X11 Applications :: KDE"
     ],
 )