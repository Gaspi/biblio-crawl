INSTALL_FOLDER=/var/www/FLASK/bibli
APACHE_PATH=/etc/apache2
PORT=8080
LOG_FOLDER=$(INSTALL_FOLDER)/logs

LOCAL_SRC = $(shell find ./ -type f -name '*.js' -o -name '*.css' -o -name '*.html' -o -name '*.py')
DIST_SRC = $(patsubst ./%, $(INSTALL_FOLDER)/%, $(LOCAL_SRC))


# Compile with "make Q=" to display the commands that are run.
Q = @

.PHONY: all install uninstall reinstall
all: install

install: $(DIST_SRC) $(APACHE_PATH)/sites-available/bibli.conf $(INSTALL_FOLDER)/bibli.wsgi
	$(Q)mkdir -m 775 -p "$(LOG_FOLDER)"
	$(Q)rm -rf "$(LOG_FOLDER)/*"
	$(Q)a2ensite bibli.conf
	$(Q)service apache2 reload
	$(Q)echo "Installation terminée !"

uninstall:
	$(Q)test -f "$(APACHE_PATH)/sites-enabled/bibli.conf" && a2dissite bibli.conf && service apache2 reload || echo "No previous conf, no need to touch apache2"
	$(Q)rm -f "$(APACHE_PATH)/sites-available/bibli.conf"
	$(Q)rm -rf "$(INSTALL_FOLDER)"
	$(Q)rm -rf "$(LOG_FOLDER)"
	$(Q)echo "Désinstallation terminée !"

reinstall: uninstall install

$(INSTALL_FOLDER)/%: %
	$(Q)mkdir -m 775 -p "$(@D)"
	$(Q)cp "$<" "$@"
	$(Q)chmod a+rx "$@"

$(APACHE_PATH)/sites-available/bibli.conf: bibli.conf
	$(Q)test -f "$(APACHE_PATH)/sites-enabled/bibli.conf" && a2dissite bibli.conf && service apache2 reload || echo "No previous conf, no need to touch apache2"
	$(Q)rm -f "$(APACHE_PATH)/sites-available/bibli.conf"
	$(Q)sed "s+\[INSTALL_FOLDER\]+$(INSTALL_FOLDER)+g" bibli.conf | sed "s+\[PORT\]+$(PORT)+g" > $(APACHE_PATH)/sites-available/bibli.conf

$(INSTALL_FOLDER)/bibli.wsgi: bibli.wsgi
	$(Q)mkdir -m 775 -p "$(INSTALL_FOLDER)"
	$(Q)rm -f "$(INSTALL_FOLDER)/bibli.wsgi"
	$(Q)sed "s+\[INSTALL_FOLDER\]+$(INSTALL_FOLDER)+g" bibli.wsgi > "$(INSTALL_FOLDER)/bibli.wsgi"
