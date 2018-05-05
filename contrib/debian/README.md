
Debian
====================
This directory contains files used to package graviumd/gravium-qt
for Debian-based Linux systems. If you compile graviumd/gravium-qt yourself, there are some useful files here.

## gravium: URI support ##


gravium-qt.desktop  (Gnome / Open Desktop)
To install:

	sudo desktop-file-install gravium-qt.desktop
	sudo update-desktop-database

If you build yourself, you will either need to modify the paths in
the .desktop file or copy or symlink your gravium-qt binary to `/usr/bin`
and the `../../share/pixmaps/gravium128.png` to `/usr/share/pixmaps`

gravium-qt.protocol (KDE)

