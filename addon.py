#/*
# * Flashrom for Raspberry.
# *
# * Copyright (C) 2016 Christian Butz
# *
# * This program is free software: you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation, either version 3 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program.  If not, see <http://www.gnu.org/licenses/>.
# *
# */
#!/usr/bin/python
# -*- coding: utf-8 -*-

import xbmcplugin
import sys
import xbmc
import xbmcaddon
import xbmcgui
import os
import urllib
import urllib2
import CommonFunctions
import subprocess
import getpass
import webbrowser
from subprocess import Popen, PIPE, STDOUT

common = CommonFunctions
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
passwd = xbmcaddon.Addon().getSetting('password')
#xbmcaddon.Addon().setSetting(id='username', value=getpass.getuser())
vers = xbmcaddon.Addon('script.berryflash').getSetting('version')
pDialog = xbmcgui.DialogProgress()

def menuSelection(name,mode,iconimage=''):
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url="%s?mode=%s" % (sys.argv[0],mode),listitem=xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=iconimage))

def translate(text):
      return xbmcaddon.Addon().getLocalizedString(text).encode('utf-8')

def kodidirs():
	menuSelection(translate(30030),1)
	menuSelection(translate(30031),2)
	menuSelection(translate(30032),3)
	menuSelection(translate(30033),4)
#	menuSelection(translate(30034),5)

def selprog():
	nr_lines = xbmcaddon.Addon().getSetting('programmer')
	if nr_lines=='0': return 'internal'
	elif nr_lines=='1': return 'dummy'
	elif nr_lines=='2': return 'nic3com'
	elif nr_lines=='3': return 'nicrealtek'
	elif nr_lines=='4': return 'nicnatsemi'
	elif nr_lines=='5': return 'nicintel'
	elif nr_lines=='6': return 'gfxnvidia'
	elif nr_lines=='7': return 'drkaiser'
	elif nr_lines=='8': return 'satasii'
	elif nr_lines=='9': return 'satamv'
	elif nr_lines=='10': return 'atahpt'
	elif nr_lines=='11': return 'atavia'
	elif nr_lines=='12': return 'atapromise'
	elif nr_lines=='13': return 'it8212'
	elif nr_lines=='14': return 'ft2232_spi'
	elif nr_lines=='15': return 'serprog'
	elif nr_lines=='16': return 'buspirate_spi'
	elif nr_lines=='17': return 'dediprog'
	elif nr_lines=='18': return 'rayer_spi'
	elif nr_lines=='19': return 'pony_spi'
	elif nr_lines=='20': return 'nicintel_spi'
	elif nr_lines=='21': return 'ogp_spi'
	elif nr_lines=='22': return 'linux_spi:dev=/dev/spidev0.0'
	elif nr_lines=='23': return 'usbblaster_spi'
	elif nr_lines=='24': return 'nicintel_eeprom'
	elif nr_lines=='25': return 'mstarddc_spi'
	elif nr_lines=='26': return 'pickit2_spi'
	elif nr_lines=='27': return 'ch341a_spi'
	else: return 0

