# gsnet-scanner

GSNetのホストでSSH password認証が有効になっているかスキャンするアプリケーション

## 動作環境・仕様

- さくらのVPS石狩第1リージョン Ubuntu
    - 管理者: @peacock0803sz
- Ubuntu 20.04, Python 3.8 (self-build), nginx
- `assets/list.csv` (git管理対象外)は毎日05:00に更新される
    - `0 5 * * * python3 scripts/scan_all.py &>/dev/null` をcrontabに設定してある

## セットアップ手順

以下にCloneした状態 `/srv/gsnet-scanner/gsnet-scanner`

```sh
$ python3.8 -m venv /srv/gsnet-scanner/venv
$ . /srv/gsnet-scanner/venv/bin/activate
$ cd /srv/gsnet-scanner/gsnet-scanner
(venv) $ pip install --upgrade pip setuptools wheel
(venv) $ pip install . -r requirements.lock
```

### uWSGI

```sh
# cp /srv/gsnet-scanner/server/gsnet-scanner.service /etc/systemd/system/
# systemctl daemon-reload
# systemctl start gsnet-scanner.service
# systemctl enable gsnet-scanner.service
```

### Nginx

```sh
# cp /srv/gsnet-scanner/gsnet-scanner/server/gsnet-scanner.conf /etc/nginx/sites-available/
# ln -s /etc/nginx/sites-available/gsnet-scanner.conf /etc/n:ginx/sites-enabled/
# nginx -t  # 構文チェック
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
# systemctl restart nginx.service
```
