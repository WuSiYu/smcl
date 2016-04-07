#!/usr/bin/python3
import os, json, sys

# default value
MinecraftDir = './.minecraft'
Version = ''
maxMen = '2048m'
ID = ''

# get jar files path from the json file
def getJars(minecraftDir, version):
	jsonFilePath = minecraftDir+'/versions/'+version+'/'+version+'.json'

	with open(jsonFilePath, 'r') as jsonFile :
		jsonFileContent = jsonFile.read()

	jsonFileKeys = json.loads( jsonFileContent )

	jars = ''
	for x in jsonFileKeys['libraries']:
		jarFileParts = x['name'].split(':')
		jarFile =	MinecraftDir+'/libraries/' + \
					jarFileParts[0].replace('.','/')+'/'+jarFileParts[1] +'/'+jarFileParts[2] + '/' + \
					jarFileParts[1]+'-'+jarFileParts[2]+'.jar'

		jars += jarFile+':'
	
	if 'inheritsFrom' in jsonFileKeys.keys():
		jars += getJars(minecraftDir, jsonFileKeys['inheritsFrom'])

	return jars

# generate the Minecraft Argvs from the json file
def getMinecraftArgvs(minecraftDir, version, ID):
	jsonFilePath = minecraftDir+'/versions/'+version+'/'+version+'.json'
	with open(jsonFilePath, 'r') as jsonFile :
		jsonFileContent = jsonFile.read()

	jsonFileKeys = json.loads( jsonFileContent )
	argvs = jsonFileKeys['minecraftArguments']
	argvs = argvs	.replace('${auth_player_name}', ID)\
					.replace('${version_name}', '{}')\
					.replace('${game_directory}', minecraftDir)\
					.replace('${assets_root}', minecraftDir+'/assets')\
					.replace('${assets_index_name}', jsonFileKeys['assets'])\
					.replace('${auth_uuid}', '{}')\
					.replace('${auth_access_token}', '{}')\
					.replace('${user_type}', 'Legacy')\
					.replace('${version_type}', jsonFileKeys['type'])\
					.replace('${user_properties}', '{}')
	argvs = jsonFileKeys['mainClass'] + ' ' + argvs
	return argvs


# process argvs for this script
job = 0
theUsageText = 'Usage:\t\t'+sys.argv[0]+' [-d Minecraft_dir] [-v version] [-m 2048m] Username\n\t\t\tLaunch Minecraft\n\n\t\t'+sys.argv[0]+' [-d Minecraft_dir] -l\n\t\t\tList Minecraft versions'

if len(sys.argv) == 1:
	print(theUsageText)
	sys.exit()
else:
	t=1
	while t<len(sys.argv):
		if sys.argv[t] == '-d':
			t+=1
			MinecraftDir = sys.argv[t]
		elif sys.argv[t] == '-v':
			t+=1
			Version = sys.argv[t]
		elif sys.argv[t] == '-m':
			t+=1
			maxMen = sys.argv[t]
		elif sys.argv[t] == '-h':
			print(theUsageText)
			sys.exit()
		elif sys.argv[t] == '-l':
			job = 1
		else:
			ID = sys.argv[t]

		t+=1

if job == 1:		#if the job is list Minecraft versions, do it and exit
	print('Minecraft versions:')
	versions = os.listdir(MinecraftDir+'/versions/')
	versions.sort(reverse=True)
	for x in versions:
		print( '\t'+x )
	sys.exit()

if ID == '':		#if do not specify a ID, print the usage and exit
	print(theUsageText)
	sys.exit()

if Version == '':	#if do not specify a version, set the Version value to the latest version
	versions = os.listdir(MinecraftDir+'/versions/')
	versions.sort(reverse=True)
	Version = versions[0]
# end of this part


# generate command to launch Minecraft
befour = 'java -Xincgc -XX:-UseAdaptiveSizePolicy -XX:-OmitStackTraceInFastThrow -Xmn128m -Xmx'+maxMen+' -Djava.library.path='+MinecraftDir+'/versions/'+Version+'/'+Version+'-natives -Dfml.ignoreInvalidMinecraftCertificates=true -Dfml.ignorePatchDiscrepancies=true -Duser.home=/ -cp "'

after = getMinecraftArgvs(MinecraftDir, Version ,ID)

jars = getJars(MinecraftDir, Version)
jars += MinecraftDir+'/versions/'+Version+'/'+Version+'.jar" '

cmd = befour + jars + after
# end of this part


# launch Minecraft
os.system(cmd)
