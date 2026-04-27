import json, os, urllib.request
from datetime import datetime, timedelta, timezone

MSK = timezone(timedelta(hours=3))
now = datetime.now(MSK)
hour = now.strftime('%H:%M')
date = now.strftime('%d.%m.%Y')
next_h = (now + timedelta(hours=1)).strftime('%H:%M')

d = json.load(open('data.json', encoding='utf-8'))

# Update timestamp
d['ts'] = f'{date} \u00b7 {hour} MSK \u00b7 \u0430\u0432\u0442\u043e\u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u0435 \u043a\u0430\u0436\u0434\u044b\u0439 \u0447\u0430\u0441 \u00b7 \u0441\u043b\u0435\u0434: {next_h}'

# Try to get VK subscribers
token = os.environ.get('VK_TOKEN', '')
if token:
    try:
        url = f'https://api.vk.com/method/groups.getById?group_id=vitapoint_ru&fields=members_count&access_token={token}&v=5.199'
        resp = json.loads(urllib.request.urlopen(url, timeout=10).read())
        members = resp.get('response', {}).get('groups', [{}])[0].get('members_count', 0)
        if members > 0:
            d['vkCount'] = str(members)
            d['vkSub'] = f'{members} \u043f\u043e\u0434\u043f.'
    except Exception:
        pass

json.dump(d, open('data.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print(f'Updated: {date} {hour}')
