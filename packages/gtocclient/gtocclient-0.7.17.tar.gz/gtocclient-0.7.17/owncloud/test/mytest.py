import owncloud

import pkg_resources

if __name__ == '__main__':
    print(pkg_resources.get_distribution('gtocclient').version)
    oc = owncloud.Client("https://dataccess.getui.com/")
    oc.login("yebk", "Q6g#nEAssXGMyGJSTen^4qkn54efU")
    oc.put_directory("/gean/", "/Users/yebk/git/gtocclient/dist",chunked=True)