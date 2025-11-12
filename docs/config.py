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
        )
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
        )
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
        )
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
