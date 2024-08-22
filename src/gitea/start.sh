#!/bin/bash
set -m
/usr/bin/entrypoint &
# Wait for Gitea to start
echo "Gitea Url: $GITEA_URL"
echo "Waiting for Gitea to start..."
while true
do

  gitea_status_code=$(curl -k --write-out %{http_code} --silent --output /dev/null $GITEA_URL)
  if [ "$gitea_status_code" -eq 200 ]; then
    echo "Gitea ready. Continue with setup..."
    break
  fi
  echo "Gitea is not ready. Waiting 5 seconds..."
  sleep 5
done

if [ -f "/data/NEW_INSTALL" ]; then
#  cp /config/private.pem /data/gitea/jwt/private.pem
  echo "Setting up Gitea for the first time"
  echo "Setting up admin user"
  su -c "gitea admin user create --username $ADMIN_USERNAME --password $ADMIN_PASSWORD --email gitadmin@localhost --admin=true --must-change-password=false" git

  # echo "Deleting default admin user"
  # su -c "gitea admin user delete --id 1" git

  echo "Setting up JWT"
  rm -rf /data/gitea/sessions
  openssl genrsa -nodes -out /data/gitea/jwt/private.pem 4096

  echo "setting up OAuth"
  if [ -n "$DRONE_GITEA_CLIENT_ID" ] && [ -n "$DRONE_GITEA_CLIENT_SECRET" ] && [ -n "$DRONE_GITEA_URL" ]; then
    sqlite3 /data/gitea/gitea.db "insert into oauth2_application(uid, name, client_id, client_secret, confidential_client, redirect_uris, created_unix, updated_unix) values(0, 'DroneCI', '$DRONE_GITEA_CLIENT_ID', '$DRONE_GITEA_CLIENT_SECRET',1,'[\"$DRONE_GITEA_URL\"]', 1709123975, 1709123975);"
  fi
fi

if [ -f "/config/users.csv" ] && [ -f "/data/NEW_INSTALL" ]; then
    echo "Creating users from /config/users.csv"
    while IFS="," read -r username email password || [ -n "$username" ]; do
        # Validate that username, email and password are not empty
        if [ -z "$username" ] || [ -z "$email" ] || [ -z "$password" ]; then
            echo "Invalid user: $username"
            continue
        fi
        password=$(echo -n "$password" | tr -d '\r')
        echo "Creating user: $username"
        su -c "gitea admin user create --username $username --password $password --email $email --must-change-password=false" git

        # Create a token for the user
        sqlite3 /data/gitea/gitea.db "insert into oauth2_grant(user_id, application_id, created_unix,updated_unix) values((select id from user where name='$username'), 3, 1709123975, 1709123975);"
    done < <(tail -n +2 /config/users.csv)
fi


if [ -f "/config/tokens.csv" ] && [ -f "/data/NEW_INSTALL" ]; then
    echo "Creating tokens...."
    while IFS="," read -r username name tokenhash salt lasteight scope || [ -n "$username" ]; do
        # Validate that username, name and tokenhash are not empty
        if [ -z "$username" ] || [ -z "$name" ] || [ -z "$tokenhash" ]; then
            echo "Invalid token: $name"
            continue
        fi
        echo "Creating token: $name"
        sqlite3 /data/gitea/gitea.db "insert into access_token(uid, name, token_hash, token_salt, token_last_eight, created_unix, updated_unix) values((select id from user where name='$username'), '$name', '$tokenhash', '$salt', '$lasteight', 1709123975, 1709123975);"
    done < <(tail -n +2 /config/tokens.csv) 
fi

python -m giteacasc gitea.yaml -u $ADMIN_USERNAME -p $ADMIN_PASSWORD

if [ -f "/config/webhooks.csv" ] && [ -f "/data/NEW_INSTALL" ]; then
    echo "Creating webhooks...."
    while IFS="," read -r webhooksecret repo url branch events || [ -n "$webhooksecret" ]; do
        # Validate that username, repo, url and secret are not empty
        while true
        do
            sqlite3_status_check=$(sqlite3 /data/gitea/gitea.db "PRAGMA integrity_check;")
            if [ -z "$sqlite3_status_check" ]; then
                echo "Gitea is not ready. Waiting 5 seconds..."
                sleep 5
            else
                echo "Database check: $sqlite3_status_check"
                echo "Database ready. Continue with setup..."
                break
            fi
        done
        if [ -z "$webhooksecret" ] || [ -z "$repo" ] || [ -z "$url" ]; then
            echo "Invalid webhook: $repo"
            continue
        fi
        echo "Creating webhook: $repo"
        sqlite3 /data/gitea/gitea.db "INSERT INTO webhook (repo_id, owner_id, is_system_webhook, url, http_method, content_type, secret, events, type, is_active, last_status, created_unix, updated_unix) VALUES ((SELECT id FROM repository WHERE name='$repo'), 1, 0, '$url/hook?secret=$webhooksecret', 'POST', 1, '$webhooksecret', '$events', 'gitea', 1, 1, 1713202651, 1713202651);"
    done < <(tail -n +2 /config/webhooks.csv)
fi

rm /data/NEW_INSTALL
echo "Gitea Configured"
fg #/usr/bin/entrypoint
