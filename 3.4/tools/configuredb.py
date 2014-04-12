try:
    import main
except:
    print('Move this script to the same directory as "main.py", and run again.')
    quit()
import os, sqlite3

if os.path.exists(main.dbLoc):
    print('Existing DB found ...\n')
    main.loadSettings()
    print('Protocols: ' + ', '.join(main.protoList))
    print('Plugins: ' + ', '.join(main.plugList))
    print('Protocol Dir: ' + main.protoFolder)
    print('Plugin Dir: ' + main.plugFolder)
    print('Nick: ' + main.nick)
    print('Quiet: ' + str(main.quiet))
    print('Function Prefix: ' + main.funcPrefix)
    print('Protocol Prefix: ' + main.protoPrefix)
    print('Main Loop Wait: ' + str(main.mainWait))

else:
    print('No DB found, creating ...')

print('\nTo leave something at it\'s default, just press enter.\n')

protoFolder = input('What folder are you protocols located in? ['+main.protoFolder+']: ')
if protoFolder != '': main.protoFolder = protoFolder
plugFolder = input('What folder are you plugins located in? ['+main.plugFolder+']: ')
if plugFolder != '': main.plugFolder = plugFolder
nick = input('What is the bot\'s nick? ['+main.nick+']: ')
if nick != '': main.nick = nick

print('\nType the numbers of the protocols you want to load, separated by spaces.')
print('Just press enter to load all of them.')
protocols_raw = os.listdir(main.protoFolder)
protocols = []
ii = 0
for i in protocols_raw:
    if len(i) > 3 and i[-3:] == '.py':
        print('%d - %s' % (ii, i))
        ii += 1
        protocols.append(i)
protoInput = input()
if protoInput != '':
    main.protoList = []
    for i in protoInput.split():
        main.protoList.append(protocols[int(i)])
else:
    main.protoList = protocols
print(main.protoList)

print('\nType the numbers of the plugins you want to load, separated by spaces.')
print('Just press enter to load all of them.')
plugins_raw = os.listdir(main.plugFolder)
plugins = []
ii = 0
for i in plugins_raw:
    if len(i) > 3 and i[-3:] == '.py':
        print('%d - %s' % (ii, i))
        ii += 1
        plugins.append(i)
plugInput = input()
if plugInput != '':
    main.plugList = []
    for i in plugInput.split():
        main.plugList.append(plugins[int(i)])
else:
    main.plugList = plugins
print(main.plugList)

funcPrefix = input('\nWhat should be the function prefix be? ['+main.funcPrefix+']: ')
if funcPrefix != '': main.funcPrefix = funcPrefix
protoPrefix = input('What should be the protocol prefix be? ['+main.protoPrefix+']: ')
if protoPrefix != '': main.protoPrefix = protoPrefix

print('\nThese last 2 are pretty technical, if you don\'t know what they do, don\'t change them.')
quiet = input('Should I supress most debugging output? (0/1) ['+str(main.quiet)+']: ')
if quiet != '': main.quiet = bool(quiet)
mainWait = input('What should the mainloop wait be? ['+str(main.mainWait)+']: ')
if mainWait != '': main.mainWait = float(mainWait)

print('\nWriting changes to DB ...')
conn = sqlite3.connect(main.dbLoc)
main.setSetting("System", "version", (main.version,), ('Value',), conn)
main.setSetting("System", "protoList", (','.join(main.protoList),), ('Value',), conn)
main.setSetting("System", "plugList", (','.join(main.plugList),), ('Value',), conn)
main.setSetting("System", "protoFolder", (main.protoFolder,), ('Value',), conn)
main.setSetting("System", "plugFolder", (main.plugFolder,), ('Value',), conn)
main.setSetting("System", "nick", (main.nick,), ('Value',), conn)
main.setSetting("System", "quiet", (int(main.quiet),), ('Value',), conn)
main.setSetting("System", "funcPrefix", (main.funcPrefix,), ('Value',), conn)
main.setSetting("System", "protoPrefix", (main.protoPrefix,), ('Value',), conn)
main.setSetting("System", "mainWait", (main.mainWait,), ('Value',), conn)
conn.close()
print('Done.')
