#/***************************************************************************
# AGT - Archaeological Geophysics Toolbox
#
# This plugin does basic processes on geophysical data for Archaeology
#							 -------------------
#		begin				: 2016-04-14
#		git sha				: $Format:%H$
#		copyright			: (C) 2016 by Nariman HATAMI / INRAP
#		email				: nariman.hatami@inrap.fr
# ***************************************************************************/
#
#/***************************************************************************
# *																		 *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU General Public License as published by  *
# *   the Free Software Foundation; either version 2 of the License, or	 *
# *   (at your option) any later version.								   *
# *																		 *
# ***************************************************************************/

#################################################
# Edit the following to match your sources lists
#################################################


#Add iso code for any locales you want to support here (space separated)
LOCALES = Agt_fr.ts

# translation
SOURCES = \
	__init__.py \
	agt.py \
	Dialog/ElectDialog.py \
	Dialog/GeorefDialog.py\
	Dialog/MagDialog.py \
	Dialog/ElecDownDialog.py\
	Dialog/GridDialog.py\
	Dialog/MagGridDialog.py\
	Dialog/ParametersDialog.py\
	Dialog/EM31Dialog.py\
	Dialog/CalibrationDialog.py\
	Dialog/GEM2Dialog.py\
	Dialog/InterpolateurDialog.py\
	Dialog/RasterMedDialog.py\
	ui/ui_electDialog.py\
	ui/ui_georefDialog.py\
	ui/ui_magDialog.py\
	ui/ui_ElecDownDialog.py\
	ui/ui_GridDialog.py\
	ui/ui_EM31Dialog.py\
	ui/ui_MagGridDialog.py\
	ui/ui_ParametersDialog.py\
	ui/ui_RasterMedDialog.py\
	ui/ui_InterpolateurDialog.py\
	ui/ui_electDialog.ui\
	ui/ui_georefDialog.ui\
	ui/ui_magDialog.ui\
	ui/ui_ElecDownDialog.ui\
	ui/ui_GridDialog.ui\
	ui/ui_EM31Dialog.ui\
	ui/ui_MagGridDialog.ui\
	ui/ui_ParametersDialog.ui\
	ui/ui_CalibrationDialog.ui\
	ui/ui_MultiFreqDialog.ui\
	ui/ui_RasterMedDialog.ui\
	ui/ui_InterpolateurDialog.ui\
	toolbox/AGTUtilities.py\
	toolbox/AGTExceptions.py
	
	
PLUGINNAME = AGT

PY_FILES = \
	agt.py \
	Dialog/electDialog.py \
	Dialog/georefDialog.py\
	Dialog/magDialog.py \
	Dialog/ElecDownDialog.py\
	Dialog/GridDialog.py\
	Dialog/MagGridDialog.py\
	Dialog/ParametersDialog.py\
	Dialog/EM31Dialog.py\
	ui/ui_electDialog.py\
	ui/ui_georefDialog.py\
	ui/ui_magDialog.py\
	ui/ui_ElecDownDialog.py\
	ui/ui_GridDialog.py\
	ui/ui_EM31Dialog.py\
	ui/ui_MagGridDialog.py\
	ui/ui_ParametersDialog.py\
	ui/ui_CalibrationDialog.py\
	ui/ui_MultiFreqDialog.py\
	toolbox/AGTUtilities.py\
	toolbox/AGTExceptions.py\
	__init__.py

EXTRAS = icons/elec_icon.png icons/mag_icon.png icons/help.svg icons/download_icon.png icons/magGrid_icon.png icons/param_icon.png metadata.txt icons/GEM2_icon.png

COMPILED_UI_FILES = ui/ui_electDialog.py \
	ui/ui_electDialog.py\
	ui/ui_georefDialog.py\
	ui/ui_EM31Dialog.py\
	ui/ui_MagGridDialog.py\
	ui/ui_ParametersDialog.py\
	ui/ui_CalibrationDialog.py\
	ui/ui_MultiFreqDialog.py
	

COMPILED_RESOURCE_FILES = resources_rc.py


#################################################
# Normally you would not need to edit below here
#################################################

HELP = help/build/html

PLUGIN_UPLOAD = $(c)/plugin_upload.py

QGISDIR=.qgis2

default: compile

compile: $(COMPILED_UI_FILES) $(COMPILED_RESOURCE_FILES)

%_rc.py : %.qrc
	pyrcc4 -o $*_rc.py  $<
	
%.py : %.ui
	pyuic4 -o $@ $<

%.qm : %.ts
	lrelease $<

