# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['anime_api', 'anime_api.apis.anime_facts_rest_api', 'anime_api.apis.trace_moe']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'anime-api',
    'version': '0.1.0',
    'description': 'A collection of anime related APIs',
    'long_description': '# The Anime API\n\nThe Anime API is a collection of wrappers for different types of free anime-related APIs.\n\n\n## Installation\n\nReally not sure how can this project be installed yet. By now, just download the project and paste it in your working directory.\n\n\n## APIs\n\nThese are the currently supported and planned to add support for APIs:\n\n| Name                        | Documentation                                                          | Available          |\n|-----------------------------|------------------------------------------------------------------------|--------------------|\n| Anime Facts Rest API        | [Documentation](https://chandan-02.github.io/anime-facts-rest-api/)    | :white_check_mark: |\n| Trace.moe                   | [Documentation](https://soruly.github.io/trace.moe-api/)               | :white_check_mark: |\n| Animechan                   | [Documentation](https://animechan.vercel.app/guide)                    | :x:                |\n| Jikan (MyAnimeList)         | [Documentation](https://jikan.docs.apiary.io/)                         | :x:                |\n| Waifu Pics                  | [Documentation](https://waifu.pics/docs)                               | :x:                |\n| Studio Ghibli API           | [Documentation](https://ghibliapi.herokuapp.com/)                      | :x:                |\n| Kitsu                       | [Documentation](https://kitsu.docs.apiary.io/)                         | :x:                |\n| AniList                     | [Documentation](https://anilist.gitbook.io/anilist-apiv2-docs/)        | :x:                |\n| AniDB                       | [Documentation](https://wiki.anidb.net/w/API)                          | :x:                |\n| Kyoko                       | [Documentation](https://github.com/Elliottophellia/kyoko)              | :x:                |\n| Animu                       | [Documentation](https://docs.animu.ml/)                                | :x:                |\n| Anisearch                   | [Documentation](https://anisearch.com/developers)                      | :x:                |\n| Anime News Network          | [Documentation](https://www.animenewsnetwork.com/encyclopedia/api.php) | :x:                |\n| Notify.moe (Anime Notifier) | [Documentation](https://notify.moe/api)                                | :x:                |\n| Hmtai                       | [Documentation](https://hmtai.herokuapp.com/endpoints)                 | :x:                |\n| Nekos.life                  | [Documentation](https://github.com/Nekos-life/nekos.py)                | :x:                |\n| NekoBot                     | [Documentation](https://docs.nekobot.xyz/)                             | :x:                |\n| Neko-Love                   | [Documentation](https://docs.neko-love.xyz/)                           | :x:                |\n| Nekos.best                  | [Documentation](https://docs.nekos.best/)                              | :x:                |\n| Nekos.moe                   | [Documentation](https://docs.nekos.moe/)                               | :x:                |\n| Shikimori                   | [Documentation](https://shikimori.one/api/doc)                         | :x:                |\n| MangaDex                    | [Documentation](https://api.mangadex.org/docs.html)                    | :x:                |\n| Danbooru                    | [Documentation](https://danbooru.donmai.us/wiki_pages/help:api)        | :x:                |\n| Yandere                     | [Documentation](https://yande.re/help/api)                             | :x:                |\n| Konachan                    | [Documentation](https://konachan.com/help/api)                         | :x:                |\n| Waifus.im                   | [Documentation](https://waifu.im/)                                     | :x:                |\n| Catboys                     | [Documentation](https://catboys.com/api)                               | :x:                |\n',
    'author': 'Neki',
    'author_email': '84998222+Nekidev@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
