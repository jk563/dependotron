# #!/usr/bin/env python
#
# import crawler, sys
#
# def usage():
# 	print 'dependotron.py usage'
# 	print
# 	print 'dependotron.py rootDirectory keyPath certificatePath'
# 	print
# 	print 'rootDirectory - The directory root to start from and recurse under.'
# 	print 'keyPath - Path to the key file used for certificate usage (pem).'
# 	print 'certificatePath - Path to your personal certificate (pem).'
#
# if len(sys.argv) != 4:
# 	usage()
# 	sys.exit()
#
# # Set up url opener with certificate
# crawler.setUpOpener(sys.argv[2], sys.argv[3])
#
# # Look for any POM files
# crawler.crawl(sys.argv[1])
