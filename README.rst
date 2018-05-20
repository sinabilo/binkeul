빈글(binkeul) 코드편집기
============================
빈글(인공언어)코드와 이모지를 편집 저장할 수 있는 GUI 어플리케이션 

설치 
=======================
본 프로그램은 윈도우즈10과 Python3.6.3 에서 테스트 되어습니다. 다른 환경에서 실행을 보장할 수 없습니다.

요구사항
-----------------------

* PySide-1.2.4 : 윈도우즈 운영체제에서 PySide-1.2.4 을 Python3.6 에서 설치하려면 `<https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyside>`_ 에서 pyside 의 whl 파일을 다운로드하여 설치하여야 한다.

* peewee-3.3.4

* Pillow-5.1.0

* svgwrite-1.1.12


.. code-block:: none

    cd C:\Python36-32\Scripts

    pip3 install wheel
    ...
    wheel install PySide-1.2.4-cp36-cp36m-win32.whl
    ...
    pip3 install peewee
    ...
    pip3 install pillow
    ...
    pip3 install svgwrite
    ...


코드복사 
---------------------------
필요한 패키지 설치가 완료되었으면 Python.3.6.x 의 Lib/site_packages 에 binkeul 폴더를 만들고 저장소로 부터 소스를 복사합니다.
        
.. code-block:: none
    
    cd C:\Python36-32\Lib\site-packages
    
    svn export https://github.com/sinabilo/binkeul/trunk/binkeul binkeul 

실행
----------------------
다음 명령을 실행하면 빈글코드 편집기를 시작할수 있습니다.
    
.. code-block:: none

    pythonw -m binkeul


추가 설치
========================
본 프로그램을 실행하는데 반드시 필요한 것은 아니지만 betlsvg, betlsvgdir 유틸을 사용하려면 다음 프로그램과 파이썬 패키지를 설치해야 한다. 

* potrace 1.13

* CairoSVG-2.1.3



참고자료 
==========================

* 빈글언어 소개 : `<https://sites.google.com/site/binkeul>`_

* 빈글코드편집기 사용자용 도움문서 : `<https://sites.google.com/site/binkeul/binkeuleditor>`_









    

