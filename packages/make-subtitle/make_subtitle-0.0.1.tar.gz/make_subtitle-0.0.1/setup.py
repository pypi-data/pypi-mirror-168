from setuptools import find_packages,setup
setup(
    name = 'make_subtitle',     #pypi中的名称，pip或者easy_install安装时使用的名称
    version = '0.0.1',
    author ='Junx',
    author_email='yk690520@outlook.com',
    packages = find_packages(),

    #需要安装的依赖
    install_requires=[
        'pyttsx3>=2.90',
        'moviepy>=1.0.3'
    ],

    # 此项需要，否则卸载时报windows error
    zip_safe=False

)