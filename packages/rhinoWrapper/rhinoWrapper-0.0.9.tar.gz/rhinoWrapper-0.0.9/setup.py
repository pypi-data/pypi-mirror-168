import setuptools

setuptools.setup(
    name="rhinoWrapper",
    version="0.0.9",
    author="김병주",
    author_email="atker14@gmail.com",
    description="최석재 선생님의 RHINO 형태소분석기를 사용하기 좋게 덧씌운 래퍼 클래스입니다. \n 출처 : https://blog.naver.com/lingua/221537630069",
    url="https://github.com/INGPlay",
    packages=setuptools.find_packages(),    # []
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires ='>=3',
    install_requires=[
        "JPype1",
        "rhinoMorph"
    ]
)