def passcheck():
	cmd = 'echo '+passwd+' | sudo -S dpkg -l | grep python'
	p = Popen(cmd.splitlines(), shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
	output=p.stdout.readlines()
	laenge=len(output)
	if int(laenge)>10:
#		xbmcgui.Dialog().ok("Password check", "Correct password", "Laenge: "+str(laenge))
		return '2'
	else:
		if passwd != "":
#			xbmcgui.Dialog().ok("Password check", "Password not correct", "Laenge: "+str(laenge))
			return '1'
		else:
#			xbmcgui.Dialog().ok("Password check", "Password not entered", "Laenge: "+str(laenge))
			return '0'

params=common.getParameters(sys.argv[2])
mode=None
try:
	mode=int(params["mode"])
except:
	pass
	
if mode == None:
        kodidirs()

elif mode == 1:
	checked = passcheck()
	if os.path.exists(os.path.expanduser("~")+"/flashrom-"+vers) and checked=='2':
		pDialog.create(translate(30030), translate(30070))
		cmd = 'echo '+passwd+' | sudo -S '+os.path.expanduser("~")+'/flashrom-'+vers+'/flashrom --p '+selprog()
		p = Popen(cmd.splitlines(), shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
		output = p.stdout.readlines()[4:]
		p.communicate()
		pDialog.close()
		sarray = []
		for line in output:
			sarray.append(line)
		output1 = '\n'.join(sarray)
		xbmcgui.Dialog().ok(translate(30030), output1)
	elif os.path.exists(os.path.expanduser("~")+"/flashrom-"+vers) and checked=='1':
		xbmcgui.Dialog().ok(translate(30030), translate(30074))
	elif os.path.exists(os.path.expanduser("~")+"/flashrom-"+vers) and checked=='0':
		xbmcgui.Dialog().ok(translate(30030), translate(30073))
	else:
		xbmcgui.Dialog().ok(translate(30030), translate(30071))

elif mode == 2:
	checked = passcheck()
	if os.path.exists(os.path.expanduser("~")+"/flashrom-"+vers) and checked=='2':
		readdir = xbmcgui.Dialog().browseSingle(3, translate(30035), 'files', '.bin', False, True, '')
		readname = xbmcgui.Dialog().input('Enter file name', type=xbmcgui.INPUT_ALPHANUM)
		if readdir != '' and readname != '':
			pDialog.create(translate(30031), translate(30070))
			test = open(os.path.abspath(readdir+readname+'.bin'), 'wb')
			cmd = 'echo '+passwd+' | sudo -S '+os.path.expanduser("~")+'/flashrom-'+vers+'/flashrom --p '+selprog()+' -r '+readdir+readname+'.bin'
			p = Popen(cmd.splitlines(), shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
			output = p.stdout.readlines()[4:]
			p.communicate()
			pDialog.close()
			sarray = []
			for line in output:
				sarray.append(line)
			output1 = '\n'.join(sarray)
			xbmcgui.Dialog().ok(translate(30031), output1)
			test.close()
		else:
			xbmcgui.Dialog().ok(translate(30031), translate(30037))
	elif os.path.exists(os.path.expanduser("~")+"/flashrom-"+vers) and checked=='1':
		xbmcgui.Dialog().ok(translate(30031), translate(30074))
	elif os.path.exists(os.path.expanduser("~")+"/flashrom-"+vers) and checked=='0':
		xbmcgui.Dialog().ok(translate(30031), translate(30073))
	else:
		xbmcgui.Dialog().ok(translate(30031), translate(30071))

elif mode == 3:
	checked = passcheck()
	if os.path.exists(os.path.expanduser("~")+"/flashrom-"+vers) and checked=='2':
		pDialog.create(translate(30032), translate(30070))
		cmd = 'echo '+passwd+' | sudo -S '+os.path.expanduser("~")+'/flashrom-'+vers+'/flashrom --p '+selprog()+' -E'
		p = Popen(cmd.splitlines(), shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
		output = p.stdout.readlines()[4:]
		p.communicate()
		pDialog.close()
		sarray = []
		for line in output:
			sarray.append(line)
		output1 = '\n'.join(sarray)
		xbmcgui.Dialog().ok(translate(30032), output1)
	elif os.path.exists(os.path.expanduser("~")+"/flashrom-"+vers) and checked=='1':
		xbmcgui.Dialog().ok(translate(30032), translate(30074))
	elif os.path.exists(os.path.expanduser("~")+"/flashrom-"+vers) and checked=='0':
		xbmcgui.Dialog().ok(translate(30032), translate(30073))
	else:
		xbmcgui.Dialog().ok(translate(30032), translate(30071))

elif mode == 4:
	checked = passcheck()
	if os.path.exists(os.path.expanduser("~")+"/flashrom-"+vers) and checked=='2':
		writebin = xbmcgui.Dialog().browseSingle(1, translate(30036), 'files', '.bin', False, False, '')
		if writebin != '':
			pDialog.create(translate(30033), translate(30070))
			test = open(os.path.abspath(writebin), 'rb')
#			xbmcgui.Dialog().ok(addonname, os.path.basename(writebin), writebin)
			cmd = 'echo '+passwd+' | sudo -S '+os.path.expanduser("~")+'/flashrom-'+vers+'/flashrom --p '+selprog()+' -w '+writebin
			p = Popen(cmd.splitlines(), shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
			output = p.stdout.readlines()[4:]
			p.communicate()
			pDialog.close()
			sarray = []
			for line in output:
				sarray.append(line)
			output1 = '\n'.join(sarray)
			xbmcgui.Dialog().ok(translate(30033), output1)
			test.close()
		else:
			xbmcgui.Dialog().ok(translate(30033), translate(30037))
	elif os.path.exists(os.path.expanduser("~")+"/flashrom-"+vers) and checked=='1':
		xbmcgui.Dialog().ok(translate(30033), translate(30074))
	elif os.path.exists(os.path.expanduser("~")+"/flashrom-"+vers) and checked=='0':
		xbmcgui.Dialog().ok(translate(30033), translate(30073))
	else:
		xbmcgui.Dialog().ok(translate(30033), translate(30071))

#elif mode == 5:
#	xbmcgui.Dialog().ok(translate(30034), "Will be implemented later on...")

xbmcplugin.endOfDirectory(int(sys.argv[1]))
