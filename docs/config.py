SCREENSHOT_CONFIG = {
    "admin01": {
        "path": "after_admin/login/",
        "selector": "#container",
        "output": "admin01t.png",
        "width": "1025",
    },
    "admin02": {
        "path": "admin02/?_user=admin",
        "output": "admin02.png",
        "width": "1025",
        "height": "280",
    },
    "admin03": {
        "path": "admin03/?_user=admin",
        "output": "admin03t.png",
        "width": "1025",
        "height": "320",
    },
    "admin04": {
        "path": "docs_screenshot/polls/question/?_user=admin",
        "selector": "div#content",
        "output": "admin04t.png",
        "width": "1025",
    },
    "admin05": {
        "path": "docs_screenshot/polls/question/1/change/?_user=admin",
        "selector": "div#content",
        "output": "admin05t.png",
        "width": "1025",
    },
    "admin06": {
        "path": "docs_screenshot/polls/question/1/history/?_user=admin",
        "selector": "div#content",
        "output": "admin06t.png",
        "width": "1025",
    },
    "admin07": {
        "path": "docs_screenshot/polls/questionadmin07/1/change/?_user=admin",
        "selector": "div#content",
        "output": "admin07.png",
        "width": "1025",
        "javascript": (
            """
            const submitRow = document.querySelector('div#content div.submit-row');
            submitRow.style.display = 'none';
            """
        ),
    },
    "admin08": {
        "path": "docs_screenshot/polls/questionadmin08/1/change/?_user=admin",
        "selector": "div#content",
        "output": "admin08t.png",
        "width": "1025",
        "javascript": (
            """
            const submitRow = document.querySelector('div#content div.submit-row');
            submitRow.style.display = 'none';
            """
        ),
    },
    "admin09": {
        "path": "docs_screenshot/polls/choice/add/?_user=admin",
        "selector": "div#content",
        "output": "admin09.png",
        "width": "1025",
        "javascript": (
            """
            const submitRow = document.querySelector('div#content div.submit-row');
            submitRow.style.display = 'none';
            """
        ),
    },
    "admin10": {
        "path": "docs_screenshot/polls/questionadmin10/add/?_user=admin",
        "selector": "div#content",
        "output": "admin10t.png",
        "width": "1025",
    },
    "admin11": {
        "path": "docs_screenshot/polls/questionadmin11/1/change/?_user=admin",
        "selector": "div#content div#choice_set-group",
        "output": "admin11t.png",
        "width": "1025",
    },
    "admin12": {
        "path": "docs_screenshot/polls/questionadmin12/?_user=admin",
        "selector": "div#content",
        "output": "admin12t.png",
        "width": "1025",
    },
    "admin13": {
        "path": "docs_screenshot/polls/questionadmin13/?_user=admin",
        "selector": "div#content",
        "output": "admin13t.png",
        "width": "1400",
        "javascript": (
            """
            const content = document.getElementById('changelist');
            content.style.minHeight = '0';
            """
        ),
    },
    "admin14": {
        "path": "docs_screenshot/polls/questionadmin14/1/change/?_user=admin",
        "selector": "div#content div#choice_set-group",
        "output": "admin14t.png",
        "width": "1025",
    },
    "list_filter": {
        "path": "docs_screenshot/users/userforscreenshot/?_user=admin",
        "selector": "div#content",
        "output": "list_filter.png",
        "width": "1400",
    },
}


DISPLAY_SCREENSHOT_LIST_DATA = {
    "tutorial_part_2": {
        "names": [
            "admin01",
            "admin02",
            "admin03",
            "admin04",
            "admin05",
            "admin06",
        ],
        "link": "https://docs.djangoproject.com/en/dev/intro/tutorial02/",
    },
    "tutorial_part_7": {
        "names": [
            "admin07",
            "admin08",
            "admin09",
            "admin10",
            "admin11",
            "admin12",
            "admin13",
            "admin14",
        ],
        "link": "https://docs.djangoproject.com/en/dev/intro/tutorial07/",
    },
    "admin_filter": {
        "names": ["list_filter"],
        "link": "https://docs.djangoproject.com/en/dev/ref/contrib/admin/filters/",
    },
}


DJANGO_DOCS_SCREENSHOT_PATH = {
    "admin01": "docs/intro/_images/admin01.png",
    "admin02": "docs/intro/_images/admin02.png",
    "admin03": "docs/intro/_images/admin03t.png",
    "admin04": "docs/intro/_images/admin04t.png",
    "admin05": "docs/intro/_images/admin05t.png",
    "admin06": "docs/intro/_images/admin06t.png",
    "admin07": "docs/intro/_images/admin07t.png",
    "admin08": "docs/intro/_images/admin08t.png",
    "admin09": "docs/intro/_images/admin09.png",
    "admin10": "docs/intro/_images/admin10t.png",
    "admin11": "docs/intro/_images/admin11t.png",
    "admin12": "docs/intro/_images/admin12t.png",
    "admin13": "docs/intro/_images/admin13t.png",
    "admin14": "docs/intro/_images/admin14t.png",
    "list_filter": "docs/ref/contrib/admin/_images/list_filter.png",
}
