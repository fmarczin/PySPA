cmake_minimum_required(VERSION 2.4.0)
include(AddFileDependencies)
find_package(Qt4 REQUIRED)
find_package(PythonInterp REQUIRED)
find_package(PythonLibs REQUIRED)

IF(WIN32)
	FIND_PATH(PYQT_TOOLDIR
		NAMES pyrcc4.exe pyuic4.bat pylupdate4.exe
		PATHS
		[HKEY_LOCAL_MACHINE\\SOFTWARE\\Python\\PythonCore\\2.5\\InstallPath]
		[HKEY_LOCAL_MACHINE\\SOFTWARE\\Python\\PythonCore\\2.4\\InstallPath]
		[HKEY_LOCAL_MACHINE\\SOFTWARE\\Python\\PythonCore\\2.3\\InstallPath]
		[HKEY_LOCAL_MACHINE\\SOFTWARE\\Python\\PythonCore\\2.2\\InstallPath]
	  "Path to PyQT tools")
ELSE(WIN32)
	FIND_PATH(PYQT_TOOLDIR
		NAMES pyrcc4 pyuic.py pylupdate4
		PATHS /usr/bin ENV PATH
	  )
ENDIF(WIN32)

find_program(PYUIC NAMES pyuic4.bat pyuic4 PATH ${PYQT_TOOLDIR} DOC "PyQT UI-compiler executable")
find_program(PYRCC NAMES pyrcc4.exe pyrcc4 PATH ${PYQT_TOOLDIR} DOC "PyRCC resource compiler executable")
find_program(PYLUPDATE NAMES pylupdate4.exe pylupdate4 PATH ${PYQT_TOOLDIR} DOC "PyQT translation file executable")

mark_as_advanced(FORCE LIBRARY_OUTPUT_PATH QT_MKSPECS_DIR QT_PLUGINS_DIR PYUIC PYRCC PYLUPDATE)

macro(build_pyqt_app)
	add_custom_target(pyqt_app ALL DEPENDS ${MAINRESOURCE} ${desform_modules} ${lang_files})
	add_custom_command(
		OUTPUT ${MAINRESOURCE}
		COMMAND ${PYRCC} -o ${MAINRESOURCE} main.qrc
		DEPENDS main.qrc ${lang_resfiles}
		)
	add_custom_command(
		OUTPUT ${lang_files}
		COMMAND ${PYLUPDATE} -noobsolete sxmgui.pro
		DEPENDS sxmgui.pro ${form_modules}
	)
endmacro(build_pyqt_app)

macro(add_pyqt_MAINRESOURCE resname)
	set(MAINRESOURCE ${resname} CACHE STRING "Project main resource")
endmacro(add_pyqt_MAINRESOURCE)

macro(add_pyqt_languages)
	separate_arguments(ARGN)
	foreach(lang ${ARGN})
		list(APPEND lang_resfiles sxmlang_${lang}.qm)
		list(APPEND lang_files sxmlang_${lang}.ts)
	endforeach(lang)
endmacro(add_pyqt_languages)

macro(add_pyqt_forms)
	separate_arguments(ARGN)
	foreach(form ${ARGN})
		list(APPEND form_modules ${form}.py)
	endforeach(form)
endmacro(add_pyqt_forms)

macro(add_pyqt_designerforms)
	separate_arguments(ARGN)
	foreach(form ${ARGN})
		list(APPEND form_modules ui_${form}.py)
		list(APPEND desform_modules ui_${form}.py)
		add_custom_command(
			OUTPUT ui_${form}.py
			COMMAND ${PYUIC} -o ui_${form}.py ui_${form}.ui
			DEPENDS ui_${form}.ui
			)
	endforeach(form)
endmacro(add_pyqt_designerforms)
