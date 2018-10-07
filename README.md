# Global Scrapers Repo

You can add the source directory to your own repository for convenience

<dir>
	 <info compressed="false">https://raw.githubusercontent.com/Dr-Know99/Global-Scrapers-Repo/master/zips/addons.xml</info>
	 <checksum>https://raw.githubusercontent.com/Dr-Know99/Global-Scrapers-Repo/master/zips/addons.xml.md5</checksum>
	 <datadir zip="true">https://raw.githubusercontent.com/Dr-Know99/Global-Scrapers-Repo/master/zips</datadir>
</dir>

# How to Import GlobalScrapers Into Any Addon

Any multi-source Kodi addon can be altered to use these new scrapers instead of its own, you can follow the instructions below to get things updated.

Open the addons/plugin.video.resistance/addon.xml.

Add the following line to the addon.xml file:

    <import addon=”script.module.globalscrapers”/>

Open addons/script.module.resistance/lib/resources/lib/modules/sources.py

Add the following line to the sources.py file:

    import globalscrapers

You can add it right after the line that says:

    from resources.lib.modules import thexem

You will also need to change a few lines in the def getConstants(self) function in sources.py file:

Find the line that says:

    from resources.lib.sources import sources

Comment out that line by adding a pound/hashtag at the beginning like this:

    #from resources.lib.sources import sources

add the following:

from globalscrapers import sources
