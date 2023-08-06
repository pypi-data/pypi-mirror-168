# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['anime_api',
 'anime_api.apis',
 'anime_api.apis.anime_facts_rest_api',
 'anime_api.apis.animechan',
 'anime_api.apis.kyoko',
 'anime_api.apis.studio_ghibli_api',
 'anime_api.apis.trace_moe',
 'anime_api.apis.waifu_pics']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'anime-api',
    'version': '0.6.1',
    'description': 'A collection of wrappers for anime-related APIs',
    'long_description': '# The Anime API Project\n\n![Loli count](https://count.getloli.com/get/@anime-api?theme=gelbooru)\n\nThe Anime API is a collection of wrappers for different types of free anime-related APIs.\n\n\n## Why anime-api (and not others)?\n\nThere are several reasons why would you prefer using anime-api:\n- **Intuitive**: anime-api is designed to be intuitive. Supports autocompletion everywhere.\n- **Complete**: Every actively supported API has no feature left apart.\n- **Simple**: Get all the anime information you want with a single line of code.\n- **Legal**: I shouldn\'t need to say this, but all the APIs are legal. (no free streaming services/others)\n- **Actively supported**: Get new releases (with new API wrappers) every now and then.\n\n\n## Installation\n\nUsing Poetry:\n```\npoetry add anime-api\n```\n\nUsing pip:\n```\npip install anime-api\n```\n\n## Documentation\n\nThe full documentation can be found [here](https://nekidev.github.io/anime-api/docs/).\n\n\n## APIs\n\nThese are the currently supported and planned to add support for APIs:\n\n| Name                        | API Documentation                                                      | Available |\n|-----------------------------|------------------------------------------------------------------------|-----------|\n| Anime Facts Rest API        | [Documentation](https://chandan-02.github.io/anime-facts-rest-api/)    | ✅        |\n| Trace.moe                   | [Documentation](https://soruly.github.io/trace.moe-api/)               | ✅        |\n| Animechan                   | [Documentation](https://animechan.vercel.app/guide)                    | ✅        |\n| Jikan (MyAnimeList)         | [Documentation](https://jikan.docs.apiary.io/)                         | ❌        |\n| Waifu Pics                  | [Documentation](https://waifu.pics/docs)                               | ✅        |\n| Studio Ghibli API           | [Documentation](https://ghibliapi.herokuapp.com/)                      | ✅        |\n| Kitsu                       | [Documentation](https://kitsu.docs.apiary.io/)                         | ❌        |\n| AniList                     | [Documentation](https://anilist.gitbook.io/anilist-apiv2-docs/)        | ❌        |\n| AniDB                       | [Documentation](https://wiki.anidb.net/w/API)                          | ❌        |\n| Kyoko                       | [Documentation](https://github.com/Elliottophellia/kyoko)              | ✅        |\n| Animu                       | [Documentation](https://docs.animu.ml/)                                | ❌        |\n| Anisearch                   | [Documentation](https://anisearch.com/developers)                      | ❌        |\n| Anime News Network          | [Documentation](https://www.animenewsnetwork.com/encyclopedia/api.php) | ❌        |\n| Notify.moe (Anime Notifier) | [Documentation](https://notify.moe/api)                                | ❌        |\n| Hmtai                       | [Documentation](https://hmtai.herokuapp.com/endpoints)                 | ❌        |\n| Nekos.life                  | [Documentation](https://github.com/Nekos-life/nekos.py)                | ❌        |\n| NekoBot                     | [Documentation](https://docs.nekobot.xyz/)                             | ❌        |\n| Neko-Love                   | [Documentation](https://docs.neko-love.xyz/)                           | ❌        |\n| Nekos.best                  | [Documentation](https://docs.nekos.best/)                              | ❌        |\n| Nekos.moe                   | [Documentation](https://docs.nekos.moe/)                               | ❌        |\n| Shikimori                   | [Documentation](https://shikimori.one/api/doc)                         | ❌        |\n| MangaDex                    | [Documentation](https://api.mangadex.org/docs.html)                    | ❌        |\n| Danbooru                    | [Documentation](https://danbooru.donmai.us/wiki_pages/help:api)        | ❌        |\n| Yandere                     | [Documentation](https://yande.re/help/api)                             | ❌        |\n| Konachan                    | [Documentation](https://konachan.com/help/api)                         | ❌        |\n| Waifus.im                   | [Documentation](https://waifu.im/)                                     | ❌        |\n| Catboys                     | [Documentation](https://catboys.com/api)                               | ❌        |\n\n### APIs that will not be supported\n- Illegal anime streaming services\n- Non anime-related APIs\n- APIs that are not APIs (i.e. web scrapping)\n\n\n## Mantainers\n<table>\n  <tr>\n    <td style="align:center;">\n      <a href="https://github.com/Nekidev">\n        <img src="https://avatars.githubusercontent.com/u/84998222?s=256&v=4" height="100" width="100" alt="Nekidev avatar" />\n        <br>\n        <span>Nekidev</span>\n      </a>\n    </td>\n  </tr>\n</table>\n',
    'author': 'Neki',
    'author_email': '84998222+Nekidev@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
