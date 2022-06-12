
INSTALL_FOLDER=/var/www/FLASK/bibli
APACHE_PATH=/etc/apache2
PORT=8080

LOCAL_SRC = $(shell find ../ -type f -name '*.js' -o -name '*.css' -o -name '*.html' -o -name '*.py')
DIST_SRC = $(patsubst ../%, $(SCRIPTS_PATH)/%, $(LOCAL_SQL))


# Compile with "make Q=" to display the commands that are run.
Q = @

.PHONY: all install uninstall reinstall
all: install

install: $(DIST_SRC) $APACHE_PATH/sites-available/bibli.conf $INSTALL_FOLDER/bibli.wsgi
	mkdir -rf $LOG_FOLDER/logs
	rm -rf $LOG_FOLDER/logs/*
	$(Q)mkdir -m 775 -p $(SCRIPTS_PATH)/LOGS
	$(Q)echo "Installation terminée !"

uninstall:
	$(Q)rm -rf $LOG_FOLDER/logs
	$(Q)rm -f $APACHE_PATH/sites-available/bibli.conf
	$(Q)rm -rf $INSTALL_FOLDER
	$(Q)echo "Désinstallation terminée !"

reinstall: uninstall install

$(SCRIPTS_PATH)/%: ../%
	$(Q)mkdir -m 775 -p "$(@D)"
	$(Q)cp $< $@
	$(Q)chmod a+rx $@

$APACHE_PATH/sites-available/bibli.conf: bibli.conf
	rm -f $APACHE_PATH/sites-available/bibli.conf
	sed 's/\[INSTALL_FOLDER\]/$INSTALL_FOLDER/g' 's/\[PORT\]/$PORT/g' bibli.conf > $APACHE_PATH/sites-available/bibli.conf

$INSTALL_FOLDER/bibli.wsgi: bibli.wsgi
	rm -f $INSTALL_FOLDER/bibli.wsgi
	sed 's/\[INSTALL_FOLDER\]/$INSTALL_FOLDER/g' bibli.wsgi > $INSTALL_FOLDER/bibli.wsgi