test: compile transcompile
	@echo
	@echo "----------------------"
	@echo "Regression Test Suite"
	@echo "----------------------"

	@# Preceding dash means that make will continue in case of errors
	@-export PYTHONPATH=`pwd`:$(PYTHONPATH); \
		export QGIS_DEBUG=0; \
		export QGIS_LOG_FILE=/dev/null; \
		nosetests -v --with-id --with-coverage --cover-package=. \
		3>&1 1>&2 2>&3 3>&- || true
	@echo "----------------------"
	@echo "If you get a 'no module named qgis.core error, try sourcing"
	@echo "the helper script we have provided first then run make test."
	@echo "e.g. source run-env-linux.sh <path to qgis install>; make test"
	@echo "----------------------"

deploy: compile doc transcompile
	@echo
	@echo "------------------------------------------"
	@echo "Deploying plugin to your .qgis2 directory."
	@echo "------------------------------------------"
	# The deploy  target only works on unix like operating system where
	# the Python plugin directory is located at:
	# $HOME/$(QGISDIR)/python/plugins
	mkdir -p $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)
	cp -vf $(PY_FILES) $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)
	cp -vf $(COMPILED_UI_FILES) $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)
	cp -vf $(COMPILED_RESOURCE_FILES) $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)
	cp -vf $(EXTRAS) $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)
	cp -vfr i18n $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)
	cp -vfr $(HELP) $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)/help

# The dclean target removes compiled python files from plugin directory
# also deletes any .svn entry
dclean:
	@echo
	@echo "-----------------------------------"
	@echo "Removing any compiled python files."
	@echo "-----------------------------------"
	find $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME) -iname "*.pyc" -delete
	find $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME) -iname ".svn" -prune -exec rm -Rf {} \;


derase:
	@echo
	@echo "-------------------------"
	@echo "Removing deployed plugin."
	@echo "-------------------------"
	rm -Rf $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)

zip: deploy dclean
	@echo
	@echo "---------------------------"
	@echo "Creating plugin zip bundle."
	@echo "---------------------------"
	# The zip target deploys the plugin and creates a zip file with the deployed
	# content. You can then upload the zip file on http://plugins.qgis.org
	rm -f $(PLUGINNAME).zip
	cd $(HOME)/$(QGISDIR)/python/plugins; zip -9r $(CURDIR)/$(PLUGINNAME).zip $(PLUGINNAME)

package: compile
	# Create a zip package of the plugin named $(PLUGINNAME).zip.
	# This requires use of git (your plugin development directory must be a
	# git repository).
	# To use, pass a valid commit or tag as follows:
	#   make package VERSION=Version_0.3.2
	@echo
	@echo "------------------------------------"
	@echo "Exporting plugin to zip package.	"
	@echo "------------------------------------"
	rm -f $(PLUGINNAME).zip
	git archive --prefix=$(PLUGINNAME)/ -o $(PLUGINNAME).zip $(VERSION)
	echo "Created package: $(PLUGINNAME).zip"

upload: zip
	@echo
	@echo "-------------------------------------"
	@echo "Uploading plugin to QGIS Plugin repo."
	@echo "-------------------------------------"
	$(PLUGIN_UPLOAD) $(PLUGINNAME).zip

transup:
	@echo
	@echo "------------------------------------------------"
	@echo "Updating translation files with any new strings."
	@echo "------------------------------------------------"
	
	pylupdate5 -noobsolete $(SOURCES) -ts i18n/$(LOCALES)
	
#	@chmod +x scripts/update-strings.sh
#	@scripts/update-strings.sh $(LOCALES)

transcompile:
	@echo
	@echo "----------------------------------------"
	@echo "Compiled translation files to .qm files."
	@echo "----------------------------------------"
	lrelease i18n\$(LOCALES)
	
#	@chmod +x scripts/compile-strings.sh
#	@scripts/compile-strings.sh $(LOCALES)

transclean:
	@echo
	@echo "------------------------------------"
	@echo "Removing compiled translation files."
	@echo "------------------------------------"
	del i18n\*.qm

clean:
	@echo
	@echo "------------------------------------"
	@echo "Removing uic and rcc generated files"
	@echo "------------------------------------"
	del $(COMPILED_UI_FILES) $(COMPILED_RESOURCE_FILES)

doc:
	@echo
	@echo "------------------------------------"
	@echo "Building documentation using sphinx."
	@echo "------------------------------------"
	cd help; make html

pylint:
	@echo
	@echo "-----------------"
	@echo "Pylint violations"
	@echo "-----------------"
	@pylint --reports=n --rcfile=pylintrc . || true
	@echo
	@echo "----------------------"
	@echo "If you get a 'no module named qgis.core' error, try sourcing"
	@echo "the helper script we have provided first then run make pylint."
	@echo "e.g. source run-env-linux.sh <path to qgis install>; make pylint"
	@echo "----------------------"


# Run pep8 style checking
#http://pypi.python.org/pypi/pep8
pep8:
	@echo
	@echo "-----------"
	@echo "PEP8 issues"
	@echo "-----------"
	@pep8 --repeat --ignore=E203,E121,E122,E123,E124,E125,E126,E127,E128 --exclude pydev,resources_rc.py,conf.py . || true
